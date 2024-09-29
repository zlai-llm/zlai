import time
import requests
from bs4 import BeautifulSoup
from pydantic import Field
from typing import Any, Dict, Literal, Callable, Optional
from zlai.types.tools import ResponseData
from zlai.tools.utils import headers
from .base import *


__all__ = [
    "NewsQueryConfig",
    "News",
]


TypeNewsTheme = Literal[
    "财经导读", "产经新闻", "国内经济", "国际经济", "证券聚焦", "纵深调查",
    "经济时评", "产业透视", "商业观察", "股市评论", "商业资讯", "创业研究",
    "A股公司", "港股公司", "中概股公司", "海外公司",
]


class NewsQueryConfig(BaseRequestConfig):
    """"""
    size: Optional[int] = Field(default=20)
    theme: TypeNewsTheme = Field(default="财经导读")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def _theme(self):
        """"""
        theme_mapping = {
            "财经导读": "344",
            "产经新闻": "355",
            "国内经济": "350",
            "国际经济": "351",
            "证券聚焦": "353",
            "纵深调查": "363",
            "经济时评": "371",
            "产业透视": "372",
            "商业观察": "373",
            "股市评论": "374",
            "商业资讯": "670",
            "创业研究": "683",
            "A股公司": "349",
            "港股公司": "535",
            "中概股公司": "437",
            "海外公司": "440",
        }
        return theme_mapping.get(self.theme, "344")

    def to_params(self) -> Dict:
        """
        :return:
        """
        params = {
            "client": "web",
            "biz": "web_news_col",
            "column": self._theme(),
            "order": 1,
            "needInteractData": 0,
            "page_index": 1,
            "page_size": self.size,
            "req_trace": str(int(time.time() * 1E3)),
            "fields": "code,showTime,title,mediaName,summary,image,url,uniqueUrl,Np_dst",
            "types": "1,20",
        }
        return params


class News(BaseRequestData):
    """新闻数据"""
    def __init__(
            self,
            query_config: Optional[NewsQueryConfig] = None,
            verbose: Optional[bool] = False,
            logger: Optional[Callable] = None,
            **kwargs: Any
    ):
        """
        :param size:
        :param theme: 新闻主题
            [
                "财经导读", "产经新闻", "国内经济", "国际经济", "证券聚焦", "纵深调查",
                "经济时评", "产业透视", "商业观察", "股市评论", "商业资讯", "创业研究",
                "A股公司", "港股公司", "中概股公司", "海外公司",
            ]
        :param query_config:
        :param verbose:
        :param logger:
        :param kwargs:
        """
        if query_config is None:
            self.query_config = NewsQueryConfig.model_validate(kwargs)
        else:
            self.query_config = query_config
        self.verbose = verbose
        self.logger = logger
        self.kwargs = kwargs

    def _base_url(self) -> str:
        """"""
        base_url = "https://np-listapi.eastmoney.com/comm/web/getNewsByColumns"
        return base_url

    def load_data(self) -> ResponseData:
        """
        :return:
        """
        metadata = self.request_json().get("data", {})
        data = metadata.pop("list")
        self.update_metadata(metadata)
        self._logger(msg=f"[{__class__.__name__}] Find {len(data)} reports.", color="green")
        return ResponseData(data=data, metadata=metadata)

    def update_metadata(self, metadata: Dict):
        """新闻"""
        metadata.update({
            "description": "新闻",
            "columns": {
                "code": "新闻编码",
                "showTime": "发布时间",
                "title": "标题",
                "mediaName": "媒体",
                "summary": "摘要",
                "image": "图片",
            }
        })

    def load_content(self, url: str) -> str:
        """"""
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            raise Exception(f"load content failed, status code: {response.status_code}")
        else:
            soup = BeautifulSoup(response.text)
            content = soup.find("div", class_="txtinfos")
            if len(content) == 0:
                raise Exception("load content failed, content is empty")
            else:
                paragraphs = content.find_all("p")
                return "\n\n".join([p.text for p in paragraphs])
