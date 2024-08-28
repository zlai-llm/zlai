import unittest
from zlai.llms import LocalCompletion
from zlai.types.generate_config.completion import GLM4GenerateConfig, GLM4LongWriter9B
from zlai.agent.long_write import *


query = """
Paragraph 1 - Main Point: 介绍杭州的基本情况，包括地理位置、气候特点和历史背景。 - Word Count: 200 words
在本文的起始段落，我们将首先介绍杭州的基本情况。杭州，位于中国浙江省，地处长江三角洲南翼，是浙江省的政治、经济、文化和科技中心。杭州的气候属于亚热带季风气候，四季分明，温暖湿润，为游客提供了良好的旅游环境。杭州有着悠久的历史，自古以来就是文人墨客钟爱的居住地，有着丰富的文化遗产和历史遗迹，如西湖、雷峰塔等，这些都为杭州增添了独特的文化魅力。

Paragraph 2 - Main Point: 详细介绍杭州著名的旅游景点，包括西湖、灵隐寺和宋城等，并描述其特点和魅力。 - Word Count: 400 words
接下来，我们将重点介绍杭州的一些著名旅游景点。西湖是杭州的象征，被誉为“人间天堂”，其美丽景色和丰富的文化内涵吸引了无数游客。灵隐寺是杭州历史悠久的佛教圣地，寺庙建筑古朴典雅，香火旺盛。宋城则是一个集娱乐、购物、餐饮于一体的主题公园，再现了宋代市井生活的繁华景象。这些景点各具特色，共同展示了杭州深厚的文化底蕴和独特的城市魅力。
"""


class TestLongWrite(unittest.TestCase):

    def setUp(self):
        """"""
        self.llm = LocalCompletion(generate_config=GLM4GenerateConfig(), stream=False, model="glm-4-9b-chat")
        self.llm_long = LocalCompletion(generate_config=GLM4LongWriter9B(), stream=False, model="LongWriter-glm4-9b")

    def test_long_write_plan(self):
        task = LongWriteAgentPlan(llm=self.llm, verbose=True)
        completion = task("杭州旅行指南")
        print(completion.content)

    def test_long_write(self):
        """"""
        task = LongWriteAgentWrite(llm=self.llm_long, verbose=True)
        completion = task(query=query)
        print(completion.content)

    def test_agent_seq(self):
        """"""
        task = LongWriteAgent(llm=self.llm_long, verbose=True)
        completion = task(query="杭州旅行指南")
        print(completion.content)

    def test_long_write_plan_stream(self):
        """"""
        llm_long = LocalCompletion(generate_config=GLM4LongWriter9B(), stream=True, model="LongWriter-glm4-9b")
        task = LongWriteAgentPlan(llm=llm_long, verbose=True, stream=True)
        completion = task("杭州旅行指南")
        for chunk in completion:
            print(chunk)

    def test_long_write_stream(self):
        """"""
        llm_long = LocalCompletion(generate_config=GLM4LongWriter9B(), stream=True, model="LongWriter-glm4-9b")
        task = LongWriteAgent(llm=llm_long, stream=True, verbose=True)
        completion = task(query="杭州旅行指南")
        answer = ""
        for chunk in completion:
            answer += chunk.content
        print(answer)
