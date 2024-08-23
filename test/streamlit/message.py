import unittest
import random
import pandas as pd
from zlai.types.messages import *
from pyecharts.charts import Bar
from pyecharts.faker import Faker
from pyecharts import options as opts
from pyecharts.globals import ThemeType


class TestStreamlitMessage(unittest.TestCase):
    """"""
    def setUp(self):
        """"""

    def test_message(self):
        """"""
        image_url = "https://pics7.baidu.com/feed/e1fe9925bc315c601ae44d2fa329e7184854771b.jpeg"
        audio_path = "/Users/chensy/OneDrive/代码及文档/zlai/zlai-doc/docs/audio/audio.wav"
        chart = Bar(init_opts=opts.InitOpts(width="640px", height="300px", theme=ThemeType.MACARONS))\
            .add_xaxis(Faker.choose())\
            .add_yaxis("商家A", Faker.values())\
            .add_yaxis("商家B", Faker.values())\
            .set_global_opts(
                title_opts={"text": "Bar-通过 dict 进行配置", "subtext": "我也是通过 dict 进行配置的"}
            ).render_embed()

        table = pd.DataFrame(
            {
                "name": ["Roadmap", "Extras", "Issues"],
                "url": ["https://roadmap.streamlit.app", "https://extras.streamlit.app",
                        "https://issues.streamlit.app"],
                "stars": [random.randint(0, 1000) for _ in range(3)],
                "views_history": [[random.randint(0, 5000) for _ in range(30)] for _ in range(3)],
            }
        )

        self.messages = [
            SystemMessage(content="System"),
            UserMessage(content="Hello 👋"),
            AssistantMessage(content="Hi there! How can I help you today?"),
            ImageMessage(content="介绍一下这个图片", images_url=[image_url]),
            AudioMessage(role="assistant", content="这是我唱的歌", audios_path=[audio_path]),
            ChartMessage(content="这是我的图表", charts=[chart]),
            TableMessage(content="这是表格", tables=[table]),
        ]

        avatar_mapping = {
            "system": "🧠",
            "user": "🧑",
            "assistant": "🤖",
        }

        import streamlit as st
        for message in self.messages:
            with st.chat_message(message.role, avatar=avatar_mapping.get(message.role)):
                message.show_streamlit()


if __name__ == "__main__":
    test = TestStreamlitMessage()
    test.test_message()
