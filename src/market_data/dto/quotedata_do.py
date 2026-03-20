from datetime import datetime, date
from enum import Enum
from typing import Union

import numpy as np
import pandas as pd

from src.market_data.contract.contract_handler import ContractHandler
from src.market_data.contract.future_contract import FutureContract
from src.market_data.contract.option_contract import OptionContract
from src.market_data.dto.marketdata_do import MarketDataDO


# #RIC, Underlying RIC,Date-Time,GMT Offset,Type,Bid Price,Bid Size,Ask Price,Ask Size

# FLG10000O0,,Market Price,2020-01-30T08:36:33.449341031Z,+0,Quote,,,0.01,100


class QuoteType(Enum):
    """Represents quote type."""
    Ask = 'Ask'
    Bid = 'Bid'


class QuoteDataDO(MarketDataDO):
    """Represents quote data do."""
    def __init__(self,
                 contract_id: str,
                 quote_time: Union[datetime, date],
                 bid_price: float,
                 bid_size: float,
                 ask_price: float,
                 ask_size: float):
        """Initialize the instance.

        Args:
            contract_id (str): Input value for contract id.
            quote_time (Union[datetime, date]): Input value for quote time.
            bid_price (float): Input value for bid price.
            bid_size (float): Input value for bid size.
            ask_price (float): Input value for ask price.
            ask_size (float): Input value for ask size.

        Returns:
            None: No value is returned.
        """
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
        """Return price.

        Returns:
            object: Requested value for the lookup.
        """
        return self.bid_price if self.quote_type == QuoteType.Bid else self.ask_price

    def get_data_time(self) -> datetime:
        """Return data time.

        Returns:
            datetime: Requested value for the lookup.
        """
        return self.quote_time

    def to_json(self) -> dict:
        """Convert to json.

        Returns:
            dict: Computed result of the operation.
        """
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
        """Convert to dataframe.

        Returns:
            pd.Series: Computed result of the operation.
        """
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
        """Convert to contract.

        Returns:
            Union[OptionContract, FutureContract]: Computed result of the operation.
        """
        contract = ContractHandler(self.contract_id).to_contract()
        return contract


