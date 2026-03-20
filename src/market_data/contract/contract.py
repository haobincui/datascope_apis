from abc import ABC, abstractmethod
from datetime import date, datetime, time
from typing import Callable, Dict, List, Optional, Union

import pandas as pd

from src.calendar.schedule import get_third_wednesday_for_current_month, get_last_business_day_for_current_month
from src.calendar.holidays import HolidayCalendar
from src.calendar.utils import future_maturity_month_map, month_map, option_maturity_month_map
from src.market_data.contract.contract_type import ContractType
from src.market_data.contract.utils import ContractTerminationRule


class Contract(ABC):
    """Abstract base model for futures and options contract identifiers."""

    def __init__(self, contract_name: str, contract_type: ContractType):
        """Initialize contract identity metadata.

        Args:
            contract_name (str): Raw contract symbol (for example, `TYH4`).
            contract_type (ContractType): Contract family such as future or option.

        Returns:
            None: No value is returned.
        """
        self.contract_name = contract_name
        self.contract_type = contract_type

    @abstractmethod
    def get_underlying(self) -> str:
        """Return the underlying asset code for this contract.

        Returns:
            str: Underlying instrument code.
        """
        pass

    @abstractmethod
    def get_maturity_month_code(self) -> str:
        """Return the maturity month code embedded in the contract id.

        Returns:
            str: Single-letter maturity month code.
        """
        pass

    @abstractmethod
    def get_maturity_year_code(self) -> int:
        """Return the maturity year code embedded in the contract id.

        Returns:
            int: Two-digit or one-digit year code, depending on symbol format.
        """
        pass

    @abstractmethod
    def to_dict(self) -> dict:
        """Serialize contract metadata into a dictionary.

        Returns:
            dict: Dictionary representation of the contract.
        """
        pass

    def to_dataframe(self) -> pd.Series:
        """Convert the contract dictionary into a pandas Series.

        Returns:
            pd.Series: One-row style representation of contract fields.
        """
        return pd.Series(self.to_dict())

    def _get_maturity_month_lookup(self) -> Dict[str, str]:
        """Return maturity month lookup by contract type.

        Returns:
            Dict[str, str]: Map from month code (for example, `H`) to month text (`MAR`).
        """
        if self.contract_type == ContractType.Option:
            return option_maturity_month_map
        if self.contract_type == ContractType.Future:
            return future_maturity_month_map
        raise ValueError(f'Invalid Contract Type: [{self.contract_type.name}]')

    @staticmethod
    def _get_maturity_date_resolver(
        termination_rule: ContractTerminationRule,
    ) -> Callable[[date, List[HolidayCalendar]], date]:
        """Return monthly maturity-date resolver for a termination rule.

        Args:
            termination_rule (ContractTerminationRule): Rule used to derive monthly maturity.

        Returns:
            Callable[[date, List[HolidayCalendar]], date]: Function to resolve maturity date.
        """
        if termination_rule == ContractTerminationRule.ThirdWednessday:
            return get_third_wednesday_for_current_month
        if termination_rule == ContractTerminationRule.EndOfMonth:
            return get_last_business_day_for_current_month
        raise ValueError(f'Invalid Termination Rule: [{termination_rule.name}]')

    def _get_maturity_month(self) -> int:
        """Return maturity month number extracted from contract code.

        Returns:
            int: Month number in the range [1, 12].
        """
        maturity_month_code = self.get_maturity_month_code().upper()
        month_lookup = self._get_maturity_month_lookup()
        if maturity_month_code not in month_lookup:
            raise ValueError(
                f'Invalid maturity month code: [{maturity_month_code}] for contract [{self.contract_name}]'
            )
        return month_map[month_lookup[maturity_month_code]]

    def get_contract_maturity_dates_by_contract_id(
            self,
            data_date: Union[date, datetime],
            calendars: List[HolidayCalendar],
            termination_rule: ContractTerminationRule = ContractTerminationRule.ThirdWednessday,
            expiration_time: Optional[time] = None
    ) -> Union[date, datetime]:
        """Compute the maturity date for this contract under a termination rule.

        Args:
            data_date (Union[date, datetime]): Reference date used to resolve ambiguous year codes.
            calendars (List[HolidayCalendar]): Holiday calendars applied to business-day calculations.
            termination_rule (ContractTerminationRule): Rule used to derive the monthly maturity date.
            expiration_time (Optional[time]): Optional intraday time component for datetime output.

        Returns:
            Union[date, datetime]: Resolved maturity date or datetime for the contract.
        """
        reference_date = data_date.date() if isinstance(data_date, datetime) else data_date
        current_year = date.today().year
        maturity_month = self._get_maturity_month()
        year_code = int(self.get_maturity_year_code())
        get_maturity_date = self._get_maturity_date_resolver(termination_rule)

        def _attach_expiration(temp_date: date):
            """Attach expiration time when requested.

            Args:
                temp_date (date): Candidate maturity date.

            Returns:
                object: Date or datetime depending on `expiration_time`.
            """
            return temp_date if not expiration_time else datetime.combine(temp_date, expiration_time)

        def _resolve_monthly_maturity(target_year: int) -> date:
            """Resolve maturity date for a target year and contract maturity month.

            Returns:
                date: Maturity date in the target year and maturity month.
            """
            return get_maturity_date(date(target_year, maturity_month, 1), calendars)

        def _resolve_when_same_year(target_year: int) -> date:
            """Resolve maturity when decoded year equals reference date year."""
            temp_maturity = _resolve_monthly_maturity(target_year)
            if temp_maturity.month > reference_date.month:
                # e.g. TY80O4 maturity (2024-03-31), reference date (2024-03-16)
                return temp_maturity

            if temp_maturity.month < reference_date.month:
                # e.g. TY80H4 maturity (2024-08-31), reference date (2024-09-16)
                return _resolve_monthly_maturity(target_year + 10)

            # Same month.
            if termination_rule == ContractTerminationRule.EndOfMonth:
                return temp_maturity
            return temp_maturity if temp_maturity.day > reference_date.day \
                else _resolve_monthly_maturity(target_year + 10)

        if year_code >= current_year % 100:
            # e.g. 25, 26, 27, maturity 2025, 2026, 2027
            contract_maturity_date = _resolve_monthly_maturity(current_year // 100 * 100 + year_code)
            return _attach_expiration(contract_maturity_date)

        if year_code >= 10:
            # e.g. 24, 13, 30, maturity 2024, 2013, 2030
            temp_year = year_code + reference_date.year // 100 * 100
        else:
            # < 10, e.g. 4, 5, 6, # maturity: 2024, 2025, 2026 (current year: 2024)
            temp_year = year_code + reference_date.year // 10 * 10

        if temp_year != reference_date.year:
            return _attach_expiration(_resolve_monthly_maturity(temp_year))

        return _attach_expiration(_resolve_when_same_year(temp_year))
