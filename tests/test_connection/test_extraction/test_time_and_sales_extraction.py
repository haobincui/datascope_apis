import unittest
from datetime import datetime
import os

from src.connection.extraction.enums.content_field_names.tick_history.time_and_sales_content_field_names import \
    TimeAndSalesContentFieldNames
from src.connection.extraction.enums.extraction_base_enums import IdentifierType
from src.connection.extraction.on_demand_extractor.tick_history_time_and_sales_extractor import \
    TickHistoryTimeAndSalesRawExtractor
from src.connection.utils.condition.tick_history_time_and_sales_condition import TickHistoryTimeAndSalesCondition
from src.connection.utils.instrument_identifier_list_base.instrument_identifier_list import InstrumentIdentifier, \
    InstrumentIdentifierList


class TestTimeAndSalesExtraction(unittest.TestCase):
    def test_time_and_sales_extraction_body(self):
        identifier = 'CLZ24'
        identifier_type = IdentifierType.Ric

        query_start_date = datetime(2022, 11, 21, 0, 0, 0)
        query_end_date = datetime(2022, 11, 22, 0, 0, 0)

        condition = TickHistoryTimeAndSalesCondition(query_start_date=query_start_date,
                                                     query_end_date=query_end_date)

        trade_ask_price = TimeAndSalesContentFieldNames.Trade.AskPrice
        quote_bid_price = TimeAndSalesContentFieldNames.Quote.BidPrice

        content_field_names = [trade_ask_price, quote_bid_price]

        identifier_list = InstrumentIdentifier(identifier=identifier,
                                               identifier_type=identifier_type)

        instrument_list = InstrumentIdentifierList(identifier_list=[identifier_list],
                                                   preferred_identifier_type=identifier_type)

        extractor = TickHistoryTimeAndSalesRawExtractor(
            identifier_list=instrument_list,
            times_and_sales_content_field_names=content_field_names,
            condition=condition,
        )

        body = extractor.get_body()
        self.assertIn('ExtractionRequest', body)
        self.assertIn('Condition', body['ExtractionRequest'])

    @unittest.skipUnless(
        os.getenv('DATASCOPE_RUN_INTEGRATION') == '1',
        'Set DATASCOPE_RUN_INTEGRATION=1 to run online extraction integration tests',
    )
    def test_time_and_sales_extraction_integration(self):
        identifier = 'CLZ24'
        identifier_type = IdentifierType.Ric

        query_start_date = datetime(2022, 11, 21, 0, 0, 0)
        query_end_date = datetime(2022, 11, 22, 0, 0, 0)

        condition = TickHistoryTimeAndSalesCondition(
            query_start_date=query_start_date,
            query_end_date=query_end_date,
        )

        trade_ask_price = TimeAndSalesContentFieldNames.Trade.AskPrice
        quote_bid_price = TimeAndSalesContentFieldNames.Quote.BidPrice
        content_field_names = [trade_ask_price, quote_bid_price]

        identifier_list = InstrumentIdentifier(
            identifier=identifier,
            identifier_type=identifier_type,
        )

        instrument_list = InstrumentIdentifierList(
            identifier_list=[identifier_list],
            preferred_identifier_type=identifier_type,
        )

        extractor = TickHistoryTimeAndSalesRawExtractor(
            identifier_list=instrument_list,
            times_and_sales_content_field_names=content_field_names,
            condition=condition,
        )

        self.assertTrue(extractor.save_output_file('./test.csv.gz'))
