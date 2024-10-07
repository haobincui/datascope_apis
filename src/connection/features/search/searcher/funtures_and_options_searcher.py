import json
from typing import Optional, List

import pandas as pd

from connection.utils.camparsions.comparison_operator import ComparisonOperator
from connection.client import search
from src.connection.utils.camparsions.date_comparison import DateComparison, _odata_type, _value, DateValueComparison, _from, _to, \
    DateRangeComparison
from connection.features.currency_codes import CurrencyCodes
from src.connection.features.exchange_codes import ExchangeCodes
from connection.features.extraction.enums.extraction_base_enums import FuturesAndOptionsType
from src.connection.features.search.enums import IdentifierType, AssetStatus
from src.connection.features.search.enums import FuturesAndOptionsStatus, ExerciseStyle, \
    PutCall
from src.connection.features.search.enums import SearchTypes
from connection.features.search.searcher.searcher import Searcher, _SearchRequest, _Identifier
from connection.utils.camparsions.numeric_comparison import NumericComparison, NumericValueComparison, \
    NumericRangeComparison
from src.calendar import DatetimeConverter

_FileCodes = 'FileCodes'
_StrikePrice = 'StrikePrice'
_ExpirationDate = 'ExpirationDate'
_PreferredIdentifierType = 'PreferredIdentifierType'


class FuturesAndOptionSearcher(Searcher):
    """
    Searcher for futures and options
    """

    def __init__(self,
                 identifier: str,
                 identifier_type: IdentifierType,
                 futures_and_options_status: Optional[FuturesAndOptionsStatus] = None,
                 expiration_date_range: Optional[DateComparison] = None,
                 strike_price_range: Optional[NumericComparison] = None,
                 asset_status: Optional[AssetStatus] = AssetStatus.Active,
                 exercise_style: Optional[ExerciseStyle] = None,
                 underlying_ric: Optional[str] = None,
                 put_call: Optional[PutCall] = None,
                 file_codes: Optional[str] = None,
                 futures_and_options_type: Optional[FuturesAndOptionsType] = None,
                 currency_codes: Optional[List[CurrencyCodes]] = None,
                 exchange_codes: Optional[List[ExchangeCodes]] = None,
                 preferred_identifier_type: IdentifierType = IdentifierType.Ric,
                 max_page_size=250,
                 token=None):
        self.asset_status = asset_status
        self.exchange_codes = exchange_codes
        self.currency_codes = currency_codes
        self.futures_and_options_type = futures_and_options_type
        self.file_codes = file_codes
        self.put_call = put_call
        self.underlying_ric = underlying_ric
        self.futures_and_options_status = futures_and_options_status
        self.identifier = identifier
        self.identifier_type = identifier_type
        self.exercise_style = exercise_style
        self.expiration_date_range = expiration_date_range,
        self.strike_price_range = strike_price_range
        self.preferred_identifier_type = preferred_identifier_type
        self.max_page_size = max_page_size
        self.token = token
        self.body = None
        self.search_type = SearchTypes.FuturesAndOptionsSearch

    def get_body(self) -> dict:
        if self.body:
            return self.body

        datetime_converter = DatetimeConverter()
        if isinstance(self.strike_price_range, NumericValueComparison):
            strike_price = {
                _odata_type: self.strike_price_range.__class__.__name__,
                ComparisonOperator.__name__: self.strike_price_range.__class__.__name__,
                _value: self.strike_price_range.target_number
            }
        elif isinstance(self.strike_price_range, NumericRangeComparison):
            strike_price = {
                _odata_type: self.strike_price_range.__class__.__name__,
                _from: self.strike_price_range.from_number,
                _to: self.strike_price_range.to_number
            }
        else:
            strike_price = None

        if isinstance(self.expiration_date_range, DateValueComparison):
            expiration_date = {
                _odata_type: self.expiration_date_range.__class__.__name__,
                ComparisonOperator.__name__: self.expiration_date_range.comparison_operator.name,
                _value: datetime_converter.from_datetime_to_searcher_input(self.expiration_date_range.target_datetime),
            }
        elif isinstance(self.expiration_date_range, DateRangeComparison):
            expiration_date = {
                _odata_type: self.expiration_date_range.__class__.__name__,
                _from: datetime_converter.from_datetime_to_searcher_input(self.expiration_date_range.from_datetime),
                _to: datetime_converter.from_datetime_to_searcher_input(self.expiration_date_range.to_datetime)
            }
        else:
            expiration_date = None

        body = {
            _SearchRequest: {
                _Identifier: self.identifier,
                FuturesAndOptionsType.__name__: self.futures_and_options_type,
                PutCall.__name__: self.put_call,
                _FileCodes: self.file_codes,
                CurrencyCodes.__name__: self.currency_codes,
                ExchangeCodes.__name__: self.exchange_codes,
                ExerciseStyle.__name__: self.exercise_style,
                _StrikePrice: strike_price,
                _ExpirationDate: expiration_date,
                AssetStatus.__name__: self.asset_status.name,
                IdentifierType.__name__: self.identifier_type.name,
                _PreferredIdentifierType: self.preferred_identifier_type.name
            }
        }
        self.body = body
        return self.body

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
