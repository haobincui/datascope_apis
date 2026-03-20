from dataclasses import dataclass, field
from typing import List

from src.connection.utils.filter.instrument_criteria_list_filter.instrument_criteria_list_filter import \
    InstrumentCriteriaListFilter
from src.connection.utils.filter.operator.multi_value_operator import MultiValueOperator
from src.connection.utils import _odata_type

_Name = 'Name'
_Op = 'Op'
_Value = 'Values'


@dataclass()
class MultiValueFilter(InstrumentCriteriaListFilter):
    """Represents multi value filter."""
    condition_name: str = None
    multi_value_operator: MultiValueOperator = MultiValueOperator.In
    condition_values: List[str] = None
    filter_name: str = field(init=False)
    dict_form: dict = field(init=False)

    def __post_init__(self):
        """Post init.

        Returns:
            None: No value is returned.
        """
        self.filter_name = '#DataScope.Select.Api.Extractions.SubjectLists.MultiValueFilter'
        self.dict_form = {
            _odata_type: self.filter_name,
            _Name: self.condition_name,
            _Op: self.multi_value_operator.value,
            _Value: self.condition_values if self.condition_values is not None else ['null']
        }
        #  remove all None value
        for key in list(self.dict_form.keys()):
            if self.dict_form[key] is None:
                self.dict_form.pop(key)

