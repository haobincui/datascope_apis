from dataclasses import dataclass, field
from typing import List

from src.connection.utils.filter.instrument_criteria_list_filter.instrument_criteria_list_filter import \
    InstrumentCriteriaListFilter
from connection.utils.filter.operator.multi_value_operator import MultiValueOperator
from connection.utils import _odata_type

_Name = 'Name'
_Op = 'Op'
_Value = 'Values'


@dataclass()
class MultiValueFilter(InstrumentCriteriaListFilter):
    condition_name: str = None
    multi_value_operator: MultiValueOperator = MultiValueOperator.In
    condition_values: List[str] = None
    filter_name: str = field(init=False)
    dict_form: dict = field(init=False)

    def __post_init__(self):
        self.filter_name = '#DataScope.Select.Api.Extractions.SubjectLists.MultiValueFilter'
        self.dict_form = {
            _odata_type: self.filter_name,
            _Name: self.condition_name,
            _Op: self.multi_value_operator.value,
            _Value: self.condition_values if self.condition_values is not None else ['null']
        }
        #  remove all None value
        for key in self.dict_form.keys():
            if self.dict_form[key] is None:
                self.dict_form.pop(key)

