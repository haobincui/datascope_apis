
from src.connection.utils.filter.operator.operator import Operator


class RangeOperator(Operator):
    """Represents range operator."""
    GreaterThan = 'GreaterThan'
    GreaterThanEqual = 'GreaterThanEqual'
    LessThan = 'LessThan'
    LessThanEqual = 'LessThanEqual'
    Equal = 'Equal'
    NotEqual = 'NotEqual'
