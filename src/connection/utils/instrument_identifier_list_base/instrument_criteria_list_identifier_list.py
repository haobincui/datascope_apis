from dataclasses import dataclass

from src.connection.utils.instrument_identifier_list_base.instrument_identifier_list_base import InstrumentIdentifierListBase

_odata_type = '@odata.type'
_id = '#DataScope.Select.Api.'
_InstrumentCriteriaListIdentifierList = 'InstrumentCriteriaListIdentifierList'
_CriteriaListId = 'CriteriaListId'


@dataclass()
class InstrumentCriteriaListIdentifierList(InstrumentIdentifierListBase):
    """Represents instrument criteria list identifier list."""
    criteria_list_id: str

    def get_dict_form(self, request_name: str) -> dict:
        """Return dict form.

        Args:
            request_name (str): Input value for request name.

        Returns:
            dict: Requested value for the lookup.
        """
        dict_form = {
            _odata_type: _id + request_name + '.' + _InstrumentCriteriaListIdentifierList,
            _CriteriaListId: self.criteria_list_id,
        }
        return dict_form
