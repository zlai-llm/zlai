from pydantic import BaseModel, Field
from typing import List, Optional


__all__ = [
    "Content",
    "LinkContent",
    "PageContent",
    "DocumentData",
]


class Content(BaseModel):
    """"""
    title: Optional[str] = Field(default=None, description="The name/title of the page")
    content: Optional[str] = Field(default=None, description="The HTML content of the page")
    vector: Optional[List[int]] = Field(default=None, description="文档向量")


class LinkContent(Content):
    """"""
    error: Optional[str] = Field(default=None, description="An error message if the page could not be fetched")


class PageContent(BaseModel):
    """ 网页内容 """
    url: Optional[str] = Field(default=None, description="The URL of the page to scrape")
    title: Optional[str] = Field(default=None, description="The name of the page")
    content: Optional[str] = Field(default=None, description="The HTML content of the page")
    vector: Optional[List[int]] = Field(default=None, description="文档向量")
    error: Optional[str] = Field(default=None, description="An error message if the page could not be fetched")
    deep: Optional[int] = Field(default=0, description="The depth of the page in the crawl")
    links: Optional[List[str]] = Field(default=None, description="The links found on the page")
    links_text: Optional[List[str]] = Field(default=None, description="The titles of the links found on the page")


class DocumentData(BaseModel):
    """ 文档内容 """
    title: Optional[str] = Field(default=None, description="文档名称")
    content: Optional[str] = Field(default=None, description="文档内容")
    vector: Optional[List[int]] = Field(default=None, description="文档向量")



