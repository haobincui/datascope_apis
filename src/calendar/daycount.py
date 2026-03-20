from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import date
from .holidays import HolidayCalendar, embedded_calendar, usd_calendar, gbp_calendar


class DayCount(ABC):
    """Abstract base for day-count conventions."""

    @abstractmethod
    def __call__(self, start: date, end: date) -> float:
        """Compute a year-fraction day count between two dates.

        Args:
            start (date): Start date of the accrual period.
            end (date): End date of the accrual period.

        Returns:
            float: Day-count fraction according to the concrete convention.
        """
        pass


@dataclass(frozen=True)
class DayCountAct365(DayCount):
    """ACT/365 fixed day-count convention."""
    name: str = 'ACT365'

    def __call__(self, start: date, end: date) -> float:
        """Compute ACT/365 day-count fraction.

        Args:
            start (date): Start date of the accrual period.
            end (date): End date of the accrual period.

        Returns:
            float: Calendar-day difference divided by 365.
        """
        return (end - start).days / 365


@dataclass(frozen=True)
class DayCountBusN(DayCount):
    """Business-day-over-N convention using a holiday calendar."""
    name: str
    calendar: HolidayCalendar
    days_in_year: int
    include_start: bool = False
    include_end: bool = True

    def __call__(self, start: date, end: date) -> float:
        """Compute business-day day-count fraction.

        Args:
            start (date): Start date of the accrual period.
            end (date): End date of the accrual period.

        Returns:
            float: Counted business days divided by `days_in_year`.
        """
        return self.calendar.count_business_days(start, end, self.include_start, self.include_end) / self.days_in_year


act_365 = DayCountAct365()

bus_250_embedded = DayCountBusN('BUS250', embedded_calendar(), 250, False, True)
bus_250_usd = DayCountBusN('BUS250USD', usd_calendar(), 250, False, True)
bus_250_gbp = DayCountBusN('BUS250GBP', gbp_calendar(), 250, False, True)
