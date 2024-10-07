from dataclasses import dataclass, field

from src.connection.utils.filter.instrument_criteria_list_filter.instrument_criteria_list_filter import \
    InstrumentCriteriaListFilter
from connection.utils.filter.operator.range_operator import RangeOperator
from connection.utils import _odata_type

_Name = 'Name'
_Op = 'Op'
_Value = 'Values'
_Max = 'Max'
_Min = 'Min'


@dataclass()
class RangeFilter(InstrumentCriteriaListFilter):
    max_value: float = None
    min_value: float = None
    condition_name: str = None
    range_operator: RangeOperator = RangeOperator.Equal
    condition_value: float = None
    filter_name: str = field(init=False)
    dict_form: dict = field(init=False)

    def __post_init__(self):
        self.filter_name = '#DataScope.Select.Api.Extractions.SubjectLists.RangeFilter'
        self.dict_form = {
            _odata_type: self.filter_name,
            _Name: self.condition_name,
            _Op: self.range_operator.value,
            _Max: self.max_value,
            _Min: self.min_value,
            _Value: self.condition_value
        }
        #  remove all None value
        for key in self.dict_form.keys():
            if self.dict_form[key] is None:
                self.dict_form.pop(key)

