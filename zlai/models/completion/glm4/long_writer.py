import torch
from typing import Any, Dict, List, Tuple, Iterable, Optional
from threading import Thread
from transformers import TextIteratorStreamer, StoppingCriteria, StoppingCriteriaList
from zlai.types.messages import TypeMessage
from zlai.types.completion_usage import CompletionUsage
from zlai.types.generate_config.completion.glm4 import GLM4LongWriter9B, Llama3LongWriter8B


__all__ = [
    "completion_long_writer_glm4",
    "stream_completion_long_writer_glm4",
    "completion_long_writer_llama3",
    "stream_completion_long_writer_llama3",
]


def trans_messages(messages: List[TypeMessage]) -> Tuple[str, List[Dict]]:
    """"""
    _messages = [message.model_dump() for message in messages]
    last_message = _messages.pop(-1)
    query = last_message["content"]
    return query, _messages


def completion_long_writer_glm4(
        model,
        tokenizer,
        messages: List[TypeMessage],
        generate_config: Optional[GLM4LongWriter9B],
        **kwargs: Any,
) -> Tuple[str, CompletionUsage]:
    """"""
    query, history = trans_messages(messages=messages)
    gen_kwargs = {**generate_config.gen_kwargs()}
    inputs = tokenizer.build_chat_input(query, history=history, role="user").to(model.device)
    eos_token_id = [tokenizer.eos_token_id, tokenizer.get_command("<|user|>"),
                    tokenizer.get_command("<|observation|>")]
    outputs = model.generate(**inputs, **gen_kwargs, eos_token_id=eos_token_id)
    outputs = outputs.tolist()[0][len(inputs["input_ids"][0]):-1]
    content = tokenizer.decode(outputs)

    completion_tokens = len(outputs)
    prompt_tokens = inputs.input_ids.shape[1]
    total_tokens = completion_tokens + prompt_tokens
    usage = CompletionUsage(completion_tokens=completion_tokens, prompt_tokens=prompt_tokens, total_tokens=total_tokens)
    return content, usage


def stream_completion_long_writer_glm4(
        model,
        tokenizer,
        messages: List[TypeMessage],
        generate_config: Optional[GLM4LongWriter9B],
        **kwargs: Any,
) -> Iterable[Tuple[str, CompletionUsage]]:
    """"""
    class StopOnTokens(StoppingCriteria):
        def __call__(self, input_ids: torch.LongTensor, scores: torch.FloatTensor, **kwargs) -> bool:
            # stop_ids = model.config.eos_token_id
            stop_ids = [tokenizer.eos_token_id, tokenizer.get_command("<|user|>"),
                        tokenizer.get_command("<|observation|>")]
            for stop_id in stop_ids:
                if input_ids[0][-1] == stop_id:
                    return True
            return False

    stop = StopOnTokens()
    query, history = trans_messages(messages=messages)
    gen_kwargs = {**generate_config.gen_kwargs()}
    usage = CompletionUsage(completion_tokens=0, prompt_tokens=0, total_tokens=0)

    streamer = TextIteratorStreamer(tokenizer, skip_prompt=True, skip_special_tokens=True)
    inputs = tokenizer.build_chat_input(query, history=history, role="user").to(model.device)
    eos_token_id = [tokenizer.eos_token_id, tokenizer.get_command("<|user|>"),
                    tokenizer.get_command("<|observation|>")]

    usage.prompt_tokens = inputs.input_ids.shape[1]
    gen_config = {
        **inputs, "streamer": streamer, "eos_token_id": eos_token_id,
        "stopping_criteria": StoppingCriteriaList([stop]), **gen_kwargs,}
    thread = Thread(target=model.generate, kwargs=gen_config)
    thread.start()
    for i, content in enumerate(streamer):
        usage.completion_tokens += 1
        usage.total_tokens = usage.prompt_tokens + usage.completion_tokens
        if "<|user|>" in content:
            content = content.replace("<|user|>", "")
        yield content, usage


def completion_long_writer_llama3(
        model,
        tokenizer,
        messages: List[TypeMessage],
        generate_config: Optional[Llama3LongWriter8B],
        **kwargs: Any,
):
    """"""
    query, history = trans_messages(messages=messages)
    gen_kwargs = {**generate_config.gen_kwargs()}
    prompt = f"[INST]{query}[/INST]"

    inputs = tokenizer(prompt, truncation=False, return_tensors="pt").to(model.device)
    context_length = inputs.input_ids.shape[-1]
    output = model.generate(**inputs, **gen_kwargs)[0]
    content = tokenizer.decode(output[context_length:], skip_special_tokens=True)

    completion_tokens = len(output[context_length:])
    prompt_tokens = context_length
    total_tokens = completion_tokens + prompt_tokens
    usage = CompletionUsage(completion_tokens=completion_tokens, prompt_tokens=prompt_tokens, total_tokens=total_tokens)
    return content, usage


def stream_completion_long_writer_llama3(
        model,
        tokenizer,
        messages: List[TypeMessage],
        generate_config: Optional[GLM4LongWriter9B],
        **kwargs: Any,
) -> Iterable[Tuple[str, CompletionUsage]]:
    """"""
    query, history = trans_messages(messages=messages)
    gen_kwargs = {**generate_config.gen_kwargs()}
    prompt = f"[INST]{query}[/INST]"

    usage = CompletionUsage(completion_tokens=0, prompt_tokens=0, total_tokens=0)

    streamer = TextIteratorStreamer(tokenizer, skip_prompt=True, skip_special_tokens=True)
    inputs = tokenizer(prompt, truncation=False, return_tensors="pt").to(model.device)

    usage.prompt_tokens = inputs.input_ids.shape[1]
    gen_config = {**inputs, "streamer": streamer, **gen_kwargs, }
    thread = Thread(target=model.generate, kwargs=gen_config)
    thread.start()
    for i, content in enumerate(streamer):
        usage.completion_tokens += 1
        usage.total_tokens = usage.prompt_tokens + usage.completion_tokens
        yield content, usage
