from typing import Any, List, Iterable, Optional
from threading import Thread
from transformers import TextIteratorStreamer
from zlai.types.messages import TypeMessage
from ...utils import trans_messages
from ...types import TypeInferenceGenerateConfig


__all__ = [
    "completion_qwen_2",
    "stream_completion_qwen_2",
]


def completion_qwen_2(
        model,
        tokenizer,
        messages: List[TypeMessage],
        generate_config: Optional[TypeInferenceGenerateConfig],
) -> str:
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
    return content


def stream_completion_qwen_2(
        model,
        tokenizer,
        messages: List[TypeMessage],
        generate_config: Optional[TypeInferenceGenerateConfig],
        **kwargs: Any,
) -> Iterable[str]:
    messages = trans_messages(messages=messages)
    streamer = TextIteratorStreamer(tokenizer)
    inputs = tokenizer.apply_chat_template(
        messages, add_generation_prompt=True, return_tensors="pt").to(model.device)

    gen_config = {
        "inputs": inputs, "streamer": streamer,
        **generate_config.gen_kwargs(),
    }
    thread = Thread(target=model.generate, kwargs=gen_config)
    thread.start()
    for i, response in enumerate(streamer):
        if i > 0:
            content = response.replace(tokenizer.eos_token, '')
            yield content
