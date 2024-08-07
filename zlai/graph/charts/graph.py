from pyecharts import options as opts
from pyecharts.charts import Graph
from typing import List, Dict, Literal, Optional


__all__ = [
    "graph_chart"
]


def graph_chart(
        nodes: List[Dict],
        links: List[Dict],
        categories: List[Dict],
        title: str = 'RelationGraph',
        show_title: bool = False,
        layout: Optional[Literal["circular", "force"]] = "circular",
        show_legend: bool = False,
):
    """
    # layout 图的布局。可选：
        # 'none' 不采用任何布局，使用节点中提供的 x， y 作为节点的位置。
        # 'circular' 采用环形布局。
        # 'force' 采用力引导布局。
    """
    c = (
        Graph(init_opts=opts.InitOpts(width="1000px", height="600px"))
        .add(
            "",
            nodes=nodes,
            links=links,
            categories=categories,
            layout=layout,
            is_rotate_label=True,
            linestyle_opts=opts.LineStyleOpts(color="source", curve=0.5),
            label_opts=opts.LabelOpts(position="right"),
        )
        .set_global_opts(
            title_opts=opts.TitleOpts(is_show=show_title, title=title, pos_left='left'),
            legend_opts=opts.LegendOpts(is_show=show_legend, orient="vertical", pos_left="2%", pos_top="20%"),
        )
    )
    return c
