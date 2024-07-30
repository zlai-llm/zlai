import yaml
import unittest
from typing import List, Dict, Union, Optional
from pydantic import BaseModel, Field, ConfigDict


class TestYml(unittest.TestCase):
    def test_load_yaml(self):
        with open('../../../models_config.yml', 'r') as f:
            data = yaml.load(f, Loader=yaml.FullLoader)
        print(data)

    def test_schema(self):
        """"""

        class ModelConfig(BaseModel):
            """"""
            model_config = ConfigDict(protected_namespaces=())
            model_name: Optional[str] = Field(default=None, description="")
            model_path: Optional[str] = Field(default=None, description="")
            model_type: Optional[str] = Field(default=None, description="")
            load_method: Optional[str] = Field(default=None, description="")
            max_memory: Optional[Dict[Union[str, int], str]] = Field(default={0: "20GB"}, description="")

        model_config = ModelConfig()

