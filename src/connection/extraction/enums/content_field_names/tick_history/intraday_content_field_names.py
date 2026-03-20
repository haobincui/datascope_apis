from enum import Enum


class IntradaySummariesContentFieldNames:
    """Represents intraday summaries content field names."""
    class Close(Enum):
        """Represents close."""
        Ask = 'Close Ask'
        AskSize = 'Close Ask Size'
        AskYield = 'Close Ask Yield'
        Bid = 'Close Bid'
        BidSize = 'Close Bid Size'
        BidYield = 'Close Bid Yield'
        DiscountFactor = 'Close Discount Factor'
        MidPrice = 'Close Mid Price'
        Yield = 'Close Yield'
        ZeroYield = 'Close Zero Yield'

    class High(Enum):
        """Represents high."""
        High = 'High'
        Ask = 'High Ask'
        AskSize = 'High Ask Size'
        AskYield = 'High Ask Yield'
        Bid = 'High Bid'
        BidSize = 'High Bid Size'
        BidYield = 'High Bid Yield'
        DiscountFactor = 'High Discount Factor'
        MidPrice = 'High Mid Price'
        Yield = 'High Yield'
        ZeroYield = 'High Zero Yield'

    class Last(Enum):
        """Represents last."""
        Last = 'Last'

    class Low(Enum):
        """Represents low."""
        Low = 'Low'
        Ask = 'Low Ask'
        AskSize = 'Low Ask Size'
        AskYield = 'Low Ask Yield'
        Bid = 'Low Bid'
        BidSize = 'Low Bid Size'
        BidYield = 'Low Bid Yield'
        DiscountFactor = 'Low Discount Factor'
        MidPrice = 'Low Mid Price'
        Yield = 'Low Yield'
        ZeroYield = 'Low Zero Yield'

    class No(Enum):
        """Represents no."""
        AskYield = 'No. Ask Yields'
        Asks = 'No. Asks'
        BidYields = 'No. Bid Yields'
        Bids = 'No. Bids'
        DiscountFactor = 'No. Discount Factors'
        Trades = 'No. Trades'
        Yields = 'No. Yields'
        ZeroYield = 'No. Zero Yield'

    class Open(Enum):
        """Represents open."""
        Open = 'Open'
        Ask = 'Open Ask'
        AskSize = 'Open Ask Size'
        AskYield = 'Open Ask Yield'
        Bid = 'Open Bid'
        BidSize = 'Open Bid Size'
        BidYield = 'Open Bid Yield'
        DiscountFactor = 'Open Discount Factor'
        MidPrice = 'Open Mid Price'
        Yield = 'Open Yield'
        ZeroYield = 'Open Zero Yield'

    class Volume(Enum):
        """Represents volume."""
        Volume = 'Volume'

    class Domain(Enum):
        """Represents domain."""
        Domain = 'Domain'

















