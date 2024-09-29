import unittest
from zlai.tools.macro import *


class TestCPI(unittest.TestCase):
    """"""

    def test_asset_invest(self):
        asset_invest = AssetInvest(size=10)
        data = asset_invest.load_data()
        print(data.metadata)
        print(data.to_frame(columns=data.metadata.get("columns")))

    def test_boom_index(self):
        """"""
        boom_index = BoomIndex(size=10)
        data = boom_index.load_data()
        print(data.metadata)
        print(data.to_frame(columns=data.metadata.get("columns")))

    def test_cpi(self):
        cpi = CPI(size=10)
        data = cpi.load_data()
        print(data.metadata)
        print(data.to_frame(columns=data.metadata.get("columns")))

    def test_currency_supply(self):
        """"""
        currency_supply = CurrencySupply(size=10)
        data = currency_supply.load_data()
        print(data.metadata)
        print(data.to_frame(columns=data.metadata.get("columns")))

    def test_customs(self):
        """"""
        customs = Customs(size=10)
        data = customs.load_data()
        print(data.metadata)
        print(data.to_frame(columns=data.metadata.get("columns")))

    def test_deposit_rate(self):
        """"""
        deposit_rate = DepositRate(size=10)
        data = deposit_rate.load_data()
        print(data.metadata)
        print(data.to_frame(columns=data.metadata.get("columns")))

    def test_deposit_reserve(self):
        """"""
        deposit_reserve = DepositReserve(size=10)
        data = deposit_reserve.load_data()
        print(data.metadata)
        print(data.to_frame(columns=data.metadata.get("columns")))

    def test_faith_index(self):
        """"""
        faith_index = FaithIndex(size=10)
        data = faith_index.load_data()
        print(data.metadata)
        print(data.to_frame(columns=data.metadata.get("columns")))

    def test_fdi(self):
        """"""
        fdi = FDI(size=10)
        data = fdi.load_data()
        print(data.metadata)
        print(data.to_frame(columns=data.metadata.get("columns")))

    def test_forex_deposit(self):
        """"""
        forex_deposit = ForexDeposit(size=10)
        data = forex_deposit.load_data()
        print(data.metadata)
        print(data.to_frame(columns=data.metadata.get("columns")))

    def test_forex_loan(self):
        """"""
        forex_loan = ForexLoan(size=10)
        data = forex_loan.load_data()
        print(data.metadata)
        print(data.to_frame(columns=data.metadata.get("columns")))

    def test_gdp(self):
        """"""
        gdp = GDP(size=10)
        data = gdp.load_data()
        print(data.metadata)
        print(data.to_frame(columns=data.metadata.get("columns")))

    def test_gold_currency(self):
        """"""
        gold_currency = GoldCurrency(size=10)
        data = gold_currency.load_data()
        print(data.metadata)
        print(data.to_frame(columns=data.metadata.get("columns")))

    def test_goods_index(self):
        """"""
        goods_index = GoodsIndex(size=10)
        data = goods_index.load_data()
        print(data.metadata)
        print(data.to_frame(columns=data.metadata.get("columns")))

    def test_gov_income(self):
        """"""
        gov_income = GovIncome(size=10)
        data = gov_income.load_data()
        print(data.metadata)
        print(data.to_frame(columns=data.metadata.get("columns")))

    def test_old_hose(self):
        """"""
        old_hose = HoseIndexOld(size=10)
        data = old_hose.load_data()
        print(data.metadata)
        print(data.to_frame(columns=data.metadata.get("columns")))

    def test_new_hose(self):
        """"""
        new_hose = HoseIndexNew(size=10)
        data = new_hose.load_data()
        print(data.metadata)
        print(data.to_frame(columns=data.metadata.get("columns")))

        new_hose = HoseIndexNew(size=10, cities=["杭州", "深圳"])
        data = new_hose.load_data()
        print(data.metadata)
        print(data.to_frame(columns=data.metadata.get("columns")))

        new_hose = HoseIndexNew(size=10, report_date="2023-01-01")
        data = new_hose.load_data()
        print(data.metadata)
        print(data.to_frame(columns=data.metadata.get("columns")))

    def test_imp_interest(self):
        """"""
        imp_interest = ImpInterest(size=10, )
        data = imp_interest.load_data()
        print(data.metadata)
        print(data.to_frame(columns=data.metadata.get("columns")))

    def test_indus_grow(self):
        """"""
        indus_grow = IndusGrow(size=10)
        data = indus_grow.load_data()
        print(data.metadata)
        print(data.to_frame(columns=data.metadata.get("columns")))

    def test_lpr(self):
        """"""
        lpr = LPR(size=10)
        data = lpr.load_data()
        print(data.metadata)
        print(data.to_frame(columns=data.metadata.get("columns")))

    def test_new_loan(self):
        """"""
        new_loan = NewLoan(size=10)
        data = new_loan.load_data()
        print(data.metadata)
        print(data.to_frame(columns=data.metadata.get("columns")))

    def test_oil_price(self):
        """"""
        oil_price = OilPrice(size=10)
        data = oil_price.load_data()
        print(data.metadata)
        print(data.to_frame(columns=data.metadata.get("columns")))

    def test_pmi(self):
        """"""
        pmi = PMI(size=10)
        data = pmi.load_data()
        print(data.metadata)
        print(data.to_frame(columns=data.metadata.get("columns")))

    def test_ppi(self):
        """"""
        ppi = PPI(size=10)
        data = ppi.load_data()
        print(data.metadata)
        print(data.to_frame(columns=data.metadata.get("columns")))

    def test_stock_open(self):
        """"""
        stock_open = StockOpen(size=10)
        data = stock_open.load_data()
        print(data.metadata)
        print(data.to_frame(columns=data.metadata.get("columns")))

    def test_stock_statistics(self):
        """"""
        stock_statistics = StockStatistics(size=10)
        data = stock_statistics.load_data()
        print(data.metadata)
        print(data.to_frame(columns=data.metadata.get("columns")))

    def test_tax(self):
        """"""
        tax = Tax(size=10)
        data = tax.load_data()
        print(data.metadata)
        print(data.to_frame(columns=data.metadata.get("columns")))

    def test_total_retail(self):
        """"""
        total_retail = TotalRetail(size=10)
        data = total_retail.load_data()
        print(data.metadata)
        print(data.to_frame(columns=data.metadata.get("columns")))

    def test_transfer_fund(self):
        """"""
        transfer_fund = TransferFund(size=10)
        data = transfer_fund.load_data()
        print(data.metadata)
        print(data.to_frame(columns=data.metadata.get("columns")))


class TestLoopLoadData(unittest.TestCase):
    """"""
    def test_loop(self):
        """"""
        macro_mapping = {
            "居民消费价格指数(CPI)": CPI,
            "工业品出厂价格指数(PPI)": PPI,
            "国内生产总值(GDP)": GDP,
            "采购经理人指数(PMI)": PMI,
            "城镇固定资产投资": AssetInvest,
            "房价指数(old)": HoseIndexOld,
            "新房价指数": HoseIndexNew,
            "企业景气及企业家信心指数": BoomIndex,
            "工业增加值增长": IndusGrow,
            "企业商品价格指数": GoodsIndex,
            "消费者信心指数": FaithIndex,
            "社会消费品零售总额": TotalRetail,
            "货币供应量": CurrencySupply,
            "海关进出口增减情况一览表": Customs,
            "全国股票交易统计表": StockStatistics,
            "外汇和黄金储备": GoldCurrency,
            "交易结算资金(银证转账)": TransferFund,
            "股票账户统计表(新)": StockOpen,
            "外商直接投资数据(FDI)": FDI,
            "财政收入": GovIncome,
            "全国税收收入": Tax,
            "新增信贷数据": NewLoan,
            "银行间拆借利率": ImpInterest,
            "本外币存款": ForexDeposit,
            "外汇贷款数据": ForexLoan,
            "存款准备金率": DepositReserve,
            "利率调整": DepositRate,
            "油价": OilPrice,
            "LPR数据": LPR,
        }
        for macro_name, macro_class in macro_mapping.items():
            macro = macro_class(size=5)
            data = macro.load_data()
            print(data.metadata)
            print(data.to_frame(columns=data.metadata.get("columns")).to_markdown())
            print("\n\n")
