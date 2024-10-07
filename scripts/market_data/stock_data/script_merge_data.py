import os
import sys

BASE_DIR = os.path.abspath(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)
sys.path.insert(0, '/home/haobin_cui/option_data_processor')

import glob
import pandas as pd
from src.calendar import DatetimeConverter


def merged_files(input_file: str) -> pd.DataFrame:
    files = glob.glob(f'{input_file}/*')
    res_df_list = []
    i = 0
    for file in files:
        df = pd.read_csv(file)
        datetime_converter = DatetimeConverter().from_string_to_datetime
        df['target_timestamp'] = df['Date-Time'].apply(lambda x: datetime_converter(x, ms=False))
        df['RIC'] = df['#RIC']
        res_df_list.append(df)
        i += 1
        print('Finished file:', i)
    
    res_df = pd.concat(res_df_list, axis=0, ignore_index=True)
    return res_df


def main(input_file: str, target_file: str, output_file: str):
    target_data = pd.read_excel(target_file)
    target_data['target_timestamp'] = pd.to_datetime(target_data['TIMESTAMP'])
    merged_raw_data = merged_files(input_file)
    merged_data = pd.merge(target_data, merged_raw_data, how='left', on=['RIC','target_timestamp'])
     #RIC,Alias Underlying RIC,Domain,Date-Time,Type,Price,Volume
    #  TIMESTAMP	SERIES_ID	PRODUCT_CODE	PRODUCT_NAME	OpeningPrice	HighPrice	LowPrice	LastPrice	UNDERLYING_ID	UNDERLYING_ISIN	RIC	COUNTRY	Date
    merged_data = merged_data.drop(columns=['#RIC', 'Alias Underlying RIC', 'Domain', 'target_timestamp'])
    merged_data.to_excel(output_file, index=False)



if __name__ == '__main__':
    main('./output/ALVG.DE', './input/DATASET_Valerie_sample.xlsx','./output/merged_ALVG_sample.xlsx')
    print('Finished!')


        

