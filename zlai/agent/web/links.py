from langchain.prompts import PromptTemplate
from langchain_community.document_loaders import SeleniumURLLoader
from typing import List, Literal, Callable, Optional
try:
    from langchain_text_splitters import CharacterTextSplitter
except ModuleNotFoundError:
    raise ModuleNotFoundError("pip install langchain_text_splitters")

from zlai.utils import LoggerMixin
from zlai.llms import TypeLLM
from zlai.prompt import MessagesPrompt
from zlai.prompt.summary import system_message, summary_prompt
from zlai.schema import Message, SystemMessage
from zlai.schema.content import PageContent
from zlai.embedding import TypeEmbedding
from zlai.schema import UserMessage, EmbeddingMatchOutput


__all__ = [
    "WebPageMixin",
    "LinksQA",
]


class WebPageMixin(LoggerMixin):
    """"""
    chunk_size: Optional[int]
    chunk_overlap: Optional[int]
    separator: Optional[str]
    keep_separator: Optional[str]
    embedding: Optional[TypeEmbedding]

    def load_links(self, links: List[str]) -> List[PageContent]:
        """"""
        self._logger(f"Start loading ...\n", color="green")
        loader = SeleniumURLLoader(urls=links)
        page_documents = loader.load()
        pages_content = [PageContent(
            content=f"{doc.page_content}\n\n{doc.metadata.get('description', '')}",
            title=doc.metadata.get('title', ''),
            url=doc.metadata.get('url', ''),
        ) for doc in page_documents]
        self._logger(f"Load {len(pages_content)} pages\n", color="green")
        return pages_content

    def split_page_content(self, page_content: PageContent) -> List[PageContent]:
        """"""
        splitter = CharacterTextSplitter(
            separator=self.separator,
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
            length_function=len,
            is_separator_regex=True,
            keep_separator=self.keep_separator,
        )
        content_list = splitter.split_text(page_content.content)
        page_chunks_content = [PageContent(content=content, url=page_content.url, title=page_content.title, error=page_content.error) for content in content_list]
        return page_chunks_content

    def split_pages_content(self, pages_content: List[PageContent]) -> List[PageContent]:
        """"""
        splitter = CharacterTextSplitter(
            separator=self.separator,
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
            length_function=len,
            is_separator_regex=True,
            keep_separator=self.keep_separator,
        )
        pages_chunks_content = []
        for p in pages_content:
            content_list = splitter.split_text(p.content)
            pages_chunks_content.extend(
                [PageContent(content=content, url=p.url, title=p.title, error=p.error) for content in content_list])
        self._logger(f"Split: {len(pages_chunks_content)} pages content.\n", color="green")
        return pages_chunks_content

    def embedding_pages_content(
            self,
            pages_content: List[PageContent],
    ) -> List[PageContent]:
        """"""
        pages_content_list = [page.content for page in pages_content]
        vectors = self.embedding.embedding(tuple(pages_content_list)).to_list()
        for page, vector in zip(pages_content, vectors):
            page.vector = vector
        return pages_content

    def merge_content(self, matched_pages: List[PageContent]) -> str:
        """"""
        if len(matched_pages) == 0:
            raise ValueError("No content to merge.")

        matched_content = [item.content for item in matched_pages]
        if len(matched_content) == 0:
            raise ValueError("No content to merge")
        elif len(matched_content) == 1:
            return matched_content[0]
        else:
            return "\n...\n".join([item for item in matched_content])

    def match_content_by_query(
            self,
            query: str,
            pages_content: List[PageContent],
            n_content: int = 1
    ) -> List[PageContent]:
        """"""
        target = [p.content for p in pages_content]
        idx = self.embedding.match_idx(source=[query], target=target, top_n=n_content)[0][::-1]
        matched_pages = [pages_content[i] for i in idx]
        return matched_pages


class LinksQA(WebPageMixin):
    """"""
    links: Optional[List[str]]
    llm: Optional[TypeLLM]
    embedding: Optional[TypeEmbedding]

    system_message: Optional[SystemMessage]
    few_shot: Optional[List[Message]]
    messages: Optional[List[Message]]
    messages_prompt: Optional[MessagesPrompt]
    pages_content: List[PageContent]
    pages_chunk_content: List[PageContent]
    chunk_size: Optional[int]
    chunk_overlap: Optional[int]
    separator: Optional[str]
    keep_separator: Optional[str]
    match_output: Optional[EmbeddingMatchOutput]

    logger: Optional[Callable]
    verbose: Optional[bool]

    def __init__(
            self,
            llm: Optional[TypeLLM] = None,
            embedding: Optional[TypeEmbedding] = None,
            system_message: Optional[SystemMessage] = system_message,
            prompt_template: Optional[PromptTemplate] = summary_prompt,
            few_shot: Optional[List[Message]] = None,
            messages_prompt: Optional[MessagesPrompt] = None,

            chunk_size: Optional[int] = 1500,
            chunk_overlap: Optional[int] = 300,
            separator: Optional[str] = "。| |\n|、|，",
            keep_separator: Optional[str] = " ",
            n_chunks: int = 1,
            ask: Literal['page', 'pages'] = 'pages',

            logger: Optional[Callable] = None,
            verbose: Optional[bool] = False,
    ):
        """"""
        self.llm = llm
        self.embedding = embedding
        self.system_message = system_message
        self.prompt_template = prompt_template
        self.few_shot = few_shot
        self.messages_prompt = messages_prompt

        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.separator = separator
        self.keep_separator = keep_separator
        self.n_chunks = n_chunks
        self.ask = ask

        self.logger = logger
        self.verbose = verbose

    def __call__(
            self,
            links: Optional[List[str]],
            query: Optional[str],
            *args, **kwargs
    ) -> List:
        """"""
        self.links = links
        pages_content = self.load_links(links=links)
        # ask for each page
        if self.ask == 'page':
            answers = self.generate_each_page(query=query, pages_content=pages_content)
        # ask for pages
        else:
            answers = [self.generate_pages(query=query, pages_content=pages_content)]
        return answers

    def _make_message(self, content: str, question: str) -> List[Message]:
        """"""
        if self.messages_prompt:
            messages = self.messages_prompt.prompt_format(content=content, question=question)
        else:
            messages = []
            if self.system_message:
                messages.append(self.system_message)
            if self.few_shot:
                messages.extend(self.few_shot)
            if self.prompt_template:
                content = self.prompt_template.format_prompt(content=content, question=question).to_string()

            messages.append(UserMessage(content=content))

        for message in messages:
            self._logger(f"{message.role}: [{message.content[:20]}]\n", color="blue")
        return messages

    def generate_each_page(
            self,
            query: str,
            pages_content: List[PageContent]
    ):
        """"""
        self._logger("Answer question for each page ...\n", color='red')
        answers = []
        for page in pages_content:
            self._logger(f"Matching content from: {page.title} - {page.url}\n", color="blue")
            page_chunks = self.split_page_content(page_content=page)
            matched_chunks = self.match_content_by_query(
                query=query, pages_content=page_chunks, n_content=self.n_chunks)
            matched_content = self.merge_content(matched_chunks)
            self._logger(f"Matched content: \n[{matched_content[:20]}\n", color="green")

            messages = self._make_message(content=matched_content, question=query)

            answer = self.llm.generate(messages=messages)
            answers.append(answer)
            self._logger(msg=f"Final answer for [{query}]: \n[{answer.choices[0].message.content}]\n", color="yellow")
        return answers

    def generate_pages(
            self,
            query: str,
            pages_content: List[PageContent]
    ):
        """"""
        self._logger("Answer question for all pages ...\n", color='red')
        page_chunks = self.split_pages_content(pages_content)
        matched_chunks = self.match_content_by_query(
            query=query, pages_content=page_chunks, n_content=self.n_chunks)
        matched_content = self.merge_content(matched_chunks)
        self._logger(f"Matched content: {matched_content}\n", color="green")

        messages = self._make_message(content=matched_content, question=query)
        answer = self.llm.generate(messages=messages)
        self._logger(msg=f"Final answer for [{query}]: \n[{answer.choices[0].message.content}]", color="yellow")
        return answer
