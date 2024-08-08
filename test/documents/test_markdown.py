import unittest
from zlai.documents.load_md import *
from zlai.graph import *


class TestMarkdown(unittest.TestCase):

    def setUp(self):
        """"""
        with open("../test_data/graph/graph.md", "r", encoding="utf-8") as f:
            self.markdown_text = f.read()

    def test_markdown(self):
        """"""
        parse_md = ParseMarkdown(text=self.markdown_text)
        df_table = parse_md.to_table()
        df_table.to_csv("./graph.csv", index=False)
        print(parse_md.to_table())

    def test_graph(self):
        """"""
        parse_md = ParseMarkdown(text=self.markdown_text)
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
        parse_md = ParseMarkdown(text=self.markdown_text)
        df = parse_md.to_table()

        tree_data = TreeData(df)
        c = tree_data.render(data=tree_data.chart_data, orient="LR")
        c.render()

    def test_get_source(self):
        """"""
        parse_md = ParseMarkdown(text=self.markdown_text)
        df = parse_md.to_table()
        data = get_node_source(df=df, node_name="方便火锅")
        print(data)
