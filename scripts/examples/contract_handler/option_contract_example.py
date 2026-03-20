from datetime import date, datetime, time

from src.calendar.holidays import usd_calendar
from src.market_data.contract.contract_type import ContractType
from src.market_data.contract.option_contract import OptionContract
from src.market_data.contract.utils import ContractTerminationRule



"""
Option Example：
'TY80E24', extracted at 2024-03-16, with termination rule EndOfMonth, the maturity date should be 2024-05-31 20:00:00
"""
contract = OptionContract(contract_name='TY80E24', contract_type=ContractType.Option)

maturity = contract.get_contract_maturity_dates_by_contract_id(
    data_date=date(2024, 3, 16),
    calendars=[usd_calendar()],
    termination_rule=ContractTerminationRule.EndOfMonth,
    expiration_time=time(20, 0, 0),
)

print(f'contract_name: {contract.contract_name}')
print(f'underlying: {contract.get_underlying()}')
print(f'strike: {contract.get_strike()}')
print(f'option_type: {contract.get_option_type().name}')
print(f'maturity_month_code: {contract.get_maturity_month_code()}')
print(f'maturity_year_code: {contract.get_maturity_year_code()}')
print(f'maturity_datetime: {maturity}')

# Expected value from unit test.
assert maturity == datetime(2024, 5, 31, 20, 0, 0)
print('Option contract example passed.')


