import unittest
from pandas import pd



class TestCSV(unittest.TestCase):
    """"""
    def setUp(self):
        self.path = "test_data/titanic.csv"
        self.df = pd.read_csv('test_data/titanic.csv')

    def test_csv_code(self):
        """"""
        embedding = Embedding(
            emb_url=EMBUrl.bge_m3,
            max_len=5000,
            max_len_error='split',
            batch_size=2,
        )
        llm = Zhipu(generate_config=GLM4AirGenerateConfig(temperature=0.01))
        csv = CSVAgent(csv_path=self.path, llm=llm, embedding=embedding, verbose=True)
        # query = "表中有多少数据？"
        # query = "请使用中文介绍这个表格"
        query = "生存率是多少？"
        csv.generate(query=query)

    def test_csv_qa(self):
        """"""
        embedding = Embedding(
            emb_url=EMBUrl.bge_m3,
            max_len=5000,
            max_len_error='split',
            batch_size=2,
        )
        llm = Zhipu(generate_config=GLM4AirGenerateConfig(temperature=0.01))
        csv = CSVQA(csv_path=self.path, llm=llm, embedding=embedding, verbose=True)
        query = "请使用中文介绍这个表格"
        csv.generate(query=query)

    def test_csv_script(self):
        """"""
        llm = Zhipu(generate_config=GLM4AirGenerateConfig(temperature=0.01))
        csv = CSVScript(csv_path=self.path, llm=llm, verbose=True)

        # query = "生存率是多少？"
        query = TaskCompletion(query="生存率是多少？", task_id=0, task_name='生存率',)
        completion = csv(query, task_id=0, task_name="生存率")
        print(completion)

    def test_csv_observation(self):
        """"""
        llm = Zhipu(generate_config=GLM4AirGenerateConfig(temperature=0.01))
        csv = CSVObservation(csv_path=self.path, llm=llm, verbose=True)

        query = TaskCompletion(
            query='生存率是多少？', task_id=0, task_name='生存率',
            content='```python\nsurvival_rate = df[\'Survived\'].mean()\nprint(f"生存率为: {survival_rate:.2f}")\n```',
            script='survival_rate = df[\'Survived\'].mean()\nprint(f"生存率为: {survival_rate:.2f}")\n',
            observation='生存率为: 0.39\n')
        completion = csv(query)
        print(completion)

    def test_csv_observation_with_script(self):
        """"""
        llm = Zhipu(generate_config=GLM4AirGenerateConfig(temperature=0.01))
        csv = SQLiteScriptWithObservation(csv_path=self.path, llm=llm, verbose=True)

        # query = '生存率是多少？'
        # query = "统计表格中船票的等级分布？"
        query = "统计表格中船票的不同船票等级的生存率？"
        # query = "计算出表格中的性别比例是多少？"
        answer = csv(query=query)
        print(answer)

        for i, completion in enumerate(csv.task_completions):
            print(f"{i} - {completion.content}")

    def test_csv_task_switch(self):
        """"""
        llm = Zhipu(generate_config=GLM4AirGenerateConfig(temperature=0.01))
        csv = CSV(llm=llm, verbose=True)
        query = "请使用中文介绍这个表格"
        # query = "生存率是多少？"
        # query = "计算出表格中的性别比例是多少？"
        # query = "统计表格中人员的年龄分布情况？"
        # query = "统计表格中船票的等级分布？"
        # query = "统计表格中船票的不同船票等级的生存率？"
        csv.generate(query=query, csv_path=self.path)

