from datetime import datetime, date

from src.calendar import DatetimeConverter

datetime_1 = datetime(2022, 1, 1, 0, 0, 30)
date_1 = date(2022 ,1 ,1)

converter = DatetimeConverter()
res_1 = converter.from_datetime_to_searcher_input(datetime_1)
res_2 = converter.from_datetime_to_searcher_input(date_1)
print(res_1, res_2)
print(datetime_1.isoformat())