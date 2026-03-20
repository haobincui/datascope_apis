from typing import List

from src.connection.extraction.enums.content_field_names.tick_history.intraday_content_field_names import IntradaySummariesContentFieldNames
from src.connection.extraction.enums.extraction_types import ExtractionTypes
from src.connection.extraction.enums.required_extraction_data_types import RequiredExtractionDataTypes
from src.connection.extraction.on_demand_extractor.on_demand_extractor import OnDemandExtractor
from src.connection.utils.condition.tick_history_intraday_summaries_condition import TickHistoryIntradaySummariesCondition
from src.connection.utils.instrument_identifier_list_base.instrument_identifier_list_base import InstrumentIdentifierListBase


class TickHistoryIntradaySummariesExtractor(OnDemandExtractor):
    """Extractor for tick history intraday summaries data."""
    def __init__(
        self,
        identifier_list: InstrumentIdentifierListBase,
        intraday_summaries_content_field_names: List[IntradaySummariesContentFieldNames],
        condition: TickHistoryIntradaySummariesCondition,
        extraction_type: ExtractionTypes = ExtractionTypes.ExtractRaw,
    ):
        """Initialize an intraday summaries extractor request.

        Args:
            identifier_list (InstrumentIdentifierListBase): Instrument identifiers included in the request.
            intraday_summaries_content_field_names (List[IntradaySummariesContentFieldNames]): Requested intraday summary fields.
            condition (TickHistoryIntradaySummariesCondition): Condition object used to build the request payload.
            extraction_type (ExtractionTypes): Extraction output format requested from DataScope.

        Returns:
            None: No value is returned.
        """
        super().__init__()
        self.identifier_list = identifier_list
        self.intraday_summaries_content_field_names = intraday_summaries_content_field_names
        self.condition = condition
        self.extraction_data_types = RequiredExtractionDataTypes.TickHistoryIntradaySummariesExtractionRequest
        self.extraction_type = extraction_type

    def get_body(self) -> dict:
        """Build and cache the extraction request payload body.

        Returns:
            dict: Request body compatible with the DataScope extractions endpoint.
        """
        if self.body:
            return self.body
        body = {
            self._ExtractionRequest: {
                self._odata_type: self._extraction_request_header + self.extraction_data_types.value,
                self._ContentFieldNames: [field_name.value for field_name in self.intraday_summaries_content_field_names],
                self._IdentifierList: self.identifier_list.get_dict_form('Extractions.ExtractionRequests'),
                self._Condition: self.condition.dict_form,
            }
        }
        self.body = body
        return body
