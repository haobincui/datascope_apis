from datetime import datetime, date
from typing import Union

import pandas as pd

from market_data.contract_handler.contract_handler import ContractHandler
from src.market_data.contract_handler.future_contract import FutureContract
from market_data.contract_handler.option_contract import OptionContract
from market_data.dto.marketdata_do import MarketDataDO


# #RIC, Underlying RIC,Date-Time, trade_price, trade_volume

class TradeDataDO(MarketDataDO):
    def __init__(self, contract_id: str,
                 trade_time: Union[datetime, date],
                 trade_price: float,
                 trade_volume: float):
        self.contract_id = contract_id
        self.trade_time = trade_time
        self.trade_price = trade_price
        self.trade_volume = trade_volume
        self.__type = 'Trade'

    def get_price(self) -> float:
        return self.trade_price

    def get_data_time(self) -> datetime:
        return self.trade_time

    def to_json(self) -> dict:
        return {
            'ric': self.contract_id,
            'trade_time': self.trade_time,
            'type': self.__type,
            'trade_price': self.trade_price,
            'trade_volume': self.trade_volume
        }

    def to_dataframe(self) -> pd.Series:
        series = pd.Series(
            data=[self.contract_id, self.trade_time, self.__type, self.trade_price, self.trade_volume],
            index=['ric', 'trade_time', 'type', 'trade_price', 'trade_volume']
        )
        return series

    def to_contract(self) -> Union[OptionContract, FutureContract]:
        contract = ContractHandler(self.contract_id).to_contract()
        return contract
