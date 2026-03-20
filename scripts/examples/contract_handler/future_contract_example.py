


from datetime import date
from src.calendar.holidays import gbp_calendar, usd_calendar
from src.market_data.contract.contract_type import ContractType
from src.market_data.contract.future_contract import FutureContract
from src.market_data.contract.utils import ContractTerminationRule



"""
Future Example：
'EDH0', extracted at 2020-04-10, with termination rule ThirdWednessday, the maturity date should be 2030-03-20
"""
contract = FutureContract(contract_name='EDH0', contract_type=ContractType.Future)

maturity = contract.get_contract_maturity_dates_by_contract_id(
    data_date=date(2020, 4, 10),
    calendars=[gbp_calendar(), usd_calendar()],
    termination_rule=ContractTerminationRule.ThirdWednessday,
)

print(f'contract_name: {contract.contract_name}')
print(f'underlying: {contract.get_underlying()}')
print(f'maturity_month_code: {contract.get_maturity_month_code()}')
print(f'maturity_year_code: {contract.get_maturity_year_code()}')
print(f'maturity_date: {maturity}')

# Expected value from unit test.
assert maturity == date(2030, 3, 20)
print('Future contract example passed.')


