from datetime import datetime, date
from typing import Union

import pandas as pd

from src.market_data.contract.contract_handler import ContractHandler
from src.market_data.contract.future_contract import FutureContract
from src.market_data.contract.option_contract import OptionContract
from src.market_data.dto.marketdata_do import MarketDataDO


# #RIC, Underlying RIC,Date-Time, trade_price, trade_volume

class TradeDataDO(MarketDataDO):
    """Represents trade data do."""
    def __init__(self, contract_id: str,
                 trade_time: Union[datetime, date],
                 trade_price: float,
                 trade_volume: float):
        """Initialize the instance.

        Args:
            contract_id (str): Input value for contract id.
            trade_time (Union[datetime, date]): Input value for trade time.
            trade_price (float): Input value for trade price.
            trade_volume (float): Input value for trade volume.

        Returns:
            None: No value is returned.
        """
        self.contract_id = contract_id
        self.trade_time = trade_time
        self.trade_price = trade_price
        self.trade_volume = trade_volume
        self.__type = 'Trade'

    def get_price(self) -> float:
        """Return price.

        Returns:
            float: Requested value for the lookup.
        """
        return self.trade_price

    def get_data_time(self) -> datetime:
        """Return data time.

        Returns:
            datetime: Requested value for the lookup.
        """
        return self.trade_time

    def to_json(self) -> dict:
        """Convert to json.

        Returns:
            dict: Computed result of the operation.
        """
        return {
            'ric': self.contract_id,
            'trade_time': self.trade_time,
            'type': self.__type,
            'trade_price': self.trade_price,
            'trade_volume': self.trade_volume
        }

    def to_dataframe(self) -> pd.Series:
        """Convert to dataframe.

        Returns:
            pd.Series: Computed result of the operation.
        """
        series = pd.Series(
            data=[self.contract_id, self.trade_time, self.__type, self.trade_price, self.trade_volume],
            index=['ric', 'trade_time', 'type', 'trade_price', 'trade_volume']
        )
        return series

    def to_contract(self) -> Union[OptionContract, FutureContract]:
        """Convert to contract.

        Returns:
            Union[OptionContract, FutureContract]: Computed result of the operation.
        """
        contract = ContractHandler(self.contract_id).to_contract()
        return contract
