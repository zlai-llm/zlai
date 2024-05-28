from .prompt.tasks import TaskDescription, TaskParameters
from .csv import CSVAgent, CSVQA
from .weather import WeatherAgent
from .address import AddressAgent


__all__ = [
    "task_list",
]

task_list = [
    TaskDescription(
        task=CSVAgent, task_id=0, task_name="数据提取与计算机器人",
        task_description="""可以帮你写一段`DataFrame`脚本代码查询表中数据的具体信息。""",
        task_parameters=TaskParameters(),
    ),
    TaskDescription(
        task=CSVQA, task_id=1, task_name="数据表介绍机器人",
        task_description="""可以介绍并回答数据表的基本信息，但不能够查询真实的数据，只能做一般性的介绍。""",
        task_parameters=TaskParameters(),
    ),
]

