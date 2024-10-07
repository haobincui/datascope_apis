import unittest
from datetime import date, time, datetime

from src.calendar.holidays import gbp_calendar, usd_calendar
from src.market_data.contract_handler.option_contract import OptionContract
from src.market_data.contract_handler.utils import ContractTerminationRule
from src.market_data.contract_handler.contract_type import ContractType
from src.utils import OptionType


class TestOptionContractHandler(unittest.TestCase):

    def test_option_contract_handler_flg(self):
        contract_name_1 = 'FLG10000O0'
        contract_name_2 = 'FLG12750N0'
        contract_name_3 = 'FLG8500L3'

        contract_handler_1 = OptionContract(contract_name=contract_name_1, contract_type=ContractType.Option)
        contract_handler_2 = OptionContract(contract_name=contract_name_2, contract_type=ContractType.Option)
        contract_handler_3 = OptionContract(contract_name=contract_name_3, contract_type=ContractType.Option)

        self.assertTrue(contract_handler_1.get_strike() == 100)
        self.assertTrue(contract_handler_1.get_maturity_year_code() == 0)
        self.assertTrue(contract_handler_1.get_underlying() == 'FLG')
        self.assertTrue(contract_handler_1.get_maturity_month_code() == 'O')
        self.assertTrue(contract_handler_1.get_option_type() == OptionType.PUT)

        self.assertTrue(contract_handler_2.get_strike() == 127.5)
        self.assertTrue(contract_handler_2.get_maturity_year_code() == 0)
        self.assertTrue(contract_handler_2.get_underlying() == 'FLG')
        self.assertTrue(contract_handler_2.get_maturity_month_code() == 'N')
        self.assertTrue(contract_handler_2.get_option_type() == OptionType.PUT)

        self.assertTrue(contract_handler_3.get_strike() == 85)
        self.assertTrue(contract_handler_3.get_maturity_year_code() == 3)
        self.assertTrue(contract_handler_3.get_underlying() == 'FLG')
        self.assertTrue(contract_handler_3.get_maturity_month_code() == 'L')
        self.assertTrue(contract_handler_3.get_option_type() == OptionType.CALL)

    def test_option_contract_handler_ty(self):
        contract_name_1 = 'TY100O0'
        contract_name_2 = 'TY12750N0'
        contract_name_3 = 'TY85L3'
        contract_name_4 = 'TY8325P24'
        contract_name_5 = 'TY1015S3'
        contract_name_6 = 'TY825S3'

        contract_handler_1 = OptionContract(contract_name=contract_name_1, contract_type=ContractType.Option)
        contract_handler_2 = OptionContract(contract_name=contract_name_2, contract_type=ContractType.Option)
        contract_handler_3 = OptionContract(contract_name=contract_name_3, contract_type=ContractType.Option)
        contract_handler_4 = OptionContract(contract_name=contract_name_4, contract_type=ContractType.Option)
        contract_handler_5 = OptionContract(contract_name=contract_name_5, contract_type=ContractType.Option)
        contract_handler_6 = OptionContract(contract_name=contract_name_6, contract_type=ContractType.Option)

        self.assertTrue(contract_handler_1.get_strike() == 100)
        self.assertTrue(contract_handler_1.get_maturity_year_code() == 0)
        self.assertTrue(contract_handler_1.get_underlying() == 'TY')
        self.assertTrue(contract_handler_1.get_maturity_month_code() == 'O')
        self.assertTrue(contract_handler_1.get_option_type() == OptionType.PUT)

        self.assertTrue(contract_handler_2.get_strike() == 127.5)
        self.assertTrue(contract_handler_2.get_maturity_year_code() == 0)
        self.assertTrue(contract_handler_2.get_underlying() == 'TY')
        self.assertTrue(contract_handler_2.get_maturity_month_code() == 'N')
        self.assertTrue(contract_handler_2.get_option_type() == OptionType.PUT)

        self.assertTrue(contract_handler_3.get_strike() == 85)
        self.assertTrue(contract_handler_3.get_maturity_year_code() == 3)
        self.assertTrue(contract_handler_3.get_underlying() == 'TY')
        self.assertTrue(contract_handler_3.get_maturity_month_code() == 'L')
        self.assertTrue(contract_handler_3.get_option_type() == OptionType.CALL)

        self.assertTrue(contract_handler_4.get_strike() == 83.25)
        self.assertTrue(contract_handler_4.get_maturity_year_code() == 24)
        self.assertTrue(contract_handler_4.get_underlying() == 'TY')
        self.assertTrue(contract_handler_4.get_maturity_month_code() == 'P')
        self.assertTrue(contract_handler_4.get_option_type() == OptionType.PUT)

        self.assertTrue(contract_handler_5.get_strike() == 101.5)
        self.assertTrue(contract_handler_5.get_maturity_year_code() == 3)
        self.assertTrue(contract_handler_5.get_underlying() == 'TY')
        self.assertTrue(contract_handler_5.get_maturity_month_code() == 'S')
        self.assertTrue(contract_handler_5.get_option_type() == OptionType.PUT)

        self.assertTrue(contract_handler_6.get_strike() == 82.5)
        self.assertTrue(contract_handler_6.get_maturity_year_code() == 3)
        self.assertTrue(contract_handler_6.get_underlying() == 'TY')
        self.assertTrue(contract_handler_6.get_maturity_month_code() == 'S')
        self.assertTrue(contract_handler_6.get_option_type() == OptionType.PUT)

    def test_get_contract_maturity_dates_by_contract_id_third_wednessday_before_maturity_1(self):
        contract_name_1 = 'FLG10000O0'
        contract_name_2 = 'FLG12750N0'
        contract_name_3 = 'FLG8500L3'
        ids = [contract_name_1, contract_name_2, contract_name_3]
        # data_date = datetime(2020, 12, 1, 0, 0, 0, 000)
        data_date = date(2020, 1, 10)
        clds = [gbp_calendar(), usd_calendar()]
        contract_termination_rule = ContractTerminationRule.ThirdWednessday
        contract_handlers = [OptionContract(contract_name=id, contract_type=ContractType.Option) for id in ids]
        contract_maturities = [contract_handler.get_contract_maturity_dates_by_contract_id(
            data_date=data_date,
            calendars=clds,
            termination_rule=contract_termination_rule
        ) for contract_handler in contract_handlers]
        # print(contract_maturities)

        target_contract_maturities = [date(2020, 3, 18),
                                      date(2020, 2, 19),
                                      date(2023, 12, 20)]
        for i, j in zip(contract_maturities, target_contract_maturities):
            self.assertTrue(i == j)

    def test_get_contract_maturity_dates_by_contract_id_third_wednessday_after_maturity_2(self):
        contract_name_1 = 'FLG10000O0'
        contract_name_2 = 'FLG12750N0'
        contract_name_3 = 'FLG8500L3'
        ids = [contract_name_1, contract_name_2, contract_name_3]
        # data_date = datetime(2020, 12, 1, 0, 0, 0, 000)
        data_date = date(2020, 3, 20)
        clds = [gbp_calendar(), usd_calendar()]
        contract_termination_rule = ContractTerminationRule.ThirdWednessday
        contract_handlers = [OptionContract(contract_name=id, contract_type=ContractType.Option) for id in ids]
        contract_maturities = [contract_handler.get_contract_maturity_dates_by_contract_id(
            data_date=data_date,
            calendars=clds,
            termination_rule=contract_termination_rule
        ) for contract_handler in contract_handlers]
        # print(contract_maturities)

        target_contract_maturities = [date(2030, 3, 20),
                                      date(2030, 2, 20),
                                      date(2023, 12, 20)]
        for i, j in zip(contract_maturities, target_contract_maturities):
            self.assertTrue(i == j)

    def test_get_contract_maturity_dates_by_contract_id_end_of_month_flg(self):
        contract_name_1 = 'FLG10000O0'
        contract_name_2 = 'FLG12750N0'
        contract_name_3 = 'FLG8500L3'
        ids = [contract_name_1, contract_name_2, contract_name_3]
        # data_date = datetime(2020, 12, 1, 0, 0, 0, 000)
        data_date = date(2020, 12, 20)
        clds = [gbp_calendar(), usd_calendar()]
        contract_termination_rule = ContractTerminationRule.EndOfMonth
        contract_handlers = [OptionContract(contract_name=id, contract_type=ContractType.Option) for id in ids]
        contract_maturities = [contract_handler.get_contract_maturity_dates_by_contract_id(
            data_date=data_date,
            calendars=clds,
            termination_rule=contract_termination_rule
        ) for contract_handler in contract_handlers]
        # print(contract_maturities)

        target_contract_maturities = [date(2030, 3, 29),
                                      date(2030, 2, 28),
                                      date(2023, 12, 29)]
        for i, j in zip(contract_maturities, target_contract_maturities):
            self.assertTrue(i == j)

    def test_get_contract_maturity_dates_by_contract_id_end_of_month_ty(self):
        contract_name_1 = 'TY11225T3'
        contract_name_2 = 'Ty10025H3'
        contract_name_3 = 'TY80E24'
        ids = [contract_name_1, contract_name_2, contract_name_3]
        # data_date = datetime(2020, 12, 1, 0, 0, 0, 000)
        data_date = date(2024, 3, 16)
        clds = [usd_calendar()]
        contract_termination_rule = ContractTerminationRule.EndOfMonth
        contract_handlers = [OptionContract(contract_name=id, contract_type=ContractType.Option) for id in ids]
        contract_maturities = [contract_handler.get_contract_maturity_dates_by_contract_id(
            data_date=data_date,
            calendars=clds,
            termination_rule=contract_termination_rule,
            expiration_time=time(20, 0, 0)
        ) for contract_handler in contract_handlers]
        # print(contract_maturities)

        target_contract_maturities = [datetime(2023, 8, 31, 20, 0, 0),
                                      datetime(2023, 8, 31, 20, 0, 0),
                                      datetime(2024, 5, 31, 20, 0, 0)]
        for i, j in zip(contract_maturities, target_contract_maturities):
            self.assertTrue(i == j)
