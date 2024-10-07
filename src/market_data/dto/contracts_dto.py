from enum import Enum

import pandas as pd

from market_data.dto.marketdata_do import MarketDataDO
from market_data.dto.tradedata_do import TradeDataDO
from market_data.dto.quotedata_do import QuoteDataDO
from src.calendar import DatetimeConverter

#


datetime_converter = DatetimeConverter()


class DataTypes(Enum):
    QUOTE = 'Quote'
    TRADE = 'Trade'


def rowdata_dto(row: pd.Series, data_type: DataTypes) -> MarketDataDO:
    # # FLG10000O0,,Market Price,2020-01-30T08:36:33.449341031Z,+0,Quote,,,0.01,100

    if data_type == DataTypes.TRADE:
        return _trade_data_dto(row)
    elif data_type == DataTypes.QUOTE:
        return _quote_data_dto(row)
    else:
        raise Exception(f'Unknown data type: [{data_type.name}]')


def _trade_data_dto(row: pd.Series) -> TradeDataDO:
    # #RIC, Underlying RIC,Date-Time, trade_price, trade_volume
    ric = row['#RIC']
    trade_time = datetime_converter.from_string_to_datetime(row['Date-Time'])  # '2020-01-30T08:36:33.449341031Z
    price = row['trade_price']
    volume = row['trade_volume']
    return TradeDataDO(ric, trade_time, price, volume)


def _quote_data_dto(row: pd.Series) -> QuoteDataDO:
    # #RIC, Underlying RIC,Date-Time,GMT Offset,Type,Bid Price,Bid Size,Ask Price,Ask Size
    ric = row['#RIC']
    quote_time = datetime_converter.from_string_to_datetime(row['Date-Time'])
    bid_price = row['Bid Price']
    bid_size = row['Bid Size']
    ask_price = row['Ask Price']
    ask_size = row['Ask Size']
    return QuoteDataDO(ric, quote_time, bid_price, bid_size, ask_price, ask_size)
