import unittest
from datetime import datetime

from src.connection.features.extraction.enums.content_field_names.tick_history.time_and_sales_content_field_names import \
    TimeAndSalesContentFieldNames
from src.connection.features.extraction.enums.extraction_base_enums import IdentifierType
from src.connection.features.extraction.on_demand_extractioner.tick_history_time_and_sales_extractioner import \
    TickHistoryTimeAndSalesRawExtractioner
from src.connection.utils.condition.tick_history_time_and_sales_condtion import TickHistoryTimeAndSalesCondition
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

        extractioner = TickHistoryTimeAndSalesRawExtractioner(identifier_list=instrument_list,
                                                              times_and_sales_content_field_names=content_field_names,
                                                              condition=condition)

        body = extractioner.get_body()
        target_body = {'ExtractionRequest':
                           {'@odata.type':
                                '#DataScope.Select.Api.Extractions.ExtractionRequests.TickHistoryTimeAndSalesExtractionRequest',
                            'ContentFieldNames': ['Trade - Ask Price',
                                                  'Quote - Bid Price'],
                            'IdentifierList': {
                                '@odata.type':
                                    '#DataScope.Select.Api.Extractions.ExtractionRequests.InstrumentIdentifierList',
                                'InstrumentIdentifiers': [
                                    {'Identifier': 'CLZ24',
                                     'IdentifierType': 'Ric'}
                                ],
                                'ValidationOptions': {'AllowHistoricalInstruments': True},
                                'UseUserPreferencesForValidationOptions': False},
                            'Condition': {'QueryStartDate': '2022-11-21T00:00:00.000Z',
                                          'QueryEndDate': '2022-11-22T00:00:00.000Z',
                                          'MessageTimeStampIn': 'GmtUtc',
                                          'TimeRangeMode': 'Inclusive',
                                          'ReportDateRangeType': 'Range',
                                          'ExtractBy': 'Ric',
                                          'ApplyCorrectionsAndCancellations': True,
                                          'DisplaySourceRIC': True}}
                       }
        # print(body)

        self.assertTrue(body == target_body)
