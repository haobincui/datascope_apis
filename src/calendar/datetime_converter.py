import math
import re
from datetime import datetime, date
from typing import Union


#
# _datetime_matcher = re.compile(r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d*)?$')
# _date_matcher = re.compile(r'^\d{4}-\d{2}-\d{2}$')
# _time_matcher = re.compile(r'^\d{2}:\d{2}:\d{2}(\.\d*)?$')
#
#
# def _to_datetime(v):
#     if type(v) is str:
#         if _datetime_matcher.match(v):
#             return datetime.fromisoformat(v)
#         elif _date_matcher.match(v):
#             return date.fromisoformat(v)
#         elif _time_matcher.match(v):
#             return time.fromisoformat(v)
#         else:
#             return v
#     elif isinstance(v, list):
#         return [_to_datetime(s) for s in v]
#     elif isinstance(v, tuple):
#         return (_to_datetime(s) for s in v)
#     else:
#         return v

def str_to_int_within_dict(d: dict):
    res = {}
    for key in d.keys():
        res.update({key: int(d[key])})
    return res


class DatetimeConverter:
    """
    datetime converters
    """
    Time = 'T'
    Z = 'Z'

    @staticmethod
    def to_datetime(input_datetime: Union[date, datetime]) -> datetime:
        if type(input_datetime) == datetime:
            return input_datetime
        else:
            y = input_datetime.year
            m = input_datetime.month
            d = input_datetime.day
            return datetime(y, m, d, 0, 0, 0)

    @staticmethod
    def from_string_to_date(date_str: str) -> date:
        """from %Y%M%D; %Y-%M-%D; %Y/%M/%D; %Y%M%DT%H%M%S to date"""

        # 2020-12-01T00:04:23.617343162Z
        date_req = re.compile(r'(?P<Y>\d{4})[-/]?(?P<M>\d{2})[-/]?(?P<D>\d{2})')

        res_dict = str_to_int_within_dict(date_req.match(date_str).groupdict())

        res = date(res_dict['Y'], res_dict['M'], res_dict['D'])

        return res

    @staticmethod
    def from_string_to_datetime(datetime_str: str, ms: bool = True) -> datetime:
        """
        from datetime string to datetime
        :param datetime_str: %Y%M%D %h%m%s%%ms or %Y%M%DT%h%m%s%ms
        :return: datetime(y, m, d, h, m, s, ms)
        """

        datetime_with_ms_req = re.compile(
            r'(?P<Y>\d{4})[-/]?(?P<M>\d{2})[-/]?(?P<D>\d{2})[T\s](?P<h>\d{2})[-:/](?P<m>\d{2})[.-:/](?P<s>\d{2})[.-:/](?P<ms>\d*)')
        datetime_without_ms_req = re.compile(
            r'(?P<Y>\d{4})[-/]?(?P<M>\d{2})[-/]?(?P<D>\d{2})[T\s](?P<h>\d{2})[-:/](?P<m>\d{2})[.-:/](?P<s>\d{2})')

        res = datetime_with_ms_req.match(datetime_str)
        if res and ms:
            res_dict = str_to_int_within_dict(res.groupdict())

            micro_sec = res_dict['ms'] if res_dict['ms'] > 1e-5 else 1e-5
            res = datetime(res_dict['Y'], res_dict['M'], res_dict['D'],
                           res_dict['h'], res_dict['m'], res_dict['s'],
                           microsecond=res_dict['ms'] // 10 ** max(int((math.log10(micro_sec) - 5)), 0))


        else:
            # """microsecond (0-999999)"""
            res_dict = str_to_int_within_dict(datetime_without_ms_req.match(datetime_str).groupdict())
            res = datetime(res_dict['Y'], res_dict['M'], res_dict['D'], res_dict['h'], res_dict['m'], res_dict['s'])
        return res

    @staticmethod
    def from_datetime_to_searcher_input(d: Union[date, datetime]) -> str:
        """e.g. 2015-11-17T00:00:00.000Z"""
        dt = d
        if type(d) == date:
            dt = datetime(d.year, d.month, d.day)
        return dt.isoformat() + '.000Z'
