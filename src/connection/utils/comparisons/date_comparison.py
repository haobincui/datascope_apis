from dataclasses import dataclass, field
from datetime import date, datetime
from typing import Union

from .comparison_operator import ComparisonOperator

_odata_type = '@odata.type'
_value = 'Value'
_from = 'From'
_to = 'To'


@dataclass()
class DateComparison:
    """Represents date comparison."""
    pass


@dataclass()
class DateValueComparison(DateComparison):
    """Represents date value comparison."""
    comparison_operator: ComparisonOperator
    target_datetime: Union[datetime, date]
    compraisoner_name: str = '#DataScope.Select.Api.Search.DateValueComparison'
    dict_form: dict = field(init=False)

    def __post_init__(self):
        """Post init.

        Returns:
            None: No value is returned.
        """
        self.dict_form = {

        }


@dataclass()
class DateRangeComparison(DateComparison):
    """Represents date range comparison."""
    from_datetime: Union[datetime, date]
    to_datetime: Union[datetime, date]
    compraisoner_name: str = '#DataScope.Select.Api.Search.DateRangeComparison'

    def __post_init__(self):
        """Post init.

        Returns:
            None: No value is returned.
        """
        if self.from_datetime.timestamp() < self.to_datetime.timestamp():
            raise ValueError(f'Start datetime need to before End datetime')
