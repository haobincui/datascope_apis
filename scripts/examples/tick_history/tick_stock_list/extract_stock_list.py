import logging
import os
import sys
from datetime import date
import pandas as pd

from src.calendar.schedule import plus_period, EomConvention, TimeUnit, Period
from src.market_data.output_validator import OutputFileIntegrityValidator

BASE_DIR = os.path.abspath(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)
# sys.path.insert(0, '/home/haobin_cui/da')
# sys.path.insert(0, '/Users/haobincui/Documents/option_data_processor')


from src.connection.apis.extraction_creator import ExtractionCreator

from src.connection.extraction.enums.content_field_names.tick_history.time_and_sales_content_field_names import \
    TimeAndSalesContentFieldNames
from src.connection.extraction.enums.extraction_base_enums import IdentifierType



# setup a logger:
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')

output_path = 'output'

"""
Instruction:
tick data.
# 1 July 2023–30 June 2025
# target_ricks = ricks.xlsx
"""

## target contracts:
identifier_type = IdentifierType.Ric
contract_ids = pd.read_excel('./ricks.xlsx')['RIC'].tolist()


## required fields:
### Quote data:
# quote_bid_price = TimeAndSalesContentFieldNames.Quote.BidPrice
# quote_bid_size = TimeAndSalesContentFieldNames.Quote.BidSize
# quote_bid_acc_size = TimeAndSalesContentFieldNames.Quote.AccBidOrderSize
# quote_ask_price = TimeAndSalesContentFieldNames.Quote.AskPrice
# quote_ask_size = TimeAndSalesContentFieldNames.Quote.AskSize
# quote_acc_ask_size = TimeAndSalesContentFieldNames.Quote.AccAskOrderSize

# quote_fields = [quote_ask_price, quote_ask_size, quote_bid_size, quote_bid_price]

### Trade data:
trade_price = TimeAndSalesContentFieldNames.Trade.Price
trade_size = TimeAndSalesContentFieldNames.Trade.Volume
trade_turnover = TimeAndSalesContentFieldNames.Trade.Turnover

trade_fields = [trade_price, trade_size, trade_turnover]

### dict of fields:
content_field_dict = {
    # 'quote': quote_fields,
    'trade': trade_fields
}

### target date:
# 1 July 2023–30 June 2025
query_start_date = date(2023, 7, 1)
query_end_date = date(2025, 6, 30)


query_start_dates = [query_start_date]
while query_start_dates[-1] < query_end_date:
    query_start_dates.append(plus_period(query_start_dates[-1], Period(1, TimeUnit.MONTH), eom=EomConvention.LAST_DAY))
#
if query_start_dates[-1] == query_end_date:
    query_start_dates.remove(query_end_date)
query_end_dates = query_start_dates[1:] + [query_end_date]



extractors = []
output_paths = []
output_ids = []


total = len(query_start_dates)
s = 0
f = 0
f_list = []
s_list = []
n = 0

for data_type in content_field_dict.keys():
    for contract_id in contract_ids:
        for query_start_date, query_end_date in zip(query_start_dates, query_end_dates):
            extractor = ExtractionCreator.time_and_sales(
                contract_id, identifier_type,
                query_start_date, query_end_date,
                content_field_dict[data_type]
            )
            cur_id = contract_id + '_' + data_type + '_' + query_start_date.isoformat()

            output_path = f'./output/{data_type}/{contract_id}/{cur_id}.csv.gz'
            try:
                os.makedirs(f'./output/{data_type}/{contract_id}/', exist_ok=True)
            except:
                pass
            output_ids.append(cur_id)
            extractors.append(extractor)
            output_paths.append(output_path)
    logging.info(f'Finished creating [{data_type}] extractions ...')
logging.info(f'Finished creating all extractions ...')

target_extract_files = OutputFileIntegrityValidator.get_missed_files_list(output_paths)
target_extract_files_set = set(target_extract_files)


logging.info(
    f'Pre-download validation finished. Total target files: [{len(output_paths)}], '
    f'Missing files before download: [{len(target_extract_files_set)}].'
)

s = 0
f = 0
s_list = []
f_list = []

if not target_extract_files_set:
    logging.info('All target files already exist. Skip extraction download.')
else:
    for extractor, output_path, output_id in zip(extractions, output_paths, output_ids):
        normalized_output_path = os.path.abspath(output_path)
        if normalized_output_path not in target_extract_files_set:
            continue

        try:
            extractor.save_output_file(output_path)
            logging.info(f'Finished extraction [{output_id}] successfully!')
            s += 1
            s_list.append(output_id)
        except Exception as e:
            logging.error(f'Extraction [{output_id}] failed with error: {e}')
            f += 1
            f_list.append(output_id)

missed_files = OutputFileIntegrityValidator.get_missed_files_list(output_paths)

logging.info(
    f'Post-download validation finished. Total target files: [{len(output_paths)}], '
    f'Missing files after download: [{len(missed_files)}].'
)

if missed_files:
    logging.warning(f'Missing files after download (show first 20): [{missed_files[:20]}]')
else:
    logging.info('All target files passed post-download validation.')

logging.info(f'Finished All, Success: [{s}], Fail: [{f}]')
logging.info(f'failed ids: [{f_list}], success ids: [{s_list}]')
print('Finished All')

