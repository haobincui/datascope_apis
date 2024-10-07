
from typing import Union, Optional

from src.market_data.contract_handler.contract_type import ContractType
from src.market_data.contract_handler.future_contract import FutureContract
from src.market_data.contract_handler.option_contract import OptionContract
from src.market_data.contract_handler.utils import has_number_before_letter


class ContractHandler:
    def __init__(self, contract_name: str):
        self.contract_name = contract_name

    # contract_name: str
    # contract_type: ContractType

    def get_contract_name(self) -> str:
        return self.contract_name

    def get_contract_type(self) -> str:
        return self._get_contract_type().name

    def to_contract(self, contract_type: Optional[ContractType] = None) -> Union[OptionContract, FutureContract]:
        if contract_type is None:
            contract_type = self._get_contract_type()

        return self._to_contract(contract_type)

    def _to_contract(self, contract_type: ContractType) -> Union[OptionContract, FutureContract]:
        if contract_type == ContractType.Option:
            return OptionContract(self.contract_name, ContractType.Option)
        elif contract_type == ContractType.Future:
            return FutureContract(self.contract_name, ContractType.Future)
        else:
            raise ValueError(f'Invalid Contract Type: [{contract_type.name}]')

    def _get_contract_type(self) -> ContractType:
        if has_number_before_letter(self.contract_name):
            return ContractType.Option
        else:
            return ContractType.Future
