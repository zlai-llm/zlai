from typing import List
from typing import Any, Tuple, Optional
from threading import Thread
from transformers import TextIteratorStreamer
from zlai.types.completion_usage import CompletionUsage
from zlai.types.messages import TypeMessage, ImageMessage
from zlai.types.generate_config.completion import Qwen2VLInstructGenerateConfig


__all__ = [
    "completion_qwen_2_vl",
    "stream_completion_qwen_2_vl",
]


def trans_image_messages(messages: List[TypeMessage], processor: Any) -> Tuple[str, List]:
    """"""
    images = []
    _messages = []
    for message in messages:
        if isinstance(message, ImageMessage):
            msg, img = message.to_message(_type="qwen2vl")
            images.extend(img)
        else:
            msg = message.to_message()
        _messages.append(msg)
    text = processor.apply_chat_template(_messages, add_generation_prompt=True, tokenize=False)
    return text, images


def completion_qwen_2_vl(
        model,
        processor,
        messages: List[TypeMessage],
        generate_config: Optional[Qwen2VLInstructGenerateConfig],
        **kwargs: Any,
):
    """"""
    text, images = trans_image_messages(messages, processor)
    inputs = processor(text=[text], images=images, padding=True, return_tensors="pt").to(model.device)
    output_ids = model.generate(**inputs, **generate_config.model_dump())
    generated_ids = [
        output_ids[len(input_ids):]
        for input_ids, output_ids in zip(inputs.input_ids, output_ids)
    ]
    response = processor.batch_decode(
        generated_ids, skip_special_tokens=True, clean_up_tokenization_spaces=True)[0]

    completion_tokens = len(generated_ids[0])
    prompt_tokens = inputs.get("input_ids").shape[1]
    total_tokens = completion_tokens + prompt_tokens
    usage = CompletionUsage(completion_tokens=completion_tokens, prompt_tokens=prompt_tokens, total_tokens=total_tokens)
    return response, usage


def stream_completion_qwen_2_vl(
        model,
        processor,
        messages: List[TypeMessage],
        generate_config: Optional[Qwen2VLInstructGenerateConfig],
        **kwargs: Any,
):
    """"""
    text, images = trans_image_messages(messages, processor)
    usage = CompletionUsage(completion_tokens=0, prompt_tokens=0, total_tokens=0)
    streamer = TextIteratorStreamer(
        processor, skip_prompt=True, skip_special_tokens=True,
        clean_up_tokenization_spaces=True,
    )
    inputs = processor(text=[text], images=images, return_tensors="pt", padding=True).to(model.device)
    usage.prompt_tokens = inputs.input_ids.shape[1]

    gen_config = {**inputs, **generate_config.gen_kwargs(), "streamer": streamer}
    thread = Thread(target=model.generate, kwargs=gen_config)
    thread.start()
    for i, content in enumerate(streamer):
        usage.completion_tokens += 1
        usage.total_tokens = usage.prompt_tokens + usage.completion_tokens
        yield content, usage
