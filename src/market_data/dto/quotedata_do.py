from datetime import datetime, date
from enum import Enum
from typing import Union

import numpy as np
import pandas as pd

from market_data.contract_handler.contract_handler import ContractHandler
from src.market_data.contract_handler.future_contract import FutureContract
from market_data.contract_handler.option_contract import OptionContract
from market_data.dto.marketdata_do import MarketDataDO


# #RIC, Underlying RIC,Date-Time,GMT Offset,Type,Bid Price,Bid Size,Ask Price,Ask Size

# FLG10000O0,,Market Price,2020-01-30T08:36:33.449341031Z,+0,Quote,,,0.01,100


class QuoteType(Enum):
    Ask = 'Ask'
    Bid = 'Bid'


class QuoteDataDO(MarketDataDO):
    def __init__(self,
                 contract_id: str,
                 quote_time: Union[datetime, date],
                 bid_price: float,
                 bid_size: float,
                 ask_price: float,
                 ask_size: float):
        self.contract_id = contract_id
        self.quote_time = quote_time
        if not np.isnan(bid_price) and not np.isnan(bid_size):
            self.quote_type = QuoteType.Bid
            self.bid_price = bid_price
            self.bid_size = bid_size
        elif not np.isnan(ask_price) and not np.isnan(ask_size):
            self.quote_type = QuoteType.Ask
            self.ask_price = ask_price
            self.ask_size = ask_size
        else:
            raise ValueError(f'Unknown quote type, contract id: [{self.contract_id}]')
        self.__type = 'Quote'

    def get_price(self):
        return self.bid_price if self.quote_type == QuoteType.Bid else self.ask_price

    def get_data_time(self) -> datetime:
        return self.quote_time

    def to_json(self) -> dict:
        if self.quote_type == QuoteType.Bid:
            return {
                'ric': self.contract_id,
                'quote_time': self.quote_time,
                'type': self.__type,
                'quote_type': self.quote_type,
                'bid_price': self.bid_price,
                'bid_size': self.bid_size,
            }
        else:
            return {
                'ric': self.contract_id,
                'quote_time': self.quote_time,
                'type': self.__type,
                'quote_type': self.quote_type,

                'ask_price': self.ask_price,
                'ask_size': self.ask_size
            }

    def to_dataframe(self) -> pd.Series:
        if self.quote_type == QuoteType.Bid:
            series = pd.Series(
                data=[self.contract_id, self.quote_time, self.__type, self.bid_price, self.bid_size, self.quote_type],
                index=['contract_id', 'quote_time', 'type', 'trade_price', 'size', 'quote_type']
            )
        else:
            series = pd.Series(
                data=[self.contract_id, self.quote_time, self.__type, self.ask_price, self.ask_size, self.quote_type],
                index=['contract_id', 'quote_time', 'type', 'trade_price', 'size', 'quote_type']
            )
        return series

    def to_contract(self) -> Union[OptionContract, FutureContract]:
        contract = ContractHandler(self.contract_id).to_contract()
        return contract


