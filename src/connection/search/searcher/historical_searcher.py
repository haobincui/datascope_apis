import json
from datetime import datetime

import pandas as pd

from src.connection.infra.http import search
from src.connection.search.enums import IdentifierType
from src.connection.search.enums import HistoricalSearchTypes
from src.connection.search.searcher.searcher import Searcher, _Identifier
from src.calendar import DatetimeConverter

_Range = 'Range'
_Start = 'Start'
_End = 'End'
_Request = 'Request'

class HistoricalSearcher(Searcher):

    """Searcher for historical instruments."""
    def __init__(self, identifier: str,
                 identifier_type: IdentifierType,
                 start: datetime,
                 end: datetime,
                 max_page_size=250,
                 token=None):
        """Initialize the instance.

        Args:
            identifier (str): Instrument identifier value.
            identifier_type (IdentifierType): Identifier type used to interpret the instrument code.
            start (datetime): Input value for start.
            end (datetime): Input value for end.
            max_page_size (object): Input value for max page size.
            token (object): Authentication token used for API requests.

        Returns:
            None: No value is returned.
        """
        self.identifier = identifier
        self.identifier_type = identifier_type
        self.start = start
        self.end = end
        self.max_page_size = max_page_size
        self.token = token
        self.search_type = HistoricalSearchTypes.HistoricalSearch
        self.body = None

    def get_body(self) -> dict:
        """Return body.

        Returns:
            dict: Requested value for the lookup.
        """
        if self.body:
            return self.body

        datetime_converter = DatetimeConverter()
        time_range = {
            _Start: datetime_converter.from_datetime_to_searcher_input(self.start),
            _End: datetime_converter.from_datetime_to_searcher_input(self.end),
        }
        self.body = {
            _Request: {
                IdentifierType.__name__: self.identifier_type.name,
                _Identifier: self.identifier,
                _Range: time_range,
            }
        }
        return self.body

    def get_dict_result(self) -> dict:
        """Return dict result.

        Returns:
            dict: Requested value for the lookup.
        """
        body = self.body if self.body else self.get_body()
        result = search(search_type=self.search_type,
                        body=body,
                        max_page_size=self.max_page_size,
                        token=self.token)
        return result

    def get_json_result(self) -> str:
        """Return json result.

        Returns:
            str: Requested value for the lookup.
        """
        res = self.get_dict_result()
        return json.dumps(res)

    def get_table_result(self) -> pd.DataFrame:
        """Return table result.

        Returns:
            pd.DataFrame: Requested value for the lookup.
        """
        return pd.DataFrame(self.get_dict_result())
