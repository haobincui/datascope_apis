from typing import List
from src.connection.features.extraction.enums.content_field_names.tick_history.time_and_sales_content_field_names import \
    TimeAndSalesContentFieldNames
from src.connection.features.extraction.enums.extraction_types import ExtractionTypes
from src.connection.features.extraction.enums.required_extraction_data_types import RequiredExtractionDataTypes
from src.connection.features.extraction.on_demand_extractioner.on_demand_extractioner import OnDemandExtractioner
from src.connection.utils.condition.tick_history_time_and_sales_condtion import TickHistoryTimeAndSalesCondition
from src.connection.utils.instrument_identifier_list_base.instrument_identifier_list_base import \
    InstrumentIdentifierListBase


class TickHistoryTimeAndSalesRawExtractioner(OnDemandExtractioner):
    def __init__(
            self,
            identifier_list: InstrumentIdentifierListBase,
            times_and_sales_content_field_names: List[TimeAndSalesContentFieldNames],
            condition: TickHistoryTimeAndSalesCondition,
            extraction_type: ExtractionTypes = ExtractionTypes.ExtractRaw):
        super().__init__()
        self.condition = condition
        self.identifier_list = identifier_list
        self.times_and_sales_content_field_names = times_and_sales_content_field_names
        self.extraction_data_types = RequiredExtractionDataTypes.TickHistoryTimeAndSalesRequest
        self.extraction_type = extraction_type

    def get_body(self) -> dict:
        if self.body:
            return self.body
        body = {
            self._ExtractionRequest: {
                self._odata_type: self._extraction_request_header + self.extraction_data_types.value,
                self._ContentFieldNames: [field_name.value for field_name in
                                          self.times_and_sales_content_field_names],
                self._IdentifierList: self.identifier_list.get_dict_form('Extractions.ExtractionRequests'),
                self._Condition: self.condition.dict_form,
            }
        }
        self.body = body

        return body
