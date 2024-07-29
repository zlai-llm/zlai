import yaml
import unittest


class TestYml(unittest.TestCase):
    def test_load_yaml(self):
        with open('../../../models_config.yml', 'r') as f:
            data = yaml.load(f, Loader=yaml.FullLoader)
        print(data)
