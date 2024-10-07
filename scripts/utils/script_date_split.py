from datetime import date, datetime

from src.calendar import DatetimeSpliter

# start = date(2021, 1, 2)
# end = date(2021, 5, 2)
# # parts = 4
#
# # end - start
#
# date_spliter = DatetimeSpliter.split_by_parts(start, end, 5)
# print(date_spliter)
#
#
# start = datetime(2021, 1, 15, 10, 5, 0)
# end = datetime(2021, 5, 28, 10, 5, 0)
#
# date_spliter = DatetimeSpliter.split_by_parts(start, end, 4)
# print(date_spliter)

start = date(1997, 1, 30)
end = date(2023, 1, 30)

parts = DatetimeSpliter.get_parts(start, end)
print(parts)

dates = DatetimeSpliter.split_by_parts(start, end, parts)


