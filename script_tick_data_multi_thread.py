import logging
import os

import pandas as pd

from src.connection.apis.extraction_creator import ExtractionCreator
from src.connection.features.extraction.enums.content_field_names.tick_history.time_and_sales_content_field_names import \
    TimeAndSalesContentFieldNames
from src.connection.features.extraction.enums.extraction_base_enums import IdentifierType
from src.multi_thread.implement.extraction_imp import ExtractionImp

# %% setup a logger:
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')

"""
Instruction:
the mean, median, min, and max prices per  timestamp and exchange
Input CSV:
origin_trade_timestamp,series_id,product_code,main_isin,RIC,Company Name
2005-10-31 09:52:15,15372001,ALVF,DE0008404005,ALVG.DE,Allianz SE

Ouput:
'./ff_output/ALVG.DE_2005-10-31T09:52:15.csv.gz'
'./ff_output/failed_extractions.csv'
"""

# load input data
input_data_df_1 = pd.read_csv('./input/Trades_data1.csv')
input_data_df_2 = pd.read_csv('./input/Trades_data2.csv')
input_data_df = pd.concat([input_data_df_1, input_data_df_2], axis=0)

# load target exchanges
exchange_codes = pd.read_csv('./input/unique_exchanges.csv')

## required fields:

### Quote data:
quote_bid_price = TimeAndSalesContentFieldNames.Quote.BidPrice
quote_bid_size = TimeAndSalesContentFieldNames.Quote.BidSize
quote_bid_acc_size = TimeAndSalesContentFieldNames.Quote.AccBidOrderSize
quote_ask_price = TimeAndSalesContentFieldNames.Quote.AskPrice
quote_ask_size = TimeAndSalesContentFieldNames.Quote.AskSize
quote_acc_ask_size = TimeAndSalesContentFieldNames.Quote.AccAskOrderSize

quote_fields = [quote_ask_price, quote_ask_size, quote_bid_size, quote_bid_price]

### Trade data:
trade_price = TimeAndSalesContentFieldNames.Trade.Price
trade_size = TimeAndSalesContentFieldNames.Trade.Volume
trade_turnover = TimeAndSalesContentFieldNames.Trade.Turnover

trade_fields = [trade_price, trade_size]

## current content
"""
Change the content here to extract different data 
"""
current_content = quote_fields

# ff_output dir
output_path = 'output'

extractions = []
output_files = []
output_ids = []

for idx, row in input_data_df.iterrows():
    # origin_trade_timestamp,series_id,product_code,main_isin,RIC,Company Name
    timestamp = row['origin_trade_timestamp']
    query_start_date = pd.to_datetime(timestamp) - pd.Timedelta(seconds=2)
    query_end_date = pd.to_datetime(timestamp) + pd.Timedelta(seconds=2)
    contract_id = row['RIC']
    for exchange_code in exchange_codes['Exchange RIC']:
        current_contract_id = contract_id.split('.')[0] + '.' + exchange_code
        output_file = f'{output_path}/{current_contract_id}_{pd.to_datetime(timestamp).isoformat()}.csv.gz'

        # Check if the file already exists
        if os.path.exists(output_file):
            logging.info(f'File already exists: {output_file}')
            continue


        extractioner = ExtractionCreator.time_and_sales(
            contract_id=current_contract_id,
            identifier_type=IdentifierType.Ric,
            query_start_date=query_start_date,
            query_end_date=query_end_date,
            content_field_names=current_content
        )

        extractions.append(extractioner)
        output_files.append(output_file)
        output_ids.append(current_contract_id)


chunk_size = 30
total_extractions = len(extractions)
total_chunks = total_extractions // chunk_size + 1

n = 0
s = 0
f = 0
s_list = []
f_list = []

for idx in range(total_chunks):
    start = idx * chunk_size
    end = min((idx + 1) * chunk_size, total_extractions)
    logging.info(f'Start downloading data, chunk No. [{idx + 1}/{total_chunks}]')

    cur_chunk_extractions = extractions[start: end]
    cur_output = output_files[start: end]
    cur_ids = output_ids[start: end]
    cur_len = len(cur_chunk_extractions)
    threaders = ExtractionImp(cur_chunk_extractions)

    try:
        threaders.save_files(cur_output)
        s += cur_len
        s_list += cur_ids
        n += s
        logging.info(f'✅Success: [{s}], No. {n}, Left: [{total_extractions - n}] ...')
    except Exception as e:
        f += cur_len
        f_list += cur_ids
        n += f
        logging.info(f'❌Fail: [{f}], No.: [{n}], Left: [{total_extractions - n}], Message: [{e}]')
        logging.info(f'Message: [{e}] ...')
        continue

pd.DataFrame(f_list).to_csv(f"{output_path}/failed_extractions.csv", index=False)
print(f'Finished processing all extractions, Total: {total_extractions}, Success: {s}, Fail: {f}')



