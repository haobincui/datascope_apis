import glob
import logging
import os
from datetime import date

import pandas as pd

from src.calendar.schedule import plus_period, Period, TimeUnit, EomConvention
from src.connection.apis.extraction_creator import ExtractionCreator
from src.connection.features.extraction.enums.content_field_names.tick_history.intraday_content_field_names import \
    IntradaySummariesContentFieldNames
from src.connection.features.extraction.enums.content_field_names.tick_history.time_and_sales_content_field_names import \
    TimeAndSalesContentFieldNames
from src.connection.features.extraction.enums.extraction_base_enums import IdentifierType
from src.connection.utils.condition.condition import TickHistorySummaryInterval
from src.multi_thread.implement.extraction_imp import ExtractionImp

# %% setup a logger:
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')

"""
11 years (or as close to 11 years as possible) of 5-minute data for the following markets:

.N225
.GSPTSE
.STOXX50E
.GDAXI
.FTSE
.AXJO
EURUSD=
EURGBP=
AUDUSD=
USDCAD=
USDJPY=
ESc1
NQc1


Ouput:
'./output_baback/ALVG.DE_2005-10-31T09:52:15.csv.gz'
'./ff_output/failed_extractions.csv'
"""

current_folders = glob.glob("output_baback/*")
current_files = []
for folder in current_folders:
    file = glob.glob(f"{folder}/*.csv.gz")
    if file:
        current_files.extend(file)


## rics:
rics = [
    ".N225",
    ".GSPTSE",
    ".STOXX50E",
    ".GDAXI",
    ".FTSE",
    ".AXJO",
    "EURUSD=",
    "EURGBP=",
    "AUDUSD=",
    "USDCAD=",
    "USDJPY=",
    "ESc1",
    "NQc1",
]

## required fields:

### Quote data:
close_ask = IntradaySummariesContentFieldNames.Close.Ask
close_asksize = IntradaySummariesContentFieldNames.Close.AskSize
close_bid = IntradaySummariesContentFieldNames.Close.Bid
close_bidsize = IntradaySummariesContentFieldNames.Close.BidSize
close_mid = IntradaySummariesContentFieldNames.Close.MidPrice

open_ask = IntradaySummariesContentFieldNames.Open.Ask
open_asksize = IntradaySummariesContentFieldNames.Open.AskSize
open_bid = IntradaySummariesContentFieldNames.Open.Bid
open_bidsize = IntradaySummariesContentFieldNames.Open.BidSize
open_mid = IntradaySummariesContentFieldNames.Open.MidPrice

last = IntradaySummariesContentFieldNames.Last.Last

high_ask = IntradaySummariesContentFieldNames.High.Ask
high_asksize = IntradaySummariesContentFieldNames.High.AskSize
high_bid = IntradaySummariesContentFieldNames.High.Bid
high_bidsize = IntradaySummariesContentFieldNames.High.BidSize
high_mid = IntradaySummariesContentFieldNames.High.MidPrice

low_ask = IntradaySummariesContentFieldNames.Low.Ask
low_asksize = IntradaySummariesContentFieldNames.Low.AskSize
low_bid = IntradaySummariesContentFieldNames.Low.Bid
low_bidsize = IntradaySummariesContentFieldNames.Low.BidSize
low_mid = IntradaySummariesContentFieldNames.Low.MidPrice

volume = IntradaySummariesContentFieldNames.Volume.Volume

## current content
"""
Change the content here to extract different data 
"""

contents = [
    close_ask, close_asksize, close_bid, close_bidsize, close_mid,
            open_ask, open_asksize, open_bid, open_bidsize, open_mid,
            last,
            high_ask, high_asksize, high_bid, high_bidsize, high_mid,
            low_ask, low_asksize, low_bid, low_bidsize, low_mid,
            volume
]

# ff_output dir
output_path = 'output_baback'

n = 0
s = 0
f = 0
f_list = []
total = len(rics)

query_start_date = date(2010, 1, 1)
query_end_date = date(2025, 7, 1)


query_start_dates = [query_start_date]
# query_end_dates = [query_end_date]

while query_start_dates[-1] < query_end_date:
    query_start_dates.append(plus_period(query_start_dates[-1], Period(1, TimeUnit.YEAR), eom=EomConvention.LAST_DAY))
#
if query_start_dates[-1] == query_end_date:
    query_start_dates.remove(query_end_date)
query_end_dates = query_start_dates[1:] + [query_end_date]






# query_start_date = start_date
# query_start_dates = []
# while query_start_date < end_date:
#     query_start_date = query_start_date.replace(year=query_start_date.year + 1)
#     query_start_dates.append(query_start_date)
#


logging.info(f'Starting extraction for {total} RICs from {query_start_dates[0]} to {query_end_dates[-1]}')

extractions = []
output_paths = []
output_ids = []

i = 0
for ric in rics:
    for start_date, end_date in zip(query_start_dates, query_end_dates):
        new_ric = ric.replace(".", "")
        output_file = f'{output_path}/{new_ric}/{new_ric}_{start_date.isoformat()}_{end_date.isoformat()}.csv.gz'
        # Check if the file already exists
        if output_file in current_files:
            logging.info(f'File already exists: {output_file}')
            continue
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        extractioner = ExtractionCreator.tick_history(contract_id=ric,
                                                      identifier_type=IdentifierType.Ric,
                                                      query_start_date=start_date,
                                                      query_end_date=end_date,
                                                      content_field_names=contents,
                                                      summary_interval=TickHistorySummaryInterval.FiveMinutes)


        extractions.append(extractioner)
        output_paths.append(output_file)
        output_ids.append(i)
        i += 1

total = len(extractions)
print(f'Total extractions to process: {total}')

logging.info(f'Finished creating all extractions ...')

chunk_size = 20
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
        s_list.append(cur_ids)
        n += s
        logging.info(f'Success: [{n}], Left: [{total - n}] ...')
    except Exception as e:
        f += cur_len
        f_list.append(cur_ids)
        logging.info(f'Fail: [{f}], No.: [{n}], Left: [{total - n}], Message: [{e}]')
        logging.info(f'Message: [{e}] ...')
        continue



        # try:
        #     extractioner.save_output_file(output_file)
        #     n += 1
        #     s += 1
        #     print(
        #         f'✅ No. {n} of {total}, Success {s}, Extraction for {ric} from {start_date} to {end_date} saved to {output_file}')
        # except Exception as e:
        #     n += 1
        #     f += 1
        #     f_list.append({
        #         'contract_id': ric,
        #         'query_start_date': start_date,
        #         'query_end_date': end_date,
        #         'error': str(e)
        #     })
        #     print(
        #         f'❌No. {n} of {total},Fail {f}, Extraction for {ric} from {start_date} to {end_date} failed: {e}')
        #     continue

pd.DataFrame(f_list).to_csv(f"{output_path}/failed_extractions.csv", index=False)
print(f'Finished processing all extractions, Total: {total}, Success: {s}, Fail: {f}')



