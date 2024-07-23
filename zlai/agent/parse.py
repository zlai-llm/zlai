from pydantic import BaseModel
from typing import List, Dict, Union, Any, Optional, Callable, Literal
from ..llms import TypeLLM
from ..schema import Message, SystemMessage
from ..prompt import MessagesPrompt, PromptTemplate
from .base import AgentMixin
from .prompt.tasks import TaskCompletion


__all__ = [
    "ParseAgent",
]


class ParseAgent(AgentMixin):
    """"""
    def __init__(
            self,
            llm: Optional[TypeLLM] = None,
            agent_name: Optional[str] = "Parse Agent",
            system_message: Optional[SystemMessage] = None,
            system_template: Optional[PromptTemplate] = None,
            prompt_template: Optional[PromptTemplate] = None,
            few_shot: Optional[List[Message]] = None,
            messages_prompt: Optional[MessagesPrompt] = None,
            text_prepare: Optional[Callable] = None,
            parse_fun: Optional[Callable] = None,
            output_schema: Optional[Any] = None,
            schema_key: Optional[Literal["description",]] = None,
            stream: Optional[bool] = False,
            logger: Optional[Callable] = None,
            verbose: Optional[bool] = False,
            *args: Any,
            **kwargs: Any,
    ):
        """"""
        self.llm = llm
        self.agent_name = agent_name
        self.system_message = system_message
        self.system_template = system_template
        self.prompt_template = prompt_template
        self.few_shot = few_shot
        self.messages_prompt = messages_prompt
        self.text_prepare = text_prepare
        self.parse_fun = parse_fun
        self.output_schema = output_schema
        self.schema_key = schema_key
        self.stream = stream
        self.logger = logger
        self.verbose = verbose
        self.args = args
        self.kwargs = kwargs

    def _clean_text(self, content: str) -> str:
        """"""
        if self.text_prepare is not None:
            cleand_content = self.text_prepare(content)
            self._logger(msg=f"[{self.agent_name}] Cleand Content: {cleand_content}", color="green")
        else:
            cleand_content = content
        return cleand_content

    def generate(
            self,
            query: Union[str, TaskCompletion],
            *args: Any,
            **kwargs: Any,
    ) -> TaskCompletion:
        """"""
        task_completion = self._make_task_completion(query=query, **kwargs)
        self._logger(msg=f"[{self.agent_name}] User Question: {task_completion.query}", color='green')
        task_completion.query = self._clean_text(content=task_completion.query)
        messages = self._make_messages(content=task_completion.query, task_completion=task_completion, **kwargs)
        self._show_messages(messages=messages, few_shot=False, logger_name=self.agent_name)
        completion = self.llm.generate(messages=messages)
        task_completion.content = completion.choices[0].message.content
        self._logger(msg=f"[{self.agent_name}] Final Answer:\n{task_completion.content}", color="green")
        task_completion.parsed_data = self._make_output(content=task_completion.content, schema=self.output_schema, **kwargs)
        return task_completion

    def parse_content(self, content: str) -> Any:
        """"""
        if self.parse_fun is not None:
            parsed_content = self.parse_fun(content)
        else:
            raise ValueError(f"Please set parse_type or parse_fun")
        self._logger(msg=f"[{self.agent_name}] Parsed Data: {parsed_content}", color="green")
        return parsed_content

    def _make_schema_output(
            self,
            parsed_data: Dict,
            schema: Optional[Any] = None,
            schema_keys: List[str] = None
    ) -> Any:
        """"""
        data = dict()
        if self.schema_key == "description":
            if schema_keys is None:
                schema_keys = [schema_key for schema_key, _ in schema.model_json_schema()["properties"].items()]
            for schema_key, schema_property in schema.model_json_schema()["properties"].items():
                if schema_key in schema_keys:
                    description = schema_property.get("description")
                    default = schema_property.get("default")
                    if description is not None:
                        val = parsed_data.get(description, default)
                        data.update({schema_key: val})
        else:
            data = parsed_data
        return schema.model_validate(data)

    def _make_output(
            self,
            content: str,
            schema: Optional[Any] = None,
            **kwargs
    ) -> Union[str, BaseModel, None]:
        """"""
        if content is not None:
            parsed_answer = self.parse_content(content=content)
            if schema:
                return self._make_schema_output(parsed_data=parsed_answer[0], schema=schema, **kwargs)
            else:
                return parsed_answer
        else:
            return None
