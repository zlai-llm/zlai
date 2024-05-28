import os
import chardet
import requests
from bs4 import BeautifulSoup
from typing import Any, List, Dict, Union, Optional, Callable, Iterable

try:
    from langchain_text_splitters import CharacterTextSplitter
except ModuleNotFoundError:
    raise ModuleNotFoundError("pip install langchain_text_splitters")

from zlai.retrievers import TextClean
from zlai.llms import TypeLLM
from zlai.embedding import TypeEmbedding
from zlai.schema import SystemMessage, EmbeddingMatchOutput
from zlai.schema.content import PageContent
from zlai.agent.base import AgentMixin
from zlai.agent.prompt.tasks import TaskCompletion
from zlai.agent.prompt.bing import *


__all__ = [
    "PageContent",
    "BingSearch",
]


class BingSearch(AgentMixin):
    """"""
    bing_url = "https://api.bing.microsoft.com/v7.0/search"

    pages: List[Dict]
    pages_content: List[PageContent]
    pages_chunk_content: List[PageContent]
    chunk_size: Optional[int]
    chunk_overlap: Optional[int]
    separator: Optional[str]
    keep_separator: Optional[str]
    n_pages: Optional[int]
    content_size: Optional[int]
    match_output: Optional[EmbeddingMatchOutput]

    api_key: Optional[str]
    api_key_name: Optional[str]

    def __init__(
            self,
            agent_name: Optional[str] = "Bing Search",
            llm: Optional[TypeLLM] = None,
            embedding: Optional[TypeEmbedding] = None,
            stream: Optional[bool] = False,

            system_message: Optional[SystemMessage] = PromptBingSearch.system_message,
            prompt_template: Optional[PromptTemplate] = PromptBingSearch.summary_prompt,

            n_pages: Optional[int] = 10,
            chunk_size: Optional[int] = 1500,
            chunk_overlap: Optional[int] = 300,
            separator: Optional[str] = "。| |\n|、|，",
            keep_separator: Optional[str] = " ",
            n_chunk: Optional[int] = 1,

            api_key: Optional[str] = None,
            api_key_name: Optional[str] = "BING_SEARCH_KEY",
            logger: Optional[Callable] = None,
            verbose: Optional[bool] = False,
    ):
        """"""
        self.llm = llm
        self.embedding = embedding
        self.agent_name =agent_name
        self.stream = stream

        self.system_message = system_message
        self.prompt_template = prompt_template

        self.n_pages = n_pages
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.separator = separator
        self.keep_separator = keep_separator
        self.n_chunk = n_chunk

        self.api_key = api_key
        self.api_key_name = api_key_name
        self.logger = logger
        self.verbose = verbose

        if self.api_key is None and os.getenv(self.api_key_name) is None:
            raise ValueError(f"api_key not found, please set api key")
        elif os.getenv(self.api_key_name):
            self.api_key = os.getenv(self.api_key_name)

    def load_page_content(self, page_info: Dict) -> PageContent:
        """"""
        url = page_info.get("url")
        title = page_info.get("name")
        page_text = None
        error_msg = None
        try:
            page_content = requests.get(url, timeout=3)
            encoding = chardet.detect(page_content.content)["encoding"]
            soup = BeautifulSoup(page_content.content, "html.parser", from_encoding=encoding)
            page_text = soup.get_text()
            page_text = TextClean.clean(string=page_text)
            self._logger(msg=f"[{self.agent_name}] Loading: {title}; URL: {url}", color="blue")
        except Exception as e:
            error_msg = f"Error fetching page content: {e}"
            self._logger(msg=f"Failed: {title}", color="red")
        page_content = PageContent(url=url, title=title, content=page_text, error=error_msg)
        return page_content

    def bing_search_list(self, query: str) -> List[Dict]:
        """"""
        headers = {"Ocp-Apim-Subscription-Key": self.api_key}
        params = {"q": query, "textDecorations": True, "textFormat": "HTML", 'setLang': 'zh-hans', 'mkt': 'zh-CN'}
        response = requests.get(self.bing_url, headers=headers, params=params)
        response.raise_for_status()
        search_results = response.json()
        self.pages = search_results['webPages']['value'][:self.n_pages]
        self._logger(msg=f"[{self.agent_name}] I find: {len(self.pages)} pages about {query} Analysis those pages ...", color="green")
        return self.pages

    def search(self, query: str) -> List[PageContent]:
        """"""
        self.bing_search_list(query=query)
        self.pages_content = list(map(self.load_page_content, self.pages))
        self.pages_content = list(filter(lambda x: not x.error, self.pages_content))
        if len(self.pages_content) == 0:
            raise ValueError("No content found.")
        self._logger(msg=f"[{self.agent_name}] Find: {len(self.pages_content)} website content:", color="green")
        for page in self.pages_content:
            self._logger(msg=f"[{self.agent_name}] Title: {page.title}, Content Length: {len(page.content)}", color="cyan")
        return self.pages_content

    def split_content(self, pages_content: List[PageContent]) -> List[PageContent]:
        """"""
        splitter = CharacterTextSplitter(
            separator=self.separator,
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
            length_function=len,
            is_separator_regex=True,
            keep_separator=self.keep_separator,
        )
        self.pages_chunk_content = []
        for p in pages_content:
            content_list = splitter.split_text(p.content)
            self.pages_chunk_content.extend([PageContent(content=content, url=p.url, title=p.title, error=p.error) for content in content_list])
        self._logger(f"Split: {len(self.pages_chunk_content)} pages content.", color="green")
        return self.pages_chunk_content

    def merge_content(self, target_content: Union[List[str], List[PageContent]]) -> str:
        """"""
        if isinstance(target_content[0], PageContent):
            target_content = [item.content for item in target_content]

        if len(target_content) == 0:
            raise ValueError("No content to merge")
        elif len(target_content) == 1:
            return target_content[0]
        else:
            return "\n...\n".join([item for item in target_content])

    def match_content(
            self,
            query: str,
            pages_content: List[PageContent],
    ) -> str:
        """"""
        target = [p.content for p in pages_content]
        self.match_output = self.embedding.match(source=[query], target=target, top_n=self.n_chunk, filter="top_n")[0]
        target_content = [content for content in self.match_output.dst]
        consult_content = self.merge_content(target_content)
        return consult_content

    def generate(
            self,
            query: Union[str, TaskCompletion],
            *args: Any,
            **kwargs: Any,
    ) -> TaskCompletion:
        """"""
        task_completion = self._make_task_completion(query=query, **kwargs)
        self._logger_agent_start(name=self.agent_name)
        self._logger_agent_question(name=self.agent_name, content=task_completion.query)
        self._logger_agent_search(name=self.agent_name, content=task_completion.query)

        # search
        _ = self.search(query=task_completion.query)
        # split
        _ = self.split_content(pages_content=self.pages_content)
        # match
        consult_content = self.match_content(query=task_completion.query, pages_content=self.pages_chunk_content)
        # messages
        messages = self._make_messages(content=consult_content, question=query)
        self._show_messages(messages=messages, logger_name=self.agent_name)
        completion = self.llm.generate(messages=messages)
        task_completion.content = completion.choices[0].message.content
        self._logger_agent_final_answer(name=self.agent_name, content=task_completion.content)
        return task_completion

    def stream_generate(
            self,
            query: Union[str, TaskCompletion],
            *args: Any,
            **kwargs: Any,
    ) -> Iterable[TaskCompletion]:
        """"""
        task_completion = self._make_task_completion(query=query, **kwargs)
        self._logger_agent_start(name=self.agent_name)
        self._logger_agent_question(name=self.agent_name, content=task_completion.query)
        self._logger_agent_search(name=self.agent_name, content=task_completion.query)

        # search
        _ = self.search(query=task_completion.query)
        open_pages_message = "Open Pages:\n " + "\n".join(
            [f"- [{page.title}]({page.url})" for page in self.pages_content])
        yield self.stream_output(task_completion, message=open_pages_message)
        yield self._new_stream_line(task_completion, n=2)
        # split
        _ = self.split_content(pages_content=self.pages_content)
        # match
        consult_content = self.match_content(query=task_completion.query, pages_content=self.pages_chunk_content)
        # messages
        messages = self._make_messages(content=consult_content, question=query)
        self._show_messages(messages=messages, logger_name=self.agent_name)
        stream_task_instance = self.stream_task_completion(
            llm=self.llm, messages=messages, task_completion=task_completion)
        for task_completion in stream_task_instance:
            yield task_completion
        yield self._new_stream_line(task_completion=task_completion)
        self._logger_agent_final_answer(name=self.agent_name, content=task_completion.content)
