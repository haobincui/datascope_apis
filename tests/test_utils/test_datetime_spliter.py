import unittest
from datetime import datetime, date

from src.calendar.date_spliter import DatetimeSpliter, DateSplitPartUnit


class TestDatetimeSpliter(unittest.TestCase):

    def test_datetime_spliter_by_year(self):
        start = date(2010, 1, 1)
        end = date(2015, 1, 1)

        dates = DatetimeSpliter.split_by_parts(start, end, 5)

        start_time = datetime(2010, 1, 3, 10, 5, 0)
        end_time = datetime(2015, 1, 5, 11, 5)

        datetimes = DatetimeSpliter.split_by_parts(start_time, end_time, 5)

        target_dates = [datetime(2010, 1, 1, 0, 0, 0),
                        datetime(2011, 1, 1, 0, 0, 0),
                        datetime(2012, 1, 1, 0, 0, 0),
                        datetime(2013, 1, 1, 0, 0, 0),
                        datetime(2014, 1, 1, 0, 0, 0),
                        datetime(2015, 1, 1, 0, 0, 0)]

        target_datetimes = [datetime(2010, 1, 3, 10, 5, 0),
                            datetime(2011, 1, 3, 10, 5, 0),
                            datetime(2012, 1, 3, 10, 5, 0),
                            datetime(2013, 1, 3, 10, 5, 0),
                            datetime(2014, 1, 3, 10, 5, 0),
                            datetime(2015, 1, 5, 11, 5, 0)]

        for d, td in zip(dates, target_dates):
            self.assertTrue(d == td)

        for dt, tdt in zip(datetimes, target_datetimes):
            self.assertTrue(dt == tdt)

    def test_datetime_spliter_by_month(self):
        datetime_spliter = DatetimeSpliter()
        start = date(2021, 1, 2)
        end = date(2021, 5, 2)

        dates = DatetimeSpliter.split_by_parts(start, end, 4)

        start_time = datetime(2021, 1, 15, 10, 5, 0)
        end_time = datetime(2021, 5, 28, 10, 5, 0)

        datetimes = DatetimeSpliter.split_by_parts(start_time, end_time, 4)

        target_dates = [datetime(2021, 1, 2, 0, 0, 0),
                        datetime(2021, 2, 2, 0, 0, 0),
                        datetime(2021, 3, 2, 0, 0, 0),
                        datetime(2021, 4, 2, 0, 0, 0),
                        datetime(2021, 5, 2, 0, 0, 0)]
        target_datetimes = [datetime(2021, 1, 15, 10, 5, 0),
                            datetime(2021, 2, 15, 10, 5, 0),
                            datetime(2021, 3, 15, 10, 5, 0),
                            datetime(2021, 4, 15, 10, 5, 0),
                            datetime(2021, 5, 28, 10, 5, 0)]

        for d, td in zip(dates, target_dates):
            self.assertTrue(d == td)

        for dt, tdt in zip(datetimes, target_datetimes):
            self.assertTrue(dt == tdt)

    def test_get_parts(self):
        parts = []
        target_parts = []
        start_y = datetime(2010, 1, 1, 10, 0, 1)
        end_y = datetime(2015, 10, 1, 5, 10, 5)

        part_1 = DatetimeSpliter.get_parts(start_y, end_y)
        target_part_1 = 5
        parts.append(part_1)
        target_parts.append(target_part_1)

        start_m = datetime(2010, 1, 2, 10, 0, 5)
        end_m = datetime(2011, 10, 5, 6, 0, 7)
        part_2 = DatetimeSpliter.get_parts(start_m, end_m)
        target_part_2 = 9 + 12
        parts.append(part_2)
        target_parts.append(target_part_2)

        start_d = datetime(2010, 1, 2, 10, 0, 5)
        end_d = datetime(2011, 2, 3, 10, 0, 5)

        part_3 = DatetimeSpliter.get_parts(start_d, end_d, DateSplitPartUnit.DAY)
        target_part_3 = 32 + 365
        parts.append(part_3)
        target_parts.append(target_part_3)

        start_d_2 = datetime(2010, 1, 2, 10, 0, 5)
        end_d_2 = datetime(2010, 2, 3, 10, 0, 5)

        part_4 = DatetimeSpliter.get_parts(start_d_2, end_d_2)
        target_part_4 = 32
        parts.append(part_4)
        target_parts.append(target_part_4)

        for part, target_part in zip(parts, target_parts):
            self.assertAlmostEqual(part, target_part, delta=1e-14)




