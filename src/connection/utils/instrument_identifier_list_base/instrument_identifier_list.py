from dataclasses import dataclass, field
from typing import List, Optional

from src.connection.features.extraction.enums.extraction_base_enums import IdentifierType
from src.connection.utils.instrument_identifier_list_base.instrument_identifier_list_base import \
    InstrumentIdentifierListBase
from src.connection.utils.validation_options.instrument_list_validation_options import \
    default_instrument_list_validation_options

from src.connection.utils.validation_options.instrument_validation_options import default_instrument_validation_options
from src.connection.utils.validation_options.validation_options import ValidationOptions

_odata_type = '@odata.type'
_id = '#DataScope.Select.Api.'
_InstrumentIdentifierList = 'InstrumentIdentifierList'
_InstrumentIdentifiers = 'InstrumentIdentifiers'
_Identifier = 'Identifier'
_ValidationOptions = 'ValidationOptions'
_UseUserPreferencesForValidationOptions = 'UseUserPreferencesForValidationOptions'


@dataclass()
class InstrumentIdentifier:
    identifier: str
    identifier_type: IdentifierType
    dict_form: dict = field(init=False)

    def __post_init__(self):
        self.dict_form = {
            _Identifier: self.identifier,
            IdentifierType.__name__: self.identifier_type.name
        }


@dataclass()
class InstrumentIdentifierList(InstrumentIdentifierListBase):
    identifier_list: List[InstrumentIdentifier]
    source: str = None
    use_user_preferences_for_validation_options: bool = False
    validation_options: Optional[ValidationOptions] = default_instrument_list_validation_options

    def get_dict_form(self, request_name: str) -> dict:
        if self.validation_options is None:
            _validation_options = None
        else:
            _validation_options = self.validation_options.dict_form

        dict_form = {
            _odata_type: _id + request_name + '.' + _InstrumentIdentifierList,
            _InstrumentIdentifiers: [ele.dict_form for ele in self.identifier_list],
            _ValidationOptions: _validation_options,
            _UseUserPreferencesForValidationOptions: self.use_user_preferences_for_validation_options
        }
        return dict_form
