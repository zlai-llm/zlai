import os
import numpy as np
from typing import *
from langchain_community.document_loaders import (
    DirectoryLoader, UnstructuredPDFLoader, UnstructuredMarkdownLoader,
    UnstructuredURLLoader, UnstructuredCSVLoader, UnstructuredExcelLoader)
from ..elasticsearch import *
from ..schema import *
from ..embedding import *
from ..schema.url import *
from langchain_text_splitters import CharacterTextSplitter


# todo: 增加长文本切片排序后再进行询问
__all__ = [
    "RAGFile",
    "RAGVectorDatabase",
]

loader_cls = {
    "pdf": UnstructuredPDFLoader,
    "md": UnstructuredMarkdownLoader,
    "txt": UnstructuredMarkdownLoader,
    "url": UnstructuredURLLoader,
    "csv": UnstructuredCSVLoader,
    "excel": UnstructuredExcelLoader,
}


class RAGVectorDatabase:
    """"""
    invoke: Callable
    index_name: str
    database_tools: ElasticSearchTools


class RAGFile:
    """"""
    loader: Any = None
    show_progress: bool = True
    separator: str = "。"
    chunk_size: int = 500
    chunk_overlap: int = 100
    documents: Union[List[Document], None]
    chunk_of_documents = None
    rag_documents = List[RAGDocuments]
    vectors: np.array = None
    max_retriever_content: Union[str, int]
    embedding: Embedding

    def __init__(
            self,
            path: Optional[str],
            embedding: Embedding,
            chunk_size: int = 500,
            chunk_overlap: int = 100,
            separator: str = "\n\n",
            glob: Optional[str] = "md",
            max_retriever_content: int = 10,
    ):
        """

        :param path:
        :param glob:
        :param max_retriever_content: "auto"
        """
        self.path = path
        self.glob = glob
        self.embedding = embedding
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.separator = separator
        self.max_retriever_content = max_retriever_content
        self.load_doc()

    def embedding_documents(self) -> List[List[float]]:
        """"""
        data = [chunk.page_content for chunk in self.chunk_of_documents]
        content_vectors = self.embedding.embedding(text=tuple(data)).to_list()
        return content_vectors

    def split_document(self):
        """"""
        text_splitter = CharacterTextSplitter(
            separator=self.separator,
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
            length_function=len,
            is_separator_regex=False,
        )
        self.chunk_of_documents = text_splitter.split_documents(self.documents)
        return self.chunk_of_documents

    def load_documents(self):
        """"""
        if os.path.isfile(self.path):
            self.load_doc()
        elif os.path.isdir(self.path):
            self.load_docs()
        else:
            raise ValueError(f"{self.path} is not a valid path")
        self.documents = self.loader.load()

    def load_doc(self):
        """"""
        Loader = loader_cls.get(self.glob)
        if Loader:
            self.loader = Loader(self.path)
        else:
            raise ValueError(f"{self.glob} is not a valid glob")

    def load_docs(self):
        """"""
        Loader = loader_cls.get(self.glob)
        if Loader:
            self.loader = DirectoryLoader(
                path=self.path, glob=f"**/*.{self.glob}",
                loader_cls=Loader,
                show_progress=True,
            )
        else:
            raise ValueError(f"{self.glob} is not a valid glob")

    def similar_chunk(self, query, thresh=0.3,) -> List[RetrieverDocuments]:
        """"""
        query_vectors = embedding(url=EMBUrl.m3e_large, text=[query])
        query_vectors = np.array(query_vectors)

        cosine_metrix = cosine_similarity(query_vectors, self.vectors.T)
        top_n_cosine, top_n_info = top_n_indices(
            cosine_metrix=cosine_metrix, axis=1, top_n=self.max_retriever_content,
            **{"retriever_document": self.rag_documents})
        retriever_documents = []
        for score, doc in zip(top_n_cosine[0], top_n_info.get("retriever_document")[0]):
            retriever_document = RetrieverDocuments(
                document=doc.document, metadata=doc.metadata, score=score,)
            retriever_documents.append(retriever_document)
        return retriever_documents

