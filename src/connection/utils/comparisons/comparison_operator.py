from enum import Enum


class ComparisonOperator(Enum):
    """Represents comparison operator."""
    GreaterThan = 'GreaterThan'
    GreaterThanEquals = 'GreaterThanEquals'
    LessThan = 'LessThan'
    LessThanEquals = 'LessThanEquals'
    Equals = 'Equals'
    NotEquals = 'NotEquals'
