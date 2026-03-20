from datetime import datetime
from typing import Union

import pandas as pd

from src.market_data.contract.future_contract import FutureContract
from src.market_data.contract.option_contract import OptionContract
from src.market_data.dto.json_obj import JsonObj


class MarketDataDO(JsonObj):

    """Represents market data do."""
    def get_price(self) -> float:
        """Return price.

        Returns:
            float: Requested value for the lookup.
        """
        raise NotImplementedError

    def to_json(self) -> dict:
        """Convert to json.

        Returns:
            dict: Computed result of the operation.
        """
        raise NotImplementedError

    def to_dataframe(self) -> pd.DataFrame:
        """Convert to dataframe.

        Returns:
            pd.DataFrame: Computed result of the operation.
        """
        raise NotImplementedError

    def to_contract(self) -> Union[OptionContract, FutureContract]:
        """Convert to contract.

        Returns:
            Union[OptionContract, FutureContract]: Computed result of the operation.
        """
        raise NotImplementedError

    def get_data_time(self) -> datetime:
        """return the trade time or the quote time of the data"""
        raise NotImplementedError



