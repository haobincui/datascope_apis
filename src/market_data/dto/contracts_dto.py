from enum import Enum

import pandas as pd

from src.market_data.dto.marketdata_do import MarketDataDO
from src.market_data.dto.tradedata_do import TradeDataDO
from src.market_data.dto.quotedata_do import QuoteDataDO
from src.calendar import DatetimeConverter
from src.error.error import InputDataError

#


datetime_converter = DatetimeConverter()


class DataTypes(Enum):
    """Represents data types."""
    QUOTE = 'Quote'
    TRADE = 'Trade'


def rowdata_dto(row: pd.Series, data_type: DataTypes) -> MarketDataDO:
    # # FLG10000O0,,Market Price,2020-01-30T08:36:33.449341031Z,+0,Quote,,,0.01,100

    """Rowdata dto.

    Args:
        row (pd.Series): Input value for row.
        data_type (DataTypes): Input value for data type.

    Returns:
        MarketDataDO: Computed result of the operation.
    """
    if data_type == DataTypes.TRADE:
        return _trade_data_dto(row)
    elif data_type == DataTypes.QUOTE:
        return _quote_data_dto(row)
    else:
        raise InputDataError(message=f'Unknown data type: [{data_type.name}]')


def _trade_data_dto(row: pd.Series) -> TradeDataDO:
    # #RIC, Underlying RIC,Date-Time, trade_price, trade_volume
    """Trade data dto.

    Args:
        row (pd.Series): Input value for row.

    Returns:
        TradeDataDO: Computed result of the operation.
    """
    ric = row['#RIC']
    trade_time = datetime_converter.from_string_to_datetime(row['Date-Time'])  # '2020-01-30T08:36:33.449341031Z
    price = row['trade_price']
    volume = row['trade_volume']
    return TradeDataDO(ric, trade_time, price, volume)


def _quote_data_dto(row: pd.Series) -> QuoteDataDO:
    # #RIC, Underlying RIC,Date-Time,GMT Offset,Type,Bid Price,Bid Size,Ask Price,Ask Size
    """Quote data dto.

    Args:
        row (pd.Series): Input value for row.

    Returns:
        QuoteDataDO: Computed result of the operation.
    """
    ric = row['#RIC']
    quote_time = datetime_converter.from_string_to_datetime(row['Date-Time'])
    bid_price = row['Bid Price']
    bid_size = row['Bid Size']
    ask_price = row['Ask Price']
    ask_size = row['Ask Size']
    return QuoteDataDO(ric, quote_time, bid_price, bid_size, ask_price, ask_size)
