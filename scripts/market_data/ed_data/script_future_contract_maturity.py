from datetime import date
from typing import List

from dateutil.utils import today

from src.market_data.contract_handler.future_contract import FutureContract
from market_data.contract_handler.contract_type import ContractType
from src.calendar import gbp_calendar, usd_calendar, HolidayCalendar
from src.calendar import get_third_wednesday_for_current_month
from src.calendar import future_maturity_month_map, month_map


def get_contract_maturity_dates_by_contract_ids(contract: FutureContract, calendars: List[HolidayCalendar]) -> date:
    current_year = today().year
    contract_maturity_month = month_map[future_maturity_month_map[contract.__maturity_month]]

    if int(contract.__maturity_year) > current_year // 100:
        contract_maturity_date = get_third_wednesday_for_current_month(
            date(current_year // 100 * 100 + int(contract.__maturity_year), contract_maturity_month, 1),
            calendars)
        return contract_maturity_date

    year_id = data_date.year // 10
    temp_year = int(contract.__maturity_year) + year_id * 10

    if temp_year > data_date.year:
        contract_maturity_date = get_third_wednesday_for_current_month(date(temp_year, contract_maturity_month, 1),
                                                                       calendars)
        return contract_maturity_date

    if temp_year == data_date.year:
        temp_maturity = get_third_wednesday_for_current_month(date(temp_year, contract_maturity_month, 1),
                                                              calendars)

        if temp_maturity <= data_date:
            contract_maturity_date = temp_maturity
            return contract_maturity_date
        if temp_maturity > data_date:
            contract_maturity_date = get_third_wednesday_for_current_month(
                date(temp_year + 1, contract_maturity_month, 1),
                calendars)
            return contract_maturity_date

    if temp_year < data_date.year:
        contract_maturity_date = get_third_wednesday_for_current_month(
            date(temp_year + 1, contract_maturity_month, 1),
            calendars)
        return contract_maturity_date


contract_names = ['EDH2', 'EDH24', 'EDH31']
data_date = date(2021, 1, 1)
current_date = date(2023, 11, 7)
target_contract_maturities = [date(2022, 3, 14), date(2024, 3, 14), date(2031, 3, 14)]

contracts = [FutureContract(contract_name=id, contract_type=ContractType.Future) for id in contract_names]

clds = [gbp_calendar(), usd_calendar()]

# res = [get_third_wednesday_for_current_month(day, calendars) for day in current_dates]

# req = re.compile(r'\d{2}(\d)(?=\d)')
# res = req.search('2043').group(1)


contract_maturity_dates = [get_contract_maturity_dates_by_contract_ids(c, clds) for c in contracts]

print(contract_maturity_dates)



    # temp_contract_maturity_year = int('20' + target_contract.__maturity_year)
    # contract_maturity_month = month_map[future_maturity_month_map[target_contract.__maturity_month]]
    #
    # temp_contract_maturity_date = get_third_wednesday_for_current_month(
    #     date(data_date.year, contract_maturity_month, 1),
    #     calendars)
    # if temp_contract_maturity_year > current_date.year:
    #     contract_maturity_year = temp_contract_maturity_year
    #
    # else:
    #

    # if temp_contract_maturity_date >= data_date:
    #     contract_maturity_year = temp_contract_maturity_year
    # else:
    #     if temp_contract_maturity_year == data_date.year:
    #         contract_maturity_year = data_date.year
    #     elif temp_contract_maturity_year <= data_date.year



# haobin.cui@durham.ac.uk




