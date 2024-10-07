import glob
import os
import re

import numpy as np
import pandas as pd

dirt = './output_docs'
contract = '/FF trades'

target_contract = []

years = glob.glob(dirt + contract + '/*')
for year in years:
    contract_numbers = []
    contracts = glob.glob(year + '/*')
    for i in contracts:
        files = glob.glob(i + '/*.gz')
        contract_numbers.append(len(files))

    max_value = np.max(contract_numbers)

    index = np.array(contracts)[~np.equal(contract_numbers, max_value)].tolist()
    if len(index) == len(contracts):
        index = []
    target_contract += index

missed_contract_df = pd.DataFrame(columns=['Name', 'Start_date', 'End_date'])

def get_contract_infor(s):
    reg = re.compile(r'(?P<Name>^[A-Z]{3}\d{1,2})-(?P<Start_date>\d{4}-\d{2}-\d{2})-(?P<End_date>\d{4}-\d{2}-\d{2})')
    res = reg.match(s)
    return res.groupdict()


for cont in target_contract:
    contract_files = glob.glob(cont + '/*.gz')
    for contract_file in contract_files:
        contract_id = contract_file.split('/')[-1]
        try:
            contract_info = get_contract_infor(contract_id)

            missed_contract_df = missed_contract_df.append(contract_info, ignore_index=True)


            # missed_contract_df['Name'] = contract_info['Name']
            # missed_contract_df['Start_date'] = contract_info['Start_date']
            # missed_contract_df['End_date'] = contract_info['End_date']
        except Exception as e:
            print(f'{contract_id}: {e}')
            continue
missed_contract_df = missed_contract_df.sort_values(by=['Name', 'Start_date'])
# missed_contract_df.to_csv('./missed_contract_ff_2020.csv', index=False)
# print('Finished')
print(target_contract)






