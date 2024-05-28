from dataclasses import dataclass
from langchain.prompts import PromptTemplate
from ...schema import SystemMessage

__all__ = [
    "PromptTemplate",
    "PromptPyecharts",
]

system_message = SystemMessage(content="""You are a chart robot. You need to choose the appropriate\
chart data for user question. You only need to select the X-axis label and Y-axis data name in the\
data table. And title and subtitle (optional). And output just in Dict.

Example: 

The following is the top 5 lines of a table:

```table
|   Pclass |   Survived |
|---------:|-----------:|
|        1 |   0.62963  |
|        2 |   0.472826 |
|        3 |   0.244353 |
```

Question: 绘制一个条形图，显示每个舱位等级的生存率。

Answer: {'x': 'Pclass', 'y': 'Survived', 'title': '舱位等级生存率分布'}""")

PROMPT_SUMMARY_TMP = """The following is the top 5 lines of a table:

```table
{table}
```

Question: {question}
Answer: """

chart_prompt = PromptTemplate(
    input_variables=["table", "question"],
    template=PROMPT_SUMMARY_TMP)


@dataclass
class PromptPyecharts:
    """"""
    system_message: SystemMessage = system_message
    chart_prompt: PromptTemplate = chart_prompt
