import pandas as pd
from ..utils import log
from ..schema import UserPrompt
from .agent import *
from typing import *

from langchain.prompts import PromptTemplate


__all__ = [
    "DFAgent",
]


DF_TOOL_HOOKS = {}
DF_TOOL_DESCRIPTIONS = []

PromptDataFrame = """请依据用户问题续写代码，
```python
import pandas as pd

df = pd.read_csv('data.csv')
print(df.columns.tolist())

>>> {columns}
```

问题：{question}

要求：不需要进行解释，文件已经被读取不要重复上面的代码，最终打印出输出内容。"""

code_prompt = PromptTemplate(
    input_variables=["columns", "question"],
    template=PromptDataFrame)


PromptObservationSummary = """
以下是代码执行返回的内容：{observation}
请回答问题：{question}
"""


observation_summary_prompt = PromptTemplate(
    input_variables=["observation", "question"],
    template=PromptObservationSummary)


class DFAgent(BaseAgent):
    """"""
    def __init__(
            self,
            stream: Optional[bool] = False,
            verbose: bool = True,
            csv_path: Optional[str] = None
    ):
        self.verbose = verbose
        self.stream = stream
        self.csv_path = csv_path
        self.df = pd.read_csv(csv_path)
        self.columns = self.df.columns

    def __call__(self, query, *args, **kwargs):
        """"""
        code_query = code_prompt.format_prompt(
            columns=self.columns, question=query).to_string()
        self.call_message(query=code_query)
        observation = self.execute(df=self.df, query=self.code)

        log(f"Observation: {observation}.")

        summary_query = observation_summary_prompt.format_prompt(
            observation=observation, question=query).to_string()
        self.messages.append(UserPrompt(content=summary_query).model_dump())

        response = self.llm.generate(prompt=self.messages)
        return response
