from abc import abstractmethod

import pandas as pd

from connection.client import search
from connection.features.feature import Feature
from src.connection.features.search.enums import SearchTypes

_SearchRequest = "SearchRequest"
_Identifier = "Identifier"


class Searcher(Feature):
    """
    abstract class for searcher
    """
    @abstractmethod
    def get_body(self) -> dict:
        pass

    @abstractmethod
    def get_json_result(self) -> str:
        """
        Serilalize dict to json
        """
        raise NotImplemented

    @abstractmethod
    def get_table_result(self) -> pd.DataFrame:
        """
        return a dataframe for data analysis
        """
        raise NotImplemented

    @abstractmethod
    def get_dict_result(self) -> dict:
        """
        de-Serialize Json to Obj
        """
        raise NotImplemented








