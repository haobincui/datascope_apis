from typing import List, Set, NoReturn
from dataclasses import dataclass, field
from datetime import date, timedelta

_none = {}

_weekends = {}

_cny_holidays = {date(2021, 1, 1), date(2021, 2, 11), date(2021, 2, 12), date(2021, 2, 15), date(2021, 2, 16),
                 date(2021, 2, 17), date(2021, 4, 5), date(2021, 5, 3), date(2021, 5, 4), date(2021, 5, 5),
                 date(2021, 6, 14), date(2021, 9, 20), date(2021, 9, 21), date(2021, 10, 1), date(2021, 10, 4),
                 date(2021, 10, 5), date(2021, 10, 6), date(2021, 10, 7),
                 date(2022, 1, 3),
                 date(2022, 1, 31), date(2022, 2, 1), date(2022, 2, 2), date(2022, 2, 3),
                 date(2022, 2, 4), date(2022, 4, 4), date(2022, 4, 5),
                 date(2022, 5, 2), date(2022, 5, 3), date(2022, 5, 4), date(2022, 6, 3), date(2022, 9, 12),
                 date(2022, 10, 3), date(2022, 10, 4), date(2022, 10, 5), date(2022, 10, 6), date(2022, 10, 7),
                 date(2023, 1, 2), date(2023, 1, 23), date(2023, 1, 24), date(2023, 1, 25), date(2023, 1, 26),
                 date(2023, 1, 27), date(2023, 4, 5), date(2023, 4, 6), date(2023, 4, 7), date(2023, 5, 1),
                 date(2023, 5, 2), date(2023, 5, 3), date(2023, 6, 22), date(2023, 6, 23),
                 date(2023, 9, 29), date(2023, 10, 2), date(2023, 10, 3), date(2023, 10, 4), date(2023, 10, 5),
                 date(2023, 10, 6),
                 date(2024, 1, 1), date(2024, 2, 9), date(2024, 2, 12), date(2024, 2, 13), date(2024, 2, 14),
                 date(2024, 2, 15), date(2024, 4, 4), date(2024, 4, 5), date(2024, 5, 1), date(2024, 5, 2),
                 date(2024, 5, 3), date(2024, 6, 10), date(2024, 9, 16), date(2024, 9, 17), date(2024, 10, 1),
                 date(2024, 10, 2), date(2024, 10, 3), date(2024, 10, 4), date(2024, 10, 7),
                 date(2025, 1, 1), date(2025, 1, 28), date(2025, 1, 29), date(2025, 1, 30), date(2025, 1, 31),
                 date(2025, 2, 3), date(2025, 4, 4), date(2025, 4, 5), date(2025, 5, 1), date(2025, 5, 2),
                 date(2025, 5, 3), date(2025, 5, 4), date(2025, 5, 5), date(2025, 6, 2), date(2025, 10, 1),
                 date(2025, 10, 2), date(2025, 10, 3), date(2025, 10, 6), date(2025, 10, 7), date(2025, 10, 8),
                 date(2026, 1, 1), date(2026, 1, 2), date(2026, 2, 16), date(2026, 2, 17), date(2026, 2, 18),
                 date(2026, 2, 19), date(2026, 2, 20), date(2026, 4, 6), date(2026, 5, 1), date(2026, 5, 4),
                 date(2026, 5, 5), date(2026, 6, 19), date(2026, 9, 25), date(2026, 10, 1), date(2026, 10, 2),
                 date(2026, 10, 5), date(2026, 10, 5), date(2026, 10, 6), date(2026, 10, 7),
                 date(2027, 1, 1), date(2027, 2, 5), date(2027, 2, 8), date(2027, 2, 9), date(2027, 2, 10),
                 date(2027, 2, 11), date(2027, 4, 5), date(2027, 5, 3), date(2027, 5, 4), date(2027, 5, 5),
                 date(2027, 6, 9), date(2027, 9, 15), date(2027, 10, 1), date(2027, 10, 4), date(2027, 10, 5),
                 date(2027, 10, 6), date(2027, 10, 7),
                 date(2028, 1, 3), date(2028, 1, 25), date(2028, 1, 26), date(2028, 1, 27), date(2028, 1, 28),
                 date(2028, 1, 31), date(2028, 4, 3), date(2028, 4, 4), date(2028, 5, 1), date(2028, 5, 2),
                 date(2028, 5, 3), date(2028, 5, 29), date(2028, 10, 2), date(2028, 10, 3), date(2028, 10, 4),
                 date(2028, 10, 5), date(2028, 10, 6), date(2028, 10, 7),
                 date(2029, 1, 1), date(2029, 2, 12), date(2029, 2, 13), date(2029, 2, 14), date(2029, 2, 15),
                 date(2029, 2, 16), date(2029, 4, 4), date(2029, 5, 1), date(2029, 5, 2), date(2029, 5, 3),
                 date(2029, 6, 18), date(2029, 9, 24), date(2029, 10, 1), date(2029, 10, 2), date(2029, 10, 3),
                 date(2029, 10, 4), date(2029, 10, 5), date(2029, 12, 31),
                 date(2030, 1, 1), date(2030, 2, 4), date(2030, 2, 5), date(2030, 2, 6), date(2030, 2, 7),
                 date(2030, 2, 8), date(2030, 4, 5), date(2030, 5, 1), date(2030, 5, 2), date(2030, 5, 3),
                 date(2030, 6, 5), date(2030, 9, 12), date(2030, 9, 13), date(2030, 10, 1), date(2030, 10, 2),
                 date(2030, 10, 3), date(2030, 10, 4), date(2030, 10, 5), date(2030, 10, 7),
                 date(2031, 1, 1), date(2031, 1, 22), date(2031, 1, 23), date(2031, 1, 24), date(2031, 1, 27),
                 date(2031, 1, 28), date(2031, 4, 7), date(2031, 5, 1), date(2031, 5, 2), date(2031, 5, 5),
                 date(2031, 6, 23), date(2031, 6, 24), date(2031, 10, 1), date(2031, 10, 2), date(2031, 10, 3),
                 date(2031, 10, 4), date(2031, 10, 6), date(2031, 10, 7), date(2031, 10, 8),
                 date(2032, 1, 1), date(2032, 1, 2), date(2032, 2, 10), date(2032, 2, 11), date(2032, 2, 12),
                 date(2032, 2, 13), date(2032, 2, 16), date(2032, 4, 5), date(2032, 5, 3), date(2032, 5, 4),
                 date(2032, 5, 5), date(2032, 6, 14), date(2032, 9, 20), date(2032, 10, 1), date(2032, 10, 4),
                 date(2032, 10, 5), date(2032, 10, 6), date(2032, 10, 7),
                 date(2033, 1, 3), date(2033, 1, 31), date(2033, 2, 1), date(2033, 2, 2), date(2033, 2, 3),
                 date(2033, 2, 4), date(2033, 4, 4), date(2033, 5, 2), date(2033, 5, 3), date(2033, 5, 4),
                 date(2033, 6, 1), date(2033, 9, 8), date(2033, 9, 9), date(2033, 10, 3), date(2033, 10, 4),
                 date(2033, 10, 5), date(2033, 10, 6), date(2033, 10, 7)
                 }

_usd_holidays = {date(2020, 1, 1), date(2020, 1, 20), date(2020, 2, 17), date(2020, 5, 25), date(2020, 7, 3),
                 date(2020, 9, 7), date(2020, 10, 12), date(2020, 11, 11), date(2020, 11, 26), date(2020, 12, 25),
                 date(2021, 1, 1), date(2021, 1, 18), date(2021, 2, 15), date(2021, 5, 31), date(2021, 7, 5),
                 date(2021, 9, 6), date(2021, 10, 11), date(2021, 11, 11), date(2021, 11, 25), date(2021, 12, 25),
                 date(2022, 1, 1), date(2022, 1, 17), date(2022, 2, 21), date(2022, 5, 30), date(2022, 6, 20),
                 date(2022, 7, 4), date(2022, 9, 5), date(2022, 10, 10), date(2022, 11, 11), date(2022, 11, 24),
                 date(2022, 12, 26), date(2023, 1, 2), date(2023, 1, 16), date(2023, 2, 20), date(2023, 5, 29),
                 date(2023, 6, 19), date(2023, 7, 4), date(2023, 9, 4), date(2023, 10, 9), date(2023, 11, 11),
                 date(2023, 11, 23), date(2023, 12, 25), date(2024, 1, 1), date(2024, 1, 15), date(2024, 2, 19),
                 date(2024, 5, 27), date(2024, 6, 19), date(2024, 7, 4), date(2024, 9, 2), date(2024, 10, 14),
                 date(2024, 11, 11), date(2024, 11, 28), date(2024, 12, 25), date(2025, 1, 1), date(2025, 1, 20),
                 date(2025, 2, 17), date(2025, 5, 26), date(2025, 6, 19), date(2025, 7, 4), date(2025, 9, 1),
                 date(2025, 10, 13), date(2025, 11, 11), date(2025, 11, 27), date(2025, 12, 25), date(2026, 1, 1),
                 date(2026, 1, 19), date(2026, 2, 16), date(2026, 5, 25), date(2026, 6, 19), date(2026, 7, 4),
                 date(2026, 9, 7), date(2026, 10, 12), date(2026, 11, 11), date(2026, 11, 26), date(2026, 12, 25),
                 date(2027, 1, 1), date(2027, 1, 18), date(2027, 2, 15), date(2027, 5, 31), date(2027, 6, 18),
                 date(2027, 7, 4),
                 date(2027, 9, 6), date(2027, 10, 11), date(2027, 11, 11), date(2027, 11, 25), date(2027, 12, 25),
                 date(2028, 1, 1), date(2028, 1, 17), date(2028, 2, 21), date(2028, 5, 29), date(2028, 6, 19),
                 date(2028, 7, 4),
                 date(2028, 9, 4), date(2028, 10, 9), date(2028, 11, 11), date(2028, 11, 23), date(2028, 12, 25),
                 date(2029, 1, 1), date(2029, 1, 15), date(2029, 2, 20), date(2029, 5, 28), date(2029, 6, 19),
                 date(2029, 7, 4),
                 date(2029, 9, 3), date(2029, 10, 8), date(2029, 11, 11), date(2029, 11, 22), date(2029, 12, 25),
                 date(2030, 1, 1), date(2030, 1, 21), date(2030, 2, 18), date(2030, 5, 27), date(2030, 6, 19),
                 date(2030, 7, 4),
                 date(2030, 9, 2), date(2030, 10, 14), date(2030, 11, 11), date(2030, 11, 28), date(2030, 12, 25),

                 }

_hkd_holidays = {date(2021, 1, 1), date(2021, 2, 12), date(2021, 2, 13), date(2021, 2, 15), date(2021, 4, 2),
                 date(2021, 4, 5), date(2021, 4, 6), date(2021, 5, 1), date(2021, 5, 19), date(2021, 6, 14),
                 date(2021, 7, 1), date(2021, 9, 22), date(2021, 10, 1), date(2021, 10, 14), date(2021, 12, 25),
                 date(2021, 12, 27), date(2022, 1, 1), date(2022, 2, 1), date(2022, 2, 2), date(2022, 2, 3),
                 date(2022, 4, 5), date(2022, 4, 15), date(2022, 4, 18), date(2022, 5, 2), date(2022, 5, 9),
                 date(2022, 6, 3), date(2022, 7, 1), date(2022, 9, 12), date(2022, 10, 1), date(2022, 10, 4),
                 date(2022, 12, 26), date(2022, 12, 27), date(2023, 1, 2), date(2023, 1, 23), date(2023, 1, 24),
                 date(2023, 1, 25), date(2023, 4, 5), date(2023, 4, 7), date(2023, 4, 10), date(2023, 5, 1),
                 date(2023, 5, 26), date(2023, 6, 22), date(2023, 7, 1), date(2023, 9, 30), date(2023, 10, 2),
                 date(2023, 10, 23), date(2023, 12, 25), date(2023, 12, 26), date(2024, 1, 1), date(2024, 2, 10),
                 date(2024, 2, 12), date(2024, 2, 13), date(2024, 3, 29), date(2024, 4, 1), date(2024, 4, 4),
                 date(2024, 5, 1), date(2024, 5, 15), date(2024, 6, 10), date(2024, 7, 1), date(2024, 9, 18),
                 date(2024, 10, 1), date(2024, 10, 11), date(2024, 12, 25), date(2024, 12, 26), date(2025, 1, 1),
                 date(2025, 1, 29), date(2025, 1, 30), date(2025, 1, 31), date(2025, 4, 4), date(2025, 4, 18),
                 date(2025, 4, 21), date(2025, 5, 1), date(2025, 5, 5), date(2025, 5, 31), date(2025, 7, 1),
                 date(2025, 10, 1), date(2025, 10, 7), date(2025, 10, 29), date(2025, 12, 25), date(2025, 12, 26),
                 date(2026, 1, 1), date(2026, 2, 17), date(2026, 2, 18), date(2026, 2, 19), date(2026, 4, 3),
                 date(2026, 4, 4), date(2026, 4, 6), date(2026, 5, 1), date(2026, 5, 25), date(2026, 6, 19),
                 date(2026, 7, 1), date(2026, 9, 26), date(2026, 10, 1), date(2026, 10, 19), date(2026, 12, 25),
                 date(2026, 12, 26)}

_eur_holidays = {date(2021, 1, 1), date(2021, 4, 2), date(2021, 4, 5), date(2021, 5, 1), date(2021, 12, 25),
                 date(2021, 12, 26), date(2022, 1, 1), date(2022, 4, 15), date(2022, 4, 18), date(2022, 5, 1),
                 date(2022, 12, 25), date(2022, 12, 26), date(2023, 1, 1), date(2023, 4, 7), date(2023, 4, 10),
                 date(2023, 5, 1), date(2023, 12, 25), date(2023, 12, 26), date(2024, 1, 1), date(2024, 3, 29),
                 date(2024, 4, 1), date(2024, 5, 1), date(2024, 12, 25), date(2024, 12, 26), date(2025, 1, 1),
                 date(2025, 4, 18), date(2025, 4, 21), date(2025, 5, 1), date(2025, 12, 25), date(2025, 12, 26),
                 date(2026, 1, 1), date(2026, 4, 3), date(2026, 4, 6), date(2026, 5, 1), date(2026, 12, 25),
                 date(2026, 12, 26)}

_gbp_holidays = {date(2020, 1, 1), date(2020, 4, 10), date(2020, 4, 13), date(2020, 5, 8), date(2020, 5, 25),
                 date(2020, 8, 31), date(2020, 12, 25), date(2020, 12, 28),
                 date(2021, 1, 1), date(2021, 4, 2), date(2021, 4, 5), date(2021, 5, 3), date(2021, 5, 31),
                 date(2021, 8, 30), date(2021, 12, 27), date(2021, 12, 28), date(2022, 1, 3), date(2022, 4, 15),
                 date(2022, 4, 18), date(2022, 5, 2), date(2022, 6, 2), date(2022, 6, 3), date(2022, 8, 29),
                 date(2022, 12, 26), date(2022, 12, 27), date(2023, 1, 2), date(2023, 4, 7), date(2023, 4, 10),
                 date(2023, 5, 1), date(2023, 5, 29), date(2023, 8, 28), date(2023, 12, 25), date(2023, 12, 26),
                 date(2024, 1, 1), date(2024, 3, 29), date(2024, 4, 1), date(2024, 5, 6), date(2024, 5, 27),
                 date(2024, 8, 26), date(2024, 12, 25), date(2024, 12, 26),
                 date(2025, 1, 1), date(2025, 4, 18),
                 date(2025, 4, 21), date(2025, 5, 5), date(2025, 5, 26), date(2025, 8, 25), date(2025, 12, 25),
                 date(2025, 12, 26),
                 date(2026, 1, 1), date(2026, 4, 3), date(2026, 4, 6), date(2026, 5, 4),
                 date(2026, 5, 25), date(2026, 8, 31), date(2026, 12, 25), date(2026, 12, 28),
                 date(2027, 1, 1), date(2027, 3, 26), date(2027, 3, 29), date(2027, 5, 3),
                 date(2027, 5, 31), date(2027, 8, 30), date(2027, 12, 27), date(2027, 12, 28),
                 date(2028, 1, 3), date(2028, 4, 14), date(2028, 4, 17), date(2028, 5, 1),
                 date(2028, 5, 29), date(2028, 8, 28), date(2028, 12, 25), date(2028, 12, 26),
                 date(2029, 1, 1), date(2029, 3, 30), date(2029, 4, 2), date(2029, 5, 7),
                 date(2029, 5, 28), date(2029, 8, 27), date(2029, 12, 25), date(2029, 12, 26),
                 date(2030, 1, 1), date(2030, 4, 19), date(2030, 4, 22), date(2030, 5, 6),
                 date(2030, 5, 27), date(2030, 8, 26), date(2030, 12, 25), date(2030, 12, 26),

                 }

_holidays_map = {
    'NONE': _none,
    'WEEKENDS': _weekends,
    'CNY': _cny_holidays,
    'USD': _usd_holidays,
    'HKD': _hkd_holidays,
    'GBP': _gbp_holidays,
    'EUR': _eur_holidays
}

_aliases_map = {}


def holidays_map() -> dict:
    return _holidays_map


def aliases_map() -> dict:
    return _aliases_map


@dataclass
class HolidayCalendar:
    calendars: List[str]
    include_weekends: bool
    actual_calendars: List[str] = field(init=False)

    # TODO: add weekends defs (may not be saturday/sundays)

    def __post_init__(self):
        self.actual_calendars = [c if c in _holidays_map else _aliases_map[c] for c in self.calendars]

    def is_holiday(self, t: date) -> bool:
        if self.include_weekends and t.weekday() >= 5:
            return True
        for c in self.actual_calendars:
            if t in _holidays_map[c]:
                return True
        return False

    def count_business_days(self, start: date, end: date, include_start: bool, include_end: bool) -> int:
        if start == end:
            return 0
        if start > end:
            return -self.count_business_days(end, start, include_end, include_start)
        total = 0
        t = start + timedelta(days=1)
        while t < end:
            if not self.is_holiday(t):
                total = total + 1
            t = t + timedelta(days=1)
        if include_start and not self.is_holiday(start):
            total = total + 1
        if include_end and not self.is_holiday(end):
            total = total + 1
        return total

    def next(self, start: date) -> date:
        t = start + timedelta(days=1)
        while self.is_holiday(t):
            t = t + timedelta(days=1)
        return t

    def prev(self, start: date) -> date:
        t = start - timedelta(days=1)
        while self.is_holiday(t):
            t = t - timedelta(days=1)
        return t


_weekends_only = HolidayCalendar(calendars=['WEEKENDS'], include_weekends=True)

_none_cld = HolidayCalendar(calendars=['NONE'], include_weekends=False)

_embedded_cny = HolidayCalendar(calendars=['CNY'], include_weekends=True)

_eur_calendar = HolidayCalendar(calendars=['EUR'], include_weekends=True)

_gbp_calendar = HolidayCalendar(calendars=['GBP'], include_weekends=True)

_usd_calendar = HolidayCalendar(calendars=['USD'], include_weekends=True)


def create_calendar(name: str, holidays: List[date]) -> HolidayCalendar:
    _holidays_map[name] = set(holidays)
    return HolidayCalendar(calendars=[name], include_weekends=True)


def delete_calendar(name: str) -> NoReturn:
    if name in _aliases_map:
        del _aliases_map[name]
    else:
        if name not in _holidays_map:
            return
        # remove all aliases first
        aliases = [s for s in _aliases_map.keys() if _aliases_map[s] == name]
        for a in aliases:
            del _aliases_map[a]
        # then delete the actual calendar
        del _holidays_map[name]


def weekends_only_calendar():
    return _weekends_only


def empty_calendar():
    return _none_cld


def embedded_calendar():
    return _embedded_cny


def eur_calendar():
    return _eur_calendar


def gbp_calendar():
    return _gbp_calendar


def usd_calendar():
    return _usd_calendar


def embedded_holidays() -> List[date]:
    return list(_cny_holidays)


def _get_holidays(c: str) -> Set[date]:  # return set for union of calendars
    h = c
    if c not in _holidays_map:
        if c in _aliases_map:
            h = _aliases_map[c]
        else:
            raise ValueError(f'calendar {c} is missing')
    return _holidays_map[h]


def get_holidays(name: str) -> List[date]:
    cs = [c.strip() for c in name.split(",")]
    hs = [_get_holidays(c) for c in cs]
    return sorted((set().union(*hs)))


def get_calendar(name: str) -> HolidayCalendar:
    if name.upper() == 'NONE':
        return _none_cld
    cs = [c.strip() for c in name.split(",")]
    for c in cs:
        if c not in _holidays_map and c not in _aliases_map:
            raise ValueError(f'calendar {c} is missing')
    return HolidayCalendar(calendars=cs, include_weekends=True)


def add_alias(alias: str, holidays: str) -> NoReturn:
    if holidays not in _holidays_map:
        raise ValueError(f'{holidays} does not exist')
    if alias in _aliases_map:
        c = _aliases_map[alias]
        if c == holidays:
            return
        else:
            raise ValueError(f'alias {alias} points to a different holiday calendar {c} '
                             f'that is not the same as the input {holidays}')
    else:
        _aliases_map[alias] = holidays


def delete_alias(alias: str) -> NoReturn:
    if alias in _aliases_map:
        del _aliases_map[alias]


def list_calendars_and_aliases() -> dict:
    calendars = list(_holidays_map.keys())
    aliases = {c: [a for a in _aliases_map.keys() if _aliases_map[a] == c] for c in calendars}
    return {'calendars': calendars,
            'aliases': aliases}
