try:
    import pyecharts.options as opts
    from pyecharts.charts import Line, Bar, Pie, Radar, Scatter, Map
except ModuleNotFoundError:
    raise ModuleNotFoundError("pip install echarts")

import random
import numpy as np
from typing import Any, List, Dict, Tuple, Literal, Optional, Annotated


__all__ = [
    "base_chart",
    "pie_chart",
    "radar_chart",
    "scatter_chart",
    "map_chart",
]


base_chart_mapping = {
    "Line": Line,
    "Bar": Bar,
    "Pie": Pie,
    "Radar": Radar,
}

colors = [
    '#c23531', '#2f4554', '#61a0a8', '#d48265', '#91c7ae', '#749f83', '#ca8622', '#bda29a', '#6e7074',
    '#546570', '#c4ccd3']


def base_chart(
        chart_type: Annotated[Literal["Line", "Bar"], "图表类型", True],
        x_ticks: Annotated[List[Any], "X轴刻度名称", True],
        data: Annotated[Dict[str, List[float]], "数据", True],
        title: Annotated[str, "标题", True],
        sub_title: Annotated[Optional[str], "副标题", True] = None,
        save_path: Annotated[Optional[str], "保存路径", False] = None,
):
    """
    绘制折线图、柱状图
    :param chart_type: Literal["Line", "Bar", "Pie", "Radar"]
    :param x_ticks: X轴刻度名称
    :param data: 数据
    :param title: 标题
    :param sub_title: 副标题
    :param save_path: 保存路径
    :return: 是否成功输出图片日志

    Example:
        1. 绘制2020年1月1日至2020年1月5日每日气温折线图，气温数据为 8℃、12℃、9℃、18℃、12℃（中国气象局）。
            ```
            base_chart(
                chart_type="Line",
                x_ticks=["2020-1-1", "2020-1-2", "2020-1-3", "2020-1-4", "2020-1-5"],
                data={"气温": [8, 12, 9, 18, 12]},
                title="2020年1月1日至2020年1月5日每日气温",
                sub_title="气温数据来源：中国气象局",
            )
            ```
    """
    c = base_chart_mapping.get(chart_type)()
    c.add_xaxis(x_ticks)
    for key, value in data.items():
        c.add_yaxis(key, value)
    c.set_global_opts(title_opts=opts.TitleOpts(title=title, subtitle=sub_title))

    if save_path is None:
        save_path = f"./{chart_type}.html"
    c.render(path=save_path)
    return f"{chart_type} chart save path: {save_path}"


def pie_chart(
        data: Annotated[Dict[str, float], "数据", True],
        title: Annotated[str, "标题", True],
        sub_title: Annotated[Optional[str], "副标题", True] = None,
        save_path: Annotated[Optional[str], "保存路径", False] = None,
):
    """
    绘制饼图
    :param data: 数据
    :param title: 标题
    :param sub_title: 副标题
    :param save_path: 保存路径
    :return: 是否成功输出图片日志

    Example:
        1. 中国、美国、日本的GDP分别为 17万亿、19万亿、7万亿，请绘制饼图展示。
            ```
            pie_chart(
                data={"中国": 17, "美国": 19, "日本": 7},
                title="中国、美国、日本的GDP",
                sub_title="数据来源：无",
            )
            ```
    """
    c = Pie()
    c.add("", [list(z) for z in data.items()])
    c.set_global_opts(title_opts=opts.TitleOpts(title=title, subtitle=sub_title))
    c.set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))
    if save_path is None:
        save_path = f"./pie.html"
    c.render(path=save_path)
    return f"Pie chart save path: {save_path}"


def radar_chart(
        labels: Annotated[List[str], "雷达维度标签", True],
        data: Annotated[Dict[str, float], "数据", True],
        title: Annotated[str, "标题", True],
        sub_title: Annotated[Optional[str], "副标题", True] = None,
        save_path: Annotated[Optional[str], "保存路径", False] = None,
):
    """
    绘制雷达图
    :param labels: 雷达维度标签
    :param data: 数据
    :param title: 标题
    :param sub_title: 副标题
    :param save_path: 保存路径
    :return: 是否成功输出图片日志

    Example:
        1. 小明期末考试成绩为数学76分、英语88分、语文98分，小红期末考试成绩为数学96分、英语78分、语文87分请绘制雷达图展示。
            ```
            radar_chart(
                labels=["数学", "英语", "语文"],
                data={"小明": [76, 88, 98], "小红": [96, 78, 87]},
                title="小明、小红期末考试成绩",
                sub_title="数据来源：无",
            )
            ```
    """
    data_metrix = np.array(list(data.values()))
    schema = [opts.RadarIndicatorItem(name=label, max_=max_) for label, max_ in zip(labels, data_metrix.max(axis=0))]

    c = Radar()
    c.add_schema(schema=schema)
    for i, (name, value) in enumerate(data.items()):
        c.add(name, [value], color=random.choice(colors))
    c.set_series_opts(label_opts=opts.LabelOpts(is_show=False))
    c.set_global_opts(title_opts=opts.TitleOpts(title=title, subtitle=sub_title))

    if save_path is None:
        save_path = f"./radar.html"
    c.render(path=save_path)
    return f"Radar chart save path: {save_path}"


def scatter_chart(
        x_data: Annotated[List[float], "x轴坐标", True],
        y_data: Annotated[List[float], "y轴坐标", True],
        title: Annotated[str, "标题", True],
        sub_title: Annotated[Optional[str], "副标题", True] = None,
        save_path: Annotated[Optional[str], "保存路径", False] = None,
):
    """
    绘制散点图
    :param x_data: x轴坐标
    :param y_data: y轴坐标
    :param title: 标题
    :param sub_title: 副标题
    :param save_path: 保存路径
    :return: 是否成功输出图片日志

    Example:
        1. 有一些列随机点，[[10, 2], [3, 2], [8, 9]] 请绘制一个散点图进行展示。
            ```
            scatter_chart(
                x_data=[10, 3, 8],
                y_data=[2, 2, 9],
                title='散点图'
            )
            ```
    """
    c = Scatter()
    c.add_xaxis(xaxis_data=x_data)
    c.add_yaxis(series_name="", y_axis=y_data,)
    c.set_series_opts(label_opts=opts.LabelOpts(is_show=False))
    c.set_global_opts(
        title_opts=opts.TitleOpts(title=title, subtitle=sub_title),
        tooltip_opts=opts.TooltipOpts(is_show=False),
        xaxis_opts=opts.AxisOpts(
            type_="value", splitline_opts=opts.SplitLineOpts(is_show=True)
        ),
        yaxis_opts = opts.AxisOpts(
            type_="value",
            axistick_opts=opts.AxisTickOpts(is_show=True),
            splitline_opts=opts.SplitLineOpts(is_show=True),
        ),
    )

    if save_path is None:
        save_path = f"./scatter.html"
    c.render(path=save_path)
    return f"Scatter chart save path: {save_path}"


def map_chart(
        data: Annotated[List[Dict[str, float]], "地区数据", True],
        title: Annotated[str, "标题", True],
        sub_title: Annotated[Optional[str], "副标题", True] = None,
        map_type: Annotated[Literal["china"], "地图地区", False] = "china",
        save_path: Annotated[Optional[str], "保存路径", False] = None,
):
    """
    将数据依据地区绘制在地图上
    :param data: 地区数据
    :param title: 标题
    :param sub_title: 副标题
    :param map_type: 地图地区
    :param save_path: 保存路径
    :return: 是否成功输出图片日志

    Example:
        1. 2024年一季度的河北省、河南省、浙江省、广东省GDP数据为1.2万亿、1.3万亿、2.5万亿、4.5万亿，绘制一个地图清晰展示该数据，
            ```
            map_chart(
                data=[{"河北省": 1.2}, {"河南省": 1.3}, {"浙江省": 2.5}, {"广东省": 4.5}],
                title='2024年一季度GDP',
                sub_title='河北省、河南省、浙江省、广东省',
            )
            ```
    """
    map_type = map_type.lower()
    data = [list(item.items())[0] for item in data]
    max_data = max([item[1] for item in data])
    c = Map()
    c.add("", data, maptype=map_type)
    c.set_global_opts(
        title_opts=opts.TitleOpts(title=title, subtitle=sub_title),
        visualmap_opts=opts.VisualMapOpts(max_=max_data, is_piecewise=True),
    )
    if save_path is None:
        save_path = f"./map.html"
    c.render(path=save_path)
    return f"Map chart save path: {save_path}"
