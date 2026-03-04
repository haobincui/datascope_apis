
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


# contract_id = contract_ids[0]
contract_id = "ABF.L"
extractioner = ExtractionCreator.time_and_sales(
    contract_id, identifier_type,
    date(2023, 7, 3), date(2023, 7, 13),
    content_fields
)
output_file = "./text.csv.gz"
extractioner.save_output_file(output_file)








