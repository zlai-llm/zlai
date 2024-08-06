from typing import List, Dict, Union, Optional, Callable
from tqdm import tqdm
from elasticsearch.helpers import bulk
from ..embedding import TypeEmbedding
from ..utils import LoggerMixin, batches, call_batches
from ..elasticsearch import ElasticSearchTools, create_index, get_es_con
from zlai.types.documents.documents import Document, VectoredDocument


__all__ = [
    "DocumentsToVectorDB",
]


class DocumentsToVectorDB(LoggerMixin):
    """"""
    index_name: Optional[str]
    tools: Optional[ElasticSearchTools]
    embedding: Optional[TypeEmbedding]
    batch_size: Optional[int]
    thresh: Optional[float]
    logger: Optional[Callable]
    verbose: Optional[bool]

    def __init__(
            self,
            host: Optional[str],
            index_name: Optional[str],
            tools: Optional[ElasticSearchTools] = None,
            embedding: Optional[TypeEmbedding] = None,
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
        self._logger(msg=f"[{__class__.__name__}] Index: {self.index_name} create successfully!", color="green")

    def reset_index(self, field_schema):
        """ ElasticSearch schema """
        create_index(index_name=self.index_name, field_schema=field_schema, reset=True, con=self.con, disp=False,)
        self._logger(msg=f"[{__class__.__name__}] Index: {self.index_name} reset successfully!", color="green")

    def save(self, data: Union[List[Document], List[VectoredDocument], List[Dict]]) -> None:
        """"""
        if not isinstance(data[0], dict):
            data = [d.model_dump() for d in data]

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