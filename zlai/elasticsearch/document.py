import os
from typing import List, Dict, Optional, Callable
from tqdm import tqdm
from elasticsearch.helpers import bulk
from langchain_community.document_loaders import *
from langchain_text_splitters import CharacterTextSplitter
from pydantic import BaseModel, Field

from ..embedding import Embedding
from ..utils import LoggerMixin, batches, call_batches
from ..schema import ESUrl
from .elasticsearch import *


__all__ = [
    "DocumentData",
    "LoadingDocuments",
    "DocumentSaveToElasticsearch",
]


loader_cls_mapping = {
    "pdf": UnstructuredPDFLoader,
    "md": UnstructuredMarkdownLoader,
    "txt": UnstructuredMarkdownLoader,
    "url": UnstructuredURLLoader,
    "csv": UnstructuredCSVLoader,
    "excel": UnstructuredExcelLoader,
}


class DocumentData(BaseModel):
    title: Optional[str] = Field(default=None, description="文档名称")
    content: Optional[str] = Field(default=None, description="文档内容")
    vector: Optional[List[float]] = Field(default=None, description="文档向量")


class DocumentSaveToElasticsearch(LoggerMixin):
    """"""
    index_name: Optional[str]
    tools: Optional[ElasticSearchTools]
    embedding: Optional[Embedding]
    batch_size: Optional[int]
    thresh: Optional[float]
    logger: Optional[Callable]
    verbose: Optional[bool]

    def __init__(
            self,
            host: Optional[str],
            index_name: Optional[str],
            tools: Optional[ElasticSearchTools] = None,
            embedding: Optional[Embedding] = None,
            batch_size: Optional[int] = 32,
            thresh: Optional[float] = 1.95,
            logger: Optional[Callable] = None,
            verbose: Optional[bool] = False,
    ):
        self.index_name = index_name
        self.tools = tools
        self.embedding = embedding
        self.batch_size = batch_size
        self.thresh = thresh
        self.logger = logger
        self.verbose = verbose
        self.con = get_es_con(hosts=host)
        self.tools = ElasticSearchTools(index_name=self.index_name, con=self.con)

    def __call__(self, data: List[Dict], *args, **kwargs):
        """"""
        documents_count = self.tools.count()
        self._logger(color="blue", msg=f"Start saving data to ElasticSearch, current document: {documents_count} ...")
        if documents_count > 0:
            data = self.prepare_data(data)
        self.save(data=data)

    def create_index(self, field_schema):
        """ ElasticSearch schema """
        create_index(
            index_name=self.index_name, field_schema=field_schema,
            reset=False, con=self.con, disp=False, )
        self._logger(msg=f"Index: {self.index_name} create successfully!", color="green")

    def reset_index(self, field_schema):
        """ ElasticSearch schema """
        create_index(
            index_name=self.index_name,field_schema=field_schema,
            reset=True, con=self.con, disp=False,)
        self._logger(msg=f"Index: {self.index_name} reset successfully!", color="green")

    def save(self, data: List[Dict]):
        """"""
        total = call_batches(data=data, batch_size=self.batch_size)
        if self.verbose:
            _iters = tqdm(batches(data, batch_size=self.batch_size), desc='Progress', total=total)
        else:
            _iters = batches(data, batch_size=self.batch_size)

        self.con.indices.open(index=self.index_name)
        for batch_data in _iters:
            actions = [{'_index': self.index_name, '_source': source} for source in batch_data]
            bulk(self.con, actions)
        self.con.close()

    def prepare_data(self, data: List[Dict]) -> List[Dict]:
        """"""
        filtered_data = []
        if self.verbose:
            data = tqdm(data, desc='Preparing data')

        for _item in data:
            vector = _item.get("vector")
            current_content = _item.get("content")
            self.tools.cos_smi(vector=vector)
            exist_data = self.tools.execute(1)[0]
            score = exist_data.get("_score")
            title = exist_data.get("_source").get("title")
            exist_content = exist_data.get("_source").get("content")
            if score < self.thresh:
                filtered_data.append(_item)
            else:
                self._logger(msg=f"Find similar content score: {score:.3f}.\nTitle: {title}\nExist Content: {exist_content}\nCurrent Content: {current_content}", color='red')
        return filtered_data


class LoadingDocuments(LoggerMixin):
    """"""
    embedding: Optional[Embedding]
    chunk_size: Optional[int]
    chunk_overlap: Optional[int]
    separator: Optional[str]
    keep_separator: Optional[str]
    glob: Optional[str]

    documents: List[DocumentData]
    chunks: List[DocumentData]

    logger: Optional[Callable]
    verbose: Optional[bool]

    def __init__(
            self,
            embedding: Embedding,
            chunk_size: int = 500,
            chunk_overlap: int = 100,
            separator: str = "\n\n",
            keep_separator: Optional[str] = " ",
            glob: Optional[str] = "md",
            logger: Optional[Callable] = None,
            verbose: Optional[bool] = False,
    ):
        """"""
        self.glob = glob
        self.embedding = embedding
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.separator = separator
        self.keep_separator = keep_separator

        self.logger = logger
        self.verbose = verbose

    def __call__(self, path: str, *args, **kwargs):
        self.documents = self.load_documents(path=path)
        self.chunks = sum(list(map(self.split_document, self.documents)), [])
        self.chunks = self.embedding_chunks(docs=self.chunks)
        return self.chunks

    def _load_file(self, file_path):
        """"""
        loader_cls = loader_cls_mapping.get(self.glob)
        if loader_cls:
            self.loader = loader_cls(file_path)
        else:
            raise ValueError(f"{self.glob} is not a valid glob")

    def _load_dir(self, dir_path):
        """"""
        loader_cls = loader_cls_mapping.get(self.glob)
        if loader_cls:
            self.loader = DirectoryLoader(path=dir_path, glob=f"**/*.{self.glob}", loader_cls=loader_cls,
                                          show_progress=self.verbose)
        else:
            raise ValueError(f"{self.glob} is not a valid glob")

    def load_documents(self, path: str) -> List[DocumentData]:
        """"""
        if os.path.isfile(path):
            self._load_file(file_path=path)
        elif os.path.isdir(path):
            self._load_dir(dir_path=path)
        else:
            raise ValueError(f"{path} is not a valid path")

        data = self.loader.load()
        docs = [DocumentData(content=item.page_content, title=os.path.basename(item.metadata['source'])) for item in data]
        return docs

    def split_document(self, doc: DocumentData) -> List[DocumentData]:
        """"""
        text_splitter = CharacterTextSplitter(
            separator=self.separator,
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
            length_function=len,
            is_separator_regex=True,
            keep_separator=self.keep_separator,
        )
        split_chunk_lst = text_splitter.split_text(text=doc.content)
        split_chunks = [DocumentData(title=doc.title, content=chunk) for chunk in split_chunk_lst]
        return split_chunks

    def embedding_chunks(self, docs: List[DocumentData]) -> List[DocumentData]:
        """"""
        def update_vector(doc: DocumentData, vector: List[float]) -> None:
            """"""
            doc.vector = vector

        data = [doc.content for doc in docs]
        vectors = self.embedding.embedding(text=tuple(data)).to_list()
        _ = [update_vector(doc, vec) for doc, vec in zip(docs, vectors)]
        return docs
