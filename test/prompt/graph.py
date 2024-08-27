import os
import unittest
from openai import OpenAI
from zlai.prompt import graph_prompt
from zlai.parse import ParseCode
from zlai.documents.load_md import ParseMarkdown
from zlai.graph import GraphData, TreeData


class TestGraph(unittest.TestCase):

    def setUp(self):
        with open("../test_data/document/graph.md", "r", encoding="utf-8") as f:
            self.content = f.read()

    def test_graph(self):
        client = OpenAI(api_key="1234", base_url=os.getenv("BASE_URL"))
        messages = [graph_prompt.format_prompt(content=self.content).to_messages("user")]
        response = client.chat.completions.create(
            model="glm-4-9b-chat-1m",
            messages=messages,
            stream=False
        )
        print(response)

    def test_render_graph(self):
        with open("../test_data/document/out_graph.md", "r", encoding="utf-8") as f:
            content = f.read()
        data = ParseCode.sparse_script(string=content, script="markdown")[0]
        df_graph = ParseMarkdown(text=data).to_table()
        print(df_graph)
        tree_data = TreeData(df=df_graph)
        c = tree_data.render(
            data=tree_data.chart_data, orient="LR", title='',
            width="780px", height="1000px"
        ).render()

