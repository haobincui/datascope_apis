import glob

import pandas as pd


class DataValidator:
    """data validator for market data"""
    @staticmethod
    def filted_data_validator(filted_data_path: str):
        '''
        trading day 1, contract 1, contract 2, ..., contract n \\
        trading day 2, contract 1, contract 2, ..., contract n \\
        :param filted_data_path:
        :return:
        '''

        files = glob.glob(filted_data_path + '/*')
        output_df = pd.DataFrame()
        output_file_name = filted_data_path.split('/')[-1]

        for file in files:
            raw_data = pd.read_csv(file)
            trading_days = raw_data['Trading-Day'].unique()
            trading_days.sort()
            for trading_day in trading_days:
                current_rics = raw_data[raw_data['Trading-Day'] == trading_day]
                current_rics = current_rics['#RIC'].unique()

                # current_rics.rename(trading_day, inplace=True)
                current_df = pd.Series(data=[trading_day, *current_rics], name=trading_day)

                # current_df = pd.DataFrame(columns=[trading_day], data=current_rics)
                # current_rics.to_csv(f'./merged_output/{trading_day}.csv', index=False)
                output_df = output_df.append(current_df, ignore_index=True)

        output_df = output_df.sort_values(by=[0])
        output_df.to_csv(f'./validator_output/validator_result_{output_file_name}.csv', index=False)
        print(f'Finished validate file: [{filted_data_path}]')
