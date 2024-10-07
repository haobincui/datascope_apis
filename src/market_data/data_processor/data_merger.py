import glob
import os
from calendar import Calendar
from typing import List

import pandas as pd

from connection.utils.file_processor.file_processor import FileProcesser
from src.market_data.contract_handler.future_contract import FutureContract
from market_data.contract_handler.utils import ContractTerminationRule
from market_data.contract_handler.contract_type import ContractType
from src.calendar import DatetimeConverter


def remove_empty_rows(raw_data: pd.DataFrame, start_header: str = None):
    first_column = raw_data.iloc[:, 0]  # 返回第一列
    if start_header:
        start_index = first_column.index[first_column == start_header].tolist()[0]  # 返回需要的table的表头的index
    else:
        start_index = first_column.index[~first_column.isnull()].tolist()[0]  # 返回需要的table的表头的index
    output_data = raw_data.iloc[start_index:].reset_index(drop=True)
    return output_data


class DataMerger:
    """data merger for market data"""

    @staticmethod
    def future_data_merge(input_path: str, output_path: str, contract_path: str,
                          contract_termination_rule: ContractTerminationRule,
                          calendars: List[Calendar]):
        def _date_to_maturity(contract_name_col, data_date_col):
            maturities = []

            for contract_name, data_datetime_str in zip(contract_name_col, data_date_col):
                # contract_name = current_row['#RIC']
                # data_datetime_str = current_row['Date-Time']
                data_date = DatetimeConverter().from_string_to_date(data_datetime_str)
                future_handler = FutureContract(contract_name=contract_name,
                                                contract_type=ContractType.Future)
                maturity = future_handler.get_contract_maturity_dates_by_contract_id(
                    data_date=data_date,
                    calendars=calendars,
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

                    if os.path.getsize(data) == 0:
                        fail += 1
                        print(f'File [{data}] 0 size, Fail [{fail}]')
                        fail_list.append(data)
                        continue
                    FileProcesser.decompress(data, f'{output_path}/.temp.csv')
                    current_data = pd.read_csv(f'./{output_path}/.temp.csv')
                    # current_data = current_data.apply(_date_to_maturity, axis=1)
                    maturity_df = _date_to_maturity(current_data['#RIC'], current_data['Date-Time'])
                    current_data = pd.concat([current_data, maturity_df], axis=1)
                    merged_contract_data = pd.concat([merged_contract_data, current_data], axis=0)
                    # merged_contract_data.apply(_date_to_maturity)
                    os.remove(f'./{output_path}/.temp.csv')
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
            print(f'Finished [{file}]')
        print(f'Finished ALL')

        # decompressed_file =

    # use glob to get all the csv files
    # loop over the list of csv files
    @staticmethod
    def read_all_files(input_file_path: str, data_sheet_name: str, indicator_sheet_name: str,
                       start_header: str = None, compressed=True):
        '''
        read all .xlsx files in the input file path, merge into an merged_output file
        '''

        excel_files = glob.glob(os.path.join(input_file_path, "*.xlsx"))
        excel_datas = pd.DataFrame()
        total_file_num = len(excel_files)
        success = 0
        fail = 0
        index = 1
        print(f'Start Merging [{data_sheet_name}]')

        for f in excel_files:
            try:
                data_sheet = pd.read_excel(f, sheet_name=data_sheet_name, engine='openpyxl')
                indicator_sheet = pd.read_excel(f, sheet_name=indicator_sheet_name, engine='openpyxl')

                # 处理data
                processed_data = remove_empty_rows(data_sheet, start_header)
                processed_data.rename(columns=processed_data.iloc[0], inplace=True)
                processed_data = processed_data.iloc[1:, :].reset_index(drop=True)  # drop the first row

                # 处理indicator
                processed_indicator = remove_empty_rows(indicator_sheet)
                processed_indicator.columns = ['Firm Names']  # names,
                # processed_indicator.rename('Firm names', inplace=True)
                processed_indicator['Index'] = index  # 添加index

                # swap position
                temp_index = processed_indicator['Index']  # swap position
                processed_indicator.drop(labels=['Index'], axis=1, inplace=True)
                processed_indicator.insert(0, 'Index', temp_index)

                # 合并indicator and data
                excel_data = pd.concat([processed_indicator, processed_data], axis=1)
                excel_datas = pd.concat([excel_datas, excel_data], axis=0)  # 合并数据
                success = success + 1
                print(f'Success: {success}')
                index = index + 1

            except Exception as e:
                fail = fail + 1
                print(f"Fail: No. [{index}], [{f}]: [{e}]")  # f-string
                index = index + 1
                continue

        print(f"Merge end [{data_sheet_name}], total [{total_file_num}], success [{success}], fail [{fail}].")
        excel_datas.to_excel('./merged_output/' + data_sheet_name + '.xlsx', index=False, sheet_name=data_sheet_name)

    # if __name__ == '__main__':
    #     input_file_path = './input_files'
    #     # output_file_name = 'merged_data.xlsx'
    #     data_sheet_names = ['Sheet1', 'test_Sheet2']
    #     indicator_name = 'names'
    #     start_headers = ['合约开仓日', 'test']
    #
    #     for name, header in zip(data_sheet_names, start_headers):
    #         try:
    #             read_all_excel(input_file_path=input_file_path,
    #                            data_sheet_name=name,
    #                            indicator_sheet_name=indicator_name,
    #                            start_header=header)
    #         except Exception as e:
    #             print(e)
    #         else:
    #             continue
