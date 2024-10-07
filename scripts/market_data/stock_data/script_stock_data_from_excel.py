import logging
import os
import sys
from datetime import timedelta



BASE_DIR = os.path.abspath(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)
sys.path.insert(0, '/home/haobin_cui/option_data_processor')


import pandas as pd
import threading

from connection.features.extraction.enums.content_field_names.tick_history.time_and_sales_content_field_names import \
    TimeAndSalesContentFieldNames
from connection.features.extraction.enums.extraction_base_enums import IdentifierType
from connection.features.extraction.on_demand_extractioner.tick_history_time_and_sales_extractioner import \
    TickHistoryTimeAndSalesRawExtractioner
from connection.utils.condition.condition import TickHistoryTimeOptions
from connection.utils.condition.tick_history_time_and_sales_condtion import TickHistoryTimeAndSalesCondition
from connection.utils.instrument_identifier_list_base.instrument_identifier_list import InstrumentIdentifier, \
    InstrumentIdentifierList

# setup a logger:
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')


def extract_data(row: pd.Series) -> bool:
    identifier = row['RIC']
    # time_stamp = pd.to_datetime(row['TIMESTAMP'])
    start_date = pd.to_datetime(row['Date'])

    query_start_date = start_date
    query_end_date = start_date + timedelta(days=1)

    identifier_type = IdentifierType.Ric

    trade_price = TimeAndSalesContentFieldNames.Trade.Price
    trade_volume = TimeAndSalesContentFieldNames.Trade.Volume

    content_field_names = [trade_price, trade_volume]

    identifier_list = InstrumentIdentifier(identifier=identifier,
                                           identifier_type=identifier_type)

    instrument_list = InstrumentIdentifierList(identifier_list=[identifier_list],
                                               preferred_identifier_type=identifier_type)
    condition = TickHistoryTimeAndSalesCondition(query_start_date=query_start_date,
                                                 query_end_date=query_end_date,
                                                 message_time_stamp_in=TickHistoryTimeOptions.LocalExchangeTime)

    extractioner = TickHistoryTimeAndSalesRawExtractioner(identifier_list=instrument_list,
                                                          times_and_sales_content_field_names=content_field_names,
                                                          condition=condition)
    output_file_name = f'./output/{identifier}/{identifier}_{query_start_date.date().isoformat()}_{query_end_date.date().isoformat()}.csv.gz'
    try:
        os.makedirs(f'./output/{identifier}', exist_ok=True)

    except:
        pass
    
    res = extractioner.save_output_file(output_file_name)
    print('Saved file:', output_file_name)
    return res

def process_timestamp(input_file: str):
    raw_data = pd.read_excel(input_file)
    # raw_data['target_date'] = raw_data['TIMESTAMP'].apply(lambda x: DatetimeConverter.from_string_to_date(x))
    
    # raw_data = raw_data.groupby(by='RIC').drop_duplicates(['Date'], keep='first').ungroup()
    raw_data = raw_data.drop_duplicates(subset=['RIC', 'Date'], keep='first')
    raw_data.to_csv('./output/merged_data.csv')
    return raw_data




def main(input_file: str):
    # df = pd.read_excel(input_file)
    df = process_timestamp(input_file)
    f_idxs = []
    chunk_size = 40
    total_rows = df.shape[0]
    no_chunk = total_rows // chunk_size + 1
    print(f'Total chunks: {no_chunk}')

    for n in range(no_chunk):
        # if n >=1:
            # break
        # if n <= 236:
            # continue
        threads = []
        start = n * chunk_size
        end = min((n + 1) * chunk_size, total_rows)
        chunk = df.iloc[start:end]
        for index, row in chunk.iterrows():
            t = threading.Thread(target=extract_data, args=(row,), name=f'extract_data_{index}')
            threads.append(t)

        print('Starting chunk:', n)
        for t in threads:
            try:
                t.start()
            except Exception as e:
                print('Start Error:', e)
                print('Start Failed', t.name)
                f_idxs.append(t.name)
                continue
        for t in threads:
            try:
                t.join()
            except Exception as e:
                print('Timeout Failed', t.name)
                print('Timeout Error:', e)
                f_idxs.append(t.name)
                continue
        print('Finished chunk:', n)
        logging.info(f'{no_chunk - n} chunks left')
    print('finished all')
    print(f'Failed indexes:', f_idxs)


if __name__ == '__main__':
    main('./input/DATASET_Valerie.xlsx')
