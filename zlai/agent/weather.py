import requests
import traceback
from typing import Any, Dict, Union, Annotated, Optional, Callable

from ..llms import TypeLLM
from ..schema import SystemMessage
from .base import AgentMixin
from .prompt.weather import *
from .prompt.tasks import TaskDescription, TaskCompletion
from .address import AddressAgent, StandardAddress
from .tasks import TaskSequence

__all__ = [
    "Weather",
    "WeatherAgent",
]


class WeatherAgent(AgentMixin):
    """"""
    agent_name: Optional[str] = "Weather Agent"
    system_message: Optional[SystemMessage] = PromptWeather.system_message,
    prompt_template: Optional[PromptTemplate] = PromptWeather.prompt_weather,

    def __init__(
            self,
            agent_name: Optional[str] = "Weather Agent",
            llm: Optional[TypeLLM] = None,
            system_message: Optional[SystemMessage] = PromptWeather.system_message,
            prompt_template: Optional[PromptTemplate] = PromptWeather.prompt_weather,
            logger: Optional[Callable] = None,
            verbose: Optional[bool] = False,
            *args: Any,
            **kwargs: Any,
    ):
        """"""
        self._clear_prompt()
        self.llm = llm
        self.agent_name = agent_name
        self.system_message = system_message
        self.prompt_template = prompt_template
        self.logger = logger
        self.verbose = verbose
        self.args = args
        self.kwargs = kwargs

    def __call__(
            self,
            query: TaskCompletion,
            *args: Any,
            **kwargs: Any,
    ) -> TaskCompletion:
        """"""
        return self.generate(query=query, *args, **kwargs)

    def get_weather(
            self,
            city_name: Annotated[str, 'The name of the city to be queried', True],
    ) -> str:
        """
        Get the current weather for `city_name`
        https://wttr.in/
        """

        if not isinstance(city_name, str):
            raise TypeError("City name must be a string")

        key_selection = {
            "current_condition": ["temp_C", "FeelsLikeC", "humidity", "weatherDesc", "observation_time"],
        }
        try:
            resp = requests.get(f"https://wttr.in/{city_name}?format=j1")
            resp.raise_for_status()
            resp = resp.json()
            ret = {k: {_v: resp[k][0][_v] for _v in v} for k, v in key_selection.items()}
        except:
            ret = "Error encountered while fetching weather data!\n" + traceback.format_exc()
        return str(ret)

    def _trans_query_city_name(self, address: Union[str, Dict, StandardAddress], ) -> Union[str, None]:
        """"""
        address_sequence = ["district", "city", "province"]
        if isinstance(address, str):
            return address
        else:
            if isinstance(address, StandardAddress):
                _dict_address = address.model_dump()
            else:
                _dict_address = address
            for address_level in address_sequence:
                if address_level in _dict_address and _dict_address[address_level] is not None:
                    return _dict_address[address_level]
            return None

    def generate(
            self,
            query: Union[str, TaskCompletion],
            *args: Any,
            **kwargs: Any,
    ) -> TaskCompletion:
        """"""
        task_completion = TaskCompletion(query=query.query, parsed_data=query.parsed_data, **kwargs)
        city_name = self._trans_query_city_name(address=query.parsed_data)
        if query is None:
            task_completion.content = f"I'm sorry, I can't find the city name in your query."
            self._logger(msg=f"End, Not find city.", color="red")
        else:
            self._logger(f"[{self.agent_name}] City Name: {city_name}", color='green')
            weather_data = self.get_weather(city_name=city_name)
            messages = self._make_messages(weather=weather_data, question=query.query)
            self._show_messages(messages=messages, logger_name=self.agent_name)
            completion = self.llm.generate(messages=messages)
            task_completion.content = completion.choices[0].message.content
            self._logger(msg=f"[{self.agent_name}] Final Answer:\n{task_completion.content}", color="green")
            return task_completion


class Weather(TaskSequence):
    """"""
    task_name: Optional[str] = "Weather"

    def __init__(
            self,
            task_name: Optional[str] = "Weather",
            *args: Any,
            **kwargs: Any,
    ):
        super().__init__(*args, **kwargs)
        self.task_name = task_name
        self.task_list = [
            TaskDescription(
                task=AddressAgent, task_id=0, task_name="地址解析机器人",
                task_description="""可以帮助你解析文本中的地址信息，并返回标准地址字段信息。""",
            ),
            TaskDescription(
                task=WeatherAgent, task_id=1, task_name="天气播报机器人",
                task_description="""提供具体的地址信息后可以帮助你查询当地的天气情况，必须提供标准地址。""",
            ),
        ]
