import unittest

from src.calendar.datetime_converter import str_to_int_within_dict


class TestUitls(unittest.TestCase):
    """Tests for util functions"""


    def test_str_to_int_within_dict(self):
        test_dict_1 = {'Y': '2000', 'M': '01', 'D': '01'}
        test_dict_2 = {'Y': '2000', 'M': '1', 'D': '1'}

        test_dicts = [test_dict_1, test_dict_2]

        target_dict = {'Y': 2000, 'M': 1, 'D': 1}

        res_dicts = [str_to_int_within_dict(d) for d in test_dicts]

        for res in res_dicts:
            self.assertDictEqual(target_dict, res)

