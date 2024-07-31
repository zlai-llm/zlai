from typing import List
from zlai.types.messages import TypeMessage


__all__ = [
    "completion_qwen_2",
]


def completion_qwen_2(
        model,
        tokenizer,
        messages: List[TypeMessage],
) -> str:
    """"""
    messages = [message.model_dump() for message in messages]
    text = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True
    )
    model_inputs = tokenizer([text], return_tensors="pt").to(model.device)
    generated_ids = model.generate(model_inputs.input_ids, max_new_tokens=512)
    generated_ids = [
        output_ids[len(input_ids):] for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)
    ]
    content = tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]
    return content



