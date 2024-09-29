import unittest
import pandas as pd
from zlai.tools.report import *
from zlai.documents.pdf import ReadPDF


class TestMapping(unittest.TestCase):
    """"""
    def test_list_industry(self):
        """"""
        mapping = ReportMapping()
        industry = mapping.list_industry()
        print(industry.to_frame().head(5).to_markdown())

    def test_list_district(self):
        """"""
        mapping = ReportMapping()
        district = mapping.list_district()
        print(district.to_frame().head(5).to_markdown())

    def test_list_conception(self):
        """"""
        mapping = ReportMapping()
        conception = mapping.list_conception()
        print(conception.to_frame().head(5).to_markdown())


class TestReport(unittest.TestCase):

    def test_stock_morning_news_report(self):
        """"""
        columns = ["orgName", "industryName", "title", "researcher", "publishDate", "infoCode"]
        report = Report(report_type="券商晨报", size=5, begin_time="2024-09-23", end_time="2024-09-23")
        data = report.load_data()
        print(data.to_frame()[columns].to_markdown())

    def test_strategy_report(self):
        """"""
        columns = ["orgName", "industryName", "title", "researcher", "publishDate", "infoCode"]
        report = Report(report_type="策略报告", size=5, begin_time="2024-09-23", end_time="2024-09-23")
        data = report.load_data()
        print(data.to_frame()[columns].to_markdown())

    def test_stock_report(self):
        """"""
        columns = ["orgName", "stockCode", "stockName", "title", "researcher", "publishDate", "infoCode"]
        report = Report(code="002222", report_type="个股研报", size=5, begin_time="2024-09-23", end_time="2024-09-23")
        data = report.load_data()
        print(data.to_frame()[columns].to_markdown())

    def test_macro_report(self):
        """"""
        columns = ["orgName", "title", "researcher", "publishDate", "infoCode"]
        report = Report(report_type="宏观研究", size=5, begin_time="2024-09-23", end_time="2024-09-23")
        data = report.load_data()
        print(data.to_frame()[columns].to_markdown())

    def test_industry_report(self):
        """"""
        columns = ["orgName", "industryName", "industryCode", "title", "researcher", "publishDate", "infoCode"]
        report = Report(report_type="行业研报", industry_code="451", size=5, begin_time="2024-09-23", end_time="2024-09-23")
        data = report.load_data()
        print(data.to_frame()[columns].to_markdown())

    def test_save_report(self):
        """"""
        report = Report(
            report_type="行业研报", industry_code="451", size=5, begin_time="2024-09-23",
            end_time="2024-09-23")
        report.save_pdf(report_code=["AP202409231639991919"], path="./")

    def test_load_pdf(self):
        """"""
        report = Report(
            report_type="行业研报", industry_code="451", size=5, begin_time="2024-09-23",
            end_time="2024-09-23")
        pdf_bytes = report.load_pdf_bytes(report_code=["AP202409231639991919"])

        code, stream = pdf_bytes[0]
        pdf = ReadPDF(stream=stream)
        for page in pdf.documents:
            print(page.metadata)
            print(page.page_images[0])
            print(page.page_content)
            break


class TestProfitForecast(unittest.TestCase):

    def test_forecast(self):
        """"""
        report = ProfitForecast(size=2)
        data = report.load_data()
        columns = data.metadata.get("columns")
        print(data.to_frame(columns=columns).to_markdown())

    def test_forecast_by_industry(self):
        """"""
        report = ProfitForecast(industry="电源设备", size=2)
        data = report.load_data()
        columns = data.metadata.get("columns")
        print(data.to_frame(columns=columns).to_markdown())

    def test_forecast_by_conception(self):
        """"""
        report = ProfitForecast(conception="高压快充", size=2)
        data = report.load_data()
        columns = data.metadata.get("columns")
        print(data.to_frame(columns=columns).to_markdown())

    def test_forecast_by_district(self):
        """"""
        report = ProfitForecast(district="北京板块", size=2)
        data = report.load_data()
        columns = data.metadata.get("columns")
        print(data.to_frame(columns=columns).to_markdown())
