from datetime import date

from src.calendar import gbp_calendar
from src.calendar import Period, TimeUnit, plus_period

cld = gbp_calendar()

start_date = date(2023, 3, 1)
end_date = date(2024, 12, 31)

period = Period(2, TimeUnit.MONTH)

dates = [start_date]

while date(dates[-1].year, dates[-1].month, 1) < end_date:
    temp_date = plus_period(date(dates[-1].year, dates[-1].month, 1), period)
    while cld.is_holiday(temp_date):
        temp_date = plus_period(temp_date, Period(1, TimeUnit.BUSINESS_DAY))
    n = 6 - temp_date.weekday()

    if n == 6:
        temp_date = temp_date
    else:
        temp_date = plus_period(temp_date, Period(abs(n), TimeUnit.DAY))
    dates.append(temp_date)



