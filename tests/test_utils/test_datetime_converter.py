import unittest
from datetime import date, datetime

from src.calendar.datetime_converter import DatetimeConverter


class TestDatetimeConverter(unittest.TestCase):
    def test_datetime_converter_from_str_to_date(self):
        date_str_1 = '20220113'
        date_str_2 = '2022-01-13'
        date_str_3 = '2022/01/13'
        # date_str_4 = '2022-01-13 12:00:00'
        # date_str_5 = '2022113'
        # date_str_6 = '2022-1-13'
        # date_str_7 = '2022/1/13'
        target_date = date(2022, 1, 13)

        converter = DatetimeConverter()
        res_1 = converter.from_string_to_date(date_str_1)
        res_2 = converter.from_string_to_date(date_str_2)
        res_3 = converter.from_string_to_date(date_str_3)
        # res_4 = converter.from_string_to_date(date_str_4)
        # res_5 = converter.from_string_to_date(date_str_5)
        # res_6 = converter.from_string_to_date(date_str_6)
        # res_7 = converter.from_string_to_date(date_str_7)
        res_list = [res_1, res_2, res_3,
                    # res_4, res_5, res_6, res_7
                    ]
        for ele in res_list:
            self.assertTrue(target_date == ele)

    def test_datetime_without_ms_converter_from_string_to_datetime(self):
        date_str_1_1 = '20220123 01:14:55'
        date_str_1_2 = '20220123T01:14:55'
        date_str_2_1 = '2022-01-23 01:14:55'
        date_str_2_2 = '2022-01-23T01:14:55'
        date_str_3_1 = '2022/01/23 01:14:55'
        date_str_3_2 = '2022/01/23T01:14:55'

        target_date = datetime(2022, 1, 23, 1, 14, 55)

        converter = DatetimeConverter()
        res_1_1 = converter.from_string_to_datetime(date_str_1_1)
        res_1_2 = converter.from_string_to_datetime(date_str_1_2)
        res_2_1 = converter.from_string_to_datetime(date_str_2_1)
        res_2_2 = converter.from_string_to_datetime(date_str_2_2)
        res_3_1 = converter.from_string_to_datetime(date_str_3_1)
        res_3_2 = converter.from_string_to_datetime(date_str_3_2)
        res_list = [res_1_1, res_1_2, res_2_1, res_2_2, res_3_1, res_3_2]
        for ele in res_list:
            self.assertTrue(ele == target_date)

    def test_datetime_with_ms_converter_from_string_to_datetime(self):
        date_str_1_1 = '20220123 01:14:55.820194801'
        date_str_1_2 = '20220123T01:14:55.820194801'
        date_str_1_3 = '20220123 01:14:55.820194801Z'
        date_str_1_4 = '20220123T01:14:55.820194801Z'
        date_str_2_2 = '2022-01-23T01:14:55.820194801'
        date_str_2_1 = '2022-01-23 01:14:55.820194801'
        date_str_2_3 = '2022-01-23T01:14:55.820194801Z'
        date_str_2_4 = '2022-01-23 01:14:55.820194801Z'
        date_str_3_1 = '2022/01/23 01:14:55.820194801'
        date_str_3_2 = '2022/01/23T01:14:55.820194801'
        date_str_3_3 = '2022/01/23 01:14:55.820194801Z'
        date_str_3_4 = '2022/01/23T01:14:55.820194801Z'

        target_date = datetime(2022, 1, 23, 1, 14, 55, 820194)

        converter = DatetimeConverter()
        res_1_1 = converter.from_string_to_datetime(date_str_1_1)
        res_1_2 = converter.from_string_to_datetime(date_str_1_2)
        res_1_3 = converter.from_string_to_datetime(date_str_1_3)
        res_1_4 = converter.from_string_to_datetime(date_str_1_4)
        res_2_1 = converter.from_string_to_datetime(date_str_2_1)
        res_2_2 = converter.from_string_to_datetime(date_str_2_2)
        res_2_3 = converter.from_string_to_datetime(date_str_2_3)
        res_2_4 = converter.from_string_to_datetime(date_str_2_4)
        res_3_1 = converter.from_string_to_datetime(date_str_3_1)
        res_3_2 = converter.from_string_to_datetime(date_str_3_2)
        res_3_3 = converter.from_string_to_datetime(date_str_3_3)
        res_3_4 = converter.from_string_to_datetime(date_str_3_4)
        res_list = [res_1_1, res_1_2, res_1_3, res_1_4,
                    res_2_1, res_2_2, res_2_3, res_2_4,
                    res_3_1, res_3_2, res_3_3, res_3_4]
        # print(res_list)
        for ele in res_list:

            self.assertTrue(ele == target_date)


    def test_datetime_converter_from_datetime_to_searcher_input(self):
        datetime_1 = datetime(2022, 1, 1, 0, 0, 0)
        date_1 = date(2022, 1, 1)
        target_date = '2022-01-01T00:00:00.000Z'

        converter = DatetimeConverter()
        res_1 = converter.from_datetime_to_searcher_input(datetime_1)
        res_2 = converter.from_datetime_to_searcher_input(date_1)

        self.assertTrue(res_1 == target_date)
        self.assertTrue(res_2 == target_date)

