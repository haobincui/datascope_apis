import glob
import logging
import os
import sys
from datetime import date

from src.calendar.schedule import plus_period, Period, TimeUnit, EomConvention

BASE_DIR = os.path.abspath(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)
sys.path.insert(0, '/home/haobin_cui/option_data_processor')
# sys.path.insert(0, '/Users/haobincui/Documents/option_data_processor')


# from src.quantlib.calendar.schedule import plus_period, Period, TimeUnit, EomConvention

# %% setup a logger:
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')

contract_ids = ['ESc1', 'CLc1', 'GCc1', 'BTCc1', 'TYc1']

contents = ["Quote", "Trade"]

### target date:
query_start_date = date(2019, 1, 1)
query_end_date = date(2024, 10, 1)

query_start_dates = [query_start_date]
# query_end_dates = [query_end_date]

while query_start_dates[-1] < query_end_date:
    query_start_dates.append(plus_period(query_start_dates[-1], Period(1, TimeUnit.MONTH), eom=EomConvention.LAST_DAY))
#
if query_start_dates[-1] == query_end_date:
    query_start_dates.remove(query_end_date)
query_end_dates = query_start_dates[1:] + [query_end_date]

target_files = []
for content in contents:
    for contract_id in contract_ids:
        for idx in range(len(query_start_dates)):
            cur_file = BASE_DIR + '/output/' + content + '/' + contract_id + '/' + contract_id + '_' + content + '_' + \
                       query_start_dates[idx].isoformat() + '.csv.gz'
            target_files.append(cur_file)

all_downloaded_files = []
for content in contents:
    for contract_id in contract_ids:
        path = os.path.join(f'{BASE_DIR}/output/{content}/{contract_id}', '*.csv.gz')
        downloaded_files = glob.glob(path)
        all_downloaded_files.extend(downloaded_files)

for all_downloaded_file in all_downloaded_files:
    if os.path.getsize(all_downloaded_file) < 70:
        logging.info(f'File [{all_downloaded_file}] has low file size!')

missing_files = set(target_files) - set(all_downloaded_files)
total_target = len(target_files)
total_downloaded = len(all_downloaded_files)
no_missing = len(missing_files)

logging.info("Finished Validation!")
logging.info(
    f"Total Target files: [{total_target}]; Total Downloaded files: [{total_downloaded}]; Total Missing files: [{no_missing}].")







