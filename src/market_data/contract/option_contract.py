import re

from src.calendar.utils import call_option_maturity_month_map, put_option_maturity_month_map
from src.market_data.contract.contract import Contract
from src.market_data.contract.contract_type import ContractType
from src.utils import OptionType


class OptionContract(Contract):
    _CONTRACT_PATTERN = re.compile(
        r'(?P<Underlying>[A-Za-z]{2,3})(?P<Moneyness>\d{2,5})(?P<Month>[A-Za-z])(?P<Year>\d{1,2})'
    )

    """
    Option contract handler class.
    e.g. FLG10000O0
    """

    def __init__(self, contract_name: str, contract_type: ContractType = ContractType.Option):
        """Initialize the instance.

        Args:
            contract_name (str): Input value for contract name.
            contract_type (ContractType): Input value for contract type.

        Returns:
            None: No value is returned.
        """
        if contract_type != ContractType.Option:
            raise ValueError(f'Contract Type: [{contract_type.name}] is not Option')
        super().__init__(contract_name, contract_type)

        contract_info = self.__get_option_contract_info()
        self.__moneyness = int(contract_info['Moneyness'])
        self.__underlying = contract_info['Underlying']

        self.__maturity_year = int(contract_info['Year'])
        self.__maturity_month = contract_info['Month']

    def get_underlying(self) -> str:
        """Return underlying.

        Returns:
            str: Requested value for the lookup.
        """
        return self.__underlying

    def get_maturity_month_code(self) -> str:
        """Return maturity month code.

        Returns:
            str: Requested value for the lookup.
        """
        return self.__maturity_month

    def get_maturity_year_code(self) -> int:
        """Return maturity year code.

        Returns:
            int: Requested value for the lookup.
        """
        return self.__maturity_year

    def get_strike(self) -> float:
        """Return strike.

        Returns:
            float: Requested value for the lookup.
        """
        return self.__get_strike_price()

    def get_option_type(self) -> OptionType:
        """Return option type.

        Returns:
            OptionType: Requested value for the lookup.
        """
        if self.__maturity_month in call_option_maturity_month_map:
            return OptionType.CALL
        if self.__maturity_month in put_option_maturity_month_map:
            return OptionType.PUT
        raise ValueError(f'Invalid Option Type: [{self.contract_name}]')

    def __get_option_contract_info(self):
        # pattern = r'(?P<Underlying>\D{2,3}(?=[a-zA-Z]{1}\d{1,2}))(?P<Month>[a-zA-Z]{1}(?=\d{1,2}))(?P<Year>\d{1,2})'
        # e.g. FLG12750N0; FLG10000O0
        """Return option contract info.

        Returns:
            object: Computed result of the operation.
        """
        contract_name = self.contract_name.strip()
        res = self._CONTRACT_PATTERN.fullmatch(contract_name)
        if res is None:
            raise ValueError(f'Invalid Contract Name: [{self.contract_name}]')

        matched_res = res.groupdict()
        matched_res['Contract Name'] = contract_name
        matched_res['Month'] = matched_res['Month'].upper()
        return matched_res

    def __get_strike_price(self):
        """Return strike price.

        Returns:
            object: Computed result of the operation.
        """
        if self.__moneyness <= 100:  # 85
            return self.__moneyness
        if 100 < self.__moneyness < 5000:  # 1275, 1025, 850
            return self.__moneyness / 10

        if self.__moneyness >= 5000:  # 8225, 10025
            return self.__moneyness / 100

    def to_dict(self) -> dict:
        """Convert to dict.

        Returns:
            dict: Computed result of the operation.
        """
        return {
            'contract_name': self.contract_name,
            'underlying': self.get_underlying(),
            'contract_type': self.contract_type.name,
            'strike': self.get_strike(),
            "option_type": self.get_option_type().name,
        }
