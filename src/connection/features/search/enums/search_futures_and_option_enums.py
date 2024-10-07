from src.connection.features.search.enums import SearchBaseEnums


class FuturesAndOptionsSearchEnums(SearchBaseEnums):
    pass


class ExerciseStyle(FuturesAndOptionsSearchEnums):
    American = 'American'
    European = 'European'


class FuturesAndOptionsStatus(FuturesAndOptionsSearchEnums):
    Inactive = 0
    Active = 1


class FuturesAndOptionTypes(FuturesAndOptionsSearchEnums):
    Futures = 0
    FuturesOnOptions = 1
    Options = 2


class PutCall(FuturesAndOptionsSearchEnums):
    Call = 0
    Put = 1
