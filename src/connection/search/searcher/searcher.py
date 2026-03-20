from abc import abstractmethod

import pandas as pd

from src.connection.infra.http import search
from src.connection.shared.feature import Feature
from src.connection.search.enums import SearchTypes

_SearchRequest = "SearchRequest"
_Identifier = "Identifier"


class Searcher(Feature):
    """
    abstract class for searcher
    """
    @abstractmethod
    def get_body(self) -> dict:
        """Return body.

        Returns:
            dict: Requested value for the lookup.
        """
        raise NotImplementedError

    @abstractmethod
    def get_json_result(self) -> str:
        """
        Serilalize dict to json
        """
        raise NotImplementedError

    @abstractmethod
    def get_table_result(self) -> pd.DataFrame:
        """
        return a dataframe for data analysis
        """
        raise NotImplementedError

    @abstractmethod
    def get_dict_result(self) -> dict:
        """
        de-Serialize Json to Obj
        """
        raise NotImplementedError






