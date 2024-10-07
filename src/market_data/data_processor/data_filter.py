import glob
import os
from datetime import date
from typing import List

import pandas as pd

from src.calendar import DatetimeConverter


class DataFilter:
    """data filter for market data"""

    @staticmethod
    def find_data_for_target_days(input_path: str, output_path: str, contract_path: str,
                                  target_days: List[date]):
        """

        :param input_path:
        :param output_path:
        :param contract_path:
        :param target_days:
        :return:
        """


        files = glob.glob(input_path + contract_path + '/*')

        dt_converter = DatetimeConverter()
        for file in files:  # different year
            raw_data = pd.read_csv(file)

            trading_day = raw_data['Date-Time'].apply(dt_converter.from_string_to_date)
            trading_day.rename('Trading-Day', inplace=True)

            filted_data = pd.concat([raw_data, trading_day], axis=1)

            filted_data = filted_data[filted_data['Trading-Day'].isin(target_days)]

            filted_data = filted_data.sort_values(by=['#RIC', 'Trading-Day'])

            contract_name = contract_path.split("/")[-1]
            output_contract_path = f"/filted_{contract_name}"

            os.makedirs(output_path + output_contract_path, exist_ok=True)

            file_path = file.split('/')[-1]

            output_file_name = f'{output_path}{output_contract_path}/filted_{file_path}'

            filted_data.to_csv(output_file_name, index=False)
            print(f'Finished filter: [{file}]')
        print(f'Finished ALL filter')
