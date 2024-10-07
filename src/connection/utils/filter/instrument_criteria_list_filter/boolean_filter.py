from dataclasses import dataclass
from enum import Enum
from connection.utils import _odata_type

from src.connection.utils.filter.instrument_criteria_list_filter.instrument_criteria_list_filter import InstrumentCriteriaListFilter

_Name = 'Name'
_Value = 'Value'


class BooleanValue(Enum):
    All = 'All',
    No = 'No',
    Yes = 'Yes'


@dataclass()
class BooleanFilter(InstrumentCriteriaListFilter):
    condition_name: str = None
    boolean_value: BooleanValue = BooleanValue.All

    def __post_init__(self):
        self.filter_name = '#DataScope.Select.Api.Extractions.SubjectLists.BooleanFilter'
        self.dict_form = {
            _odata_type: self.filter_name,
            _Name: self.condition_name,
            _Value: self.boolean_value.value
        }
        #  remove all None value
        for key in self.dict_form.keys():
            if self.dict_form[key] is None:
                self.dict_form.pop(key)

