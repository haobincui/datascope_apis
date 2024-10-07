import glob
import logging
import threading
from datetime import date, datetime, time

import numpy as np
import pandas as pd
import torch

from market_data.contract_handler.contract_handler import ContractHandler
from market_data.contract_handler.contract_type import ContractType
from src.market_data.contract_handler.future_contract import FutureContract
from market_data.contract_handler.option_contract import OptionContract
from market_data.contract_handler.utils import ContractTerminationRule
from quantlib.calculation.analytics.models.analytical.equity.formula import black_scholes_implied_vol_torch
from src.calendar import DatetimeConverter
from src.calendar import DayCountBusN, bus_250_usd
from scripts.data_to_distribution.data_to_distribution_algos.get_spot import get_spot_from_quote_time_df, \
    _get_target_month_code


def get_spot_price_df(input_file: str, start_date) -> pd.DataFrame:
    # RIC,Date-Time,Type,Close Bid,Close Ask,Close Bid Size,Close Ask Size,contract_type
    raw_data = pd.read_csv(input_file)
    maturity_month_code = raw_data['#RIC'].apply(
        lambda x: FutureContract(x, ContractType.Future).get_maturity_month_code())

    target_month_code = _get_target_month_code(start_date.month)

    # raw_data = raw_data[maturity_month_code == target_month_code]
    raw_data['Spot Price'] = (raw_data['Close Bid'] + raw_data['Close Ask']) / 2
    raw_data = raw_data.drop(columns=['Close Bid', 'Close Ask'])
    raw_data['Date-Time'] = raw_data['Date-Time'].apply(lambda x: DatetimeConverter.from_string_to_datetime(x))

    return raw_data.sort_values(by='Date-Time')



def get_tau(quote_time: datetime, maturity: datetime, daycount: DayCountBusN):
    _seconds_per_day = 86400
    tau = daycount(quote_time.date(), maturity.date())
    if quote_time.time():
        tau = (datetime.combine(maturity.date(), time(20, 0, 0)) -
               datetime.combine(maturity.date(), quote_time.time())).total_seconds() / _seconds_per_day \
              / daycount.days_in_year
        return tau
    else:
        return tau


def get_vols(input_dataframe: pd.DataFrame, daycount: DayCountBusN, data_date: date,
             spot_price_df: pd.DataFrame, device: torch.device = None) -> pd.DataFrame:
    """
    Get the distribution of the option data.
    distribution = \partial^2 C / \partial K^2
    ContractId, ContractType, Maturity, Spot, Price, Size, Strike, QuoteTime, Vol, Density

    :param input_dataframe: #RIC,Date-Time,GMT Offset,Type,Bid Price,Bid Size,Ask Price,Ask Size,contract_type
    :param daycount:
    :param data_date:
    :param spot_price_df: get_spot_from_quote_time_df()
    :param device:
    :return: ContractId,ContractType,Maturity,AskSpot,AskPrice,AskSize,ASKStrike,AskQuoteTime,AskVol,AskDensity,
    BidSpot,BidPrice,BidSize,BidStrike,BidQuoteTIme,BidVol,BidDensity
    """
    if not device:
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    # print(f'Using device: [{device}] in [{threading.current_thread().getName()}]')
    logging.info(f'Using device: {device} in [{threading.current_thread().getName()}]')

    bid_price = input_dataframe['Close Bid'].to_numpy(na_value=np.NaN)
    bid_size = input_dataframe['Close Bid Size'].to_numpy()

    ask_price = input_dataframe['Close Ask'].to_numpy(na_value=np.NaN)
    ask_size = input_dataframe['Close Ask Size'].to_numpy()

    datetime_converter = DatetimeConverter()
    quote_times = input_dataframe['Date-Time'].apply(lambda x: datetime_converter.from_string_to_datetime(x))

    contract_ids = input_dataframe['#RIC']

    cld = daycount.calendar

    terminal_rule = ContractTerminationRule.EndOfMonth
    contracts_obj = contract_ids.apply(lambda x: OptionContract(x, ContractType.Option))
    maturities = contracts_obj.apply(
        lambda x: x.get_contract_maturity_dates_by_contract_id(data_date, [cld], terminal_rule, time(23, 59, 59)))
    # maturities = maturities.apply(lambda x: datetime.combine(x, time(20, 0, 0)))
    raw_option_types = contracts_obj.apply(lambda x: x.get_option_type().name)
    option_types = contracts_obj.apply(lambda x: bool(x.get_option_type().value)).to_numpy()

    # taus = [get_tau(quote_time, maturity, daycount) for quote_time, maturity in zip(quote_times, maturities)]
    _seconds_per_day = 86400
    taus = (maturities - quote_times).dt.total_seconds() / _seconds_per_day / 365
    taus = taus.to_numpy()

    # spots = quote_times.apply(lambda x: get_spot(x, spot_price_map)).to_numpy()
    spots = get_spot_from_quote_time_df(quote_times, spot_price_df).to_numpy()

    strikes = contracts_obj.apply(lambda x: x.get_strike()).to_numpy()

    bid_price = torch.tensor(bid_price, dtype=torch.float64).to(device)
    bid_size = torch.tensor(bid_size, dtype=torch.float64).to(device)
    ask_price = torch.tensor(ask_price, dtype=torch.float64).to(device)
    ask_size = torch.tensor(ask_size, dtype=torch.float64).to(device)

    taus = torch.tensor(taus, dtype=torch.float64).to(device)
    strikes = torch.tensor(strikes, dtype=torch.float64).to(device)
    spots = torch.tensor(spots, dtype=torch.float64).to(device)
    option_types = torch.tensor(option_types, dtype=torch.bool).to(device)
    r = torch.tensor([0.05], dtype=torch.float64).to(device)

    # calc the density

    print('Start calculating density ... ')
    logging.info(f'Start calculating the density ...')
    bid_vol = black_scholes_implied_vol_torch(bid_price, strikes, option_types, spots, taus, r, r, device)
    ask_vol = black_scholes_implied_vol_torch(ask_price, strikes, option_types, spots, taus, r, r, device, True)
    print('Finished calculating the Vol ...')
    logging.info(f'Finished calculating the Vol ...')

    result_ask = pd.DataFrame()
    result_ask['ContractId'] = contract_ids
    result_ask['ContractType'] = raw_option_types
    result_ask['Maturity'] = maturities
    result_ask['AskSpot'] = spots.cpu()
    result_ask['AskPrice'] = ask_price.cpu()
    result_ask['AskSize'] = ask_size.cpu()
    result_ask['ASKStrike'] = strikes.cpu()
    result_ask['AskQuoteTime'] = quote_times

    result_ask['AskVol'] = ask_vol.cpu()
    # result_ask['AskDensity'] = ask_density_results.cpu()

    result_bid = pd.DataFrame()
    result_bid['ContractId'] = contract_ids
    result_bid['ContractType'] = raw_option_types
    result_bid['Maturity'] = maturities
    result_bid['BidSpot'] = spots.cpu()
    result_bid['BidPrice'] = bid_price.cpu()
    result_bid['BidSize'] = bid_size.cpu()
    result_bid['BidStrike'] = strikes.cpu()
    result_bid['BidQuoteTIme'] = quote_times

    result_bid['BidVol'] = bid_vol.cpu()
    # result_bid['BidDensity'] = bid_density_results.cpu()

    result = pd.concat([result_ask, result_bid], axis=0)

    return result





def calc_vol(input_file_path: str, output_file_path: str, future_file_path: str,
             daycount: DayCountBusN, data_date: date,
             chunksize: int = 4_096_000 * 4, device: torch.device = None, compress: bool = False):
    start_date = date.fromisoformat(future_file_path.split('_')[-2])
    spot_price_df = get_spot_price_df(future_file_path, start_date)
    chunk_data = pd.read_csv(input_file_path, chunksize=chunksize)

    first_chunk = True
    for chunk in chunk_data:
        if first_chunk:
            result = get_vols(chunk, daycount, data_date, spot_price_df, device=device)
            result.to_csv(
                output_file_path,
                index=False,
                mode='w',
                encoding='utf-8'
            )
            first_chunk = False
        else:
            result = get_vols(chunk, daycount, data_date, spot_price_df, device=device)
            result.to_csv(
                output_file_path,
                index=False,
                mode='a',
                header=False,
                encoding='utf-8'
            )


def get_option_data_from_raw_data(input_file: str,
                                  output_file: str,
                                  future_data_output_file: str = None,
                                  chunk_size: int = 4_096_000 * 4,
                                  ):
    first_chunk = True
    for chunk in pd.read_csv(input_file, chunksize=chunk_size):
        chunk['contract_type'] = chunk['#RIC'].apply(lambda x: ContractHandler(x).get_contract_type())
        option_data = chunk[chunk['contract_type'] == 'Option']

        option_data = option_data.drop(columns=['Alias Underlying RIC', 'Domain'])
        if future_data_output_file:
            future_data = chunk[chunk['contract_type'] == 'Future']
            future_data = future_data.drop(columns=['Alias Underlying RIC', 'Domain'])
        else:
            future_data = None
        del chunk

        if first_chunk:
            option_data.to_csv(output_file, index=False, mode='w')
            if future_data is not None:
                future_data.to_csv(future_data_output_file, index=False, mode='w')
            first_chunk = False
        else:
            option_data.to_csv(output_file, index=False, mode='a', header=False)
            if future_data is not None:
                future_data.to_csv(future_data_output_file, index=False, mode='a', header=False)

def get_contract_for_target_maturity(maturity_date, contracts):
    return [contract for contract in contracts if contract.get_maturity() == maturity_date]

def separate_contracts_by_maturity(input_file):
    # ContractId, ContractType, Maturity, AskSpot, AskPrice, AskSize, ASKStrike, AskQuoteTime, AskVol,
    # BidSpot, BidPrice, BidSize, BidStrike, BidQuoteTIme, BidVol
    raw_data = pd.read_csv(input_file)
    maturities = raw_data['Maturity'].unique()
    contracts = []
    for maturity in maturities:
        temp_contracts = raw_data[raw_data['Maturity'] == maturity]
        output_file = './output/vols/'

        temp_contracts.to_csv(output_file + maturity + '.csv', index=False)


if __name__ == '__main__':
    input_path = './input'
    data_date = date(2024, 6, 13)
    daycount = bus_250_usd
    input_files = glob.glob(f'{input_path}/*.csv.gz')
    output_files = []
    future_output_files = []
    output_vol_files = []
    for input_file in input_files:
        output_file = './output/option/'
        future_output_file = './output/future/'
        output_vol_file = './output/vol/'
        output_file = output_file + input_file.split('/')[-1].split('.csv.gz')[0] + '_option.csv'
        output_files.append(output_file.replace('input', 'output'))
        future_output_file = future_output_file + input_file.split('/')[-1].split('.csv.gz')[0] + '_future.csv'
        future_output_files.append(future_output_file)
        get_option_data_from_raw_data(input_file, output_file, future_output_file)
        print(f'Finished processing file: [{input_file}]')
        # print(f'Finished processing all files ...')
        output_vol_file = output_vol_file + input_file.split('/')[-1].split('.csv.gz')[0] + '_vol.csv'
        output_vol_files.append(output_vol_file)

        calc_vol(output_file, output_vol_file, future_output_file, daycount, data_date)
        print(f'Finished processing file: [{output_file}]')
    print(f'Finished processing all files ...')
    vol_contracts = glob.glob('./output/vol/*.csv')
    for vol_contract in vol_contracts:
        separate_contracts_by_maturity(vol_contract)
    print(f'Finished processing all files ...')
