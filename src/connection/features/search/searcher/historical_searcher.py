import json
from datetime import datetime

import pandas as pd

from connection.client import search
from src.connection.features.search.enums import IdentifierType
from src.connection.features.search.enums import HistoricalSearchTypes
from connection.features.search.searcher.searcher import Searcher, _Identifier
from src.calendar import DatetimeConverter

_Range = 'Range'
_Start = 'Start'
_End = 'End'
_Request = 'Request'

class HistoricalSearcher(Searcher):

    def __init__(self, identifier: str,
                 identifier_type: IdentifierType,
                 start: datetime,
                 end: datetime,
                 max_page_size=250,
                 token=None):
        self.identifier = identifier
        self.identifier_type = identifier_type
        self.start = start
        self.end = end
        self.max_page_size = max_page_size
        self.token = token
        self.search_type = HistoricalSearchTypes.HistoricalSearch

    def get_dict_result(self) -> dict:
        datetime_converter = DatetimeConverter()

        time_range = {
            _Start: datetime_converter.from_datetime_to_searcher_input(self.start),
            _End: datetime_converter.from_datetime_to_searcher_input(self.end)
        }
        body = {
            _Request: {
                IdentifierType.__name__: self.identifier_type.name,
                _Identifier: self.identifier,
                _Range: time_range
            }
        }
        result = search(search_type=self.search_type,
                        body=body,
                        max_page_size=self.max_page_size,
                        token=self.token)
        return result

    def get_json_result(self) -> str:
        res = self.get_dict_result()
        return json.dumps(res)

    def get_table_result(self) -> pd.DataFrame:
        pass
