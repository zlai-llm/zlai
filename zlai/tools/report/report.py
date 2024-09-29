import os
import time
import random
import requests
from pydantic import BaseModel, Field
from typing import Any, List, Dict, Tuple, Union, Literal, Callable, Optional
from zlai.tools.utils import headers
from zlai.utils.mixin import LoggerMixin
from zlai.types.tools import ResponseData


__all__ = [
    "ReportQueryConfig",
    "Report",
]


TypeReport = Literal["个股研报", "行业研报", "策略报告", "宏观研究", "券商晨报"]


class ReportQueryConfig(BaseModel):
    """"""
    code: Optional[str] = Field(default=None)
    industry: Optional[str] = Field(default="*")
    industry_code: Optional[Union[str, int]] = Field(default="*")
    size: Optional[int] = Field(default=5)
    rating: Optional[str] = Field(default="*")
    rating_change: Optional[str] = Field(default="*")
    begin_time: Optional[str] = Field(default="*")
    end_time: Optional[str] = Field(default="*")
    page_no: Optional[int] = Field(default=1)
    report_type: Optional[TypeReport] = Field(default="*")
    q_type: Optional[Union[int, str]] = Field(default=None)

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
        :param report_type: 个股研报 行业研报 策略报告 宏观研究 券商晨报
        """
        super().__init__(**kwargs)

    def _reports_type(self):
        """"""
        q_types = ["个股研报", "行业研报", "策略报告", "宏观研究", "券商晨报"]
        if self.report_type is None or self.report_type == "*":
            self.q_type = "*"
        elif self.report_type in q_types:
            self.q_type = q_types.index(self.report_type)

    def _random_cb(self) -> str:
        """"""
        return str(int(random.random() * 1E7 + 1))

    def _current_time(self) -> str:
        """"""
        return str(int(time.time() * 1E3))

    def to_params(self) -> Dict:
        """"""
        if self.q_type is None:
            self._reports_type()

        params = {
            "industry": self.industry,
            "industryCode": self.industry_code,
            "pageSize": self.size,
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


class Report(LoggerMixin):
    """"""
    def __init__(
            self,
            query_config: Optional[ReportQueryConfig] = None,
            verbose: Optional[bool] = False,
            logger: Optional[Callable] = None,
            **kwargs: Any
    ):
        if query_config is None:
            self.query_config = ReportQueryConfig.model_validate(kwargs)
        else:
            self.query_config = query_config
        self.verbose = verbose
        self.logger = logger
        self.kwargs = kwargs

    def _base_url(self) -> str:
        """jg/dg/list"""
        if self.query_config.q_type is None:
            self.query_config._reports_type()

        base_url = "https://reportapi.eastmoney.com/report/"
        if self.query_config.q_type in [0, 1,]:
            base_url += "list"
        else:
            base_url += "dg"
        return base_url

    def load_data(
            self,
    ) -> ResponseData:
        """"""
        base_url = self._base_url()
        params = self.query_config.to_params()
        response = requests.get(base_url, params=params, headers=headers)
        data = response.json()
        reports = data.pop("data")
        metadata = data
        self._logger(msg=f"[{__class__.__name__}] Find {len(reports)} reports.", color="green")
        return ResponseData(data=reports, metadata=metadata)

    def save_pdf(
            self,
            report_code: Union[str, List[str]],
            path: str = "./"
    ) -> None:
        """"""
        pdf_bytes = self.load_pdf_bytes(report_code=report_code)
        for code, bytes_content in pdf_bytes:
            if isinstance(bytes_content, bytes):
                file_name = f"{code}.pdf"
                file_path = os.path.join(path, file_name)
                with open(file_path, "wb") as f:
                    f.write(bytes_content)

    def load_pdf_bytes(self, report_code: Union[str, List[str]], ) -> List[Tuple[str, Union[str, bytes]]]:
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
