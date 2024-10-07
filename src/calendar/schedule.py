from calendar import monthrange
from typing import List, Union
from enum import Enum
from dataclasses import dataclass
from datetime import date, timedelta, datetime
from dateutil.relativedelta import relativedelta

import re
from .holidays import HolidayCalendar, empty_calendar


class TimeUnit(Enum):
    BUSINESS_DAY = 1
    DAY = 2
    WEEK = 3
    MONTH = 4
    YEAR = 5


class BusinessDayConvention(Enum):
    NONE = 0
    FOLLOWING = 1
    MODIFIED_FOLLOWING = 2
    PRECEDING = 3
    MODIFIED_PRECEDING = 4


class EomConvention(Enum):
    NONE = 0
    LAST_DAY = 1
    LAST_BUSINESS_DAY = 2


class StubType(Enum):
    NONE = 0
    SHORT_INITIAL = 1
    SHORT_FINAL = 2
    LONG_INITIAL = 3
    LONG_FINAL = 4
    AUTO_INITIAL = 5
    AUTO_FINAL = 6
    BOTH = 7


@dataclass()
class Period:
    length: int
    time_unit: TimeUnit

    def __str__(self):
        def time_unit_to_str(tu: TimeUnit) -> str:
            if tu == TimeUnit.BUSINESS_DAY:
                return 'B'
            if tu == TimeUnit.DAY:
                return 'D'
            if tu == TimeUnit.WEEK:
                return 'W'
            if tu == TimeUnit.MONTH:
                return 'M'
            if tu == TimeUnit.YEAR:
                return 'Y'

        return f'{self.length}{time_unit_to_str(self.time_unit)}'

    def is_month_based(self):
        return self.time_unit == TimeUnit.MONTH or self.time_unit == TimeUnit.YEAR


def adjust_date(start: date, convention: BusinessDayConvention, calendar: HolidayCalendar) -> date:
    if convention == BusinessDayConvention.NONE:
        return start
    end = start
    if convention == BusinessDayConvention.FOLLOWING or convention == BusinessDayConvention.MODIFIED_FOLLOWING:
        while calendar.is_holiday(end):
            end = end + timedelta(days=1)
        if convention == BusinessDayConvention.MODIFIED_FOLLOWING and not end.month == start.month:
            return adjust_date(start, BusinessDayConvention.PRECEDING, calendar)
    else:
        while calendar.is_holiday(end):
            end = end - timedelta(days=1)
        if convention == BusinessDayConvention.MODIFIED_PRECEDING and not end.month == start.month:
            return adjust_date(start, BusinessDayConvention.FOLLOWING, calendar)
    return end


def last_day_of_month(start: date) -> date:
    _, d = monthrange(start.year, start.month)
    return date(start.year, start.month, d)


def is_day_last_day_of_month(start: date) -> bool:
    return start == last_day_of_month(start)


def last_business_day_of_month(start: date, calendar: HolidayCalendar) -> date:
    return adjust_date(last_day_of_month(start), BusinessDayConvention.PRECEDING, calendar)


def is_day_last_business_day_of_month(start: date, calendar: HolidayCalendar) -> bool:
    return start == last_business_day_of_month(start, calendar)


def plus_period(start: date, period: Period,
                adj: BusinessDayConvention = BusinessDayConvention.NONE, calendar: HolidayCalendar = empty_calendar(),
                eom: EomConvention = EomConvention.NONE) -> date:
    n = period.length
    if n == 0:
        return start
    tu = period.time_unit
    if tu == TimeUnit.BUSINESS_DAY:
        end = start
        if n > 0:
            for _ in range(n):
                end = calendar.next(end)
        else:
            for _ in range(-n):
                end = calendar.prev(end)
        return end
    if tu == TimeUnit.DAY:
        end = start + timedelta(days=n)
    elif tu == TimeUnit.WEEK:
        end = start + timedelta(weeks=n)
    elif tu == TimeUnit.MONTH:
        end = start + relativedelta(months=n)
    elif tu == TimeUnit.YEAR:
        end = start + relativedelta(years=n)
    else:
        raise ValueError('unknown time unit')
    if eom == EomConvention.LAST_DAY and period.is_month_based() and is_day_last_day_of_month(start):
        return last_day_of_month(end)
    elif eom == EomConvention.LAST_BUSINESS_DAY and period.is_month_based() \
            and is_day_last_business_day_of_month(start, calendar):
        return last_business_day_of_month(end, calendar)
    else:
        return adjust_date(end, adj, calendar)


def generate_daily_schedule(start: date, end: date, calendar: HolidayCalendar) -> List[date]:
    if start > end:
        raise ValueError(f'start date is after end date')
    schedule = []
    t = start
    while t <= end:
        schedule.append(t)
        t = calendar.next(t)
    return schedule


def _time_unit_from_string(u: str) -> TimeUnit:
    unit = u.upper()
    if unit == 'B':
        return TimeUnit.BUSINESS_DAY
    elif unit == 'D':
        return TimeUnit.DAY
    elif unit == 'W':
        return TimeUnit.WEEK
    elif unit == 'M':
        return TimeUnit.MONTH
    elif unit == 'Y':
        return TimeUnit.YEAR
    else:
        raise ValueError(f'unable to parse {u} into a time unit')


_period_re = re.compile('([0-9]+)([BDWMYbdwmy])')


def period_from_string(period: str) -> Period:
    m = _period_re.match(period)
    if not m:
        raise ValueError(f'{period} is not a valid Period')
    n = int(m[1])
    u = _time_unit_from_string(m[2])
    return Period(length=n, time_unit=u)


def generate_schedule_simple(start: date,
                             end: date,
                             freq: Period,
                             bus_rule: BusinessDayConvention,
                             calendar: HolidayCalendar,
                             eom_rule: EomConvention,
                             roll_backward: bool) -> List[date]:
    adj_eom = freq.is_month_based() and \
              (eom_rule == EomConvention.LAST_DAY
               and last_day_of_month(end if roll_backward else start)) or \
              (eom_rule == EomConvention.LAST_BUSINESS_DAY
               and last_business_day_of_month(end if roll_backward else start, calendar))
    q = freq.length
    u = freq.time_unit
    dates = set()
    if roll_backward:
        t = end
        c = 1
        while t > start:
            dates.add(t)
            t = plus_period(end, Period(-c * q, u), BusinessDayConvention.NONE, calendar, EomConvention.NONE)
            if adj_eom:
                t = last_day_of_month(t) if eom_rule == EomConvention.LAST_DAY else last_business_day_of_month(t,
                                                                                                               calendar)
            c += 1
        dates.add(start)
    else:
        t = start
        c = 1
        while t < end:
            dates.add(t)
            t = plus_period(start, Period(c * q, u), BusinessDayConvention.NONE, calendar, EomConvention.NONE)
            if adj_eom:
                t = last_day_of_month(t) if eom_rule == EomConvention.LAST_DAY else last_business_day_of_month(t,
                                                                                                               calendar)
            c += 1
        dates.add(end)
    bus_dates = set()
    for t in dates:
        bus_dates.add(adjust_date(t, bus_rule, calendar))
    return sorted(list(bus_dates))


def generate_schedule_by_tenor(start: date,
                               tenor: Period,
                               freq: Period,
                               bus_rule: BusinessDayConvention,
                               calendar: HolidayCalendar,
                               eom: EomConvention = EomConvention.NONE,
                               roll_backward: bool = True) -> List[date]:
    end = plus_period(start, tenor, BusinessDayConvention.NONE, calendar, EomConvention.NONE)
    return generate_schedule_simple(start, end, freq, bus_rule, calendar, eom, roll_backward)


def get_third_wednesday_for_current_month(d: Union[date, datetime], calendars: List[HolidayCalendar]) -> date:
    first_day = date(d.year, d.month, 1)
    first_day_idx = first_day.weekday() + 1
    if first_day_idx > 3:
        wed = first_day + timedelta(days=2 * 7 + 3 + 7 - first_day_idx)
    else:
        wed = first_day + timedelta(days=2 * 7 + 3 - first_day_idx)

    is_holiday = [cld.is_holiday(wed) for cld in calendars]

    while True in is_holiday:
        wed = wed + timedelta(days=1)
        is_holiday = [cld.is_holiday(wed) for cld in calendars]
    return wed


def get_last_business_day_for_current_month(d: Union[date, datetime], calendars: List[HolidayCalendar]) -> date:
    _, end_day = monthrange(d.year, d.month)
    target_date = date(d.year, d.month, end_day)
    is_holiday = [cld.is_holiday(target_date) for cld in calendars]
    while True in is_holiday:
        target_date = target_date - timedelta(days=1)
        is_holiday = [cld.is_holiday(target_date) for cld in calendars]
    return target_date
