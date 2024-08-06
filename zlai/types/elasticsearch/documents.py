from elasticsearch_dsl import Document, tokenizer, analyzer
from elasticsearch_dsl.field import Text, Object, DenseVector


__all__ = [
    "tokenizer_ik",
    "analyzer_ik",
    "ESDocument",
    "VectoredESDocument",
]

tokenizer_ik = tokenizer('ik_smart')
analyzer_ik = analyzer('ik_smart', tokenizer=tokenizer_ik)


class ESDocument(Document):
    """知识文档的结构信息"""
    page_content = Text(analyzer=analyzer_ik, search_analyzer=analyzer_ik)
    metadata = Object(dynamic=True)


class VectoredESDocument(ESDocument):
    """知识文档的结构信息"""
    vector = DenseVector(dims=1024)
