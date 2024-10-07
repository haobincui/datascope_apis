import os

import pandas as pd

from connection.features.extraction.enums.content_field_names.tick_history.time_and_sales_content_field_names import \
    TimeAndSalesContentFieldNames
from connection.features.extraction.enums.extraction_base_enums import IdentifierType
from connection.features.extraction.on_demand_extractioner.tick_history_time_and_sales_extractioner import \
    TickHistoryTimeAndSalesRawExtractioner
from connection.utils.condition.tick_history_time_and_sales_condtion import TickHistoryTimeAndSalesCondition
from connection.utils.instrument_identifier_list_base.instrument_identifier_list import InstrumentIdentifier, \
    InstrumentIdentifierList
from src.multi_thread import ExtractionImp

identifier_type = IdentifierType.Ric
missed_contracts = pd.read_excel('./target_ids.xlsx', sheet_name='missed_contracts')
identifier_list = missed_contracts['names'].tolist()

# identifiers_groups = [[i] for i in identifier_list]
query_start_dates = missed_contracts['start_date'].apply(lambda x: x.date()).tolist()
query_end_dates = missed_contracts['end_date'].apply(lambda x: x.date()).tolist()

chunks = len(identifier_list) // 40
# id_groups = []
# start_dates = []
# end_dates = []

trade_volume = TimeAndSalesContentFieldNames.Trade.Volume
trade_price = TimeAndSalesContentFieldNames.Trade.Price

content_field_names = [trade_price, trade_volume]

extractions = []
output_paths = []
cur_ids = []
for i in range(0, chunks + 1):
    start = i * 40
    end = (i + 1) * 40
    ids = identifier_list[start: end]
    start_dates = query_start_dates[start: end]
    end_dates = query_end_dates[start: end]
    chunk_extraction = []
    output_path = []

    for idx in range(len(ids)):

        identifier = InstrumentIdentifier(identifier=ids[idx],
                                          identifier_type=identifier_type)

        instrument_list = InstrumentIdentifierList(identifier_list=[identifier],
                                                   preferred_identifier_type=identifier_type)
        condition = TickHistoryTimeAndSalesCondition(query_start_date=start_dates[idx],
                                                     query_end_date=end_dates[idx])

        extractioner = TickHistoryTimeAndSalesRawExtractioner(identifier_list=instrument_list,
                                                              times_and_sales_content_field_names=content_field_names,
                                                              condition=condition)
        cur_id = ids[idx] + '-' + start_dates[idx].isoformat() + '-' + end_dates[idx].isoformat()
        cur_ids.append(cur_id)
        chunk_extraction.append(extractioner)
        output_path.append(f'./output_docs/FF trades/{start_dates[idx].year}/{ids[idx]}/{cur_id}.csv.gz')
        try:
            os.mkdir(f'./output_docs/FF trades/{start_dates[idx].year}/{ids[idx]}')
        except:
            pass
    extractions.append(chunk_extraction)
    output_paths.append(output_path)

s = 0
n = 0
f = 0
total = chunks
s_list = []
f_list = []
for idx in range(len(extractions)):

    threaders = ExtractionImp(extractions[idx])
    try:
        threaders.save_files(output_paths[idx])
        s += 1
        n += 1
        slit = s_list + cur_ids
        print(f'Success [{cur_ids}]: [{s}] , No.: [{n}], Left: [{total - n}]')
    except Exception as e:
        f_list = f_list + cur_ids
        f += 1
        print(f'Fail [{cur_ids}]: [{f}], No.: [{n}], Left: [{total - n}], Message: [{e}]')
        continue
print('Finished All')


# id_groups.append(ids)

# start =chunks * 40
# ids = identifier_list[start: -1]
# id_groups.append(ids)
#
