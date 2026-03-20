from enum import Enum


class MarketDepthContentFieldNames(Enum):
    """Represents market depth content field names."""
    AskPrice = 'Ask Price'
    AskSize = 'Ask Size'
    BidPrice = 'Bid Price'
    BidSize = 'Bid Size'
    ExchangeTime = 'Exchange Time'
    NumberOfSellers = 'Number of Sellers'
    NumberOfBuyers = 'Number of Buyers'
