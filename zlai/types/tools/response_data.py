import pandas as pd
from pydantic import BaseModel, Field
from typing import List, Dict, Optional


__all__ = [
    "ResponseData",
]


class ResponseData(BaseModel):
    """"""
    metadata: Optional[Dict] = Field(default={})
    data: List[Dict] = Field(default=[])

    def __init__(
            self,
            data: List[Dict],
            metadata: Optional[Dict] = None,
            **kwargs
    ):
        """"""
        super().__init__(**kwargs)
        self.data = data
        self.metadata = metadata

    def to_dict(self) -> List[Dict]:
        """"""
        return self.reports

    def to_frame(self, columns: Optional[List[Dict]] = None) -> pd.DataFrame:
        """"""
        df = pd.DataFrame(data=self.data)
        if columns:
            df.rename(columns=columns, inplace=True)
        return df
