### script for FF future trades data

import logging
import os
from datetime import date

from connection.features.extraction.enums.content_field_names.tick_history.time_and_sales_content_field_names import \
    TimeAndSalesContentFieldNames
from connection.features.extraction.enums.extraction_base_enums import IdentifierType
from connection.features.extraction.on_demand_extractioner.tick_history_time_and_sales_extractioner import \
    TickHistoryTimeAndSalesRawExtractioner
from connection.utils.condition.tick_history_time_and_sales_condtion import TickHistoryTimeAndSalesCondition
from connection.utils.instrument_identifier_list_base.instrument_identifier_list import InstrumentIdentifier, \
    InstrumentIdentifierList
from src.multi_thread import ExtractionImp
from src.calendar import plus_period, Period, TimeUnit, EomConvention

# %% setup a logger:
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')


contract_id = 'CL'

numbers = [int(i) for i in range(0, 10)]
month_keys = {"F": "Jan",
              "G": "Feb",
              "H": "Mar",
              "J": "Apr",
              "K": "May",
              "M": "Jun",
              "N": "Jul",
              "Q": "Aug",
              "U": "Sep",
              "V": "Oct",
              "X": "Nov",
              "Z": "Dec"
              }
months = [i for i in month_keys.keys()]

identifiers_group1 = []
identifiers_group2 = []
identifiers_group3 = []
temp_identifiers_groups = [identifiers_group1, identifiers_group2, identifiers_group3]
for n in numbers:
    for month in months:
        identifiers_group1.append('CL' + month + str(n))
        identifiers_group2.append('CL' + month + '2' + str(n))
        identifiers_group3.append('CL' + month + '3' + str(n))

identifiers_groups = []

for id in temp_identifiers_groups:
    group_1 = []
    group_2 = []
    group_3 = []

    for idx, ele in enumerate(id):

        if 0 <= idx < 40:
            group_1.append(ele)
        elif 40 <= idx < 80:
            group_2.append(ele)
        else:  # 80 - 120
            group_3.append(ele)
    identifiers_groups = identifiers_groups + [group_1] + [group_2] + [group_3]

# ['EDH1', 'EDZ3', 'EDU9']
# ED and FFR: 2020-11-30 -> 2022-12-31, intraday,
# maturity <= 2 year, e.g. 2020-11-30 => 2022-11-30
#

identifier_type = IdentifierType.Ric

query_start_date = date(2014, 1, 1)
query_end_date = date(2024, 1, 1)

# total_months = (query_end_date.year - query_start_date.year) * 12 + query_end_date.month - query_start_date.month
query_start_dates = [query_start_date]

while query_start_dates[-1] < query_end_date:
    query_start_dates.append(plus_period(query_start_dates[-1], Period(1, TimeUnit.MONTH), eom=EomConvention.LAST_DAY))

if query_start_dates[-1] == query_end_date:
    query_start_dates.remove(query_end_date)

query_end_dates = query_start_dates[1:] + [query_end_date]

quote_bid_price = TimeAndSalesContentFieldNames.Quote.BidPrice
quote_bid_size = TimeAndSalesContentFieldNames.Quote.BidSize
quote_ask_price = TimeAndSalesContentFieldNames.Quote.AskPrice
quote_ask_size = TimeAndSalesContentFieldNames.Quote.AskSize

trade_volume = TimeAndSalesContentFieldNames.Trade.Volume
trade_price = TimeAndSalesContentFieldNames.Trade.Price

# content_field_names = [trade_price, trade_volume]

content_field_names = [quote_ask_price, quote_ask_size,
                       quote_bid_size, quote_bid_price]
#

total = len(query_start_dates)
s = 0
f = 0
f_list = []
s_list = []
n = 0

for start_date, end_date in zip(query_start_dates, query_end_dates):
    for identifiers in identifiers_groups:
        try:
            os.mkdir(f'./output_docs/{contract_id}trades/{start_date.year}')
        except:
            pass
        extractioners = []
        cur_ids = []
        output_paths = []

        cur_ids = [identifier + '-' + start_date.isoformat() + '-' + end_date.isoformat() for identifier in identifiers]
        for identifier in identifiers:
            # cur_id = identifier + '-' + start_date.isoformat() + '-' + end_date.isoformat()
            identifier_list = InstrumentIdentifier(identifier=identifier,
                                                   identifier_type=identifier_type)

            instrument_list = InstrumentIdentifierList(identifier_list=[identifier_list],
                                                       preferred_identifier_type=identifier_type)
            condition = TickHistoryTimeAndSalesCondition(query_start_date=start_date,
                                                         query_end_date=end_date)

            extractioner = TickHistoryTimeAndSalesRawExtractioner(identifier_list=instrument_list,
                                                                  times_and_sales_content_field_names=content_field_names,
                                                                  condition=condition)
            extractioners.append(extractioner)
            cur_id = identifier + '-' + start_date.isoformat() + '-' + end_date.isoformat()
            cur_ids.append(cur_id)
            output_paths.append(f'./output_docs/{contract_id}_trades/{start_date.year}/{identifier}/{cur_id}.csv.gz')
            try:
                os.mkdir(f'./output_docs/{contract_id}_trades/{start_date.year}/{identifier}')
            except:
                pass

        try:
            # output_paths = [f'./output_docs/FF/{start_date.year}/{identifier}/{cur_id}.csv.gz' for identifier in identifiers]
            threaders = ExtractionImp(extractioners)
            threaders.save_files(output_paths)

            # output_path = f'./output_docs/FF/{start_date.year}/{identifier}/{cur_id}.csv.gz'
            # extractioner.save_output_file(output_path)
            s += 1
            n += 1
            slit = s_list + cur_ids
            print(f'Success [{cur_ids}]: [{s}] , No.: [{n}], Left: [{total - n}]')
        except Exception as e:
            f_list = f_list + cur_ids
            f += 1
            print(f'Fail [{cur_ids}]: [{f}], No.: [{n}], Left: [{total - n}], Message: [{e}]')
            continue
print(f'Finished All')
print(f_list)

# res = extractioner.get_text_results()
