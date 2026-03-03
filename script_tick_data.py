
import logging
import os

import pandas as pd

from src.connection.apis.extraction_creator import ExtractionCreator
from src.connection.features.extraction.enums.content_field_names.tick_history.time_and_sales_content_field_names import \
    TimeAndSalesContentFieldNames
from src.connection.features.extraction.enums.extraction_base_enums import IdentifierType



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


n = 0
s = 0
f = 0
f_list = []
total = len(input_data_df) * len(exchange_codes)

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


        try:
            os.makedirs(os.path.dirname(output_file), exist_ok=True)
            extractioner.save_output_file(output_file)
            n += 1
            s += 1
            print(f'✅ No. {n} of {total}, Success {s}, Extraction for {current_contract_id} from {query_start_date} to {query_end_date} saved to {output_file}')
        except Exception as e:
            n += 1
            f += 1
            f_list.append({
                'contract_id': current_contract_id,
                'query_start_date': query_start_date,
                'query_end_date': query_end_date,
                'error': str(e)
            })
            print(f'❌No. {n} of {total},Fail {f}, Extraction for {current_contract_id} from {query_start_date} to {query_end_date} failed: {e}')
            continue

pd.DataFrame(f_list).to_csv(f"{output_path}/failed_extractions.csv", index=False)
print(f'Finished processing all extractions, Total: {total}, Success: {s}, Fail: {f}')



