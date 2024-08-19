from typing import Any, Dict, List, Tuple, Iterable, Optional
from threading import Thread
from transformers import TextIteratorStreamer
from zlai.types.messages import TypeMessage, AudioMessage
from zlai.types.completion_usage import CompletionUsage
from zlai.models.types.generate_config import TypeInferenceGenerateConfig


__all__ = [
    "completion_qwen_2",
    "stream_completion_qwen_2",
]


def trans_messages(messages: List[TypeMessage]) -> List[Dict]:
    """"""
    _messages = [message.model_dump() for message in messages]
    return _messages


def completion_qwen_2(
        model,
        tokenizer,
        messages: List[TypeMessage],
        generate_config: Optional[TypeInferenceGenerateConfig],
) -> Tuple[str, CompletionUsage]:
    """"""
    messages = trans_messages(messages=messages)
    text = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True
    )
    model_inputs = tokenizer([text], return_tensors="pt").to(model.device)
    generated_ids = model.generate(model_inputs.input_ids, **generate_config.gen_kwargs())
    generated_ids = [
        output_ids[len(input_ids):] for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)
    ]
    content = tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]

    completion_tokens = len(generated_ids[0])
    prompt_tokens = model_inputs.get("input_ids").shape[1]
    total_tokens = completion_tokens + prompt_tokens
    usage = CompletionUsage(completion_tokens=completion_tokens, prompt_tokens=prompt_tokens, total_tokens=total_tokens)
    return content, usage


def stream_completion_qwen_2(
        model,
        tokenizer,
        messages: List[TypeMessage],
        generate_config: Optional[TypeInferenceGenerateConfig],
        **kwargs: Any,
) -> Iterable[Tuple[str, CompletionUsage]]:
    messages = trans_messages(messages=messages)
    usage = CompletionUsage(completion_tokens=0, prompt_tokens=0, total_tokens=0)

    streamer = TextIteratorStreamer(tokenizer)
    inputs = tokenizer.apply_chat_template(
        messages, add_generation_prompt=True, return_tensors="pt").to(model.device)
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


def trans_audio_messages(messages: List[TypeMessage], processor: Any) -> Tuple[str, List]:
    """"""
    audios = []
    _messages = []
    for message in messages:
        if isinstance(message, AudioMessage):
            audios.extend(message.get_audios(sr=processor.feature_extractor.sampling_rate))
        _messages.append(message.model_dump())
    text = processor.apply_chat_template(_messages, add_generation_prompt=True, tokenize=False)
    return text, audios


def completion_qwen_2_audio(
        model,
        processor,
        messages: List[TypeMessage],
        generate_config: Optional[TypeInferenceGenerateConfig],
        **kwargs: Any,
):
    """"""
    text, audios = trans_audio_messages(messages, processor)
    inputs = processor(text=text, audios=audios, return_tensors="pt", padding=True)
    inputs.input_ids = inputs.input_ids.to("cuda")
    generate_ids = model.generate(**inputs, **generate_config.model_dump())
    generate_ids = generate_ids[:, inputs.input_ids.size(1):]
    response = processor.batch_decode(generate_ids, skip_special_tokens=True, clean_up_tokenization_spaces=False)[0]
    return response
