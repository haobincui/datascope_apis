from datetime import datetime
from typing import Union

import pandas as pd

from src.market_data.contract_handler.future_contract import FutureContract
from market_data.contract_handler.option_contract import OptionContract
from market_data.dto.json_obj import JsonObj


class MarketDataDO(JsonObj):

    def get_price(self) -> float:
        pass

    def to_json(self) -> dict:
        pass

    def to_dataframe(self) -> pd.DataFrame:
        pass

    def to_contract(self) -> Union[OptionContract, FutureContract]:
        pass

    def get_data_time(self) -> datetime:
        """return the trade time or the quote time of the data"""
        pass




