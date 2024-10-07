import unittest

from src.market_data.contract_handler.utils import has_number_before_letter

class TestNumberBeforeText(unittest.TestCase):
    def test_has_number_before_text(self):
        option_contract_ids = ['FLG10000O20', 'FLG12750N0', 'FLG8500L3',
                               'FLG10025O0', 'FLG12750A30', 'FLG8500D3',
                               'TY80D24', 'TY80D4', 'TY100D4', 'TY100D24',
                               'TY8175D24', 'TY8175D4', 'TY10075D24', 'TY10075D4']

        for option_contract_id in option_contract_ids:
            self.assertTrue(has_number_before_letter(option_contract_id))

        future_contract_ids = ['FLGO20', 'FLGN0', 'FLGL3',
                               'FLGO0', 'FLGA30', 'FLGD3',
                               'TYD24', 'TYD4', 'TYD4', 'TYD24',
                               'TYD24', 'TYD4', 'TYD24', 'TYD4']

        for future_contract_id in future_contract_ids:
            self.assertFalse(has_number_before_letter(future_contract_id))

