from dataclasses import dataclass
from typing import List

from src.connection.utils.filter.instrument_criteria_list_filter.instrument_criteria_list_filter import \
    InstrumentCriteriaListFilter
from src.connection.utils.instrument_identifier_list_base.instrument_identifier_list_base import InstrumentIdentifierListBase


_odata_type = '@odata.type'

_id = '#DataScope.Select.Api.'
_InstrumentCriteriaList = 'InstrumentCriteriaList'
_Filters = 'Filters'
_PreferredIdentifierType = 'PreferredIdentifierType'


@dataclass()
class InstrumentCriteriaList(InstrumentIdentifierListBase):
    """Represents instrument criteria list."""
    filters: List[InstrumentCriteriaListFilter]

    # dict_form: dict = field(init=False)

    def get_dict_form(self, request_name: str) -> dict:
        """Return dict form.

        Args:
            request_name (str): Input value for request name.

        Returns:
            dict: Requested value for the lookup.
        """
        dict_form = {
                        _odata_type: _id + request_name + '.' + _InstrumentCriteriaList,
                        _Filters: [
                            filt.dict_form for filt in self.filters
                        ],
                        _PreferredIdentifierType: self.preferred_identifier_type.name
                    }
        return dict_form


