from typing import Any, Dict, List, Union, Iterable, Optional, Callable

from ..llms import TypeLLM
from ..schema import Message, SystemMessage
from ..prompt import MessagesPrompt
from ..parse import ParseDict
from .base import AgentMixin
from .prompt.tasks import TaskCompletion
from .prompt.pyecharts import *
from .echarts import *

__all__ = [
    "ChartAgent"
]


class ChartAgent(AgentMixin):
    """"""
    def __init__(
            self,
            llm: Optional[TypeLLM] = None,
            stream: Optional[bool] = False,
            incremental: Optional[bool] = True,
            agent_name: Optional[str] = "Pyecharts Agent",
            system_message: Optional[SystemMessage] = PromptPyecharts.system_message,
            system_template: Optional[PromptTemplate] = None,
            prompt_template: Optional[PromptTemplate] = PromptPyecharts.chart_prompt,
            few_shot: Optional[List[Message]] = None,
            messages_prompt: Optional[MessagesPrompt] = None,
            logger: Optional[Callable] = None,
            verbose: Optional[bool] = False,
            *args: Any,
            **kwargs: Any,
    ):
        """"""
        self.llm = llm
        self.stream = stream
        self.incremental = incremental
        self.agent_name = agent_name
        self.system_message = system_message
        self.system_template = system_template
        self.prompt_template = prompt_template
        self.few_shot = few_shot
        self.messages_prompt = messages_prompt
        self.logger = logger
        self.verbose = verbose
        self.args = args
        self.kwargs = kwargs

    def plot(
            self,
            data_info: Dict[str, str],
            task_completion: TaskCompletion
    ) -> AxisData:
        """"""
        plot_data = AxisData()
        for key, name in data_info.items():
            if key == "x":
                plot_data.x = task_completion.data.get(name)
            if key == "y":
                y_data = dict()
                if isinstance(name, str):
                    name = [name]
                for n in name:
                    y_data.update({n: task_completion.data.get(n)})
                plot_data.data = y_data
        plot_data.title = data_info.get("title")
        plot_data.subtitle = data_info.get("subtitle")
        c = chart_line(plot_data)
        c.render(path="")

    def parse_data(self, task_completion: TaskCompletion) -> Dict:
        """"""
        data = ParseDict.eval_dict(task_completion.content)
        if len(data) > 0:
            return data[0]
        else:
            return {}

    def generate(
            self,
            query: Union[str, TaskCompletion],
            *args: Any,
            **kwargs: Any,
    ) -> TaskCompletion:
        """"""
        # start task
        self._logger_agent_start(name=self.agent_name)
        task_completion = self._make_task_completion(query=query, **kwargs)
        self._logger_agent_question(name=self.agent_name, content=task_completion.query)

        # message
        messages = self._make_messages(question=task_completion.query, table=task_completion.observation, **kwargs)
        self._show_messages(messages=messages, few_shot=False, drop_system=True, logger_name=self.agent_name)

        # generate
        completion = self.llm.generate(messages=messages)
        task_completion.content = completion.choices[0].message.content
        self._logger(msg=f"[{self.agent_name}] Assistant: {task_completion.content}", color="green")
        return TaskCompletion()

    def stream_generate(
            self,
            query: Union[str, TaskCompletion],
            *args: Any,
            **kwargs: Any,
    ) -> Iterable[TaskCompletion]:
        """"""
        yield TaskCompletion()
