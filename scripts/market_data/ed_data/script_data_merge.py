import glob
import os.path

import pandas as pd

from connection.utils.file_processor.file_processor import FileProcesser
from src.market_data.contract_handler.future_contract import FutureContract
from market_data.contract_handler.utils import ContractTerminationRule
from market_data.contract_handler.contract_type import ContractType
from src.market_data.data_processor.data_filter import DataFilter
from market_data.data_processor.data_validator import DataValidator
from src.calendar import DatetimeConverter
from src.calendar import gbp_calendar, usd_calendar

clds = [gbp_calendar(), usd_calendar()]


# clds = [usd_calendar()]


# output_contract_name = 'ED'

def data_merge(input_path, output_path, contract_path, contract_termination_rule):
    def _date_to_maturity(contract_name_col, data_date_col):
        maturities = []

        for contract_name, data_datetime_str in zip(contract_name_col, data_date_col):
            # contract_name = current_row['#RIC']
            # data_datetime_str = current_row['Date-Time']
            data_date = DatetimeConverter().from_string_to_date(data_datetime_str)
            future_handler = FutureContract(contract_name=contract_name,
                                            contract_type=ContractType.Future)
            maturity = future_handler.get_contract_maturity_dates_by_contract_id(data_date=data_date,
                                                                                 calendars=clds,
                                                                                 termination_rule=contract_termination_rule)
            maturities.append(maturity)

        return pd.DataFrame(columns=['Maturity'], data=maturities)
        # return current_row

    files = glob.glob(input_path + contract_path + '/*')
    suc = 0
    fail = 0
    fail_list = []

    for file in files:  # different year
        current_data_year = file.split('/')[-1]  # 2020
        contracts = glob.glob(pathname=file + '/*')
        output_df = pd.DataFrame()
        for contract in contracts:
            datas = glob.glob(os.path.join(contract, '*.gz'))
            merged_contract_data = pd.DataFrame()
            if not datas:
                print(f'No data in Folder [{contract}]')
                continue
            for data in datas:

                # if os.path.getsize(data) == 0:
                try:
                    FileProcesser.decompress(data, f'{output_path}/temp.csv')
                    current_data = pd.read_csv(f'./{output_path}/temp.csv')
                except Exception as e:

                    fail += 1
                    print(f'File [{data}] 0 size, Fail [{fail}]')
                    fail_list.append(data)
                    continue

                # FileProcesser.decompress(data, f'{output_path}/temp.csv')
                # current_data = pd.read_csv(f'./{output_path}/temp.csv')
                # current_data = current_data.apply(_date_to_maturity, axis=1)
                maturity_df = _date_to_maturity(current_data['#RIC'], current_data['Date-Time'])
                current_data = pd.concat([current_data, maturity_df], axis=1)
                merged_contract_data = pd.concat([merged_contract_data, current_data], axis=0)
                # merged_contract_data.apply(_date_to_maturity)
                os.remove(f'./{output_path}/temp.csv')
                suc += 1
                print(f'Finished [{data}], Success [{suc}]')
            output_df = pd.concat([output_df, merged_contract_data], axis=0)
            # output_df = output_df.sort_values(by=['Maturity', '#RIC'])

        # os.remove(f'{output_path}/temp.csv')
        os.makedirs(output_path + contract_path, exist_ok=True)
        output_df = output_df.sort_values(by=['Maturity', '#RIC'])

        output_file_name = f'{output_path}{contract_path}/{contract_path}-{current_data_year}.csv'

        output_df.to_csv(output_file_name, index=False)
        # compressed_file = FileProcesser.compress(output_file_name)
        # os.rmdir(output_file_name)
        print(f'Finished merge: [{file}]')
    print(f'Finished ALL Merge, Success [{suc}], Fail [{fail}]')

    # decompressed_file =


# FileProcesser.decompress()

if __name__ == '__main__':
    input_path = 'input'
    # input_path = '/Users/haobincui/Documents/option_data_processor/scripts/extraction/output_docs'
    output_path = 'merged_output'
    contract_path = '/ED'
    date_time_header = 'Date-Time'
    contract_termination_rule = ContractTerminationRule.ThirdWednessday
    # processor = date_to_maturity(date_time_header)

    data_merge(input_path, output_path, contract_path, contract_termination_rule)
    print(f'Finished data merge')

    # input_path = 'merged_output'
    # output_path = 'filter_output'
    # contract_path = '/ED'
    #
    target_days = sum(pd.read_excel('./target_maturity.xlsx', header=None).values.tolist(), [])
    target_days = [pd.to_datetime(i, format='%d/%m/%Y').date() for i in target_days]
    filter_input = output_path
    filter_output = './filter_output'
    # start_date = date(2020, 4, 1)
    # target_days = [date(2020, 4, 29)]


    filter = DataFilter()
    filter.find_data_for_target_days(filter_input, filter_output, contract_path, target_days)

    print(f'Finished data filter')

    # data_days_filter(input_path, output_path, contract_path, target_days)

    filted_data_path = ['./filter_output/filted_ED']

    validator = DataValidator()
    for f in filted_data_path:
        validator.filted_data_validator(f)

    print('Finished ALLLL!!!!!!')
    # '20200101'
    # 20200101
    # 2020/01/01
