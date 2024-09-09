from typing import List, Dict, Tuple, Optional, Iterable
from threading import Thread
from transformers import TextIteratorStreamer
from zlai.types.messages import *
from zlai.types.completion_usage import CompletionUsage
from zlai.types.generate_config.completion.mini_cpm import MiniCPMV26GenerateConfig


__all__ = [
    "mini_cpm_v3_messages_process",
    "completion_mini_cpm_v3",
    "stream_completion_mini_cpm_v3",
]


def mini_cpm_v3_messages_process(
        messages: List[TypeMessage],
) -> List[Dict]:
    """"""
    _messages = [message.model_dump() for message in messages]
    return _messages


def completion_mini_cpm_v3(
        model,
        tokenizer,
        messages: List[TypeMessage],
        tools: Optional[List[Dict]] = None,
        generate_config: Optional[MiniCPMV26GenerateConfig] = None,
        **kwargs,
) -> Tuple[str, CompletionUsage]:
    """"""
    messages = mini_cpm_v3_messages_process(messages)
    inputs = tokenizer.apply_chat_template(
        messages, tools=tools, return_tensors="pt",
        add_generation_prompt=True, return_dict=True,
    ).to(model.device)

    kwargs = {**inputs, **generate_config.model_dump()}
    output_ids = model.generate(**kwargs)
    output_ids = [
        output_ids[i][len(inputs.input_ids[i]):] for i in range(len(inputs.input_ids))
    ]
    content = tokenizer.batch_decode(output_ids, skip_special_tokens=True)[0]

    completion_tokens = len(output_ids[0])
    prompt_tokens = inputs.get("input_ids").shape[1]
    total_tokens = completion_tokens + prompt_tokens
    usage = CompletionUsage(
        completion_tokens=completion_tokens,
        prompt_tokens=prompt_tokens,
        total_tokens=total_tokens
    )
    return content, usage


def stream_completion_mini_cpm_v3(
        model,
        tokenizer,
        messages: List[TypeMessage],
        tools: Optional[List[Dict]] = None,
        generate_config: Optional[MiniCPMV26GenerateConfig] = None,
        **kwargs,
) -> Iterable[Tuple[str, CompletionUsage]]:
    """"""
    usage = CompletionUsage(completion_tokens=0, prompt_tokens=0, total_tokens=0)
    messages = mini_cpm_v3_messages_process(messages)

    streamer = TextIteratorStreamer(tokenizer, skip_prompt=True, skip_special_tokens=True)
    inputs = tokenizer.apply_chat_template(
        messages, tools=tools, add_generation_prompt=True, return_dict=True, return_tensors='pt',
    ).to(model.device)
    usage.prompt_tokens = inputs.input_ids.shape[1]

    gen_config = {
        **inputs, "streamer": streamer,
        **generate_config.gen_kwargs(),
    }
    thread = Thread(target=model.generate, kwargs=gen_config)
    thread.start()
    for i, chunk in enumerate(streamer):
        usage.completion_tokens += 1
        usage.total_tokens = usage.prompt_tokens + usage.completion_tokens
        yield chunk, usage
