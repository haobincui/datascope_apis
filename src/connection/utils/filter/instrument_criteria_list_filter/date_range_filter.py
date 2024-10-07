from dataclasses import dataclass, field
from datetime import datetime

from src.connection.utils.filter.instrument_criteria_list_filter.instrument_criteria_list_filter import \
    InstrumentCriteriaListFilter
from connection.utils.filter.operator.range_operator import RangeOperator
from connection.utils import _odata_type
from src.calendar import DatetimeConverter

_Name = 'Name'
_Value = 'Value'
_Max = 'Max'
_Min = 'Min'
_Op = 'Op'


@dataclass()
class DateRangeFilter(InstrumentCriteriaListFilter):
    max_datetime_value: datetime = None
    min_datetime_value: datetime = None
    condition_name: str = None
    range_operator: RangeOperator = None
    operator_datetime_value: datetime = None
    filter_name: str = field(init=False)
    dict_form: dict = field(init=False)

    def __post_init__(self):
        datetime_converter_to_input = DatetimeConverter().from_datetime_to_searcher_input
        self.filter_name = '#DataScope.Select.Api.Extractions.SubjectLists.DateRangeFilter'
        self.dict_form = {
            _odata_type: self.filter_name,
            _Name: self.condition_name,
            _Op: self.range_operator.value,
            _Max: datetime_converter_to_input(self.max_datetime_value),
            _Min: datetime_converter_to_input(self.min_datetime_value),
            _Value: datetime_converter_to_input(self.operator_datetime_value)
        }
        #  remove all None value
        for key in self.dict_form.keys():
            if self.dict_form[key] is None:
                self.dict_form.pop(key)







