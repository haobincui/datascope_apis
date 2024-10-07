import re


from src.market_data.contract_handler.contract import Contract
from src.market_data.contract_handler.contract_type import ContractType


class FutureContract(Contract):

    def __init__(self, contract_name: str, contract_type: ContractType):
        super().__init__(contract_name, contract_type)
        if contract_type != ContractType.Future:
            raise ValueError(f'Contract Type [{contract_type.name}] is not Future')
        self.contract_type = contract_type
        self.contract_name = contract_name

        self.contract_info = self._get_future_contract_info()
        if self.contract_info is None:
            raise ValueError(f'Invalidate Contract Name [{self.contract_name}]')
        self.__underlying = self.contract_info['Underlying']

        self.__contract_maturity = None
        self.__maturity_year = int(self.contract_info['Year'])
        self.__maturity_month = self.contract_info['Month']

    def get_underlying(self):
        return self.__underlying

    def get_maturity_month_code(self) -> str:
        return self.__maturity_month

    def get_maturity_year_code(self) -> int:
        return self.__maturity_year

    def _get_future_contract_info(self):
        pattern = r'(?P<Underlying>\D{2,3})(?P<Month>[a-zA-Z]{1})(?P<Year>\d{1,2})'
        req = re.compile(pattern)

        res = req.search(self.contract_name)
        if res:
            matched_res = {
                'Contract Name': f'{self.contract_name}',
                **res.groupdict()
            }
        else:
            matched_res = None
            print(f'Not Found {self.contract_name}')

        return matched_res

    def to_dict(self) -> dict:
        return {
            'contract_name': self.contract_name,
            'underlying': self.get_underlying(),
            'contract_type': self.contract_type.name,
        }


