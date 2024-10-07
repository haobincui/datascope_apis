from dataclasses import dataclass, field

from src.connection.utils.filter.instrument_criteria_list_filter.instrument_criteria_list_filter import \
    InstrumentCriteriaListFilter
from connection.utils import _odata_type

_Name = 'Name'
_Value = 'Values'


@dataclass()
class SingleFilter(InstrumentCriteriaListFilter):
    condition_name: str = None
    condition_value: float = None
    filter_name: str = field(init=False)
    dict_form: dict = field(init=False)

    def __post_init__(self):
        self.filter_name = '#DataScope.Select.Api.Extractions.SubjectLists.SingleValueFilter'
        self.dict_form = {
            _odata_type: self.filter_name,
            _Name: self.condition_name,
            _Value: self.condition_value
        }
        #  remove all None value
        for key in self.dict_form.keys():
            if self.dict_form[key] is None:
                self.dict_form.pop(key)




