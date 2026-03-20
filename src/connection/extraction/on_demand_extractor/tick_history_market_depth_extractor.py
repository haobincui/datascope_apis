from typing import List

from src.connection.extraction.enums.content_field_names.tick_history.market_depth_content_field_name import MarketDepthContentFieldNames
from src.connection.extraction.enums.extraction_types import ExtractionTypes
from src.connection.extraction.enums.required_extraction_data_types import RequiredExtractionDataTypes
from src.connection.extraction.on_demand_extractor.on_demand_extractor import OnDemandExtractor
from src.connection.utils.condition.tick_history_market_depth_condition import TickHistoryMarketDepthCondition
from src.connection.utils.instrument_identifier_list_base.instrument_identifier_list_base import InstrumentIdentifierListBase


class TickHistoryMarketDepthExtractor(OnDemandExtractor):
    """Extractor for tick history market depth data."""
    def __init__(
        self,
        identifier_list: InstrumentIdentifierListBase,
        market_depth_content_field_names: List[MarketDepthContentFieldNames],
        condition: TickHistoryMarketDepthCondition,
        extraction_type: ExtractionTypes = ExtractionTypes.ExtractRaw,
    ):
        """Initialize the instance.

        Args:
            identifier_list (InstrumentIdentifierListBase): Collection of instruments to query.
            market_depth_content_field_names (List[MarketDepthContentFieldNames]): Input value for market depth content field names.
            condition (TickHistoryMarketDepthCondition): Condition object used to build the request payload.
            extraction_type (ExtractionTypes): Extraction output format requested from DataScope.

        Returns:
            None: No value is returned.
        """
        super().__init__()
        self.condition = condition
        self.identifier_list = identifier_list
        self.market_depth_content_field_names = market_depth_content_field_names
        self.extraction_data_types = RequiredExtractionDataTypes.TickHistoryMarketDepthExtractionRequest
        self.extraction_type = extraction_type

    def get_body(self) -> dict:
        """Return body.

        Returns:
            dict: Requested value for the lookup.
        """
        if self.body:
            return self.body
        body = {
            self._ExtractionRequest: {
                self._odata_type: self._extraction_request_header + self.extraction_data_types.value,
                self._ContentFieldNames: [field_name.value for field_name in self.market_depth_content_field_names],
                self._IdentifierList: self.identifier_list.get_dict_form('Extractions.ExtractionRequests'),
                self._Condition: self.condition.dict_form,
            }
        }
        self.body = body
        return body
