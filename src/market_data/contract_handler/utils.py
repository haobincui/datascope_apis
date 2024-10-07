import re
from enum import Enum


class ContractTerminationRule(Enum):
    EndOfMonth = 0
    ThirdWednessday = 1
    Other = 9


def has_number_before_letter(text):
    pattern = r'\d+[A-Za-z]{1}'
    return bool(re.search(pattern, text))

