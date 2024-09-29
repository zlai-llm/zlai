import unittest
from zlai.tools.report.news import *


class TestNews(unittest.TestCase):
    """"""
    def test_news(self):
        """"""
        news = News(size=10)
        data = news.load_data()
        print(data.metadata)
        print(data.to_frame(columns=data.metadata.get("columns")).to_markdown())

    def test_news_theme(self):
        """"""
        news = News(size=10, theme="国际经济")
        data = news.load_data()
        print(data.metadata)
        print(data.to_frame(columns=data.metadata.get("columns")).to_markdown())

    def test_load_content(self):
        """"""
        url = "http://finance.eastmoney.com/news/1344,202409293194209890.html"
        news = News(size=10)
        content = news.load_content(url)
        print(content)
