from dataclasses import dataclass, field

from connection.utils.camparsions.comparison_operator import ComparisonOperator


@dataclass()
class NumericComparison:
    pass


@dataclass()
class NumericValueComparison(NumericComparison):
    comparison_operator: ComparisonOperator
    target_number: float
    comparisoner_name: str = field(init=False)

    def __post_init__(self):
        self.comparisoner_name = '#DataScope.Select.Api.Search.NumericValueComparison'


@dataclass()
class NumericRangeComparison(NumericComparison):
    from_number: float
    to_number: float
    comparisoner_name: str = field(init=False)

    def __post_init__(self):
        self.comparisoner_name = '#DataScope.Select.Api.Search.NumericRangeComparison'

        if self.from_number - self.to_number < 0:
            raise ValueError(f'start need to smaller than end')