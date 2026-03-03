






import logging
import os
import sys
from datetime import date


from src.calendar.schedule import plus_period, EomConvention, TimeUnit, Period
from src.connection.features.extraction.enums.content_field_names.tick_history.intraday_content_field_names import \
    IntradaySummariesContentFieldNames
from src.connection.utils.condition.condition import TickHistorySummaryInterval
from src.multi_thread.implement.extraction_imp import ExtractionImp

BASE_DIR = os.path.abspath(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)
sys.path.insert(0, '/home/haobin_cui/option_data_processor')
# sys.path.insert(0, '/Users/haobincui/Documents/option_data_processor')


from src.connection.apis.extraction_creator import ExtractionCreator
from src.connection.features.extraction.enums.extraction_base_enums import IdentifierType



# %% setup a logger:
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')

output_path = 'ff_output'

"""
Instruction:
# 30 Day Federal Funds (FF rate)
# 0#FF:
2000-01-01 to 2025-11-01
"""

## target contracts:
identifier_type = IdentifierType.ChainRIC
# contract_ids = pd.read_csv('./input/ftse100_sample_request_ranges 251107.csv')["RIC"].tolist()
contract_id = "0#FF:"



## required fields:

close_ask_price = IntradaySummariesContentFieldNames.Close.Ask
close_ask_size = IntradaySummariesContentFieldNames.Close.AskSize
close_bid_price = IntradaySummariesContentFieldNames.Close.Bid
close_bid_size = IntradaySummariesContentFieldNames.Close.BidSize
close_mid_price = IntradaySummariesContentFieldNames.Close.MidPrice



content_fields = [close_ask_size, close_ask_price, close_bid_price, close_bid_size, close_mid_price]


### target date:
query_start_date = date(2000, 1, 1)
query_end_date = date(2025, 11, 1)

query_start_dates = [query_start_date]
# query_end_dates = [query_end_date]

while query_start_dates[-1] < query_end_date:
    query_start_dates.append(plus_period(query_start_dates[-1], Period(1, TimeUnit.MONTH), eom=EomConvention.LAST_DAY))
#
if query_start_dates[-1] == query_end_date:
    query_start_dates.remove(query_end_date)
query_end_dates = query_start_dates[1:] + [query_end_date]


i = 0
extractions = []
output_paths = []
output_ids = []

for idx in range(len(query_start_dates)):
    extractioner = ExtractionCreator.tick_history(
        contract_id, identifier_type,
        query_start_dates[idx], query_end_dates[idx],
        content_fields,
        summary_interval=TickHistorySummaryInterval.OneHour
    )
    cur_id = contract_id.split(".")[0] + '_' + query_start_dates[idx].isoformat()
    cur_id = cur_id.replace(':', '').replace('.', '')
    output_path = f'./ff_output/{cur_id}.csv.gz'
    try:
        os.makedirs(f'./ff_output', exist_ok=True)
    except:
        pass
    output_ids.append(cur_id)
    extractions.append(extractioner)
    output_paths.append(output_path)
logging.info(f'Finished creating all extractions ...')



chunk_size = 10
total_extractions = len(extractions)
total_chunks = total_extractions // chunk_size + 1

n = 0
s = 0
f = 0
s_list = []
f_list = []

total = len(extractions)
for idx in range(len(extractions)):
    start = idx * chunk_size
    end = (idx + 1) * chunk_size
    logging.info(f'Start downloading data, No. [{n}]')

    cur_chunk_extractions = extractions[start: end]
    cur_output = output_paths[start: end]
    cur_ids = output_ids[start: end]
    cur_len = len(cur_chunk_extractions)
    threaders = ExtractionImp(cur_chunk_extractions)

    try:
        threaders.save_files(cur_output)
        s += cur_len
        s_list += cur_ids
        # s_list.append(*cur_ids)
        n += s
        logging.info(f'Success: [{n}], Left: [{total - n}] ...')
    except Exception as e:
        f += cur_len
        # f_list.append(*cur_ids)
        f_list += cur_ids
        logging.info(f'Fail: [{f}], No.: [{n}], Left: [{total - n}], Message: [{e}]')
        logging.info(f'Message: [{e}] ...')
        continue
logging.info(f'Finished All, Total: [{total}], Success: [{s}], Fail: [{f}]')
logging.info(f'failed ids: [{f_list}], success ids: [{s_list}]')
print('Finished All')









# query_start_dates = [query_start_date]
# # query_end_dates = [query_end_date]
#
# while query_start_dates[-1] < query_end_date:
#     query_start_dates.append(plus_period(query_start_dates[-1], Period(1, TimeUnit.MONTH), eom=EomConvention.LAST_DAY))
# #
# if query_start_dates[-1] == query_end_date:
#     query_start_dates.remove(query_end_date)
# query_end_dates = query_start_dates[1:] + [query_end_date]

# extractions = []
# output_paths = []
# output_ids = []
#
#
# # contract_id = contract_ids[0]
# contract_id = "ABF.L"
# extractioner = ExtractionCreator.time_and_sales(
#     contract_id, identifier_type,
#     date(2023, 7, 3), date(2023, 7, 13),
#     content_fields
# )
# output_file = "./text.csv.gz"
# extractioner.save_output_file(output_file)








