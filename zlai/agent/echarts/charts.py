try:
    import pyecharts.options as opts
    from pyecharts.charts import Line, Bar
except ModuleNotFoundError:
    raise ModuleNotFoundError("pip install echarts")

from typing import List, Dict, Optional
from pydantic import BaseModel, Field


__all__ = [
    "AxisData",
    "chart_line",
    "chart_bar",
]


class AxisData(BaseModel):
    """"""
    x: Optional[List] = Field(default=None, description="x")
    data: Optional[Dict[str, List[float]]] = Field(default=None, description="y")
    title: Optional[str] = Field(default=None, description="title")
    subtitle: Optional[str] = Field(default=None, description="subtitle")


def chart_line(data: AxisData):
    """

    :param xaxis:
    :param data:
    :param title:
    :param subtitle:
    :return:
    """
    c = Line()
    c.add_xaxis(data.x)
    for key, value in data.data.items():
        c.add_yaxis(key, value)
    c.set_global_opts(title_opts=opts.TitleOpts(title=data.title, subtitle=data.subtitle))
    return c


def chart_bar(data: AxisData):
    """

    :param xaxis:
    :param data:
    :param title:
    :param subtitle:
    :return:
    """
    c = Bar()
    c.add_xaxis(data.x)
    for key, value in data.data.items():
        c.add_yaxis(key, value)
    c.set_global_opts(title_opts=opts.TitleOpts(title=data.title, subtitle=data.subtitle))
    return c
