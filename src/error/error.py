from typing import Any, Dict, Mapping, Optional


class ProjectError(Exception):
    """Base error for this project with optional structured details."""

    default_id = 'Project Error'

    def __init__(self, message: str = '', *, details: Optional[Mapping[str, Any]] = None):
        """Initialize a project-level error with optional structured details.

        Args:
            message (str): Error or status message text.
            details (Optional[Mapping[str, Any]]): Optional structured metadata for diagnostics.

        Returns:
            None: No value is returned.
        """
        self.message = message
        self.details: Dict[str, Any] = dict(details) if details else {}
        super().__init__(message)

    @property
    def id(self) -> str:
        """Return the stable identifier for this error type.

        Returns:
            str: Default error id used for display and classification.
        """
        return self.default_id

    def __str__(self) -> str:
        """Return a readable string representation.

        Returns:
            str: Error message optionally enriched with structured details.
        """
        base = self.message or self.id
        if self.details:
            return f'{base} | details={self.details}'
        return base


class ConnectionError(ProjectError):
    """Error type for connection failures."""
    default_id = 'Connection Error'


class InputDataError(ProjectError):
    """Error type for input data failures."""
    default_id = 'Input Data Error'


class DataScopeError(ProjectError):
    """Error type for data scope failures."""
    default_id = 'DataScope Error'


class DataScopeAuthError(DataScopeError):
    """Error type for data scope auth failures."""
    default_id = 'DataScope Auth Error'


class DataScopeInputError(DataScopeError):
    """Error type for data scope input failures."""
    default_id = 'DataScope Input Error'


class SearchError(DataScopeError):
    """Error type for search failures."""
    default_id = 'Search Error'


class ExtractionError(DataScopeError):
    """Error type for extraction failures."""
    default_id = 'Extraction Error'


class ThreadError(ProjectError):
    """Error type for thread failures."""
    default_id = 'Thread Error'


class QuantLibError(ProjectError):
    """Error type for quant lib failures."""
    default_id = 'QuantLib Error'


class CalendarError(QuantLibError):
    """Error type for calendar failures."""
    default_id = 'Calendar Error'


class DateTimeError(QuantLibError):
    """Error type for date time failures."""
    default_id = 'DateTime Error'


class PricingError(QuantLibError):
    """Error type for pricing failures."""
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
