import torch
from typing import List, Dict, Union, Optional
from zlai.types.messages import TypeMessage
from .utils import ProcessMessages


__all__ = [
    "completion_glm_4"
]


def completion_glm_4(
        model,
        tokenizer,
        messages: List[TypeMessage],
        validate: bool = False,
        tools: Optional[List[Dict]] = None,
        tool_choice: Optional[Union[dict, str]] = "none"
) -> str:
    """"""
    if validate and tools is not None and tool_choice != 'none':
        process_messages = ProcessMessages(messages, tools, tool_choice)
        messages = process_messages.to_messages()

    messages = [message.model_dump() for message in messages]
    inputs = tokenizer.apply_chat_template(
        messages, add_generation_prompt=True, tokenize=True, return_tensors="pt", return_dict=True
    ).to(model.device)
    gen_kwargs = {"max_length": 2500, "do_sample": True, "top_k": 1}
    with torch.no_grad():
        outputs = model.generate(**inputs, **gen_kwargs)
        outputs = outputs[:, inputs['input_ids'].shape[1]:]
        content = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return content
