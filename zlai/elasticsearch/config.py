import os
from elasticsearch_dsl.analysis import tokenizer, analyzer

__all__ = [
    "env",
    "tokenizer_ik",
    "analyzer_ik",
    "elastic_search_index_settings",
]

env = os.environ

tokenizer_ik = tokenizer('ik_smart')
analyzer_ik = analyzer('ik_smart', tokenizer=tokenizer_ik)

elastic_search_index_settings = {
    "analysis": {
        "analyzer": {
            "ik_smart": {
                "tokenizer": "ik_smart"
            }
        },
        "search_analyzer": {
            "ik_smart": {
                "tokenizer": "ik_smart"
            }
        },
    }
}
