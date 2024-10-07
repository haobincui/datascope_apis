from dataclasses import dataclass


#
@dataclass()
class ConnectionError(Exception):
    id = 'Connection Error'
    message: str = ''


@dataclass()
class InputDataError(Exception):
    id = 'Input Data Error'
    message: str = ''


class DataScopeError(Exception):
    pass


@dataclass()
class ExtractionError(DataScopeError):
    id = 'Extraction Error'
    message: str = ''


@dataclass()
class SearchError(DataScopeError):
    id = 'Search Error'
    message: str = ''


@dataclass()
class DataScopeInputError(DataScopeError):
    id = 'DataScope Input Error'
    message: str = ''


@dataclass()
class ThreadError(Exception):
    id = 'Thread Error'
    message: str = ''


class QuantLibError(Exception):
    pass


@dataclass()
class CalendarError(QuantLibError):
    id = 'Calendar Error'
    message: str = ''


@dataclass()
class DateTimeError(QuantLibError):
    id = 'DateTime Error'
    message: str = ''


@dataclass()
class PricingError(QuantLibError):
    id = 'Pricing Error'
    message: str = ''


class DataScopeError(Exception):
    pass

class DataScopeInputError(DataScopeError):
    pass

class ExtractionError(DataScopeError):
    pass

class SearchError(DataScopeError):
    pass

class ThreadError(Exception):
    pass

class QuantLibError(Exception):
    pass
pass

class CalendarError(QuantLibError):
    pass






