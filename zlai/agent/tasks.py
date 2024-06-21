import re
from typing import Any, List, Dict, Tuple, Iterable, Literal, Optional, Callable
from langchain.prompts import PromptTemplate

from ..prompt import MessagesPrompt
from ..schema import Message, SystemMessage
from ..embedding import Embedding
from ..parse import ParseList
from ..llms import *
from .base import *
from .prompt.tasks import *


__all__ = [
    "Tasks",
    "TaskSwitch",
    "TaskSequence",
    "TaskPlan"
]


class Tasks(AgentMixin):
    """"""
    task_prompt: Optional[TaskSwitchPrompt]
    task_list: Optional[List[TaskDescription]]
    task_mapping: Optional[Dict[str, int]]

    def __init__(
            self,
            llm: Optional[TypeLLM] = None,
            embedding: Optional[Embedding] = None,
            task_prompt: Optional[TaskSwitchPrompt] = None,

            system_message: Optional[SystemMessage] = None,
            system_template: Optional[PromptTemplate] = TaskSwitchPrompt.task_prompt,
            prompt_template: Optional[PromptTemplate] = None,
            few_shot: Optional[List[Message]] = None,
            messages_prompt: Optional[MessagesPrompt] = None,
            task_list: Optional[List[TaskDescription]] = None,

            parse_code: Literal["python", "sql"] = "python",
            stream: Optional[bool] = False,
            logger: Optional[Callable] = None,
            verbose: Optional[bool] = False,
            *args: Any,
            **kwargs: Any,
    ):
        """"""
        self.llm = llm
        self.embedding = embedding

        self.task_prompt = task_prompt
        self.system_message = system_message
        self.system_template = system_template
        self.prompt_template = prompt_template
        self.few_shot = few_shot
        self.messages_prompt = messages_prompt

        self.parse_code = parse_code
        self.task_list = task_list

        self.stream = stream
        self.logger = logger
        self.verbose = verbose

        self.args = args
        self.kwargs = kwargs

        if task_list:
            self.task_mapping = self._get_task_mapping(task_list)
            self._make_system_message(task_info=self.task_info(task_list=self.task_list))

    def _validate_task_list(self):
        """"""
        if len(self.task_list) == 0:
            raise ValueError(f"Task List ERROR: Not find Task.")


class TaskSwitch(Tasks):
    """"""
    task_name: Optional[str] = "Task Switch"

    def __init__(
            self,
            task_name: Optional[str] = "Task Switch",
            system_template: Optional[PromptTemplate] = TaskSwitchPrompt.task_prompt,
            use_memory: Optional[bool] = False,
            *args: Any,
            **kwargs: Any,
    ):
        super().__init__(*args, **kwargs)
        self.task_name = task_name
        self.system_template = system_template
        self.task_completions = []
        self.use_memory = use_memory
        self.args = args
        self.kwargs = kwargs

    def make_task_system_message(self):
        """"""
        self.task_mapping = self._get_task_mapping(self.task_list)
        self._make_system_message(task_info=self.task_info(task_list=self.task_list))

    def parse_task(self, content: str) -> TaskDescription:
        """"""
        def _parse_task(content: str) -> List[str]:
            """"""
            matches = re.findall(r"\d+", content)
            return matches
        match_task_idx = _parse_task(content=content)
        self._logger(msg=f"[{self.task_name}] matched task id: {match_task_idx}\n", color="green")
        if len(match_task_idx) == 0:
            return TaskDescription()
        else:
            task_id = int(match_task_idx[0])
            for task in self.task_list:
                if task.task_id == task_id:
                    self._logger(msg=f"[{self.task_name}] task id: {task.task_id}, task name: {task.task_name}, content: [{content}]\n",
                                 color="green")
                    return task
            return TaskDescription()

    def _validate_switch_llm_stream(self):
        """"""
        if self.llm.generate_config.stream:
            self.llm.generate_config.stream = False

    def _validate_task_llm_stream(self, gen_config: Dict):
        """"""
        gen_config.update({"stream": self.stream})
        gen_config["llm"].generate_config.stream = self.stream

    def switch_task(self, task_completion: TaskCompletion) -> TaskDescription:
        """"""
        messages = self._make_messages(
            content=task_completion.query,
            task_info=self.task_info(task_list=self.task_list),
        )
        self._show_messages(messages=messages, drop_system=True, content_length=None, logger_name="Task")
        self._validate_switch_llm_stream()
        completion = self.llm.generate(messages=messages)
        content = completion.choices[0].message.content
        task = self.parse_task(content)

        task_completion.task_description = task
        self.task_completions.append(self._deep_copy_task_completion(task_completion))
        return task

    def update_task_params(self, task_params: Dict, items: List[Tuple]):
        """"""
        for key, val in items:
            if key not in task_params:
                task_params.update({key: val})

    def update_gen_config_few_shot(self, gen_config: Dict):
        """"""
        if "few_shot" in gen_config:
            gen_config.update({"few_shot": [Message.model_validate(shot) for shot in gen_config["few_shot"]]})

    def update_gen_config_system_message(self, gen_config: Dict):
        """"""
        if "system_message" in gen_config:
            gen_config.update({"system_message": SystemMessage.model_validate(gen_config["system_message"])})

    def _task_config(self, task: TaskDescription, *args: Any, **kwargs: Any) -> Dict:
        """"""
        if task.task_parameters:
            gen_config = {**self.kwargs, **task.task_parameters.params(), **kwargs}
        else:
            gen_config = {**self.kwargs, **kwargs}
        self.update_gen_config_system_message(gen_config)
        self.update_gen_config_few_shot(gen_config)
        self._validate_task_llm_stream(gen_config)
        return gen_config

    def register_task_agent_and_generate(self, task: TaskDescription, *args: Any, **kwargs: Any):
        """"""
        gen_config = self._task_config(task, *args, **kwargs)
        _task_generate = task.task(**gen_config)
        task_completion = _task_generate(query=self.task_completions[-1], *args, **kwargs)
        self.task_completions.append(self._deep_copy_task_completion(task_completion))

    def generate(
            self,
            query: Union[str, TaskCompletion],
            *args: Any,
            **kwargs: Any,
    ) -> TaskCompletion:
        """"""
        self._validate_task_list()
        self._logger(msg=f"[{self.task_name}] Start ...\n", color="green")
        task_completion = self._make_task_completion(query)
        self._logger(msg=f"[{self.task_name}] Question: {task_completion.query}", color="green")
        self.task_completions.append(self._deep_copy_task_completion(task_completion))

        task = self.switch_task(task_completion)
        if task.task_id is None:
            answer = f"[{self.task_name}] Not find task. \n{task}"
            self.task_completions.append(TaskCompletion(query=self.task_completions[-1].query, content=answer))
            self._logger(msg=answer, color="red")
        else:
            self.register_task_agent_and_generate(task=task, *args, **kwargs)
        self._logger(msg=f"[{self.task_name}] End ...\n", color="green")
        return self.task_completions[-1]

    def stream_generate(
            self,
            query: Union[str, TaskCompletion],
            *args: Any,
            **kwargs: Any,
    ) -> Iterable[TaskCompletion]:
        """"""
        self._validate_task_list()
        self._logger_agent_start(name=self.task_name)
        self._logger_agent_question(name=self.task_name, content=query)
        task_completion = self._make_task_completion(query)
        self.task_completions.append(self._deep_copy_task_completion(task_completion))

        task = self.switch_task(task_completion)
        if task.task_id is None:
            answer = f"[{self.task_name}] Not find task. \n{task}"
            self.task_completions.append(TaskCompletion(query=self.task_completions[-1].query, content=answer))
            self._logger(msg=answer, color="red")
        else:
            gen_config = self._task_config(task, *args, **kwargs)
            _task_generate = task.task(**gen_config)
            for task_completion in _task_generate(query=self.task_completions[-1], *args, **kwargs):
                yield task_completion
            self.task_completions.append(self._deep_copy_task_completion(task_completion))
        self._logger(msg=f"[{self.task_name}] End ...\n", color="green")


class TaskSequence(Tasks):
    """"""
    task_name: Optional[str] = "Task Sequence"

    def __init__(
            self,
            task_list: Optional[List[TaskDescription]] = None,
            task_name: Optional[str] = "Task Sequence",
            *args: Any,
            **kwargs: Any,
    ):
        super().__init__(*args, **kwargs)
        self.task_list = task_list
        self.task_name = task_name
        self.args = args
        self.kwargs = kwargs

    def generate(
            self,
            query: Union[str, TaskCompletion],
            *args: Any,
            **kwargs: Any,
    ) -> TaskCompletion:
        """"""
        self._validate_task_list()
        self._logger(msg=f"[{self.task_name}] Running {len(self.task_list)} tasks...\n", color="green")
        self.task_completions = []
        task_completion = self._make_task_completion(
            query, task_id=self.task_list[0].task_id, task_name=self.task_list[0].task_name)
        for i, task in enumerate(self.task_list):
            if task.task_parameters:
                gen_config = {**self.kwargs, **task.task_parameters.params(), **kwargs}
            else:
                gen_config = {**self.kwargs, **kwargs}
            _task_generate = task.task(**gen_config)
            self._logger(msg=f"[{self.task_name} @ {_task_generate.agent_name}] Start ...", color="magenta")
            task_completion = _task_generate(task_completion, *args, **kwargs)
            self.task_completions.append(self._deep_copy_task_completion(task_completion))
            self._logger(msg=f"[{self.task_name} @ {_task_generate.agent_name}] End.\n", color="magenta")
        self._logger(msg=f"[{self.task_name}] End.", color="green")
        return self.task_completions[-1]

    def stream_generate(
            self,
            query: Union[str, TaskCompletion],
            *args: Any,
            **kwargs: Any,
    ) -> Iterable[TaskCompletion]:
        """"""
        self._validate_task_list()
        self._logger(msg=f"[{self.task_name}] Running {len(self.task_list)} tasks...\n", color="green")
        self.task_completions = []
        task_completion = self._make_task_completion(
            query, task_id=self.task_list[0].task_id, task_name=self.task_list[0].task_name)
        for i, task in enumerate(self.task_list):
            if task.task_parameters:
                gen_config = {**self.kwargs, **task.task_parameters.params(), **kwargs}
            else:
                gen_config = {**self.kwargs, **kwargs}
            _task_generate = task.task(**gen_config)
            self._logger(msg=f"[{self.task_name} @ {_task_generate.agent_name}] Start ...", color="magenta")

            for task_completion in _task_generate(task_completion, *args, **kwargs):
                yield task_completion

            self.task_completions.append(self._deep_copy_task_completion(task_completion))
            self._logger(msg=f"[{self.task_name} @ {_task_generate.agent_name}] End.\n", color="magenta")
        self._logger(msg=f"[{self.task_name}] End.", color="green")


class TaskPlan(TaskSwitch):
    """"""
    task_name: Optional[str] = "Task Plan"

    def __init__(
            self,
            task_name: Optional[str] = "Task Plan",
            task_list: Optional[List[TaskDescription]] = None,
            messages_prompt: Optional[MessagesPrompt] = TaskPlanPrompt.messages_prompt,
            use_memory: Optional[bool] = False,
            *args: Any,
            **kwargs: Any,
    ):
        super().__init__(*args, **kwargs)
        self.task_list = task_list
        self.task_name = task_name
        self.messages_prompt = messages_prompt
        self.switch = TaskSwitch(task_list=task_list, use_memory=use_memory, *args, **kwargs)

    def _task_plan(self, task_completion: TaskCompletion) -> List[TaskCompletion]:
        """"""
        messages = self._make_messages(content=task_completion.query, task_completion=task_completion)
        self._show_messages(messages=messages)
        completion = self.llm.generate(messages=messages)
        content = completion.choices[0].message.content

        task_completion.content = content
        task_completion.parsed_data = ParseList.eval_list(content)[0]
        self.task_completions.append(self._deep_copy_task_completion(task_completion))

        for i, task_description in enumerate(task_completion.parsed_data):
            self._logger(msg=f"[{self.task_name}] description - [{i}]: {task_description}\n", color="green")

        task_plan = []
        for i, query in enumerate(task_completion.parsed_data):
            if len(task_completion.parsed_data) == 1:
                previous_question = None
                next_question = None
            elif i == 0:
                previous_question = None
                next_question = task_completion.parsed_data[i + 1]
            elif i + 1 == len(task_completion.parsed_data):
                previous_question = task_completion.parsed_data[i - 1]
                next_question = None
            else:
                previous_question = task_completion.parsed_data[i - 1]
                next_question = task_completion.parsed_data[i + 1]

            _task_completion = self._make_task_completion(
                query=query, query_id=i, previous_question=previous_question,
                next_question=next_question, )
            task_plan.append(_task_completion)
        return task_plan

    def generate(
            self,
            query: Union[str, TaskCompletion],
            *args: Any,
            **kwargs: Any,
    ) -> List[TaskCompletion]:
        """"""
        self._logger(msg=f"[{self.task_name}] Start ...\n", color="green")
        task_completion = self._make_task_completion(query)
        self._logger(msg=f"[{self.task_name}] Question: {task_completion.query}", color="green")
        self.task_completions.append(self._deep_copy_task_completion(task_completion))

        plan_list = self._task_plan(task_completion)
        for todo_item in plan_list:
            todo_item.task_completion = self.switch(todo_item.task, *args, **kwargs)
        return plan_list
