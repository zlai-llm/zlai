import unittest
from zlai.documents.load_md import ParseMarkdown
from zlai.graph import *

markdown_text = """
# 副食产业
## 瓜果
- 西瓜
- 哈密瓜
## 干果
- 核桃
    - 山核桃
- 花生
- 杏仁
    - 高级杏仁
- 栗子
    - 美栗子
        - 红枣
## 蔬菜
## 肉类
"""


class TestMarkdown(unittest.TestCase):
    def test_markdown(self):
        """"""
        parse_md = ParseMarkdown(text=markdown_text)
        print(parse_md.to_table())

    def test_graph(self):
        """"""
        parse_md = ParseMarkdown(text=markdown_text)
        df = parse_md.to_table()
        graph_data = GraphData(df)
        c = graph_data.render(
            nodes=graph_data.nodes,
            links=graph_data.links,
            categories=graph_data.categories,
            show_legend=True,
        )
        c.render()

    def test_tree(self):
        """"""
        parse_md = ParseMarkdown(text=markdown_text)
        df = parse_md.to_table()

        tree_data = TreeData(df)
        c = tree_data.render(data=tree_data.chart_data, orient="LR")
        c.render()
