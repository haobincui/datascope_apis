from enum import Enum


class ExchangeCodes(Enum):
    """Represents exchange codes."""
    LSE = 'LSE'
    NYSE = 'NYSE'
    NASDAQ = 'NASDAQ'
    CME = 'CME'
    ICE = 'ICE'
    EUREX = 'EUREX'
