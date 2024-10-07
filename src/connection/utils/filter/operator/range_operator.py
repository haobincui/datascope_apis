
from connection.utils.filter.operator.operator import Operator


class RangeOperator(Operator):
    GreaterThan = 'GreaterThan',
    GreaterThanEqual = 'GreaterThanEqual',
    LessThan = 'LessThan',
    LessThanEqual = 'LessThanEqual',
    Equal = None,
    NotEqual = 'NotEqual'
