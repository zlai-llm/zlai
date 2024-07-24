from dataclasses import dataclass
from ...prompt import PromptTemplate
from ...schema.messages import Message, SystemMessage
from ..schema import AgentPrompt


__all__ = [
    "prompt_csv_agent",
    "prompt_csv_qa",
    "prompt_csv_script",
    "prompt_csv_observation",
]


# write pandas dataframe code for QA
PromptDataFrameCode = """You have access to a pandas dataframe `df`. \
Here is the output of `df.head().to_markdown()`:

```
{df_head_markdown}
```

Given a user question, write the Python code to answer it. \
Return ONLY the valid Python code and nothing else. \
Don't assume you have access to any libraries other than built-in Python ones and pandas."""

prompt_dataframe_code = PromptTemplate(
    input_variables=["df_head_markdown"],
    template=PromptDataFrameCode)

system_message_dataframe_summary = SystemMessage(content="""
Given you a question and the execution result of the relevant code, please answer the user's question concisely based on the observation.
""")

PromptObservationSummary = """
Question: {question}
Script: {script}
Observation：```\n{observation}\n```
Answer：
"""

prompt_dataframe_observation_summary = PromptTemplate(
    input_variables=["question", "script", "observation"],
    template=PromptObservationSummary)

# just for csv head QA
PromptCSV = """The following is the top 5 lines of a table, \
please answer the user’s question according to these contents.

```
{df_head_markdown}
```
"""

prompt_csv = PromptTemplate(input_variables=["df_head_markdown"], template=PromptCSV)

# CSVAgent
prompt_csv_agent = AgentPrompt(system_template=prompt_dataframe_code,)
# CSVQA
prompt_csv_qa = AgentPrompt(system_template=prompt_csv)
# CSVScript
prompt_csv_script = AgentPrompt(system_template=prompt_dataframe_code)
# CSVObservation
prompt_csv_observation = AgentPrompt(
    system_message=system_message_dataframe_summary,
    prompt_template=prompt_dataframe_observation_summary,
)
