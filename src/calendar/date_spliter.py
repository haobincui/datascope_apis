import logging
from datetime import date, datetime, timedelta
from enum import Enum
from typing import Union, List
from dateutil.relativedelta import relativedelta

from src.calendar.datetime_converter import DatetimeConverter


class DateSplitPartUnit(Enum):
    DAY = 1
    MONTH = 2
    YEAR = 3
    NONE = 0


class DatetimeSpliter:
    @staticmethod
    def split_by_year(start_date: Union[date, datetime], end_date: Union[date, datetime], parts: int) -> List[datetime]:
        datetime_converter = DatetimeConverter()
        start_date = datetime_converter.to_datetime(start_date)
        end_date = datetime_converter.to_datetime(end_date)

        ey = end_date.year
        sy = start_date.year

        dy = ey - sy
        if dy == 0:
            raise ValueError('Years should be different')

        if dy < parts:
            if parts < 2:
                return [start_date, end_date]
            else:
                raise ValueError(f'Parts [{parts}] need to equal or greater than the Year difference [{dy}]')
        else:
            dt = dy // parts
            dates = [start_date + relativedelta(years=dt * i) for i in range(parts)]
            # dates = [start_date.replace(year=start_date.year + dt * i) for i in range(parts)]
            dates.append(end_date)

            return dates

    @staticmethod
    def split_by_month(start_date: Union[date, datetime], end_date: Union[date, datetime], parts: int) -> List[
        datetime]:
        datetime_converter = DatetimeConverter()
        start_date = datetime_converter.to_datetime(start_date)
        end_date = datetime_converter.to_datetime(end_date)

        ey = end_date.year
        sy = start_date.year

        em = end_date.month
        sm = start_date.month

        dy = ey - sy
        dm = em - sm

        total_dm = dy * 12 + dm
        if total_dm == 0:
            raise ValueError('Total month difference is 0')

        if total_dm < parts:
            if parts < 2:
                return [start_date, end_date]
            else:
                raise ValueError(f'Parts [{parts}] need to equal or greater than the Month difference [{total_dm}]')
        else:
            dt = total_dm // parts
            dates = [start_date + relativedelta(months=dt * i) for i in range(parts)]
            # dates = [start_date.replace(month=start_date.month + dt * i) for i in range(parts)]
            dates.append(end_date)

            return dates

    @staticmethod
    def split_by_day(start_date: Union[date, datetime], end_date: Union[date, datetime], parts: int) -> List[datetime]:
        datetime_converter = DatetimeConverter()
        start_date = datetime_converter.to_datetime(start_date)
        end_date = datetime_converter.to_datetime(end_date)

        dt = ((end_date - start_date) / parts)

        if dt >= timedelta(days=1):
            dates = [start_date + dt * i for i in range(parts)]
            dates.append(end_date)
        else:
            dates = [start_date, end_date]
        return dates

    @staticmethod
    def split_by_parts(start_date: Union[date, datetime], end_date: Union[date, datetime], parts: int) -> List[
        datetime]:

        if start_date.month == end_date.month:
            try:
                dates = DatetimeSpliter.split_by_year(start_date, end_date, parts)
                return dates
            except Exception as e:
                logging.debug(f'Failed to split by Year [{e}]')
                pass
        try:
            dates = DatetimeSpliter.split_by_month(start_date, end_date, parts)
            return dates
        except Exception as e:
            logging.debug(f'Failed to split by Month [{e}]')
            pass

        dates = DatetimeSpliter.split_by_day(start_date, end_date, parts)
        logging.debug(f'Succeed to split by dates')
        return dates

    @staticmethod
    def get_parts(start_date: Union[date, datetime], end_date: Union[date, datetime],
                  part_unit: DateSplitPartUnit = DateSplitPartUnit.NONE) -> int:
        datetime_converter = DatetimeConverter()
        start_date = datetime_converter.to_datetime(start_date)
        end_date = datetime_converter.to_datetime(end_date)

        if part_unit == DateSplitPartUnit.DAY:
            return (end_date - start_date).days

        if part_unit == DateSplitPartUnit.MONTH:
            ys = end_date.year - start_date.year
            return ys * 12 + end_date.month - start_date.month

        if part_unit == DateSplitPartUnit.YEAR:
            return end_date.year - start_date.year

        part_unit = DateSplitPartUnit.DAY
        parts = DatetimeSpliter.get_parts(start_date, end_date, part_unit)
        if parts >= 40:
            part_unit = DateSplitPartUnit.MONTH
            parts = DatetimeSpliter.get_parts(start_date, end_date, part_unit)

        if parts >= 40:
            part_unit = DateSplitPartUnit.YEAR
            parts = DatetimeSpliter.get_parts(start_date, end_date, part_unit)

        if parts < 2:
            parts = 1
        logging.debug(f'Can be split into [{parts}] parts by [{part_unit.name}]')
        return parts
