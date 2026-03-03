
import logging
import os
import sys
from datetime import date

import pandas as pd

from src.calendar.schedule import plus_period, EomConvention, TimeUnit, Period
from src.multi_thread.implement.extraction_imp import ExtractionImp

BASE_DIR = os.path.abspath(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)
sys.path.insert(0, '/home/haobin_cui/option_data_processor')
# sys.path.insert(0, '/Users/haobincui/Documents/option_data_processor')


from src.connection.apis.extraction_creator import ExtractionCreator

from src.connection.features.extraction.enums.content_field_names.tick_history.time_and_sales_content_field_names import \
    TimeAndSalesContentFieldNames
from src.connection.features.extraction.enums.extraction_base_enums import IdentifierType



# %% setup a logger:
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')

output_path = 'output'

"""
Instruction:
trade data from 20230701 to 20250701.
"""

## target contracts:
identifier_type = IdentifierType.Ric
contract_ids = pd.read_csv('./input/ftse100_sample_request_ranges 251107.csv')["RIC"].tolist()




## required fields:
### Trade data:
trade_price = TimeAndSalesContentFieldNames.Trade.Price
trade_size = TimeAndSalesContentFieldNames.Trade.Volume
trade_turnover = TimeAndSalesContentFieldNames.Trade.Turnover

trade_fields = [trade_price, trade_size]
content_fields = trade_fields

### target date:
query_start_date = date(2023, 7, 1)
query_end_date = date(2025, 7, 1)

query_start_dates = [query_start_date]
# query_end_dates = [query_end_date]

while query_start_dates[-1] < query_end_date:
    query_start_dates.append(plus_period(query_start_dates[-1], Period(1, TimeUnit.MONTH), eom=EomConvention.LAST_DAY))
#
if query_start_dates[-1] == query_end_date:
    query_start_dates.remove(query_end_date)
query_end_dates = query_start_dates[1:] + [query_end_date]

extractions = []
output_paths = []
output_ids = []


for contract_id in contract_ids:
    for idx in range(len(query_start_dates)):
        extractioner = ExtractionCreator.time_and_sales(
            contract_id, identifier_type,
            query_start_dates[idx], query_end_dates[idx],
            content_fields
        )
        cur_id = contract_id.split(".")[0] +  '_' + query_start_dates[idx].isoformat()
        cur_id = cur_id.replace(':', '').replace('.', '')
        output_path = f'./output/{contract_id.split(".")[0]}/{cur_id}.csv.gz'
        try:
            os.makedirs(f'./output/{contract_id.split(".")[0]}/', exist_ok=True)
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



