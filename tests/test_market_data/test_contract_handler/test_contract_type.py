import unittest

from src.market_data.contract_handler.contract_handler import ContractHandler
from src.market_data.contract_handler.future_contract import FutureContract
from src.market_data.contract_handler.option_contract import OptionContract


class TestContractType(unittest.TestCase):
    def test_contract_type(self):
        future_contract_ids = ['FLGO20', 'FLGN0', 'FLGL3',
                               'FLGO0', 'FLGA30', 'FLGD3',
                               'TYD24', 'TYD4', 'TYD4', 'TYD24',
                               'TYD24', 'TYD4', 'TYD24', 'TYD4']
        option_contract_ids = ['FLG10000O20', 'FLG12750N0', 'FLG8500L3',
                               'FLG10025O0', 'FLG12750A30', 'FLG8500D3',
                               'TY80D24', 'TY80D4', 'TY100D4', 'TY100D24',
                               'TY8175D24', 'TY8175D4', 'TY10075D24', 'TY10075D4']

        future_contract_type = 'Future'
        option_contract_type = 'Option'

        for future_contract_id in future_contract_ids:
            self.assertEqual(ContractHandler(future_contract_id).get_contract_type(), future_contract_type)

        for option_contract_id in option_contract_ids:
            self.assertEqual(ContractHandler(option_contract_id).get_contract_type(), option_contract_type)

    def test_contract_obj(self):
        future_contract_ids = ['FLGO20', 'FLGN0', 'FLGL3',
                               'FLGO0', 'FLGA30', 'FLGD3',
                               'TYD24', 'TYD4', 'TYD4', 'TYD24',
                               'TYD24', 'TYD4', 'TYD24', 'TYD4']
        option_contract_ids = ['FLG10000O20', 'FLG12750N0', 'FLG8500L3',
                               'FLG10025O0', 'FLG12750A30', 'FLG8500D3',
                               'TY80D24', 'TY80D4', 'TY100D4', 'TY100D24',
                               'TY8175D24', 'TY8175D4', 'TY10075D24', 'TY10075D4']
        future_contract_obj = FutureContract
        option_contract_obj = OptionContract

        for future_contract_id in future_contract_ids:
            self.assertEqual(type(ContractHandler(future_contract_id).to_contract()), future_contract_obj)

        for option_contract_id in option_contract_ids:
            self.assertEqual(type(ContractHandler(option_contract_id).to_contract()), option_contract_obj)
