from src.connection.search.enums.search_base_enums import SearchBaseEnums


class FuturesAndOptionsSearchEnums(SearchBaseEnums):
    """Represents futures and options search enums."""
    pass


class ExerciseStyle(FuturesAndOptionsSearchEnums):
    """Represents exercise style."""
    American = 'American'
    European = 'European'


class FuturesAndOptionsStatus(FuturesAndOptionsSearchEnums):
    """Represents futures and options status."""
    Inactive = 0
    Active = 1


class FuturesAndOptionTypes(FuturesAndOptionsSearchEnums):
    """Represents futures and option types."""
    Futures = 0
    FuturesOnOptions = 1
    Options = 2


class PutCall(FuturesAndOptionsSearchEnums):
    """Represents put call."""
    Call = 0
    Put = 1
