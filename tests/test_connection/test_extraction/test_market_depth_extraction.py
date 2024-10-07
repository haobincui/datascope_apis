import unittest
from datetime import datetime

from src.connection.features.extraction.enums.content_field_names.tick_history.market_depth_content_field_name import \
    MarketDepthContentFieldNames
from src.connection.features.extraction.enums.extraction_base_enums import IdentifierType
from src.connection.features.extraction.on_demand_extractioner.tick_history_market_depth_extractioner import \
    TickHistoryMarketDepthExtractioner
from src.connection.utils.condition.tick_history_market_depth_condition import TickHistoryMarketDepthCondition
from src.connection.utils.instrument_identifier_list_base.instrument_identifier_list import InstrumentIdentifier, \
    InstrumentIdentifierList


class TestMarketDepthExtraction(unittest.TestCase):
    def test_market_depth_extraction_body(self):
        identifier = 'CLZ24'
        identifier_type = IdentifierType.Ric

        query_start_date = datetime(2022, 11, 21, 0, 0, 0)
        query_end_date = datetime(2022, 11, 22, 0, 0, 0)

        bid_price = MarketDepthContentFieldNames.BidPrice
        ask_price = MarketDepthContentFieldNames.AskPrice
        num_of_buyer = MarketDepthContentFieldNames.NumberOfBuyers
        num_of_seller = MarketDepthContentFieldNames.NumberOfSellers
        bid_size = MarketDepthContentFieldNames.BidSize
        ask_size = MarketDepthContentFieldNames.AskSize
        exchange_time = MarketDepthContentFieldNames.ExchangeTime
        content_field_names = [bid_price, bid_size, ask_price, ask_size,
                               num_of_buyer, num_of_seller, exchange_time]

        nums_of_levels = 10

        identifier_list = InstrumentIdentifier(identifier=identifier,
                                               identifier_type=identifier_type)

        instrument_list = InstrumentIdentifierList(identifier_list=[identifier_list],
                                                   preferred_identifier_type=identifier_type)

        condition = TickHistoryMarketDepthCondition(query_start_date,
                                                    query_end_date,
                                                    number_of_levels=nums_of_levels)
        extractioner = TickHistoryMarketDepthExtractioner(instrument_list, content_field_names, condition)

        body = extractioner.get_body()
        target_body = {
            'ExtractionRequest':
                {
                    '@odata.type':
                        '#DataScope.Select.Api.Extractions.ExtractionRequests.TickHistoryMarketDepthExtractionRequest',
                    'ContentFieldNames':
                        [
                            'Bid Price',
                            'Bid Size',
                            'Ask Price',
                            'Ask Size',
                            'Number of Buyers',
                            'Number of Sellers',
                            'Exchange Time'
                        ],
                    'IdentifierList':
                        {
                            '@odata.type':
                                '#DataScope.Select.Api.Extractions.ExtractionRequests.InstrumentIdentifierList',
                            'InstrumentIdentifiers':
                                [
                                    {'Identifier': 'CLZ24',
                                     'IdentifierType': 'Ric'}
                                ],
                            'ValidationOptions': {'AllowHistoricalInstruments': True},
                            'UseUserPreferencesForValidationOptions': False
                        },
                    'Condition':
                        {
                            'QueryEndDate': '2022-11-22T00:00:00.000Z',
                            'QueryStartDate': '2022-11-21T00:00:00.000Z',
                            'NumberOfLevels': 10,
                            'View': 'NormalizedLL2',
                            'DisplaySourceRIC': True,
                            'ExtractBy': 'Ric',
                            'MessageTimeStampIn': 'GmtUtc',
                            'ReportDateRangeType': 'Range',
                            'SortBy': 'SingleByRic'
                        }
                }
        }
        # print(body)

        self.assertTrue(target_body == body)
