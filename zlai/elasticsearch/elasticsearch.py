from typing import *
from termcolor import colored
from tqdm import tqdm
from functools import reduce
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
from elasticsearch_dsl import (
    Q, Search, connections, Index, Document, tokenizer, analyzer)
from elasticsearch_dsl.field import Text
from elasticsearch_dsl.query import (
    Match, MatchPhrase, MatchAll, ScriptScore, Term, Terms)
from datetime import date

from ..schema.url import ESUrl
from ..utils import batches
from .config import elastic_search_index_settings


__all__ = [
    "tokenizer_ik",
    "analyzer_ik",
    "get_es_global_con",
    "get_es_con",
    "create_index",
    "doc2es",
    "ElasticSearchTools",
    "es_cosine_similarity",
]

tokenizer_ik = tokenizer('ik_smart')
analyzer_ik = analyzer('ik_smart', tokenizer=tokenizer_ik)
es_url = ESUrl


def get_es_global_con(
        hosts: str,
) -> None:
    """

    :param hosts:
    :return:

    >>> con = get_es_con(hosts=ESUrl.model)
    """
    connections.create_connection(hosts=hosts, timeout=20)
    print(colored(f'ES connected!', 'green', attrs=['bold']))
    return None


def get_es_con(
        hosts: str,
) -> Elasticsearch:
    """

    :param hosts:
    :return:

    >>> con = get_es_con(hosts=ESUrl.model)
    """
    return Elasticsearch(hosts=hosts)


def create_index(
        index_name: str,
        field_schema: Document,
        reset: bool = False,
        con: Elasticsearch = None,
        disp: bool = True,
):
    """
    desc: 创建ES索引
    :param index_name:
    :param field_schema:
    :param reset:
    :param con:
    :param disp:
    :return:

    >>> class ElasticSearchSchemaTest(Document):
    >>>     url = Text()
    >>>     title = Text(analyzer=analyzer_ik, search_analyzer=analyzer_ik)
    >>>     context = Text(analyzer=analyzer_ik, search_analyzer=analyzer_ik)
    >>>     vector = DenseVector(dims=1024)
    >>>     date = Text()

    >>> con = get_es_con(hosts=ESUrl.model)
    >>> create_index(
    >>>     index_name='test_index',
    >>>     field_schema=ElasticSearchSchemaTest,
    >>>     reset=True, con=con, disp=True)
    """
    index = Index(index_name, using=con)
    index = index.settings(**elastic_search_index_settings)

    class DocField(field_schema):
        class Index:
            name = index_name

    if reset and index.exists():
        index.delete()
    if not index.exists() or reset:
        index.create()
        index.close()
        DocField.init(index=index_name, using=con)
        if disp: print(colored(f'Index {index_name} created!', 'green', attrs=['bold']))
    else:
        if disp: print(colored(f'Index {index_name} existed!', 'red', attrs=['bold']))


def doc2es(
        data: List[Dict],
        index_name: str,
        batch_size: int = 10,
        con: Elasticsearch = None,
) -> None:
    """
    desc: 保存文件至ES数据库
    :param data:
    :param index_name:
    :param batch_size:
    :param con:
    :return:
    """
    if len(data) // batch_size == len(data) / batch_size:
        total = len(data) // batch_size
    else:
        total = (len(data) // batch_size) + 1
    con.indices.open(index=index_name)
    for batch_data in tqdm(batches(data, batch_size=batch_size), desc='保存进度', total=total):
        actions = []
        for source in batch_data:
            action = {
                '_index': index_name,
                '_source': source
            }
            actions.append(action)
        bulk(con, actions)
    con.close()
    print(colored(f'Docs in {index_name} saved!', 'green', attrs=['bold']))


def es_cosine_similarity(
        vector,
        index_name: str,
        size: int = 10,
        thresh: Union[None, float] = None,
        doc_vec_name='vector',
        con=None
):
    """
    desc: 计算中知识库中文本的相似度
    :param thresh:
    :param con:
    :param doc_vec_name:
    :param vector:
    :param index_name:
    :param size:
    :return:
    """
    index = Index(index_name, using=con)
    search = Search(index=index_name, using=con)

    script = {
        "source": f"cosineSimilarity(params.query_vector, doc['{doc_vec_name}']) + 1.0",
        "params": {"query_vector": vector}
    }
    query = MatchAll()
    script_score = ScriptScore(query=query, script=script)
    index.open()
    index.refresh()
    s = search.query(script_score).params(size=size)
    response = s.execute()
    index.close()

    hits = response.hits.hits
    if thresh:
        hits = [hit for hit in hits if hit._score > thresh]
    return hits


class ElasticSearchTools:
    """"""

    def __init__(self, index_name, con):
        self.con = con
        self.index_name = index_name
        self.index = Index(index_name, using=con)
        self.search = Search(index=self.index_name, using=con)
        self.search_exe = None
        self.search_query = []

    def match_query(
            self,
            query,
    ) -> List[Dict]:
        """弃用"""
        self.index.open()
        s = self.search.query(query)
        response = s.execute()
        data = [hit.to_dict() for hit in response.hits]
        self.index.close()
        return data

    def check_score_script(self) -> bool:
        """"""
        if len(self.search_query) > 0:
            for q in self.search_query:
                if isinstance(q, ScriptScore):
                    return True
            return False
        else:
            return False

    def execute(
            self,
            size=10,
            sort_by: Union[List[str], str, None] = None,
            ascending: bool = True,
    ) -> List[Dict]:
        """"""
        if self.search_exe is not None:
            self.index.open()
            self.index.refresh()
            if sort_by and not self.check_score_script():
                if isinstance(sort_by, str):
                    sort_by = [sort_by]
                if not ascending:
                    sort_by = [f"-{s}" for s in sort_by]
                self.search_exe = self.search_exe.sort(*sort_by)

            self.search_exe = self.search_exe.params(size=size)
            response = self.search_exe.execute()
            data = [hit.to_dict() for hit in response.hits.hits]
            self.index.close()
            self.search_exe = None
            self.search_query = []
            return data
        else:
            return []

    def add_search_execute(self, query=None, _filter=None):
        """"""
        if query:
            self.search_query.append(query)
        if _filter:
            self.search_query.append(_filter)

        combined_query = reduce(lambda q1, q2: q1 & q2, self.search_query)
        self.search_exe = self.search.query(combined_query)

    def match_context(
            self,
            key_word: Union[str, None] = None,
            fields: Union[List[str], str, None] = None,
            match_type='match',
            **kwargs
    ) -> None:
        """
        :param key_word:
        :param fields:
        :param match_type: ['match', 'match_phrase', 'match_all', 'multi_match']
        :param kwargs:
        :return:
        """
        if match_type in ['multi_match']:
            query = Q(match_type, query=key_word, fields=fields)
        elif match_type in ['match', 'match_phrase', ]:
            query = Q(match_type, **{fields: key_word})
        elif match_type == 'match_all':
            query = Q(match_type)
        else:
            raise ValueError(f"Argument 'match_type' must be either 'match' or 'match_phrase'.")
        self.add_search_execute(query)

    def count(self, clear_query=False) -> int:
        """"""
        self.index.open()
        self.index.refresh()

        if self.search_exe is not None:
            count = self.search_exe.count()
            if clear_query:
                self.search_exe = None
                self.search_query = []
        else:
            count = self.search.count()
        self.index.close()
        return count

    def date_between(
            self,
            start_date: Union[str, date],
            end_date: Union[str, date],
            date_name: str = "create_date",
            **kwargs,
    ) -> None:
        """

        :param date_name:
        :param start_date:
        :param end_date:
        :param kwargs:
        :return:
        """
        date_info = {f"{date_name}": {'gte': start_date, 'lte': end_date}}
        query = Q('range', **date_info)
        self.add_search_execute(query)

    def filter(self, field: str, values: Union[str, List[str]]):
        """"""
        if isinstance(values, str):
            query = Q("term", **{field: values})
        else:
            query = Q("terms", **{field: values})
        self.add_search_execute(query)

    def cos_smi(self, vector, doc_vec_name='vector') -> None:
        """"""
        script = {
            "source": f"cosineSimilarity(params.query_vector, '{doc_vec_name}') + 1.0",
            "params": {"query_vector": vector}
        }
        query = ScriptScore(query=MatchAll(), script=script)
        self.add_search_execute(query=query)

    def agg_metric(self, field: str, op: str):
        """"""
        self.index.open()
        self.search.aggs.metric(field, op, field=field)
        response = self.search.execute()
        self.index.close()
        return response.aggregations.to_dict()

    def max(self, field: str, ):
        """"""
        return self.agg_metric(field, 'max')

    def min(self, field: str, ):
        """"""
        return self.agg_metric(field, 'min')

    def agg_sum(self, field):
        """"""
        return self.agg_metric(field, 'sum')

    def agg_avg(self, field):
        """"""
        return self.agg_metric(field, 'avg')
