from pydantic import BaseModel, Field
from typing import Any, List, Dict, Union, Optional
from pymilvus import MilvusClient, DataType
from pymilvus.orm.schema import CollectionSchema
from ...utils import LoggerMixin


__all__ = [
    "MilvusClient",
    "MilvusTools",
    "MilvusFilter",
]


class MilvusFilter(BaseModel):
    """"""
    def compare(self, field: str, operate: str, value: Any) -> str:
        """

        :param field:
        :param operate: > < >= <=
        :param value:
        :return:
        """
        return f"{field} {operate} {value}"

    def between(self, field: str, start: Any, end: Any, operate: str = "<=") -> str:
        """

        :param field:
        :param start:
        :param end:
        :param operate:
        :return:
        """
        return f"{field} {operate} {start} {operate} {end}"

    def like(self, field: str, pattern: str) -> str:
        return f"{field} like %{pattern}%"

    def startwith(self, field: str, pattern: str) -> str:
        return f"{field} like {pattern}%"

    def endwith(self, field: str, pattern: str) -> str:
        return f"{field} like %{pattern}"

    def not_in(self, field: str, values: List[Any]) -> str:
        """"""
        return f'{field} not in {values}'

    def is_in(self, field: str, values: List[Any]) -> str:
        """"""
        return f'{field} in {values}'

    def count(self, ) -> str:
        """"""
        return "count(*)"

    def merge_conditions(self, conditions: List[str]) -> str:
        """"""
        return " and ".join(conditions)


class MilvusManager(LoggerMixin):
    """"""
    schema: CollectionSchema

    def __init__(
            self,
            host: str = "http://localhost",
            port: int = 19530,
    ):
        """"""
        self.uri = f"{host}:{port}"
        self.client = self.set_client()

    def set_client(self) -> MilvusClient:
        """"""
        return MilvusClient(uri=self.uri)

    def create_schema(
            self,
    ):
        """"""
        self.schema = self.client.create_schema(
            auto_id=False,
            enable_dynamic_field=True,
        )

    def create_index(
            self,

    ):
        """"""
        self.client.prepare_index_params()

    def create_collection(
            self,
            collection_name: str,
    ):
        """"""
        self.client.create_collection(
            collection_name=collection_name,
            schema=self.schema,
            index_params=self.index_params,
        )


class MilvusTools(LoggerMixin):
    """"""
    def __init__(
            self,
            host: str = "http://localhost",
            port: int = 19530,
    ):
        """"""
        self.uri = f"{host}:{port}"
        self.client = self.set_client()

    def set_client(self) -> MilvusClient:
        """"""
        return MilvusClient(uri=self.uri)

    def insert(
            self,
            collection_name: str,
            data: List[Any],
            partition_name: Optional[str] = None,
    ):
        msg = self.client.insert(
            collection_name=collection_name, data=data, partition_name=partition_name)
        self._logger(msg=f"Insert {msg.get('insert_count')} data.", color="green")

    def search(
            self,
            collection_name: str,
            data: Union[List, List[List]],
            filter: str = "",
            limit: int = 10,
            output_fields: Optional[List[str]] = None,
            search_params: Optional[Dict] = None,
            partition_names: Optional[List[str]] = None,
            anns_field: Optional[str] = None,
    ) -> List[List[Dict]]:
        """"""
        data = self.client.search(
            collection_name=collection_name,
            data=data, filter=filter, limit=limit,
            output_fields=output_fields,
            search_params=search_params,
            partition_names=partition_names,
            anns_field=anns_field,
        )
        return data

    def get(
            self,
            collection_name: str,
            ids: Union[List, str, int],
            output_fields: Optional[List[str]] = None,
            partition_names: Optional[List[str]] = None
    ):
        """"""
        data = self.client.get(
            collection_name=collection_name, ids=ids,
            output_fields=output_fields, partition_names=partition_names,
        )
        return data

