import re
from typing import Any, Dict, List, Tuple, Union, Iterable, Optional
from threading import Thread
from pathlib import Path
from transformers import TextIteratorStreamer
from zlai.types.messages import TypeMessage, AudioMessage
from zlai.types.completion_usage import CompletionUsage
from zlai.types.generate_config.completion.qwen2 import Qwen2GenerateConfig


__all__ = [
    "completion_qwen_2",
    "stream_completion_qwen_2",
    "completion_qwen_2_audio",
]


def trans_messages(messages: List[TypeMessage]) -> List[Dict]:
    """"""
    _messages = [message.model_dump() for message in messages]
    return _messages


def completion_qwen_2(
        model,
        tokenizer,
        messages: List[TypeMessage],
        generate_config: Optional[Qwen2GenerateConfig],
        tools: Optional[List[Dict]] = None,
        tool_choice: Optional[Union[dict, str]] = "none",
        **kwargs: Any,
) -> Tuple[str, CompletionUsage]:
    """"""
    messages = trans_messages(messages=messages)
    if tools is not None:
        with open(Path(__file__).parent / 'qwen_tool_call_template.jinja') as fin:
            tokenizer.chat_template = fin.read()
        inputs = tokenizer.apply_chat_template(
            messages,
            tools=tools,
            add_generation_prompt=True,
            return_dict=True,
            return_tensors='pt',
        ).to(model.device)
    else:
        inputs = tokenizer.apply_chat_template(
            messages,
            tokenize=True,
            return_tensors="pt",
            return_dict=True,
            add_generation_prompt=True
        ).to(model.device)
    generated_ids = model.generate(**inputs, **generate_config.gen_kwargs())
    generated_ids = [
        output_ids[len(input_ids):] for input_ids, output_ids in zip(inputs.input_ids, generated_ids)
    ]
    content = tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]

    if tools is not None:
        content = re.sub(r"<tool_call>\n|\n</tool_call>", "", content)

    completion_tokens = len(generated_ids[0])
    prompt_tokens = inputs.get("input_ids").shape[1]
    total_tokens = completion_tokens + prompt_tokens
    usage = CompletionUsage(completion_tokens=completion_tokens, prompt_tokens=prompt_tokens, total_tokens=total_tokens)
    return content, usage


def stream_completion_qwen_2(
        model,
        tokenizer,
        messages: List[TypeMessage],
        generate_config: Optional[Qwen2GenerateConfig],
        tools: Optional[List[Dict]] = None,
        tool_choice: Optional[Union[dict, str]] = "none",
        **kwargs: Any,
) -> Iterable[Tuple[str, CompletionUsage]]:
    messages = trans_messages(messages=messages)
    usage = CompletionUsage(completion_tokens=0, prompt_tokens=0, total_tokens=0)

    streamer = TextIteratorStreamer(tokenizer, skip_prompt=True, skip_special_tokens=True)
    if tools is not None:
        with open(Path(__file__).parent / 'qwen_tool_call_template.jinja') as fin:
            tokenizer.chat_template = fin.read()
        inputs = tokenizer.apply_chat_template(
            messages,
            tools=tools,
            add_generation_prompt=True,
            return_dict=True,
            return_tensors='pt',
        ).to(model.device)
    else:
        inputs = tokenizer.apply_chat_template(
            messages, add_generation_prompt=True, return_tensors="pt", return_dict=True,
        ).to(model.device)
    usage.prompt_tokens = inputs.input_ids.shape[1]

    gen_config = {
        **inputs, "streamer": streamer,
        **generate_config.gen_kwargs(),
    }
    thread = Thread(target=model.generate, kwargs=gen_config)
    thread.start()
    for i, content in enumerate(streamer):
        if tools is not None:
            content = re.sub(r"<tool_call>|</tool_call>", "", str(content))
        usage.completion_tokens += 1
        usage.total_tokens = usage.prompt_tokens + usage.completion_tokens
        yield content, usage


def trans_audio_messages(messages: List[TypeMessage], processor: Any) -> Tuple[str, List]:
    """"""
    audios = []
    _messages = []
    for message in messages:
        if isinstance(message, AudioMessage):
            message = message.to_instance()
            audios.extend(message.get_audios(sr=processor.feature_extractor.sampling_rate))
        _messages.append(message.model_dump())
    text = processor.apply_chat_template(_messages, add_generation_prompt=True, tokenize=False)
    return text, audios


def completion_qwen_2_audio(
        model,
        processor,
        messages: List[TypeMessage],
        generate_config: Optional[Qwen2GenerateConfig],
        **kwargs: Any,
):
    """"""
    text, audios = trans_audio_messages(messages, processor)
    inputs = processor(
        text=text, audios=audios, return_tensors="pt", padding=True,
        sampling_rate=processor.feature_extractor.sampling_rate,
    ).to(model.device)
    generated_ids = model.generate(**inputs, **generate_config.model_dump())
    generated_ids = generated_ids[:, inputs.input_ids.size(1):]
    response = processor.batch_decode(
        generated_ids, skip_special_tokens=True, clean_up_tokenization_spaces=False)[0]

    completion_tokens = generated_ids.shape[1]
    prompt_tokens = inputs.get("input_ids").shape[1]
    total_tokens = completion_tokens + prompt_tokens
    usage = CompletionUsage(completion_tokens=completion_tokens, prompt_tokens=prompt_tokens, total_tokens=total_tokens)
    return response, usage


def stream_completion_qwen_2_audio(
        model,
        processor,
        messages: List[TypeMessage],
        generate_config: Optional[Qwen2GenerateConfig],
        **kwargs: Any,
):
    """"""
    text, audios = trans_audio_messages(messages, processor)
    usage = CompletionUsage(completion_tokens=0, prompt_tokens=0, total_tokens=0)

    streamer = TextIteratorStreamer(processor, skip_prompt=True, skip_special_tokens=True)
    inputs = processor(
        text=text, audios=audios, return_tensors="pt", padding=True,
        sampling_rate=processor.feature_extracor.sampling_rate,
    ).to(model.device)
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
