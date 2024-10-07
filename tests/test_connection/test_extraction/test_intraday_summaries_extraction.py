import unittest
from datetime import datetime

from src.connection.features.extraction.enums.content_field_names.tick_history.intraday_content_field_names import \
    IntradaySummariesContentFieldNames
from src.connection.features.extraction.enums.extraction_base_enums import IdentifierType
from src.connection.features.extraction.on_demand_extractioner.tick_history_intraday_summaries_extractioner import \
    TickHistoryIntradaySummariesExtractioner
from src.connection.utils.condition.tick_history_intraday_summaries_condition import TickHistoryIntradaySummariesCondition
from src.connection.utils.instrument_identifier_list_base.instrument_identifier_list import InstrumentIdentifier, \
    InstrumentIdentifierList


class TestIntradaySummariesExtraction(unittest.TestCase):
    def test_intraday_summaries_extraction_body(self):
        identifier = 'IBM.N'
        identifier_type = IdentifierType.Ric
        identifier_list = InstrumentIdentifier(identifier=identifier,
                                               identifier_type=identifier_type)

        instrument_list = InstrumentIdentifierList(identifier_list=[identifier_list],
                                                   preferred_identifier_type=identifier_type)

        query_start_date = datetime(2016, 11, 20, 20, 18, 14)
        query_end_date = datetime(2016, 11, 23, 20, 18, 14)

        close_ask = IntradaySummariesContentFieldNames.Close.Ask
        close_bid = IntradaySummariesContentFieldNames.Close.Bid
        high = IntradaySummariesContentFieldNames.High.High
        low = IntradaySummariesContentFieldNames.Low.Low
        open_ask = IntradaySummariesContentFieldNames.Open.Ask
        open_bid = IntradaySummariesContentFieldNames.Open.Bid

        content_field_names = [close_ask, close_bid, high, low, open_ask, open_bid]

        condition = TickHistoryIntradaySummariesCondition(query_start_date=query_start_date, query_end_date=query_end_date)

        extractioner = TickHistoryIntradaySummariesExtractioner(identifier_list=instrument_list,
                                                                intraday_summaries_content_field_names=content_field_names,
                                                                condition=condition)
        body = extractioner.get_body()

