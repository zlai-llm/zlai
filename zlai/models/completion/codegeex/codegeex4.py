import torch
from typing import Any, Dict, List, Tuple, Iterable, Optional
from threading import Thread
from transformers import TextIteratorStreamer
from zlai.types.messages import TypeMessage
from zlai.types.completion_usage import CompletionUsage
from zlai.types.generate_config.completion.codegeex import CodeGeexGenerateConfig


__all__ = [
    "completion_codegeex_4",
    "stream_completion_codegeex_4",
]


def trans_messages(messages: List[TypeMessage]) -> List[Dict]:
    """"""
    _messages = [message.model_dump() for message in messages]
    return _messages


def completion_codegeex_4(
        model,
        tokenizer,
        messages: List[TypeMessage],
        generate_config: Optional[CodeGeexGenerateConfig],
        **kwargs,
) -> Tuple[str, CompletionUsage]:
    """"""
    messages = trans_messages(messages=messages)

    inputs = tokenizer.apply_chat_template(
        messages, add_generation_prompt=True, tokenize=True,
        return_tensors="pt", return_dict=True).to(model.device)
    with torch.no_grad():
        generated_ids = model.generate(**inputs, **generate_config.model_dump())
        generated_ids = generated_ids[:, inputs['input_ids'].shape[1]:]
        content = tokenizer.decode(generated_ids[0], skip_special_tokens=True)

    completion_tokens = len(generated_ids[0])
    prompt_tokens = inputs.get("input_ids").shape[1]
    total_tokens = completion_tokens + prompt_tokens
    usage = CompletionUsage(completion_tokens=completion_tokens, prompt_tokens=prompt_tokens, total_tokens=total_tokens)
    return content, usage


def stream_completion_codegeex_4(
        model,
        tokenizer,
        messages: List[TypeMessage],
        generate_config: Optional[CodeGeexGenerateConfig],
        **kwargs: Any,
) -> Iterable[Tuple[str, CompletionUsage]]:
    messages = trans_messages(messages=messages)
    usage = CompletionUsage(
        completion_tokens=0, prompt_tokens=0, total_tokens=0)

    streamer = TextIteratorStreamer(tokenizer)
    inputs = tokenizer.apply_chat_template(
        messages, add_generation_prompt=True, tokenize=True,
        return_tensors="pt", return_dict=True).to(model.device)
    usage.prompt_tokens = inputs.shape[1]

    gen_config = {
        "inputs": inputs, "streamer": streamer,
        **generate_config.gen_kwargs(),
    }
    thread = Thread(target=model.generate, kwargs=gen_config)
    thread.start()
    for i, response in enumerate(streamer):
        usage.completion_tokens += 1
        usage.total_tokens = usage.prompt_tokens + usage.completion_tokens
        if i > 0:
            content = response.replace(tokenizer.eos_token, '')
            yield content, usage
