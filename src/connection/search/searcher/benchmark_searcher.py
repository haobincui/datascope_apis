import json

import pandas as pd

from src.connection.infra.http import search
from src.connection.search.enums import IdentifierType
from src.connection.search.enums import SearchTypes
from src.connection.search.searcher.searcher import Searcher, _SearchRequest, _Identifier

_PreferredIdentifierType = 'PreferredIdentifierType'


class BenchmarkSearcher(Searcher):
    """
    Searcher for benchmark
    """

    def __init__(self, identifier: str,
                 identifier_type: IdentifierType,
                 preferred_identifier_type: IdentifierType = IdentifierType.Ric,
                 max_page_size=250,
                 token=None):
        """Initialize the instance.

        Args:
            identifier (str): Instrument identifier value.
            identifier_type (IdentifierType): Identifier type used to interpret the instrument code.
            preferred_identifier_type (IdentifierType): Input value for preferred identifier type.
            max_page_size (object): Input value for max page size.
            token (object): Authentication token used for API requests.

        Returns:
            None: No value is returned.
        """
        self.identifier = identifier
        self.identifier_type = identifier_type
        self.preferred_identifier_type = preferred_identifier_type
        self.max_page_size = max_page_size
        self.token = token
        self.search_type = SearchTypes.BenchmarkSearch
        self.body = None

    def get_body(self) -> dict:
        """Return body.

        Returns:
            dict: Requested value for the lookup.
        """
        if self.body:
            return self.body
        self.body = {
            _SearchRequest: {
                IdentifierType.__name__: self.identifier_type.name,
                _Identifier: self.identifier,
                _PreferredIdentifierType: self.preferred_identifier_type.name
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
