from unstructured.partition.html import partition_html
from urllib.parse import urljoin, urlparse
from typing import Any, List, Union, Callable, Optional

try:
    from langchain_text_splitters import CharacterTextSplitter
except ModuleNotFoundError:
    raise ModuleNotFoundError("pip install langchain_text_splitters")

from ...utils import headers
from ...llms import TypeLLM
from ...prompt import MessagesPrompt
from ...embedding import TypeEmbedding
from ...schema import Message, SystemMessage
from ...schema.content import PageContent
from ..base import AgentMixin
from ..prompt.tasks import TaskCompletion
from ..prompt.auto_web import *


__all__ = [
    "AutoDeepWeb",
    "AutoDeepWebAgent",
]


class AutoDeepWebAgent(AgentMixin):
    """"""
    max_deep: Optional[int]
    min_content_length: Optional[int]
    chunk_size: Optional[int]
    chunk_overlap: Optional[int]
    separator: Optional[str]
    keep_separator: Optional[str]
    embedding: Optional[TypeEmbedding]
    splitter: CharacterTextSplitter
    top_n: Optional[int]
    pages_content: List[PageContent]

    def __init__(
            self,
            llm: Optional[TypeLLM] = None,
            embedding: Optional[TypeEmbedding] = None,
            agent_name: Optional[str] = "Auto Deep Web Agent",

            system_message: Optional[SystemMessage] = None,
            system_template: Optional[PromptTemplate] = None,
            prompt_template: Optional[PromptTemplate] = None,
            few_shot: Optional[List[Message]] = None,
            messages_prompt: Optional[MessagesPrompt] = None,

            max_deep: Optional[int] = 0,
            max_pages: Optional[int] = 10,
            key_words: Optional[List[str]] = None,
            min_content_length: Optional[int] = 8,
            chunk_size: Optional[int] = 2000,
            chunk_overlap: Optional[int] = 500,
            separator: Optional[str] = "\n\n",
            keep_separator: Optional[str] = "\n\n",
            top_n: Optional[int] = 3,

            stream: Optional[bool] = False,
            logger: Optional[Callable] = None,
            verbose: Optional[bool] = False,
            *args: Any,
            **kwargs: Any,
    ):
        """"""
        self.llm = llm
        self.embedding = embedding
        self.agent_name = agent_name

        self.system_message = system_message
        self.system_template = system_template
        self.prompt_template = prompt_template
        self.few_shot = few_shot
        self.messages_prompt = messages_prompt

        self.max_deep = max_deep
        self.max_pages = max_pages
        self.min_content_length = min_content_length
        self.key_words = key_words
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.separator = separator
        self.keep_separator = keep_separator
        self.top_n = top_n

        self.stream = stream
        self.logger = logger
        self.verbose = verbose

        self.args = args
        self.kwargs = kwargs
        self.visited_urls = set()
        self.set_splitter()
        self.pages_content = []

    def set_splitter(self):
        """"""
        self.splitter = CharacterTextSplitter(
            separator=self.separator,
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
            length_function=len,
            is_separator_regex=True,
            keep_separator=self.keep_separator,
        )

    def get_page_content(
            self, url: str,
            title: Optional[str] = None,
            deep: Optional[int] = None,
    ) -> PageContent:
        """"""
        try:
            elements = partition_html(url=url, headers=headers)
        except Exception as e:
            elements = []
            self._logger(msg=f"Link Error: {e}", color="red")
        page_content = PageContent(url=url, deep=deep, title=title)
        if len(elements) > 0:
            page_content.content = "\n\n".join([str(element) for element in elements if len(str(element)) > 0])
        else:
            page_content.content = ""

        links_set = list()
        for element in elements:
            if element.metadata.link_urls:
                links_set.extend(list(zip(element.metadata.link_texts, element.metadata.link_urls)))
        links_set = set(links_set)

        links = []
        links_text = []
        for link_text, link in links_set:
            link = urljoin(url, link)
            url_schema = urlparse(link)
            if url_schema.netloc:
                links.append(link)
                links_text.append(link_text)
        page_content.links = links
        page_content.links_text = links_text
        return page_content

    def filter_links(
            self,
            total_links: Optional[int],
            title: Optional[str],
    ) -> bool:
        """"""
        if total_links > self.max_pages:
            if title is None:
                return False
            for key in self.key_words:
                if key in title:
                    return True
            return False
        else:
            return True

    def load_url_content(
            self,
            url: str,
            pages_content: List[PageContent],
            title: Optional[str] = None,
            deep: Optional[int] = None,
    ):
        """"""
        if deep <= self.max_deep and url is not None:
            self._logger(msg=f"[{self.agent_name}] Link: {url}", color="green")
            page_content = self.get_page_content(url=url, title=title, deep=deep)
            pages_content.append(page_content)
            self.visited_urls.add(page_content.url)
            self._logger(msg=f"[{self.agent_name}] Deep: {deep}, len: {len(page_content.content)}, visited urls: {len(self.visited_urls)}",
                         color="green")

            total_links = len(page_content.links)
            for title, link in zip(page_content.links_text, page_content.links):
                if link not in self.visited_urls and self.filter_links(total_links=total_links, title=title):
                    self.load_url_content(url=link, pages_content=pages_content, title=title, deep=deep + 1)
                else:
                    pass
                # self._logger(msg=f"Link: {link} already visited", color="yellow")

    def load_pages_content(
            self,
            url: str,
            deep: Optional[int] = 0
    ):
        """
        列出所有可点击的标签
        参数：
        - url: 要访问的网页URL
        """
        self.load_url_content(url=url, pages_content=self.pages_content, deep=deep)

    def clean_pages_content(
            self,
            pages_content: List[PageContent],
    ) -> List[str]:
        """"""
        contents = sum([page.content.split("\n\n") for page in pages_content], [])
        segments = [content for content in contents if len(content) > self.min_content_length]
        return segments

    def match_content_by_query(
            self,
            query: str,
            pages_content: List[PageContent],
    ):
        segments = self.clean_pages_content(pages_content=pages_content)
        chunks_content = self.splitter.split_text("\n\n".join(segments))

        idx = self.embedding.match_idx(source=[query], target=chunks_content, top_n=self.top_n)[0][::-1]
        matched_segments = [chunks_content[i] for i in idx]
        return "\n\n".join([segment for segment in matched_segments])


class AutoDeepWeb(AutoDeepWebAgent):
    """"""
    def __init__(
            self,
            llm: Optional[TypeLLM] = None,
            agent_name: Optional[str] = "Auto Deep Web",
            system_message: Optional[SystemMessage] = PromptAutoWeb.system_message,
            prompt_template: Optional[PromptTemplate] = PromptAutoWeb.summary_prompt,
            logger: Optional[Callable] = None,
            verbose: Optional[bool] = False,
            *args: Any,
            **kwargs: Any,
    ):
        """"""
        super().__init__(*args, **kwargs)

        self.llm = llm
        self.agent_name = agent_name
        self.system_message = system_message
        self.prompt_template = prompt_template
        self.logger = logger
        self.verbose = verbose
        self.args = args
        self.kwargs = kwargs

    def __call__(
            self,
            query: Union[str, TaskCompletion],
            *args: Any,
            **kwargs: Any,
    ) -> TaskCompletion:
        """"""
        return self.generate(query=query, *args, **kwargs)

    def find_page_content(
            self,
            url: Optional[str] = None,
    ):
        """"""
        if url is None:
            self._logger(msg=f"[{self.agent_name}] None URL.", color='red')
        else:
            self.load_pages_content(url=url, deep=0)

    def generate(
            self,
            query: Union[str, TaskCompletion],
            *args: Any,
            **kwargs: Any,
    ) -> TaskCompletion:
        """"""
        task_completion = self._make_task_completion(query=query, **kwargs)
        self._logger(msg=f"[{self.agent_name}] User Question: {task_completion.query}", color='green')
        self.find_page_content(**kwargs)
        content = self.match_content_by_query(query=task_completion.query, pages_content=self.pages_content)
        messages = self._make_messages(question=task_completion.query, content=content)
        self._show_messages(messages=messages, few_shot=False, logger_name=self.agent_name)
        completion = self.llm.generate(messages=messages)
        task_completion.content = completion.choices[0].message.content
        self._logger(msg=f"[{self.agent_name}] Final Answer:\n{task_completion.content}", color="green")
        return task_completion
