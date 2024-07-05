import json
import unittest
from zlai.parse import *
from zlai.schema import *
from zlai.warpper import *


class TestSparse(unittest.TestCase):
    """"""
    def setUp(self):
        """"""
        with open("../test_data/sparse.json") as f:
            self.data = json.loads(f.read())

    def test_load_data(self):
        """"""
        print(len(self.data))

    def test_sparse_dict(self):
        string = "{'name': 'John', 'age': 30} Some text {'color': 'blue'}"
        dicts = sparse_dict(string)
        print(dicts)

    def test_sparse_list(self):
        """"""
        data = [
            "[1, 2]",
            "[1, 2], da [2, 3]",
            "[1, 2], da [2, 3], [3, 4]",
        ]
        for item in data:
            out = sparse_list(string=item, first=False)
            print(out, type(out))

    def test_sparse_markdown_table(self):
        text = """
        | Column 1 | Column 2 | Column 3 |
        |----------|----------|----------|
        | Value 1  | Value 2  | Value 3  |
        | Value 4  | Value 5  | Value 6  |
        """
        result_df = sparse_markdown_table(text)
        print(result_df)

    def test_parse_code(self):
        """"""
        data = """```sql\nSELECT COUNT(*) FROM "company_base";\n```"""
        data = """```sql\nSELECT COUNT(*) FROM "company_base";```"""
        data = """```sql\nSELECT COUNT(*) FROM company_base;\n```"""
        script = ParseCode.sparse_script(string=data, script="sql")
        print(data)
        print(script, '-------------')


class TestSparseDict(unittest.TestCase):
    """"""

    def setUp(self):
        """"""
        self.sparse = ParseString()
        with open("../test_data/sparse.json") as f:
            self.data = json.loads(f.read())

        self.eval_cases = []
        self.nested_cases = []
        self.greedy_cases = []
        self.key_val_cases = []

        for item in self.data:
            if "eval" in item.get("type"):
                self.eval_cases.append((item.get("content"), item.get("except")))
            if "nested" in item.get("type"):
                self.nested_cases.append((item.get("content"), item.get("except")))
            if "greedy" in item.get("type"):
                self.greedy_cases.append((item.get("content"), item.get("except")))
            if "key_val" in item.get("type"):
                self.key_val_cases.append((item.get("content"), item.get("except")))

    def test_eval_dict(self):
        """"""
        for case, expect in self.eval_cases:
            sparse_out = self.sparse.eval_dict(string=case)
            print(sparse_out, expect)
            self.assertListEqual(sparse_out, expect)

    def test_greedy_dict(self):
        """"""
        for case, expect in self.greedy_cases:
            sparse_out = self.sparse.greedy_dict(string=case)
            print(sparse_out, expect)
            self.assertListEqual(sparse_out, expect)

    def test_nested_dict(self):
        """"""
        for case, expect in self.nested_cases:
            sparse_out = self.sparse.nested_data(string=case)
            print(sparse_out, expect)
            self.assertListEqual(sparse_out, expect)

    def test_key_value_dict(self):
        """"""
        for case, expect in self.key_val_cases:
            sparse_out = self.sparse.key_value_dict(string=case)
            print(sparse_out, expect)
            self.assertListEqual(sparse_out, expect)

    def test_warp_eval_dict(self):
        """"""
        @warp_sparse_eval_dict
        def generate():
            return CompletionMessage(role='assistant', content=self.eval_cases[0][0])

        data = generate()
        print(type(data), type(data.content))


class TestSparseAmount(unittest.TestCase):
    """"""
    def test_sparse_amount(self):
        from zlai.parse.amount import sparse_amount

        # 测试输入列表中包含元、万元和亿元的情况
        input_list = ['100元', '10.5万元', '0.8亿元', 'abc']
        expected_output = [100.0, 10.5*1e4, 0.8*1e8, None]
        sparse_output = sparse_amount(input_list)
        print(f"parse output: {sparse_output}")
        self.assertEqual(sparse_output, expected_output)

        # 测试输入列表中只包含元的情况
        input_list = ['50元', '0.5元', 'abc']
        expected_output = [50.0, 0.5, None]
        sparse_output = sparse_amount(input_list)
        print(f"parse output: {sparse_output}")
        self.assertEqual(sparse_output, expected_output)

        # 测试输入列表为空的情况
        input_list = []
        expected_output = []
        sparse_output = sparse_amount(input_list)
        print(f"parse output: {sparse_output}")
        self.assertEqual(sparse_output, expected_output)

        # 测试输入列表中包含其他单位的情况
        input_list = ['100美元', '10万日元', '1千英镑']
        expected_output = [None, None, None]
        sparse_output = sparse_amount(input_list)
        print(f"parse output: {sparse_output}")
        self.assertEqual(sparse_output, expected_output)


class TestParseValues(unittest.TestCase):
    def test_parse_values(self):
        from zlai.parse.amount import sparse_values

        # 测试包含有效数值和无效数值的情况
        input_list = ['1.5', '2', '3.7', 'abc', '10.2']
        expected_output = [1.5, 2.0, 3.7, None, 10.2]
        self.assertEqual(sparse_values(input_list), expected_output)

        # 测试空列表的情况
        input_list = []
        expected_output = []
        self.assertEqual(sparse_values(input_list), expected_output)

        # 测试所有元素都包含有效数值的情况
        input_list = ['0.1', '2.5', '3.14', '100']
        expected_output = [0.1, 2.5, 3.14, 100.0]
        self.assertEqual(sparse_values(input_list), expected_output)

        # 测试所有元素都不包含数值的情况
        input_list = ['abc', 'def', 'xyz']
        expected_output = [None, None, None]
        self.assertEqual(sparse_values(input_list), expected_output)

        # 测试BP
        input_list = ['50BP', '100BP', 'LPR-150BP以下部分']
        expected_output = [50., 100., -150.,]
        spase_out = sparse_values(input_list)
        self.assertEqual(spase_out, expected_output)


if __name__ == '__main__':
    unittest.main()
