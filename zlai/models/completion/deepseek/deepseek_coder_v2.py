from typing import Any, Dict, List, Tuple, Iterable, Optional
from threading import Thread
from transformers import TextIteratorStreamer
from zlai.types.messages import TypeMessage
from zlai.types.completion_usage import CompletionUsage
from zlai.types.generate_config.completion.deepseek import DeepSeekGenerateConfig


__all__ = [
    "completion_deepseek_coder_v2",
    "stream_completion_deepseek_coder_v2",
]


def trans_messages(messages: List[TypeMessage]) -> List[Dict]:
    """"""
    _messages = [message.model_dump() for message in messages]
    return _messages


def completion_deepseek_coder_v2(
        model,
        tokenizer,
        messages: List[TypeMessage],
        generate_config: Optional[DeepSeekGenerateConfig],
        **kwargs: Any,
) -> Tuple[str, CompletionUsage]:
    """"""
    messages = trans_messages(messages=messages)
    input_tensor = tokenizer.apply_chat_template(
        messages, add_generation_prompt=True, return_tensors="pt"
    ).to(model.device)
    outputs = model.generate(input_tensor, **generate_config.gen_kwargs())
    generated_ids = outputs[0][input_tensor.shape[1]:]
    content = tokenizer.decode(generated_ids, skip_special_tokens=True)

    completion_tokens = len(generated_ids)
    prompt_tokens = input_tensor.shape[1]
    total_tokens = completion_tokens + prompt_tokens
    usage = CompletionUsage(completion_tokens=completion_tokens, prompt_tokens=prompt_tokens, total_tokens=total_tokens)
    return content, usage


def stream_completion_deepseek_coder_v2(
        model,
        tokenizer,
        messages: List[TypeMessage],
        generate_config: Optional[DeepSeekGenerateConfig],
        **kwargs: Any,
) -> Iterable[Tuple[str, CompletionUsage]]:
    messages = trans_messages(messages=messages)
    usage = CompletionUsage(completion_tokens=0, prompt_tokens=0, total_tokens=0)

    streamer = TextIteratorStreamer(tokenizer, skip_prompt=True, skip_special_tokens=True)
    inputs = tokenizer.apply_chat_template(
        messages, add_generation_prompt=True, return_tensors="pt").to(model.device)
    usage.prompt_tokens = inputs.shape[1]

    gen_config = {
        "inputs": inputs, "streamer": streamer,
        **generate_config.gen_kwargs(),
    }
    thread = Thread(target=model.generate, kwargs=gen_config)
    thread.start()
    for i, content in enumerate(streamer):
        usage.completion_tokens += 1
        usage.total_tokens = usage.prompt_tokens + usage.completion_tokens
        yield content, usage
