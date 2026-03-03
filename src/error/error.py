from typing import Any, Dict, Mapping, Optional


class ProjectError(Exception):
    """Base error for this project with optional structured details."""

    default_id = 'Project Error'

    def __init__(self, message: str = '', *, details: Optional[Mapping[str, Any]] = None):
        self.message = message
        self.details: Dict[str, Any] = dict(details) if details else {}
        super().__init__(message)

    @property
    def id(self) -> str:
        return self.default_id

    def __str__(self) -> str:
        base = self.message or self.id
        if self.details:
            return f'{base} | details={self.details}'
        return base


class ConnectionError(ProjectError):
    default_id = 'Connection Error'


class InputDataError(ProjectError):
    default_id = 'Input Data Error'


class DataScopeError(ProjectError):
    default_id = 'DataScope Error'


class DataScopeAuthError(DataScopeError):
    default_id = 'DataScope Auth Error'


class DataScopeInputError(DataScopeError):
    default_id = 'DataScope Input Error'


class SearchError(DataScopeError):
    default_id = 'Search Error'


class ExtractionError(DataScopeError):
    default_id = 'Extraction Error'


class ThreadError(ProjectError):
    default_id = 'Thread Error'


class QuantLibError(ProjectError):
    default_id = 'QuantLib Error'


class CalendarError(QuantLibError):
    default_id = 'Calendar Error'


class DateTimeError(QuantLibError):
    default_id = 'DateTime Error'


class PricingError(QuantLibError):
    default_id = 'Pricing Error'


__all__ = [
    'ProjectError',
    'ConnectionError',
    'InputDataError',
    'DataScopeError',
    'DataScopeAuthError',
    'DataScopeInputError',
    'SearchError',
    'ExtractionError',
    'ThreadError',
    'QuantLibError',
    'CalendarError',
    'DateTimeError',
    'PricingError',
]
