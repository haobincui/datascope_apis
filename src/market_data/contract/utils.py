import re
from enum import Enum


class ContractTerminationRule(Enum):
    """Represents contract termination rule."""
    EndOfMonth = 0
    ThirdWednessday = 1
    Other = 9


def has_number_before_letter(text):
    """Check whether number before letter is present.

    Args:
        text (object): Input value for text.

    Returns:
        bool: True when the check passes; otherwise False.
    """
    pattern = r'\d+[A-Za-z]{1}'
    return bool(re.search(pattern, text))

