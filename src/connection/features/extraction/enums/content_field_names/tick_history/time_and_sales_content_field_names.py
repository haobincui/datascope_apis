from enum import Enum
from typing import Any


class TimeAndSalesContentFieldNames:
    class Quote(Enum):
        _Quote = 'Quote - '
        AskPrice = _Quote + 'Ask Price'
        BidPrice = _Quote + 'Bid Price'
        BidImpliedVolatility = _Quote + 'Bid Implied Volatility'
        AskImpliedVolatility = _Quote + 'Ask Implied Volatility'
        AskSize = _Quote + 'Ask Size'
        BidSize = _Quote + 'Bid Size'
        AccAskOrder = _Quote + 'Accumulated Ask Order'
        AccAskOrderSize = _Quote + 'Accumulated Ask Order Size'
        AccBidOrder = _Quote + 'Accumulated Bid Order'
        AccBidOrderSize = _Quote + 'Accumulated Bid Order Size'

    class Trade(Enum):
        _Trade = 'Trade - '
        AskPrice = _Trade + 'Ask Price'
        BidPrice = _Trade + 'Bid Price'
        Asksize = _Trade + 'Ask Size'
        BidSize = _Trade + 'Bid Size'
        NumberofTrades = _Trade + 'Number of Trades'
        Turnover = _Trade + 'Turnover'
        ImpliedVolatility = _Trade + 'Implied Volatility'
        Volume = _Trade + 'Volume'
        Price = _Trade + 'Price'

        # def __repr__(self):
        #     return self._Trade + self.__class__.name
