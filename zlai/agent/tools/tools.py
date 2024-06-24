from typing import Annotated
import subprocess
from .register import *

# from .browser import tool_call as browser
# from .cogview import tool_call as cogview
# from .python import tool_call as python
#
# ALL_TOOLS = {
#     "simple_browser": browser,
#     "python": python,
#     "cogview": cogview,
# }


__all__ = [
    "random_number_generator",
    "get_weather",
    "get_shell",
]


def random_number_generator(
        seed: Annotated[int, "The random seed used by the generator", True],
        range: Annotated[tuple[int, int], "The range of the generated numbers", True],
) -> int:
    """
    Generates a random number x, s.t. range[0] <= x < range[1]
    """
    if not isinstance(seed, int):
        raise TypeError("Seed must be an integer")
    if not isinstance(range, tuple):
        raise TypeError("Range must be a tuple")
    if not isinstance(range[0], int) or not isinstance(range[1], int):
        raise TypeError("Range must be a tuple of integers")
    import random
    return random.Random(seed).randint(*range)


def get_weather(
        city_name: Annotated[str, "The name of the city to be queried", True],
) -> str:
    """
    Get the current weather for `city_name`
    """

    if not isinstance(city_name, str):
        raise TypeError("City name must be a string")

    key_selection = {
        "current_condition": [
            "temp_C",
            "FeelsLikeC",
            "humidity",
            "weatherDesc",
            "observation_time",
        ],
    }
    import requests

    try:
        resp = requests.get(f"https://wttr.in/{city_name}?format=j1")
        resp.raise_for_status()
        resp = resp.json()
        ret = {k: {_v: resp[k][0][_v] for _v in v} for k, v in key_selection.items()}
    except:
        import traceback
        ret = ("Error encountered while fetching weather data!\n" + traceback.format_exc())
    return str(ret)


def get_shell(
        query: Annotated[str, "The command should run in Linux shell", True],
) -> str:
    """
    Use shell to run command
    """
    if not isinstance(query, str):
        raise TypeError("Command must be a string")
    try:
        result = subprocess.run(
            query,
            shell=True,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        return e.stderr
