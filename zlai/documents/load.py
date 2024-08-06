import os
from typing import Any, Dict, List, Callable, Optional
from zlai.utils.mixin import LoggerMixin
from zlai.embedding import TypeEmbedding
from zlai.types.documents import Document, VectoredDocument
from langchain_community.document_loaders import *
from langchain_text_splitters import CharacterTextSplitter


__all__ = [
    "LoadDocuments"
]


loader_cls_mapping = {
    "pdf": UnstructuredPDFLoader,
    "md": UnstructuredMarkdownLoader,
    "txt": UnstructuredMarkdownLoader,
    "url": UnstructuredURLLoader,
    "csv": UnstructuredCSVLoader,
    "excel": UnstructuredExcelLoader,
}


class LoadDocuments(LoggerMixin):
    """"""
    embedding: Optional[TypeEmbedding]
    chunk_size: Optional[int]
    chunk_overlap: Optional[int]
    separator: Optional[str]
    keep_separator: Optional[str]
    glob: Optional[str]
    documents: List[Document]

    def __init__(
            self,
            embedding: TypeEmbedding,
            chunk_size: int = 500,
            chunk_overlap: int = 100,
            separator: str = "\n\n",
            keep_separator: Optional[str] = " ",
            glob: Optional[str] = "md",
            logger: Optional[Callable] = None,
            verbose: Optional[bool] = False,
            **kwargs: Any,
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

    def __call__(
            self,
            path: Optional[str] = None,
            contents: Optional[List[str]] = None,
            *args: Any,
            **kwargs: Any,
    ) -> List[VectoredDocument]:
        """"""
        if path:
            self.documents = self.load_documents(path=path)
        elif contents:
            self.documents = self.content_to_documents(contents=contents, **kwargs)
        else:
            raise ValueError("Either path or contents must be provided.")
        self._logger(msg=f"[{__class__.__name__}] Loaded {len(self.documents)} documents.", color="green")
        self.chunks = sum(list(map(self.split_document, self.documents)), [])
        self._logger(msg=f"[{__class__.__name__}] Split {len(self.chunks)} chunks.", color="green")
        self.chunks = self.embedding_chunks(docs=self.chunks)
        self._logger(msg=f"[{__class__.__name__}] Embedded {len(self.chunks)} chunks.", color="green")
        return self.chunks

    def content_to_documents(self, contents: List[str], **kwargs) -> List[Document]:
        """"""
        return [Document(page_content=content, metadata=kwargs) for content in contents]

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

    def load_documents(self, path: str) -> List[Document]:
        """"""
        if os.path.isfile(path):
            self._load_file(file_path=path)
        elif os.path.isdir(path):
            self._load_dir(dir_path=path)
        else:
            raise ValueError(f"{path} is not a valid path")

        data = self.loader.load()
        docs = [Document.model_validate(item.dict()) for item in data]
        return docs

    def split_document(self, doc: Document) -> List[Document]:
        """"""
        text_splitter = CharacterTextSplitter(
            separator=self.separator,
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
            length_function=len,
            is_separator_regex=True,
            keep_separator=self.keep_separator,
        )
        split_chunk_lst = text_splitter.split_text(text=doc.page_content)
        split_chunks = [Document(page_content=chunk, metadata=doc.metadata) for chunk in split_chunk_lst]
        return split_chunks

    def embedding_chunks(self, docs: List[Document]) -> List[VectoredDocument]:
        """"""
        data = [doc.page_content for doc in docs]
        vectors = self.embedding.embedding(text=tuple(data)).to_list()
        vectored_documents = []
        for doc, vec in zip(docs, vectors):
            vectored_document = VectoredDocument.model_validate(doc.model_dump())
            vectored_document.vector = vec
            vectored_documents.append(vectored_document)
        return vectored_documents
