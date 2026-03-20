
from typing import Union, Optional

from src.market_data.contract.contract_type import ContractType
from src.market_data.contract.future_contract import FutureContract
from src.market_data.contract.option_contract import OptionContract
from src.market_data.contract.utils import has_number_before_letter


class ContractHandler:
    """Represents contract handler."""
    def __init__(self, contract_name: str):
        """Initialize the instance.

        Args:
            contract_name (str): Input value for contract name.

        Returns:
            None: No value is returned.
        """
        self.contract_name = contract_name

    # contract_name: str
    # contract_type: ContractType

    def get_contract_name(self) -> str:
        """Return contract name.

        Returns:
            str: Requested value for the lookup.
        """
        return self.contract_name

    def get_contract_type(self) -> str:
        """Return contract type.

        Returns:
            str: Requested value for the lookup.
        """
        return self._get_contract_type().name

    def to_contract(self, contract_type: Optional[ContractType] = None) -> Union[OptionContract, FutureContract]:
        """Convert to contract.

        Args:
            contract_type (Optional[ContractType]): Input value for contract type.

        Returns:
            Union[OptionContract, FutureContract]: Computed result of the operation.
        """
        if contract_type is None:
            contract_type = self._get_contract_type()

        return self._to_contract(contract_type)

    def _to_contract(self, contract_type: ContractType) -> Union[OptionContract, FutureContract]:
        """Convert to contract.

        Args:
            contract_type (ContractType): Input value for contract type.

        Returns:
            Union[OptionContract, FutureContract]: Computed result of the operation.
        """
        if contract_type == ContractType.Option:
            return OptionContract(self.contract_name, ContractType.Option)
        elif contract_type == ContractType.Future:
            return FutureContract(self.contract_name, ContractType.Future)
        else:
            raise ValueError(f'Invalid Contract Type: [{contract_type.name}]')

    def _get_contract_type(self) -> ContractType:
        """Return contract type.

        Returns:
            ContractType: Computed result of the operation.
        """
        if has_number_before_letter(self.contract_name):
            return ContractType.Option
        else:
            return ContractType.Future
