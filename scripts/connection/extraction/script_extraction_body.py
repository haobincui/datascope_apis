from datetime import datetime

from connection.features.extraction.enums.extraction_base_enums import IdentifierType
from connection.features.extraction.on_demand_extractioner.tick_history_market_depth_extractioner import \
    TickHistoryMarketDepthExtractioner
from connection.features.extraction.enums.content_field_names.tick_history.market_depth_content_field_name import \
    MarketDepthContentFieldNames
from connection.utils.condition.tick_history_market_depth_condition import TickHistoryMarketDepthCondition, \
    TickHistoryMarketDepthViewOptions
from connection.utils.instrument_identifier_list_base.instrument_identifier_list import InstrumentIdentifierList, \
    InstrumentIdentifier

# %% example for market depth  for CLZ24

# % ids:
identifier = 'CLZ24'
identifier_type = IdentifierType.Ric

# %% dates (%Y, %M, %D, %h, %s, %ms):
query_start_date = datetime(2023, 1, 21, 12, 0, 0)
query_end_date = datetime(2023, 2, 21, 12, 0, 0)

bid_price = MarketDepthContentFieldNames.BidPrice
ask_price = MarketDepthContentFieldNames.AskPrice
num_of_buyer = MarketDepthContentFieldNames.NumberOfBuyers
num_of_seller = MarketDepthContentFieldNames.NumberOfSellers
bid_size = MarketDepthContentFieldNames.BidSize
ask_size = MarketDepthContentFieldNames.AskSize
exchange_time = MarketDepthContentFieldNames.ExchangeTime

# %% content filed names here:
content_field_names = [
    # bid_price,
    # bid_size,
    ask_price,
    ask_size,
    # num_of_buyer,
    # num_of_seller,
    # exchange_time
]

# %% data view conditions :
nums_of_levels = 2
view = TickHistoryMarketDepthViewOptions.NormalizedLL2

# %% ignore:
identifier_list = InstrumentIdentifier(identifier=identifier,
                                       identifier_type=identifier_type)

instrument_list = InstrumentIdentifierList(identifier_list=[identifier_list],
                                           preferred_identifier_type=identifier_type)

condition = TickHistoryMarketDepthCondition(query_start_date,
                                            query_end_date,
                                            view=view,
                                            number_of_levels=nums_of_levels)

# %% create the extraction report obj:
extractioner = TickHistoryMarketDepthExtractioner(instrument_list, content_field_names, condition)

# %% body:
# body = extractioner.get_body()
# body = {
#     'ExtractionRequest':
#             {
#                 '@odata.type': '#DataScope.Select.Api.Extractions.ExtractionRequests.TickHistoryMarketDepthExtractionRequest',
#                 'MarketDepthContentFieldNames':
#                     [
#                         'Bid Price',
#                         'Bid Size',
#                         'Ask Price',
#                         'Ask Size',
#                         'Number of Buyers',
#                         'Number of Sellers',
#                         'Exchange Time'
#                     ],
#                 'IdentifierList':
#                     {
#                         '@odata.type': '#DataScope.Select.Api.Extractions.ExtractionRequests.InstrumentIdentifierList',
#                         'InstrumentIdentifiers':
#                             [
#                                 {
#                                     'Identifier': 'CLZ24',
#                                     'IdentifierType': 'Ric'
#                                 }
#                             ],
#                         'ValidationOptions': None,
#                         'UseUserPreferencesForValidationOptions': True
#                     },
#                 'Condition':
#                     {
#                         'DisplaySourceRIC': True,
#                         'ExtractBy': 'Ric',
#                         'MessageTimeStampIn': 'GmtUtc',
#                         'NumberOfLevels': 10,
#                         'QueryEndDate': '2022-11-22T00:00:00.000Z',
#                         'QueryStartDate': '2022-11-21T00:00:00.000Z',
#                         'ReportDateRangeType': 'Range',
#                         'SortBy': 'SingleByRic',
#                         'View': 'NormalizedLL2'
#                     }
#             }
# }

body = {'ExtractionRequest':
            {'@odata.type': '#DataScope.Select.Api.Extractions.ExtractionRequests.TickHistoryMarketDepthExtractionRequest',
             'ContentFieldNames': ['Ask Price',
                                   'Ask Size'],
             'IdentifierList':
                 {'@odata.type': '#DataScope.Select.Api.Extractions.ExtractionRequests.InstrumentIdentifierList',
                  'InstrumentIdentifiers':
                      [{'Identifier': 'CLZ24', 'IdentifierType': 'Ric'}],
                  'ValidationOptions': {'AllowHistoricalInstruments': True},
                  'UseUserPreferencesForValidationOptions': False},
             'Condition': {'QueryEndDate': '2023-02-21T12:00:00.000Z',
                           'QueryStartDate': '2023-01-21T12:00:00.000Z',
                           'NumberOfLevels': 2,
                           'View': 'NormalizedLL2',
                           'DisplaySourceRIC': True,
                           'ExtractBy': 'Ric',
                           'MessageTimeStampIn': 'GmtUtc',
                           'ReportDateRangeType': 'Range',
                           'SortBy': 'SingleByRic'}
             }
        }

