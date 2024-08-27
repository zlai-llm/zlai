from .template import PromptTemplate


__all__ = [
    'graph_prompt',
]


graph_template = """文本材料：```
{content}
```

你需要将以上文本材料梳理形成思维导图，以层次清晰的Markdown格式输出。"""


graph_prompt = PromptTemplate(
    input_variables=["content"],
    template=graph_template)
