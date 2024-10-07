from enum import Enum


class ComparisonOperator(Enum):
    GreaterThan = 'GreaterThan'
    GreaterThanEquals = 'GreaterThanEquals'
    LessThan = 'LessThan'
    LessThanEquals = 'LessThanEquals'
    Equals = 'Equals'
    NotEquals = 'NotEquals'

