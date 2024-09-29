from typing import Optional, List, Dict, Any
from zlai.types.tools import ResponseData

from .asset_invest import *
from .boom_index import *
from .cpi import *
from .currency_supply import *
from .customs import *
from .deposit_rate import *
from .deposit_reserve import *
from .faith_index import *
from .fdi import *
from .forex_deposit import *
from .forex_loan import *
from .gdp import *
from .gold_currency import *
from .goodes_index import *
from .gov_income import *
from .hose_index import *
from .imp_intrestraten import *
from .indus_grow import *
from .lpr import *
from .new_loan import *
from .oil_price import *
from .pmi import *
from .ppi import *
from .stock_open import *
from .stock_statistics import *
from .tax import *
from .total_retail import *
from .transfer_fund import *


__all__ = [
    "MacroIndex"
]


data_mapping: Dict = {
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


class MacroIndex:
    def __init__(self):
        """"""

    def list_data(self) -> List[str]:
        """"""
        return list(data_mapping.keys())

    def load_data(
            self,
            macro: str,
            size: Optional[int] = 20,
            **kwargs: Any,
    ) -> ResponseData:
        """"""
        if macro not in data_mapping:
            raise ValueError(f"Invalid macro index: {macro}, valid options: {list(data_mapping.keys())}")

        new_loan = data_mapping.get(macro)(size=size, **kwargs)
        data = new_loan.load_data()
        return data
