from datetime import datetime

from connection.features.extraction.enums.content_field_names.tick_history.intraday_content_field_names import \
    IntradaySummariesContentFieldNames
from connection.features.extraction.enums.content_field_names.tick_history.time_and_sales_content_field_names import \
    TimeAndSalesContentFieldNames
from connection.features.extraction.enums.extraction_base_enums import IdentifierType
from connection.features.extraction.on_demand_extractioner.tick_history_time_and_sales_extractioner import \
    TickHistoryTimeAndSalesRawExtractioner
from connection.utils.condition.condition import TickHistorySummaryInterval
from connection.apis.extraction_creator import get_intraday_data
from connection.utils.condition.tick_history_time_and_sales_condtion import TickHistoryTimeAndSalesCondition
from connection.utils.instrument_identifier_list_base.instrument_identifier_list import InstrumentIdentifier, \
    InstrumentIdentifierList

# logging.basicConfig(level=logging.DEBUG,
#                     format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')

required_fields = [TimeAndSalesContentFieldNames.Quote.AskPrice,
                   TimeAndSalesContentFieldNames.Quote.AskSize,
                   TimeAndSalesContentFieldNames.Quote.BidPrice,
                   TimeAndSalesContentFieldNames.Quote.BidSize]

contract_ids = ['GB8Y3LSTK11=TRDL']


identifier_type = IdentifierType.Ric
query_start_dates = [
    # datetime(2023, 10, 30, 0, 0, 0),
    datetime(2024, 2, 6, 0, 0, 0),
    # datetime(2023, 5, 11, 0, 0, 0),
    # datetime(2023, 3, 23, 0, 0, 0)
    # datetime(2010, 5, 6, 0, 0, 0),
    # datetime(2022, 5, 2, 0, 0, 0)
]
query_end_dates = [
    # datetime(2023, 10, 31, 0, 0, 0),
    datetime(2024,2, 7, 0, 0, 0),
    # datetime(2023, 5, 12, 0, 0, 0),
    # datetime(2023, 3, 24, 0, 0, 0)
    # datetime(2010, 5, 7, 0, 0, 0),
    # datetime(2022, 5, 3, 0, 0, 0)
]

identifier = InstrumentIdentifier(
    identifier=contract_ids[0],
    identifier_type=identifier_type
)

instrument_list = InstrumentIdentifierList(
    identifier_list=[identifier],
    preferred_identifier_type=identifier_type
)
condition = TickHistoryTimeAndSalesCondition(
    query_start_date=query_start_dates[0],
    query_end_date=query_end_dates[0]
)

extractioner = TickHistoryTimeAndSalesRawExtractioner(
    identifier_list=instrument_list,
    times_and_sales_content_field_names=required_fields,
    condition=condition
)

res = extractioner.save_output_file('./gbp_cap.csv.gz')
print('Finished extraction')






print('Finished all')
# 3 Aug 2023
# 22 Jun 2023
# 11 May 2023
# 23 Mar 2023

# https://on.ft.com/44RMkfO
# https://www.bankofengland.co.uk/monetary-policy-summary-and-minutes/2023/august-2023
