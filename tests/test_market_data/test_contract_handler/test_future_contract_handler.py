import unittest
from datetime import date

from src.calendar.holidays import gbp_calendar, usd_calendar
from src.market_data.contract_handler.future_contract import FutureContract
from src.market_data.contract_handler.utils import ContractTerminationRule
from src.market_data.contract_handler.contract_type import ContractType



class TestFutureContractHandler(unittest.TestCase):

    def test_future_contract_info(self):
        ids = ['EDG4', 'FFZ2', 'FFM30', 'FLGZ3', 'FLGH30', 'EDH0']

        target_underlyings = ['ED', 'FF', 'FF', 'FLG', 'FLG', 'ED']
        target_month_indicator = ['G', 'Z', 'M', 'Z', 'H', 'H']
        target_year = [4, 2, 30, 3, 30, 0]

        contract_handlers = [FutureContract(contract_name=id, contract_type=ContractType.Future) for id in ids]

        for idx, contract in enumerate(contract_handlers):
            self.assertTrue(contract.get_underlying() == target_underlyings[idx])
            self.assertTrue(contract.get_maturity_year_code() == target_year[idx])
            self.assertTrue(contract.get_maturity_month_code() == target_month_indicator[idx])

    def test_get_contract_maturity_dates_by_contract_id_third_wednessday_before_maturity_1(self):
        ids = ['EDH24', 'FFZ2', 'FFM30', 'FLGZ3', 'FLGH30', 'EDH2', 'FFZ0']
        # data_date = datetime(2020, 12, 1, 0, 0, 0, 000)
        data_date = date(2020, 12, 10)
        clds = [gbp_calendar(), usd_calendar()]
        contract_termination_rule = ContractTerminationRule.ThirdWednessday
        contract_handlers = [FutureContract(contract_name=id, contract_type=ContractType.Future) for id in ids]
        contract_maturities = [contract_handler.get_contract_maturity_dates_by_contract_id(
            data_date=data_date,
            calendars=clds,
            termination_rule=contract_termination_rule
        ) for contract_handler in contract_handlers]
        # print(contract_maturities)

        target_contract_maturities = [date(2024, 3, 20),
                                      date(2022, 12, 21),
                                      date(2030, 6, 20),
                                      date(2023, 12, 20),
                                      date(2030, 3, 20),
                                      date(2022, 3, 16),
                                      date(2020, 12, 16)]
        for i, j in zip(contract_maturities, target_contract_maturities):
            self.assertTrue(i == j)

    def test_get_contract_maturity_dates_by_contract_id_third_wednessday_after_maturity_2(self):
        ids = ['EDH24', 'FFZ2', 'FFM30', 'FLGZ3', 'FLGH30', 'EDH2', 'FFZ0']
        # data_date = datetime(2020, 12, 1, 0, 0, 0, 000)
        data_date = date(2020, 12, 20)
        clds = [gbp_calendar(), usd_calendar()]
        contract_termination_rule = ContractTerminationRule.ThirdWednessday
        contract_handlers = [FutureContract(contract_name=id, contract_type=ContractType.Future) for id in ids]
        contract_maturities = [contract_handler.get_contract_maturity_dates_by_contract_id(
            data_date=data_date,
            calendars=clds,
            termination_rule=contract_termination_rule
        ) for contract_handler in contract_handlers]
        # print(contract_maturities)

        target_contract_maturities = [date(2024, 3, 20),
                                      date(2022, 12, 21),
                                      date(2030, 6, 20),
                                      date(2023, 12, 20),
                                      date(2030, 3, 20),
                                      date(2022, 3, 16),
                                      date(2030, 12, 18)]
        for i, j in zip(contract_maturities, target_contract_maturities):
            self.assertTrue(i == j)

    def test_get_contract_maturity_dates_by_contract_id_end_of_month(self):
        ids = ['EDH24', 'FFZ2', 'FFM30', 'FLGZ3', 'FLGH30', 'EDH2', 'FFZ0']
        # data_date = datetime(2020, 12, 1, 0, 0, 0, 000)
        data_date = date(2020, 12, 20)
        clds = [gbp_calendar(), usd_calendar()]
        contract_termination_rule = ContractTerminationRule.EndOfMonth
        contract_handlers = [FutureContract(contract_name=id, contract_type=ContractType.Future) for id in ids]
        contract_maturities = [contract_handler.get_contract_maturity_dates_by_contract_id(
            data_date=data_date,
            calendars=clds,
            termination_rule=contract_termination_rule
        ) for contract_handler in contract_handlers]
        # print(contract_maturities)

        target_contract_maturities = [date(2024, 3, 28),
                                      date(2022, 12, 30),
                                      date(2030, 6, 28),
                                      date(2023, 12, 29),
                                      date(2030, 3, 29),
                                      date(2022, 3, 31),
                                      date(2020, 12, 31)]
        for i, j in zip(contract_maturities, target_contract_maturities):
            self.assertTrue(i == j)

    def test_get_contract_maturity_dates_by_contract_id_third_wednessday_before_maturity_3(self):

        ids = ['EDH0']
        # data_date = datetime(2020, 12, 1, 0, 0, 0, 000)
        data_date = date(2020, 4, 10)
        clds = [gbp_calendar(), usd_calendar()]
        contract_termination_rule = ContractTerminationRule.ThirdWednessday
        contract_handlers = [FutureContract(contract_name=id, contract_type=ContractType.Future) for id in ids]
        contract_maturities = [contract_handler.get_contract_maturity_dates_by_contract_id(
            data_date=data_date,
            calendars=clds,
            termination_rule=contract_termination_rule
        ) for contract_handler in contract_handlers]
        # print(contract_maturities)

        target_contract_maturities = [date(2030, 3, 20)]
        for i, j in zip(contract_maturities, target_contract_maturities):
            self.assertTrue(i == j)

    def test_get_contract_maturity_dates_by_contract_id_third_wednessday_before_maturity_4(self):
        ids = ['EDH24', 'FFZ2', 'FFM30', 'FLGZ3', 'FLGH30', 'EDH2', 'FFZ0']
        # data_date = datetime(2020, 12, 1, 0, 0, 0, 000)
        data_date = date(2020, 4, 2)
        clds = [gbp_calendar(), usd_calendar()]
        contract_termination_rule = ContractTerminationRule.ThirdWednessday
        contract_handlers = [FutureContract(contract_name=id, contract_type=ContractType.Future) for id in ids]
        contract_maturities = [contract_handler.get_contract_maturity_dates_by_contract_id(
            data_date=data_date,
            calendars=clds,
            termination_rule=contract_termination_rule
        ) for contract_handler in contract_handlers]
        # print(contract_maturities)

        target_contract_maturities = [date(2024, 3, 20),
                                      date(2022, 12, 21),
                                      date(2030, 6, 20),
                                      date(2023, 12, 20),
                                      date(2030, 3, 20),
                                      date(2022, 3, 16),
                                      date(2020, 12, 16)]
        for i, j in zip(contract_maturities, target_contract_maturities):
            self.assertTrue(i == j)
