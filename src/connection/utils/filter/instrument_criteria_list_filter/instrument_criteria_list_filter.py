from dataclasses import dataclass, field


@dataclass()
class InstrumentCriteriaListFilter:
    """
    abstract class for criteria list filter
    """
    filter_name: str = field(init=False)
    dict_form: dict = field(init=False)
