from enum import Enum


class OptionType(Enum):
    """Option contract side classification."""
    PUT = 1
    CALL = 2
    OTHER = 0
