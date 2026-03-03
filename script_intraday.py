
import logging
import os
from datetime import date

import pandas as pd

from src.connection.apis.extraction_creator import ExtractionCreator
from src.connection.features.extraction.enums.content_field_names.tick_history.intraday_content_field_names import \
    IntradaySummariesContentFieldNames
from src.connection.features.extraction.enums.content_field_names.tick_history.time_and_sales_content_field_names import \
    TimeAndSalesContentFieldNames
from src.connection.features.extraction.enums.extraction_base_enums import IdentifierType
from src.connection.utils.condition.condition import TickHistorySummaryInterval

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

start_date = date(2010, 1, 1)
end_date = date(2010, 2, 1)




# query_start_date = start_date
# query_start_dates = []
# while query_start_date < end_date:
#     query_start_date = query_start_date.replace(year=query_start_date.year + 1)
#     query_start_dates.append(query_start_date)
#



logging.info(f'Starting extraction for {total} RICs from {start_date} to {end_date}')

for ric in rics:
    output_file = f'{output_path}/{ric.replace(".","")}_{start_date.isoformat()}_{end_date.isoformat()}.csv.gz'
    # Check if the file already exists
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    extractioner = ExtractionCreator.tick_history(contract_id=ric,
                                                  identifier_type=IdentifierType.Ric,
                                                  query_start_date=start_date,
                                                  query_end_date=end_date,
                                                  content_field_names=contents,
                                                  summary_interval=TickHistorySummaryInterval.FiveMinutes)
    try:
        extractioner.save_output_file(output_file)
        n += 1
        s += 1
        print(f'✅ No. {n} of {total}, Success {s}, Extraction for {ric} from {start_date} to {end_date} saved to {output_file}')
    except Exception as e:
        n += 1
        f += 1
        f_list.append({
            'contract_id': ric,
            'query_start_date': start_date,
            'query_end_date': end_date,
            'error': str(e)
        })
        print(
            f'❌No. {n} of {total},Fail {f}, Extraction for {ric} from {start_date} to {end_date} failed: {e}')
        continue

pd.DataFrame(f_list).to_csv(f"{output_path}/failed_extractions.csv", index=False)
print(f'Finished processing all extractions, Total: {total}, Success: {s}, Fail: {f}')



