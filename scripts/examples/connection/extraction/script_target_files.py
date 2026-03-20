from datetime import date

import pandas as pd

start_date = date(2021, 1, 1)
dates_1 = [date(2021, i, 1) for i in range(1, 13)]
dates_2 = [date(2022, i, 1) for i in range(1, 13)]
start_dates = dates_1 + dates_2
end_dates = start_dates[1:] + [date(2023, 1, 1)]
ids = pd.read_excel('./target_file_names.xlsx', sheet_name='names')['Names'].tolist()

df = pd.DataFrame()

for id in ids:
    temp_df = pd.DataFrame()
    temp_df['start_date'] = start_dates
    temp_df['end_date'] = end_dates
    temp_df['names'] = id
    df = df.append(temp_df)
df.to_excel('./target_ids.xlsx', index=False)




