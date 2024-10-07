import json

import pandas as pd

from connection.client import search
from src.connection.features.search.enums import IdentifierType, AssetStatus
from src.connection.features.search.enums import SearchTypes
from connection.features.search.searcher.searcher import Searcher, _Identifier, _SearchRequest


class OtcsSearcher(Searcher):
    """
    Searcher for otc derivatives
    """

    def __init__(self,
                 identifier: str,
                 identifier_type: IdentifierType,
                 asset_status: AssetStatus = AssetStatus.All,
                 max_page_size=250,
                 token=None):
        self.asset_status = asset_status
        self.identifier = identifier
        self.identifier_type = identifier_type
        self.max_page_size = max_page_size
        self.token = token
        self.search_type = SearchTypes.OtcsSearch
        self.body = None

    def get_body(self) -> dict:
        if self.body:
            return self.body
        body = {
            _SearchRequest: {
                IdentifierType.__name__: self.identifier_type.name,
                _Identifier: self.identifier,
                AssetStatus.__name__: self.asset_status.name
            }
        }
        self.body = body
        return body

    def get_dict_result(self) -> dict:
        body = self.body if self.body else self.get_body()

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
