from dataclasses import dataclass, field
from datetime import datetime, date
from typing import Union

from connection.utils.camparsions.comparison_operator import ComparisonOperator

_odata_type = '@odata.type'
_value = 'Value'
_from = 'From'
_to = 'To'


@dataclass()
class DateComparison:
    pass


@dataclass()
class DateValueComparison(DateComparison):
    comparison_operator: ComparisonOperator
    target_datetime: Union[datetime, date]
    compraisoner_name: str = '#DataScope.Select.Api.Search.DateValueComparison'
    dict_form: dict = field(init=False)

    def __post_init__(self):
        self.dict_form = {

        }


@dataclass()
class DateRangeComparison(DateComparison):
    from_datetime: Union[datetime, date]
    to_datetime: Union[datetime, date]
    compraisoner_name: str = '#DataScope.Select.Api.Search.DateRangeComparison'

    def __post_init__(self):
        if self.from_datetime.timestamp() < self.to_datetime.timestamp():
            raise ValueError(f'Start datetime need to before End datetime')
