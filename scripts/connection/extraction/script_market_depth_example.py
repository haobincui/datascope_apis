import logging
import time
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

# %% setup a logger:
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')

# %% example for market depth  for CLZ24

# % ids:
identifier = 'CLZ24'
identifier_type = IdentifierType.Ric

# %% dates (%Y, %M, %D, %h, %s, %ms):
query_start_date = datetime(2022, 10, 17, 0, 0, 0)
query_end_date = datetime(2022, 10, 20, 0, 0, 0)

bid_price = MarketDepthContentFieldNames.BidPrice
ask_price = MarketDepthContentFieldNames.AskPrice
num_of_buyer = MarketDepthContentFieldNames.NumberOfBuyers
num_of_seller = MarketDepthContentFieldNames.NumberOfSellers
bid_size = MarketDepthContentFieldNames.BidSize
ask_size = MarketDepthContentFieldNames.AskSize
exchange_time = MarketDepthContentFieldNames.ExchangeTime

# %% content filed names here:
content_field_names = [bid_price,
                       # bid_size,
                       # ask_price,
                       # ask_size,
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

condition = TickHistoryMarketDepthCondition(query_start_date=query_start_date,
                                            query_end_date=query_end_date,
                                            view=view,
                                            number_of_levels=nums_of_levels)

# %% create the extraction report obj:
extractioner = TickHistoryMarketDepthExtractioner(instrument_list, content_field_names, condition)

logging.info('Created extractioner')

# %% save file:

# output_file_name = f'./output_docs/{identifier}_{view.value}_{nums_of_levels}_{query_start_date.isoformat()}.csv.gz'
output_file_name = './output_docs/market_depth_testclz4.csv.gz'
logging.info('start downloading merged_output file')
s = time.time()
extractioner.save_output_file(output_file_name)
e = time.time()
print(f'Save success, use {e - s}s')
