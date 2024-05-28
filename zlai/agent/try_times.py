from typing import *
from ..parse import sparse_dict
from pydantic import BaseModel, Field

__all__ = [
    "TryTimes",
]


class TryTimes(BaseModel):
    """"""
    try_times: int = Field(3, description="尝试次数")
    generate_fun: Callable = Field(..., description="生成模型")
    generate_config: Dict[str, Any] = Field(..., description="生成模型配置")
    generate_data: List[Dict] = Field([], description="生成的数据")
    parsed_data: Union[List, Dict, bool, None] = Field(None, description="解析后的数据")

    def parse(
            self,
            result,
            sparse_fun: Optional[Callable] = None,
            _type: Type[Union[Dict, List, Any]] = dict) -> Union[dict, list, bool, None]:
        if sparse_fun is None:
            sparse_fun = sparse_dict
        try:
            parsed_dict = sparse_fun(result)
            if isinstance(parsed_dict, _type):
                self.parsed_data = parsed_dict
                return parsed_dict
        except Exception as e:
            return None

    def run(self):
        """"""
        try_no = 0
        result = self.generate_fun(**self.generate_config)
        _ = self.parse(result)
        self.generate_data.append({"no": try_no, "result": result})

        while self.parsed_data is None and self.try_times > try_no:
            """"""
            result = self.generate_fun(**self.generate_config)
            _ = self.parse(result)
            try_no += 1
            self.generate_data.append({"no": try_no, "result": result})

