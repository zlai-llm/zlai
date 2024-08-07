from typing import Literal, Optional
from pyecharts import options as opts
from pyecharts.charts import Tree


__all__ = [
    "tree_chart",
]


def tree_chart(
        data,
        title: str = 'TreeGraph',
        orient: Literal["BT", "TB", "LR", "RL"] = "LR",
        layout: Optional[Literal["radial"]] = None,
        width: Optional[str] = "1200px",
        height: Optional[str] = "900px",
        show_title: bool = True,
        show_legend: bool = True,
):
    """"""
    if orient in ["BT", "TB",]:
        label_opts = {"position": "top", "horizontal_align": "right", "vertical_align": "middle", "rotate": -90, }
    else:
        label_opts = {"position": "bottom", "horizontal_align": "center", "vertical_align": "middle", "rotate": 0, }

    c = (
        Tree(init_opts=opts.InitOpts(width=width, height=height))
        .add(
            "graph",
            data,
            collapse_interval=0,
            layout=layout,
            orient=orient,
            label_opts=opts.LabelOpts(**label_opts),
        )
        .set_global_opts(
            title_opts=opts.TitleOpts(is_show=show_title, title=title,),
            legend_opts=opts.LegendOpts(is_show=show_legend, orient="vertical", pos_left="2%", pos_top="20%"),
        )
    )
    return c
