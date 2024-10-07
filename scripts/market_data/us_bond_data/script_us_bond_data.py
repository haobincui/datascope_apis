import logging
import os
import sys
from datetime import date

BASE_DIR = os.path.abspath(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)
sys.path.insert(0, '/home/haobin_cui/option_data_processor')
# sys.path.insert(0, '/Users/haobincui/Documents/option_data_processor')


from connection.apis.extraction_creator import ExtractionCreator

from connection.features.extraction.enums.content_field_names.tick_history.time_and_sales_content_field_names import \
    TimeAndSalesContentFieldNames
from connection.features.extraction.enums.extraction_base_enums import IdentifierType
from src.multi_thread import ExtractionImp
from src.calendar import plus_period, Period, TimeUnit, EomConvention

# %% setup a logger:
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')

output_path = 'output'

# 0#TY+: 10 year us bond option
# 0#US+: 30 year us bond option

id = '0#TY:'

identifier_type = IdentifierType.ChainRIC
quote_bid_price = TimeAndSalesContentFieldNames.Quote.BidPrice
quote_bid_size = TimeAndSalesContentFieldNames.Quote.BidSize
quote_ask_price = TimeAndSalesContentFieldNames.Quote.AskPrice
quote_ask_size = TimeAndSalesContentFieldNames.Quote.AskSize
quote_ask_vol = TimeAndSalesContentFieldNames.Quote.AskImpliedVolatility
quote_bid_vol = TimeAndSalesContentFieldNames.Quote.BidImpliedVolatility
quote_acc_ask_order = TimeAndSalesContentFieldNames.Quote.AccAskOrder
quote_acc_ask_order_size = TimeAndSalesContentFieldNames.Quote.AccAskOrderSize
quote_acc_bid_order = TimeAndSalesContentFieldNames.Quote.AccBidOrder
quote_acc_bid_order_size = TimeAndSalesContentFieldNames.Quote.AccBidOrderSize

content_field_names = [quote_ask_price, quote_ask_size,
                       quote_bid_size, quote_bid_price]
# quote_acc_ask_order, quote_acc_ask_order_size,
# quote_acc_bid_order, quote_acc_bid_order_size]
#
query_start_date = date(2015, 1, 1)
query_end_date = date(2015, 4, 1)

query_start_dates = [query_start_date]
# query_end_dates = [query_end_date]


while query_start_dates[-1] < query_end_date:
    query_start_dates.append(plus_period(query_start_dates[-1], Period(1, TimeUnit.MONTH), eom=EomConvention.LAST_DAY))
#
if query_start_dates[-1] == query_end_date:
    query_start_dates.remove(query_end_date)
query_end_dates = query_start_dates[1:] + [query_end_date]


total_len = len(query_start_dates)
extractions = []
output_paths = []
cur_ids = []

chunks = total_len
for i in range(0, chunks):
    start = i * 1
    end = (i + 1) * 1
    start_dates = query_start_dates[start: end]
    end_dates = query_end_dates[start: end]
    chunk_extraction = []
    output_path = []
    # start_dates = query_start_dates
    # end_dates = query_end_dates

    for idx in range(len(start_dates)):
        extractioner = ExtractionCreator.time_and_sales(
            id, identifier_type, start_dates[idx], end_dates[idx], content_field_names
        )

        cur_id = id + '_' + start_dates[idx].isoformat() + '_' + end_dates[idx].isoformat()
        cur_ids.append(cur_id)
        chunk_extraction.append(extractioner)
        output_path.append(f'./output/{id}/{start_dates[idx].year}/{cur_id}.csv.gz')
        try:
            os.mkdir(f'./output/{id}/{start_dates[idx].year}/')
        except:
            pass
    extractions.append(chunk_extraction)
    output_paths.append(output_path)

s = 0
n = 0
f = 0
total = chunks
s_list = []
f_list = []

# extractions = extractions[0]
# output_paths = output_paths[0]
for idx in range(len(extractions)):
    print(f'Start downloading data: [{cur_ids[idx]}]')

    threaders = ExtractionImp(extractions[idx])
    try:
        threaders.save_files(output_paths[idx])
        s += 1
        n += 1
        slit = s_list + cur_ids
        print(f'Success: [{s}] , No.: [{n}], Left: [{total - n}], ids: [{cur_ids}]')
    except Exception as e:
        f_list = f_list + cur_ids
        f += 1
        print(f'Fail: [{f}], No.: [{n}], Left: [{total - n}], Message: [{e}], ,ids: [{cur_ids}]')
        continue
print('Finished All')
