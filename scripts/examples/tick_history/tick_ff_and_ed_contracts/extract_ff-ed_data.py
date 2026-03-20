### script for FF future trades data

import logging
import os
from datetime import date

from src.calendar import plus_period, Period, TimeUnit, EomConvention
from src.connection.apis import ExtractionCreator
from src.connection.extraction.enums.content_field_names.tick_history.time_and_sales_content_field_names import \
    TimeAndSalesContentFieldNames
from src.connection.extraction.enums.extraction_base_enums import IdentifierType
from src.market_data.output_validator import OutputFileIntegrityValidator

# %% setup a logger:
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')






"""

Extract Fed Fund Future and Eurodollar Future (SOFR Future) quote and trade tick data,
for all contracts from 2014-01-01 to 2014-02-01.
"""
chain_contract_id_ff = '0#FF:'
chain_contract_id_ed = '0#SRA:'

contract_ids = [chain_contract_id_ff, chain_contract_id_ed]


# Example: For 3 Month SOFR Futures its RIC is SRA, for its Future Outright chain its 0#SRA:
# for its Futures spread chain its 0#SRA-:,
# for its futures butterfly chain its 0#SRABF-:
# similarly for condor chain its 0#SRACF-:.


identifier_type = IdentifierType.ChainRIC

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
# quote
quote_bid_price = TimeAndSalesContentFieldNames.Quote.BidPrice
quote_bid_size = TimeAndSalesContentFieldNames.Quote.BidSize
quote_ask_price = TimeAndSalesContentFieldNames.Quote.AskPrice
quote_ask_size = TimeAndSalesContentFieldNames.Quote.AskSize

quote_field = [quote_ask_price, quote_ask_size,quote_bid_size, quote_bid_price]

# trade
trade_volume = TimeAndSalesContentFieldNames.Trade.Volume
trade_price = TimeAndSalesContentFieldNames.Trade.Price

trade_field = [trade_price, trade_volume]



content_field_dict = {
    'quote': quote_field,
    'trade': trade_field
}


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


