from pandas import DataFrame
from typing import Any, List, Dict
from .charts import tree_chart


__all__ = [
    "TreeData"
]


class TreeData:
    """"""
    def __init__(
            self,
            df: DataFrame = None,
            src: str = 'src',
            dst: str = 'dst',
            **kwargs: Any,
    ):
        self.df = df
        self.src = src
        self.dst = dst
        self.chart_data = self.tree_chart_data(df.to_dict('records'))
        self.kwargs = kwargs

    def tree_chart_data(self, data: List[Dict]):
        """"""
        node_dict = {}
        for entry in data:
            src = entry[self.src]
            dst = entry[self.dst]
            if src not in node_dict:
                node_dict[src] = {'name': src}
            if dst not in node_dict:
                node_dict[dst] = {'name': dst}
            if 'children' not in node_dict[src]:
                node_dict[src]['children'] = []
            node_dict[src]['children'].append(node_dict[dst])
        root = None
        for node in node_dict.values():
            if self.src not in node:
                root = node
                break
        return [root]

    def render(self, **kwargs: Any):
        """"""
        return tree_chart(**kwargs)
