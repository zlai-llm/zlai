from pandas import DataFrame
from typing import List, Dict, Any, Union, Optional
from .charts import graph_chart


__all__ = [
    "GraphData",
]


class GraphData:
    """
    graph_data = GenGraphData(df=df_top_chain)
    categories = graph_data.gen_categories()
    nodes = graph_data.gen_nodes()
    links = graph_data.gen_links()
    """
    links: List[Dict]
    categories: List[Dict]
    nodes: List[Dict]
    categories_map: Dict[str, int]

    def __init__(
            self,
            df: DataFrame = None,
            symbol_size_name: Optional[str] = None,
            default_symbol_size: int = 20,
            src: str = 'src',
            dst: str = 'dst',
            **kwargs: Any,
    ):
        super().__init__(**kwargs)
        self.df = df
        self.src = src
        self.dst = dst
        self.symbol_size_name = symbol_size_name
        self.default_symbol_size = default_symbol_size

        self.links = []
        self.nodes = []
        self.categories = []
        self.categories_map = dict()
        self.nodes_name = list(set(sum([df[src].tolist(), df[dst].tolist()], [])))
        self._gen_name_id()
        self.gen_categories()
        self.gen_nodes()
        self.gen_links()

    def _gen_name_id(self, ):
        """"""
        self.name_id = dict(zip(self.nodes_name, range(len(self.nodes_name))))

    def gen_categories(self, ):
        """"""
        source_id = 0
        source = self.df.src.unique()
        for source_id, source_name in enumerate(source):
            self.categories.append({
                'id': source_id,
                'name': source_name,
                'description': f'<source {source_name}>'
            })
            self.categories_map.update({source_name: source_id})

        for group_name, group in self.df.groupby('src'):
            source_id += 1
            group_target = group.dst.tolist()
            self.categories.append({
                'id': source_id,
                'name': group_name,
                'description': f'<target {group_name}>',
            })
            for dst_name in group_target:
                self.categories_map.update({dst_name: source_id})

    def gen_nodes(self, ):
        """"""
        size_mapping = None
        if isinstance(self.symbol_size_name, str):
            size_mapping = dict(zip(self.df[self.src], self.df[self.symbol_size_name]))

        for node_name in self.nodes_name:
            if size_mapping is not None:
                symbol_size = size_mapping.get(node_name, self.default_symbol_size)
            else:
                symbol_size = self.default_symbol_size
            node = {
                'id': self.name_id.get(node_name),
                "name": node_name,
                "symbolSize": symbol_size,
                "category": self.categories_map.get(node_name)
            }
            self.nodes.append(node)

    def gen_links(self, ):
        """"""
        self.links = [
            {"id": i, "source": self.name_id.get(line['src']), "target": self.name_id.get(line['dst'])}
            for i, line in enumerate(self.df.to_dict('records'))]

    def render(self, **kwargs):
        """"""
        return graph_chart(**kwargs)
