from typing import Any, List, Tuple, Optional
from zlai.types.messages import TypeMessage, CiteMessage
from zlai.types.completion_usage import CompletionUsage
from zlai.types.generate_config.completion.glm4 import GLM4LongCite9B, Llama3LongCite8B


__all__ = [
    "completion_long_cite_glm4",
    "completion_long_cite_llama3",
]


def trans_messages(messages: List[TypeMessage]) -> Tuple[str, str]:
    """"""
    last_message = messages.pop(-1)
    query, content = '', ''
    if isinstance(last_message, CiteMessage):
        for item in last_message.content:
            if item.type == "query":
                query = item.content
            elif item.type == "cite":
                content = item.content
    else:
        query = last_message.content
    return query, content


def completion_long_cite_glm4(
        model,
        tokenizer,
        messages: List[TypeMessage],
        generate_config: Optional[GLM4LongCite9B],
        **kwargs: Any,
) -> Tuple[str, CompletionUsage]:
    """"""
    gen_kwargs = {**generate_config.gen_kwargs()}
    query, context = trans_messages(messages=messages)
    output = model.query_longcite(context, query, tokenizer=tokenizer, **gen_kwargs)
    output = str(output)
    completion_tokens = len(output)
    prompt_tokens = len(context)
    total_tokens = completion_tokens + prompt_tokens
    usage = CompletionUsage(completion_tokens=completion_tokens, prompt_tokens=prompt_tokens, total_tokens=total_tokens)
    return output, usage


def completion_long_cite_llama3(
        model,
        tokenizer,
        messages: List[TypeMessage],
        generate_config: Optional[Llama3LongCite8B],
        **kwargs: Any,
):
    """"""
    gen_kwargs = {**generate_config.gen_kwargs()}
    context, query = trans_messages(messages=messages)
    output = model.query_longcite(context, query, tokenizer=tokenizer, **gen_kwargs)
    output = str(output)
    completion_tokens = len(output)
    prompt_tokens = len(context)
    total_tokens = completion_tokens + prompt_tokens
    usage = CompletionUsage(completion_tokens=completion_tokens, prompt_tokens=prompt_tokens, total_tokens=total_tokens)
    return output, usage
