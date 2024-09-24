from PIL import Image
from typing import List, Dict, Tuple, Optional, Iterable
from zlai.types.messages import *
from zlai.types.completion_usage import CompletionUsage
from zlai.types.generate_config.completion.stepfun import GotOCR2GenerateConfig


__all__ = [
    "got_ocr_messages_process",
    "completion_got_ocr",
]


def got_ocr_messages_process(
        messages: List[TypeMessage],
) -> Tuple[Dict, Image.Image]:
    """"""
    message = messages[-1]
    if isinstance(message, ImageMessage):
        message, images = message.to_message(_type="ocr")
        return message, images[-1]
    raise ValueError("The last message must be ImageMessage.")


def completion_got_ocr(
        model,
        tokenizer,
        messages: List[TypeMessage],
        generate_config: Optional[GotOCR2GenerateConfig],
        **kwargs,
) -> Tuple[str, CompletionUsage]:
    """"""
    usage = CompletionUsage(completion_tokens=0, prompt_tokens=0, total_tokens=0)
    message, image = got_ocr_messages_process(messages)
    content = model.chat(tokenizer, image_file=image, gradio_input=True, ocr_type='format', stream_flag=False)
    usage.completion_tokens = len(content)
    usage.total_tokens = usage.prompt_tokens + usage.completion_tokens
    return content, usage
