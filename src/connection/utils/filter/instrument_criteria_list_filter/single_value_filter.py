from dataclasses import dataclass, field

from src.connection.utils.filter.instrument_criteria_list_filter.instrument_criteria_list_filter import \
    InstrumentCriteriaListFilter
from src.connection.utils import _odata_type

_Name = 'Name'
_Value = 'Values'


@dataclass()
class SingleFilter(InstrumentCriteriaListFilter):
    """Represents single filter."""
    condition_name: str = None
    condition_value: float = None
    filter_name: str = field(init=False)
    dict_form: dict = field(init=False)

    def __post_init__(self):
        """Post init.

        Returns:
            None: No value is returned.
        """
        self.filter_name = '#DataScope.Select.Api.Extractions.SubjectLists.SingleValueFilter'
        self.dict_form = {
            _odata_type: self.filter_name,
            _Name: self.condition_name,
            _Value: self.condition_value
        }
        #  remove all None value
        for key in list(self.dict_form.keys()):
            if self.dict_form[key] is None:
                self.dict_form.pop(key)




