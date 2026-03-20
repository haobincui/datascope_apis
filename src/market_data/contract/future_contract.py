import re
from typing import Dict


from src.market_data.contract.contract import Contract
from src.market_data.contract.contract_type import ContractType


class FutureContract(Contract):
    _CONTRACT_PATTERN = re.compile(
        r'(?P<Underlying>[A-Za-z]{2,3})(?P<Month>[A-Za-z])(?P<Year>\d{1,2})'
    )

    """Represents future contract."""
    def __init__(self, contract_name: str, contract_type: ContractType):
        """Initialize the instance.

        Args:
            contract_name (str): Input value for contract name.
            contract_type (ContractType): Input value for contract type.

        Returns:
            None: No value is returned.
        """
        if contract_type != ContractType.Future:
            raise ValueError(f'Contract Type [{contract_type.name}] is not Future')
        super().__init__(contract_name, contract_type)

        contract_info = self._get_future_contract_info()
        self.__underlying = contract_info['Underlying']

        self.__maturity_year = int(contract_info['Year'])
        self.__maturity_month = contract_info['Month']

    def get_underlying(self):
        """Return underlying.

        Returns:
            object: Requested value for the lookup.
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

    def _get_future_contract_info(self):
        """Return future contract info.

        Returns:
            object: Computed result of the operation.
        """
        contract_name = self.contract_name.strip()
        res = self._CONTRACT_PATTERN.fullmatch(contract_name)
        if res is None:
            raise ValueError(f'Invalid Contract Name [{self.contract_name}]')

        matched_res: Dict[str, str] = res.groupdict()
        matched_res['Contract Name'] = contract_name
        matched_res['Underlying'] = matched_res['Underlying'].upper()
        matched_res['Month'] = matched_res['Month'].upper()
        return matched_res

    def to_dict(self) -> dict:
        """Convert to dict.

        Returns:
            dict: Computed result of the operation.
        """
        return {
            'contract_name': self.contract_name,
            'underlying': self.get_underlying(),
            'contract_type': self.contract_type.name,
        }

