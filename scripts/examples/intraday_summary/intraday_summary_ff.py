### script for FF future trades data

import logging
import os
from datetime import date

from src.calendar import plus_period, Period, TimeUnit, EomConvention
from src.connection.apis import ExtractionCreator
from src.connection.extraction.enums.content_field_names.tick_history.intraday_content_field_names import \
    IntradaySummariesContentFieldNames
from src.connection.extraction.enums.content_field_names.tick_history.time_and_sales_content_field_names import \
    TimeAndSalesContentFieldNames
from src.connection.extraction.enums.extraction_base_enums import IdentifierType
from src.connection.utils.condition.condition import TickHistorySummaryInterval
from src.market_data.output_validator import OutputFileIntegrityValidator

# %% setup a logger:
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')






"""

Extract Intraday summary data for contract FFZ1 (30 DAY FED DEC1) and FFH1 (30 DAY FED MAR1),
for all contracts from 2014-01-01 to 2014-02-01.
"""

contract_ids = ['FFZ4', 'FFH4']
identifier_type = IdentifierType.Ric

summary_interval = TickHistorySummaryInterval.OneMinute


query_start_date = date(2014, 1, 1)
query_end_date = date(2014, 2, 1)

# total_months = (query_end_date.year - query_start_date.year) * 12 + query_end_date.month - query_start_date.month
query_start_dates = [query_start_date]

while query_start_dates[-1] < query_end_date:
    query_start_dates.append(plus_period(query_start_dates[-1], Period(1, TimeUnit.MONTH), eom=EomConvention.LAST_DAY))

if query_start_dates[-1] == query_end_date:
    query_start_dates.remove(query_end_date)

query_end_dates = query_start_dates[1:] + [query_end_date]

# fields for time and sales data, can be customized based on needs
close_ask = IntradaySummariesContentFieldNames.Close.Ask
close_asksize = IntradaySummariesContentFieldNames.Close.AskSize
close_bid = IntradaySummariesContentFieldNames.Close.Bid
close_bidsize = IntradaySummariesContentFieldNames.Close.BidSize

open_ask = IntradaySummariesContentFieldNames.Open.Ask
open_asksize = IntradaySummariesContentFieldNames.Open.AskSize
open_bid = IntradaySummariesContentFieldNames.Open.Bid
open_bidsize = IntradaySummariesContentFieldNames.Open.BidSize

content_field_names = [close_ask, close_asksize,
                       close_bid, close_bidsize
                       ]





extractors = []
output_paths = []
output_ids = []


total = len(query_start_dates)
s = 0
f = 0
f_list = []
s_list = []
n = 0


for contract_id in contract_ids:
    for query_start_date, query_end_date in zip(query_start_dates, query_end_dates):
        extractor = ExtractionCreator.tick_history (
            contract_id,
            identifier_type,
            query_start_date, query_end_date,
            content_field_names,
            summary_interval
        )
        cur_id = contract_id + '_' +  '_' + query_start_date.isoformat()

        output_path = f'./output/{contract_id}/{cur_id}.csv.gz'
        try:
            os.makedirs(f'./output/{contract_id}/', exist_ok=True)
        except:
            pass
        output_ids.append(cur_id)
        extractors.append(extractor)
        output_paths.append(output_path)

logging.info(f'Finished creating all extractions ...')

target_extract_files = OutputFileIntegrityValidator.get_missed_files_list(output_paths)
target_extract_files_set = set(target_extract_files)

logging.info(
    f'Pre-download validation finished. Total target files: [{len(output_paths)}], '
    f'Missing files before download: [{len(target_extract_files_set)}].'
)

if not target_extract_files_set:
    logging.info('All target files already exist. Skip extraction download.')
else:
    for extractor, output_path, output_id in zip(extractors, output_paths, output_ids):
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


