from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import date
from .holidays import HolidayCalendar, embedded_calendar, usd_calendar, gbp_calendar


class DayCount(ABC):
    @abstractmethod
    def __call__(self, start: date, end: date) -> float:
        pass


@dataclass(frozen=True)
class DayCountAct365(DayCount):
    name: str = 'ACT365'

    def __call__(self, start: date, end: date) -> float:
        return (end - start).days / 365


@dataclass(frozen=True)
class DayCountBusN(DayCount):
    name: str
    calendar: HolidayCalendar
    days_in_year: int
    include_start: bool = False
    include_end: bool = True

    def __call__(self, start: date, end: date) -> float:
        return self.calendar.count_business_days(start, end, self.include_start, self.include_end) / self.days_in_year


act_365 = DayCountAct365()

bus_250_embedded = DayCountBusN('BUS250', embedded_calendar(), 250, False, True)
bus_250_usd = DayCountBusN('BUS250USD', usd_calendar(), 250, False, True)
bus_250_gbp = DayCountBusN('BUS250GBP', gbp_calendar(), 250, False, True)

