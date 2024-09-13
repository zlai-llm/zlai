import os
import requests
from datetime import datetime
from typing import List, Dict, Optional
from zlai.tools.utils import headers


__all__ = [
    "ReportTools",
]


class ReportTools:
    """"""
    report_info: Optional[Dict]
    report_list: Optional[List[Dict]]

    def __init__(
            self,
            industry: Optional[str] = "*",
            industry_code: Optional[str] = "*",
            page_size: Optional[int] = 5,
            rating: Optional[str] = "*",
            rating_change: Optional[str] = "*",
            begin_time: Optional[str] = "2024-09-12",
            end_time: Optional[str] = "2024-09-12",
            page_no: Optional[int] = 1,
            q_type: Optional[int] = 1,
    ):
        """"""
        self.industry = industry
        self.industry_code = industry_code
        self.page_size = page_size
        self.rating = rating
        self.rating_change = rating_change
        self.begin_time = begin_time
        self.end_time = end_time
        self.page_no = page_no
        self.q_type = q_type
        self.list_reports()

    def list_reports(
            self,
    ) -> Dict:
        """"""
        """
        =*&pageSize=5&industry=*&rating=*&ratingChange=*&beginTime=2020-09-12&endTime=2024-09-12&pageNo=1&qType=1
        """
        base_url = "https://reportapi.eastmoney.com/report/list"
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
        }
        response = requests.get(base_url, params=params, headers=headers)
        data = response.json()
        self.report_list = data.pop("data")
        self.report_info = data

    def save_reports(self, path: str = "./"):
        """"""
        base_url = """https://pdf.dfcfw.com/pdf/H3_{}_1.pdf""".format
        for report in self.report_list:
            info_code = report.get("infoCode", None)
            industry_name = report.get("industryName", None)
            title = report.get("title", None)
            publish_date = report.get("publishDate")
            date_object = datetime.strptime(publish_date, "%Y-%m-%d %H:%M:%S.%f")
            date = date_object.strftime("%Y%m%d")
            file_name = f"{date}-{industry_name}-{title}.pdf"
            response = requests.get(base_url(info_code))
            file_path = os.path.join(path, file_name)
            with open(file_path, "wb") as f:
                f.write(response.content)

    def load_bytes(self) -> List[bytes]:
        base_url = """https://pdf.dfcfw.com/pdf/H3_{}_1.pdf""".format
        pdf_bytes = []
        for report in self.report_list:
            info_code = report.get("infoCode", None)
            response = requests.get(base_url(info_code))
            pdf_bytes.append(response.content)
        return pdf_bytes
