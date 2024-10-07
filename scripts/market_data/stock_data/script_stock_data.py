import logging
import os
from datetime import datetime
import sys


BASE_DIR = os.path.abspath(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)
sys.path.insert(0, '/home/haobin_cui/option_data_processor')

from connection.features.extraction.enums.content_field_names.tick_history.time_and_sales_content_field_names import \
    TimeAndSalesContentFieldNames
from connection.features.extraction.enums.extraction_base_enums import IdentifierType
from connection.features.extraction.on_demand_extractioner.tick_history_time_and_sales_extractioner import \
    TickHistoryTimeAndSalesRawExtractioner
from connection.utils.condition.condition import TickHistoryTimeOptions
from connection.utils.condition.tick_history_time_and_sales_condtion import TickHistoryTimeAndSalesCondition
from connection.utils.instrument_identifier_list_base.instrument_identifier_list import InstrumentIdentifier, \
    InstrumentIdentifierList

# %% setup a logger:
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')

# ED and FFR: 2020-11-30 -> 2022-12-31, intraday,
# maturity <= 2 year, e.g. 2020-11-30 => 2022-11-30


# query_start_date = datetime(2009, 10, 7, 17, 16, 1)
# query_end_date = datetime(2009, 10, 7, 17, 16, 59)

# 2009-12-16 17:28:21

query_start_date = datetime(2005, 12, 19, 13, 22, 50)
query_end_date = datetime(2009, 12, 19, 13, 22, 51)
# 2005-12-19 14:22:50

identifier_type = IdentifierType.Ric

quote_bid_price = TimeAndSalesContentFieldNames.Quote.BidPrice
quote_bid_size = TimeAndSalesContentFieldNames.Quote.BidSize
quote_ask_price = TimeAndSalesContentFieldNames.Quote.AskPrice
quote_ask_size = TimeAndSalesContentFieldNames.Quote.AskSize

trade_price = TimeAndSalesContentFieldNames.Trade.Price
trade_volume = TimeAndSalesContentFieldNames.Trade.Volume

#
# content_field_names = [quote_ask_price, quote_ask_size,
#                        quote_bid_size, quote_bid_price]

content_field_names = [trade_price, trade_volume]

identifier = 'ALVG.DE'
print('start extracting')

identifier_list = InstrumentIdentifier(identifier=identifier,
                                       identifier_type=identifier_type)

instrument_list = InstrumentIdentifierList(identifier_list=[identifier_list],
                                           preferred_identifier_type=identifier_type)
condition = TickHistoryTimeAndSalesCondition(query_start_date=query_start_date,
                                             query_end_date=query_end_date,
                                             message_time_stamp_in = TickHistoryTimeOptions.LocalExchangeTime)

extractioner = TickHistoryTimeAndSalesRawExtractioner(identifier_list=instrument_list,
                                                      times_and_sales_content_field_names=content_field_names,
                                                      condition=condition)
output_file_name = f'./output/SLB_trade_{query_start_date.isoformat()}_{query_end_date.isoformat()}.csv.gz'
output_file_name = f'./time_zone_example2.csv.gz'
# try:
#     os.makedirs(output_file_name,exist_ok=True)
#
# except:
#     pass
res = extractioner.save_output_file(output_file_name)
print('success!!')


# res = extractioner.get_text_results()
