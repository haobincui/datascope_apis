import json

import pandas as pd

from connection.client import search
from src.connection.features.search.enums import IdentifierType
from src.connection.features.search.enums import SearchTypes
from connection.features.search.searcher.searcher import Searcher, _SearchRequest, _Identifier

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
        self.identifier = identifier
        self.identifier_type = identifier_type
        self.preferred_identifier_type = preferred_identifier_type
        self.max_page_size = max_page_size
        self.token = token
        self.search_type = SearchTypes.BenchmarkSearch

    def get_dict_result(self) -> dict:
        body = {
            _SearchRequest: {
                IdentifierType.__name__: self.identifier_type.name,
                _Identifier: self.identifier,
                _PreferredIdentifierType: self.preferred_identifier_type.name
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
