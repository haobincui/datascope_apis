from enum import Enum


class RequiredExtractionDataTypes(Enum):
    """Represents required extraction data types."""
    TickHistoryIntradaySummariesExtractionRequest = 'TickHistoryIntradaySummariesExtractionRequest'
    TickHistoryMarketDepthExtractionRequest = 'TickHistoryMarketDepthExtractionRequest'
    TickHistoryTimeAndSalesRequest = 'TickHistoryTimeAndSalesExtractionRequest'
