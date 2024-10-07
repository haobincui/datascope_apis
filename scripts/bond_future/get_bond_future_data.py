import glob
import logging
import os
import sys

import pandas as pd

BASE_DIR = os.path.abspath(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)
sys.path.insert(0, '/home/haobin_cui/option_data_processor')
from datetime import date

from connection.apis.extraction_creator import ExtractionCreator
from connection.features.extraction.enums.content_field_names.tick_history.intraday_content_field_names import \
    IntradaySummariesContentFieldNames
from connection.features.extraction.enums.extraction_base_enums import IdentifierType
from connection.utils.condition.condition import TickHistorySummaryInterval

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')


"""
ref : [https://developers.lseg.com/en/tools-catalog/ric-search] -> "bond future" -> "chain"
"""

"""
EU bond futures:
ref: [https://www.eurex.com/ex-en/markets/int/fix/government-bonds/Euro-Bobl-Futures-137276]
Notional short-, medium- or long-term debt instruments issued by the Federal Republic of Germany,
the Republic of Italy, the Republic of France,
the Kingdom of Spain or the Swiss Confederation with remaining terms
and a coupon of 6% p.a. or 4% p.a. and a notional of EUR 100,000 or CHF 100,000.:
"""
eur_contracts = [
    '0#FGBS:',  # Euro-Schatz Futures, 1.75-2.25 years, EUR, EUREX
    '0#FGBM:',  # Euro-Bobl Futures, 4.5-5.5 years, EUR, EUREX
    '0#FGBL:',  # Euro-Bund Futures, 8.5-10.5 years, EUR, EUREX
    '0#FGBX:',  # Euro-Buxl Futures (4% coupon), 24-35 years, EUR, EUREX
    '0#FBTS:',  # Short-Term Euro-BTP Futures, 2.0-3.25 years, EUR, EUREX
    '0#FBTM:',  # Medium-Term Euro-BTP Futures, 4.5-6.0 years, EUR, EUREX
    '0#FBTP:',  # Long-Term Euro-BTP Futures, 8.5-11.0 years, EUR, EUREX
    '0#FOAM:',  # OAT Medium-Term Futures, 4.5-5.5 years, EUR, EUREX
    '0#FOAT:',  # OAT Long-Term Futures, 8.5-10.5 years, EUR, EUREX
    '0#FBON:',  # Euro-Bono Futures, 8.5-10.5 years, EUR, EUREX
    '0#CONF:',  # CONF Futures, 8.0-13.0 years, CHF, EUREX
]

"""
UK bond futures (gilts): 
ref: [https://www.ice.com/products/37650336/Long-Gilt-Future]
Deliverable futures contract on UK Gilts with maturities 8 years and 9 months to 13 years
"""

uk_contracts = [
    '0#G:',  # UK Short Gilt Futures, 1.5 - 3.25 years, GBP, ICE
    '0#H:',  # UK Medium Gilt Futures, 4.0-6.25 years, GBP, ICE
    '0#FLG:',  # UK Long Gilt Futures, 8.75-13 years, GBP, ICE
    '0#U:'  # UK Ultra Long Gilt Future, 28-37 years, GBP, ICE
]

"""
US bond futures:
ref: [https://www.cmegroup.com/trading/interest-rates/basics-of-us-treasury-futures.html]

"""

us_contracts = [
    '0#TU:',  # 2-Year US Treasury Note Futures, 1.75-2 years, USD, CME
    '0#YR:',  # 3-Year US Treasury Note Futures, 2.75-3 years, USD, CME ?
    '0#FV:',  # 5-Year US Treasury Note Futures, 4.25-5.25 years, USD, CME
    '0#TY:',  # 10-Year US Treasury Note Futures, 6.5-8 years, USD, CME
    '0#TN:',  # Ultra 10-Year US Treasury Bond Futures, 9.4-10 years, USD, CME
    '0#US:',  # US Treasury Bond Futures, 15-25 years, USD, CME
    '0#ZP:',  # 20-Year Treasury Bond Futures, 19.22-19.92 years, USD, CME
    '0#AUL:'  # Ultra US Treasury Bond Futures, 25-30 years, USD, CME
]

contracts = [
    *eur_contracts,
    *uk_contracts,
    *us_contracts
]
# contracts = [contracts[4]]

def download_data():

    start_dates = [date(i, 1, 1) for i in range(2021, 2024)]
    end_dates = [date(i, 1, 1) for i in range(2022, 2025)]
    required = [IntradaySummariesContentFieldNames.Volume.Volume,
                IntradaySummariesContentFieldNames.Close.MidPrice,
                IntradaySummariesContentFieldNames.Close.AskSize,
                IntradaySummariesContentFieldNames.Close.Ask]

    i = 0
    for start_date, end_date in zip(start_dates, end_dates):
        print('Start downloading data ...')
        for contract_id in contracts:
            extractioner = ExtractionCreator.tick_history(
                contract_id,
                identifier_type=IdentifierType.ChainRIC,
                query_start_date=start_date,
                query_end_date=end_date,
                content_field_names=required,
                summary_interval=TickHistorySummaryInterval.OneHour
            )
            output_file_name = f'./output/{contract_id}_{start_date.isoformat()}-{end_date.isoformat()}.csv.gz'
            try:
                extractioner.save_output_file(output_file_name)
            except Exception as e:
                print(f"Failed to save {output_file_name}, No.{i} ...")
                print(e)
                i += 1
                continue
            i += 1
            print(f"Saved {output_file_name}, No.{i} ...")
    print("Done!")



def merge_data():
    """
    #RIC,Alias Underlying RIC,Domain,Date-Time,GMT Offset,Type,Volume,Close Ask,Close Ask Size,Close Mid Price
    AULH5,,Market Price,2015-01-01T22:00:00.000000000Z,-6,Intraday 1Hour,,165.09375,17,
    AULH5,,Market Price,2015-01-01T23:00:00.000000000Z,-6,Intraday 1Hour,61,164.875,9,
    :return:
    """
    output_file = './output/merged.csv'
    start_dates = [date(i, 1, 1) for i in range(2014, 2024)]
    end_dates = [date(i, 1, 1) for i in range(2015, 2025)]
    first_part = True

    for contract in contracts:
        print(f"Processing {contract} ...")
        for start_date, end_date in zip(start_dates, end_dates):
            # file = glob.glob(f'./output/*_{start_date.isoformat()}-{end_date.isoformat()}.csv.gz')
            file = f'./output/{contract}_{start_date.isoformat()}-{end_date.isoformat()}.csv.gz'
            try:
                raw_data = pd.read_csv(file).fillna({"Volume":0})
            except Exception as e:
                print(f'Failed to load [{file}], message: [{e}]')
                yearly_total_volume = 0
                yearly_average_price = 0
                yearly_average_volume = 0

                # continue
            yearly_total_volume = raw_data["Volume"].sum()
            yearly_average_price = raw_data['Close Ask'].mean() * 24
            yearly_average_volume = raw_data['Volume'].mean() * 24
            output_df = pd.DataFrame({
                "Contract": [contract],
                "Year": [start_date.year],
                "TotalVolume": [yearly_total_volume],
                "DailyAveragePrice": [yearly_average_price],
                "DailyAverageVolume": [yearly_average_volume]
            })
            if first_part:
                output_df.to_csv(output_file, mode='w', index=False)
                first_part = False
            else:
                output_df.to_csv(output_file, mode='a', index=False, header=False)
        print(f"Finished processing {contract} ...")
    print('Finished all !!')




if __name__ == '__main__':
    # download_data()
    merge_data()





