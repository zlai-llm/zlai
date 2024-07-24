import unittest
import pandas as pd

from zlai.llms import *
from zlai.embedding import *
from zlai.agent import *
from zlai.schema import *


class TestSQLite(unittest.TestCase):
    """"""
    def setUp(self):
        """"""
        self.db_path = "./test_data/database.db"
        model_path = "/home/models/BAAI/bge-m3"
        self.llm = Zhipu(generate_config=GLM4AirGenerateConfig(temperature=0.01))
        self.embedding = Embedding(
            emb_url=EMBUrl.bge_m3,
            # model_path=model_path,
            max_len=5000,
            max_len_error='split',
            batch_size=128,
            verbose=True,
        )

    def test_catalog(self):
        """"""
        sqlite_qa = SQLiteAgent(llm=self.llm, embedding=self.embedding, db_path=self.db_path, verbose=True)
        print(sqlite_qa.catalog)

    def test_match_table(self):
        """"""
        sqlite_qa = SQLiteAgent(llm=self.llm, embedding=self.embedding, db_path=self.db_path, verbose=True)
        matched_tables = sqlite_qa.match_tables(question="工商基本信息")
        print(matched_tables)

    def test_table_info(self):
        """"""
        sqlite_qa = SQLiteAgent(llm=self.llm, embedding=self.embedding, db_path=self.db_path, verbose=True)
        table_info = sqlite_qa.get_table_info(question="工商基本信息")
        print(table_info)

    def test_sqlite_qa(self):
        """"""
        sqlite_qa = SQLiteQA(llm=self.llm, embedding=self.embedding, db_path=self.db_path, verbose=True)

        # query = "介绍工商基本信息表。"
        query = "简单介绍工商基本信息表"
        table_info = sqlite_qa(query=query)
        print(table_info)

    def test_sqlite_query(self):
        """"""
        sqlite_query = SQLiteScriptWithObservation(llm=self.llm, embedding=self.embedding, db_path=self.db_path, verbose=True)

        query = "工商基本信息表有多少数据？"
        # query = "数据库中有哪些数据信息？"
        table_info = sqlite_query(query=query)
        print(table_info)

    def test_sqlite_switch(self):
        """"""
        sqlite_query = SQLite(llm=self.llm, embedding=self.embedding, db_path=self.db_path, verbose=True)

        # query = "工商基本信息表有多少数据？"
        # query = "请介绍一下工商基本信息表？"
        # query = "请介绍一下这个数据库"
        query = "你好，你是谁？"
        table_info = sqlite_query(query=query)
        print(table_info.content)

    def test_sqlite_qa_stream(self):
        """"""
        llm = Zhipu(generate_config=GLM4AirGenerateConfig(stream=True))

        sqlite_qa = SQLiteQA(
            llm=llm, embedding=self.embedding, db_path=self.db_path, verbose=True, stream=True)

        # query = "介绍工商基本信息表。"
        query = "简单介绍工商基本信息表"
        query = "介绍绍工商基本信息表"
        answer = ""
        for table_info in sqlite_qa(query=query):
            answer += table_info.delta
        print(answer)

    def test_sqlite_script_stream(self):
        """"""
        llm = Zhipu(generate_config=GLM4AirGenerateConfig(stream=True))

        sqlite_script = SQLiteScript(
            llm=llm, embedding=self.embedding, db_path=self.db_path, verbose=True, stream=True)

        query = "工商基本信息表有多少数据？"
        for table_info in sqlite_script(query=query):
            print(table_info.content)

    def test_sqlite_script_with_observation(self):
        """"""
        llm = Zhipu(generate_config=GLM4AirGenerateConfig(stream=True))

        sqlite_script = SQLiteScriptWithObservation(
            llm=llm, embedding=self.embedding, db_path=self.db_path,
            verbose=True, stream=True)

        query = "工商基本信息表有多少数据？"
        for table_info in sqlite_script(query=query):
            print(table_info.content)

    def test_sqlite_stream(self):
        """"""
        # llm = Zhipu(generate_config=GLM4AirGenerateConfig())

        llm = LocalLLMAPI(
            verbose=False, generate_config=Qwen15Chat14BGenerateConfig(stream=True, incremental=True),
        )

        sqlite = SQLite(
            llm=llm, embedding=self.embedding, db_path=self.db_path,
            verbose=True, stream=True)

        # query = "你好"
        # query = "工商基本信息表有多少数据？"
        # query = "介绍绍工商基本信息表"
        # query = "查询工商数据"
        # query = "查询武器保养表的数据量"
        query = "查询工商基本信息中的企业数据"
        display_content = ""
        for table_info in sqlite(query=query):
            display_content += str(table_info.delta)

        print("==================")
        print(display_content)



