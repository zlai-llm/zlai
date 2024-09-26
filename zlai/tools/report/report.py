import os
import time
import random
import requests
import pandas as pd
from pydantic import BaseModel, Field
from typing import Any, List, Dict, Tuple, Union, Literal, Callable, Optional
from zlai.tools.utils import headers
from zlai.utils.mixin import LoggerMixin


__all__ = [
    "ReportQueryConfig",
    "ReportList",
    "ReportTools",
]


TypeReport = Literal[0, 1, 2, 3, 4, "个股研报", "行业研报", "策略报告", "宏观研究", "券商晨报"]


class ReportQueryConfig(BaseModel):
    """"""
    code: Optional[str] = Field(default=None)
    industry: Optional[str] = Field(default="*")
    industry_code: Optional[str] = Field(default="*")
    size: Optional[int] = Field(default=5)
    rating: Optional[str] = Field(default="*")
    rating_change: Optional[str] = Field(default="*")
    begin_time: Optional[str] = Field(default="*")
    end_time: Optional[str] = Field(default="*")
    page_no: Optional[int] = Field(default=1)
    q_type: Optional[TypeReport] = Field(default=1)

    def __init__(self, **kwargs):
        """
        :param code:
        :param industry:
        :param industry_code:
        :param size:
        :param rating:
        :param rating_change:
        :param begin_time:
        :param end_time:
        :param page_no:
        :param q_type: 0 个股研报 1 行业研报 2 策略报告 3 宏观研究 4 券商晨报
        """
        super().__init__(**kwargs)
        self.q_type = self._reports_type(q_type=self.q_type)

    def _reports_type(
            self,
            q_type: Optional[TypeReport] = 1,
    ) -> Union[int, str]:
        """"""
        if q_type is None:
            return "*"
        elif isinstance(q_type, int):
            return q_type
        elif isinstance(q_type, str):
            _type_ids = ["个股研报", "行业研报", "策略报告", "宏观研究", "券商晨报"]
            return _type_ids.index(q_type)

    def _random_cb(self) -> str:
        """"""
        return str(int(random.random() * 1E7 + 1))

    def _current_time(self) -> str:
        """"""
        return str(int(time.time() * 1E3))

    def to_params(self) -> Dict:
        """"""
        params = {
            "industry": self.industry,
            "industryCode": self.industry_code,
            "pageSize": self.page_size,
            "rating": self.rating,
            "ratingChange": self.rating_change,
            "beginTime": self.begin_time,
            "endTime": self.end_time,
            "pageNo": self.page_no,
            "qType": self.q_type,
            "_": self._current_time()
        }
        if self.code:
            params.update({"code": self.code})
        return params


class ReportList(BaseModel):
    """"""
    url: Optional[str] = Field(default=None)
    metadata: Optional[Dict] = Field(default=None)
    reports: List[Dict] = Field(default=[])

    def __init__(
            self,
            url: Optional[str] = None,
            metadata: Optional[Dict] = None,
            reports: Optional[List[Dict]] = None,
            **kwargs
    ):
        """"""
        super().__init__(**kwargs)
        self.url = url
        self.metadata = metadata
        self.reports = reports

    def to_dict(self) -> List[Dict]:
        """"""
        return self.reports

    def to_frame(self) -> pd.DataFrame:
        """"""
        return pd.DataFrame(data=self.reports)


class ReportTools(LoggerMixin):
    """"""
    report_info: Optional[Dict]
    report_list: Optional[List[Dict]]

    def __init__(
            self,
            query_config: Optional[ReportQueryConfig] = ReportQueryConfig(),
            verbose: Optional[bool] = False,
            logger: Optional[Callable] = None,
            **kwargs: Any
    ):
        self.query_config = query_config
        self.verbose = verbose
        self.logger = logger
        self.kwargs = kwargs

    def list_industry(self) -> Dict:
        """"""
        base_url = "https://reportapi.eastmoney.com/report/bk"
        params = {
            "bkCode": "016",
            "_": str(int(time.time() * 1E3))
        }
        response = requests.get(base_url, params=params, headers=headers)
        data = response.json()
        return data.get("data", {})

    def _base_url(self) -> str:
        """jg/dg/list"""
        base_url = "https://reportapi.eastmoney.com/report/"
        if self.query_config.q_type in [0, 1, 2, 3]:
            base_url += "list"
        else:
            base_url += "dg"
        return base_url

    def list_reports(
            self,
    ) -> ReportList:
        """"""
        base_url = self._base_url()
        params = self.query_config.to_params()
        response = requests.get(base_url, params=params, headers=headers)
        data = response.json()
        reports = data.pop("data")
        metadata = data
        self._logger(msg=f"[{__class__.__name__}] Find {len(reports)} reports.", color="green")
        return ReportList(url=base_url, metadata=metadata, reports=reports)

    def save(
            self,
            report_code: Union[str, List[str]],
            path: str = "./"
    ) -> None:
        """"""
        pdf_bytes = self.load_bytes(report_code=report_code)
        for code, bytes_content in pdf_bytes:
            if isinstance(bytes_content, bytes):
                file_name = f"{code}.pdf"
                file_path = os.path.join(path, file_name)
                with open(file_path, "wb") as f:
                    f.write(bytes_content)

    def load_bytes(self, report_code: Union[str, List[str]], ) -> List[Tuple[str, Union[str, bytes]]]:
        """"""
        base_url = """https://pdf.dfcfw.com/pdf/H3_{}_1.pdf""".format
        pdf_bytes = []

        if isinstance(report_code, str):
            report_code = [report_code]

        for code in report_code:
            try:
                response = requests.get(base_url(code), headers=headers)
                pdf_bytes.append((code, response.content))
            except Exception as e:
                pdf_bytes.append((code, str(e)))
                self._logger(msg=f"[{__class__.__name__}] Load `{code}` error, error message: {e}", color="red")
        return pdf_bytes
