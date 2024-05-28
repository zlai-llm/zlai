import re
import httpx
from typing import List, Optional
from zlai.utils import LoggerMixin
from zlai.schema import *
from zlai.llms import *


__all__ = [
    "WebSearch"
]


system_prompt_wikipedia = """
You run in a loop of Thought, Action, Observation.
At the end of the loop you output an Answer
Use Thought to describe your thoughts about the question you have been asked.
Use Action to run one of the actions available to you。
Observation will be the result of running those actions.

Your available actions is:

call_wikipedia:
e.g. call_wikipedia: China
Returns a summary from searching China on wikipedia

You can look things up on wikipedia if you have the opportunity to do so, or you are not sure about the query

Example1:

Question: What is the capital of France?
Thought: I can look up France on wikipedia
Action: call_wikipedia: France

You will be called again with this:

Observation: France is a country. The capital is Paris.

You then output:

Answer: The capital of France is Paris

Example2:

Question: How many Administrative Autonomous Region are there in China? Try to list all of them.
Thought: I can search the autonomous region in China by Google 
Action: call_wikipedia: autonomous region in China

Observation: There are five autonomous regions in China, namely Inner Mongolia, Guangxi, Tibet, Ningxia, Xinjiang

Answer: There are 5 autonomous regions in China, the name of autonomous regions are listed as follows
1. Inner Mongolia
2. Guangxi
3. Ningxia
4. Xinjiang
5. Tibet
""".strip()


system_prompt_wikipedia_zh = """
你是一个信息检索机器人，你需要一步一步的进行思考：

第一步, 思考任务，但不给出回答：
    1. Thought: 思考用户的问题，总结搜索关键词。
    2. Action: 执行搜索任务。
第二步，等待搜索引擎查询的结果：
    3. Observation: 搜索结果。
第三步，你总结搜索结果并给出最终回答：
    4. Answer: 回答结果。

你可以使用以下搜索方式:

call_wikipedia:
e.g. call_wikipedia: 中国
返回从wikipedia上搜索到的关于中国的相关信息摘要。
""".strip()


few_shot = [
    UserMessage(content="Question: 法国的首都是哪里?"),
    AssistantMessage(content="""Thought: 我可以在维基百科上检索法国相关的信息\nAction: call_wikipedia: 法国"""),
    UserMessage(content="""Question: 法国的首都是哪里?\nObservation: 法国是一个国家。首都是巴黎。"""),
    AssistantMessage(content="""Answer: 法国的首都是巴黎。"""),
]


class FUNCTIONS:
    """ All available functions for calling """
    @classmethod
    def call_wikipedia(cls, query: str):
        """ The wikipedia search function """
        return httpx.get("https://zh.wikipedia.org/w/api.php", params={
            "action": "query",
            "list": "search",
            "srsearch": query,
            "format": "json"
        }).json()["query"]["search"][0]["snippet"]


# Available functions
available_functions = {
    "call_wikipedia": FUNCTIONS.call_wikipedia,
}

# User query and system prompt to form the messages
user_query = f"How many provinces are there in China? Please list all of them."


class ReAct:
    """"""
    @classmethod
    def print(cls):
        """"""


class WebSearch(LoggerMixin):
    """"""
    llm: TypeLLM
    messages: List[Message]
    # regular expression regex patterns
    action_re = re.compile('^Action: (\w+): (.*)$')
    answer_re = re.compile("Answer: ")
    verbose: Optional[bool]

    def __init__(
            self,
            llm: TypeLLM,
            verbose: Optional[bool] = False
    ):
        """"""
        self.llm = llm
        self.verbose = verbose

    @classmethod
    def _make_messages(cls, query: str) -> List[Message]:
        """"""
        messages = [SystemMessage(content=system_prompt_wikipedia_zh)]
        messages.extend(few_shot)
        messages.append(UserMessage(content=f"Question: {query}"))
        return messages

    def generate(self, query: str) -> str:
        """"""
        self.messages = self._make_messages(query=query)

        while True:
            response = self.llm.generate(messages=self.messages)

            # Get the response from the GPT and add it as a part of memory
            response_content = response.choices[0].message.content
            self.messages.append(AssistantMessage(content=response_content))

            # If the response contains the keyword "Answer: ", then return
            if self.answer_re.search(response_content):
                self._logger_color(msg=response_content)
                break

            # Print the thinking process
            self._logger_color(msg=response_content)

            # Take actions
            action = self.action_re.match(response_content.split("\n")[-1])
            if action:
                action, action_input = action.groups()
                try:
                    self._logger_color(msg=f"Running ... {action} {action_input}")
                    obervation = available_functions[action](action_input)
                    self._logger_color(msg=f"Observation: {obervation}")
                    self.messages.append(UserMessage(content=f"Question: {query}\nObservation: {obervation}"))
                except:
                    raise NotImplementedError
            else:
                self._logger_color(msg=f"No Action is detected, you can give some feedback by input.")
                break
        return response_content
