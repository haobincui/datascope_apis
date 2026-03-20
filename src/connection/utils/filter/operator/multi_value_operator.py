from src.connection.utils.filter.operator.operator import Operator


class MultiValueOperator(Operator):
    """Represents multi value operator."""
    In = 'In'
    NotIn = 'NotIn'
