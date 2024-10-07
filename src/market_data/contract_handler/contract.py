from abc import ABC, abstractmethod
from datetime import date, datetime, time
from typing import Union, List, Optional

import pandas as pd
from dateutil.utils import today

from src.calendar.schedule import get_third_wednesday_for_current_month, get_last_business_day_for_current_month
from src.market_data.contract_handler.contract_type import ContractType
from src.market_data.contract_handler.utils import ContractTerminationRule
from src.calendar.holidays import HolidayCalendar

from src.calendar.utils import option_maturity_month_map, future_maturity_month_map, month_map


class Contract(ABC):

    def __init__(self, contract_name: str, contract_type: ContractType):
        self.contract_name = contract_name
        self.contract_type = contract_type

    @abstractmethod
    def get_underlying(self) -> str:
        pass

    @abstractmethod
    def get_maturity_month_code(self) -> str:
        pass

    @abstractmethod
    def get_maturity_year_code(self) -> int:
        pass

    @abstractmethod
    def to_dict(self) -> dict:
        pass

    def to_dataframe(self) -> pd.Series:
        return pd.Series(self.to_dict())

    def get_contract_maturity_dates_by_contract_id(
            self,
            data_date: Union[date, datetime],
            calendars: List[HolidayCalendar],
            termination_rule: ContractTerminationRule = ContractTerminationRule.ThirdWednessday,
            expiration_time: Optional[time] = None
    ) -> Union[date, datetime]:
        def _get_maturity(temp_date: date):
            return temp_date if not expiration_time else datetime.combine(temp_date, expiration_time)

        def _temp_year_equal_data_year():
            temp_maturity = get_maturity_date(date(temp_year, contract_maturity_month, 1), calendars)
            if temp_maturity.month > data_date.month:
                # e.g. TY80O4 maturity (2024, 3, 31), data_date(2024, 3, 16)
                return temp_maturity

            elif temp_maturity.month == data_date.month:
                if termination_rule == ContractTerminationRule.EndOfMonth:
                    return temp_maturity
                else:  # termination_rule == ContractTerminationRule.ThirdWednessday:
                    return temp_maturity if temp_maturity.day > data_date.day \
                        else get_maturity_date(date(temp_year + 10, contract_maturity_month, 1), calendars)
            else:  # temp_maturity.month < data_date.month:
                # TY80H4 e.g. maturity (2024, 8, 31), data_date (2024, 9, 16)
                return get_maturity_date(date(temp_year + 10, contract_maturity_month, 1), calendars)

        current_year = today().year
        if self.contract_type == ContractType.Option:
            _map = option_maturity_month_map
        elif self.contract_type == ContractType.Future:
            _map = future_maturity_month_map
        else:
            raise ValueError(f'Invalid Contract Type: {self.contract_type.name}')

        contract_maturity_month = month_map[_map[self.get_maturity_month_code()]]

        if termination_rule == ContractTerminationRule.ThirdWednessday:
            get_maturity_date = get_third_wednesday_for_current_month
        elif termination_rule == ContractTerminationRule.EndOfMonth:
            get_maturity_date = get_last_business_day_for_current_month
        else:
            raise ValueError(f'Invalid Termination Rule: {termination_rule.name}')

        if self.get_maturity_year_code() >= current_year % 100:
            # e.g. 25, 26, 27, maturity 2025, 2026, 2027
            contract_maturity_date = get_maturity_date(
                date(current_year // 100 * 100 + self.get_maturity_year_code(), contract_maturity_month, 1),
                calendars)
            return _get_maturity(contract_maturity_date)

        if self.get_maturity_year_code() >= 10:
            # e.g. 24, 13, 30, maturity 2024, 2013, 2030
            temp_year = int(self.get_maturity_year_code()) + data_date.year // 100 * 100
        else:
            # < 10, e.g. 4, 5, 6, # maturity: 2024, 2025, 2026 (current year: 2024)
            temp_year = int(self.get_maturity_year_code()) + data_date.year // 10 * 10

        if temp_year > data_date.year:
            return _get_maturity(get_maturity_date(date(temp_year, contract_maturity_month, 1), calendars))

        elif temp_year < data_date.year:
            return _get_maturity(get_maturity_date(date(temp_year, contract_maturity_month, 1), calendars))

        elif temp_year == data_date.year:
            return _get_maturity(_temp_year_equal_data_year())

        else:
            raise ValueError(f'Invalid Year: {temp_year}')

