import logging
from datetime import date

from connection.apis.extraction_creator import ExtractionCreator
from connection.features.extraction.enums.content_field_names.tick_history.intraday_content_field_names import \
    IntradaySummariesContentFieldNames
from connection.features.extraction.enums.extraction_base_enums import IdentifierType
from connection.features.extraction.on_demand_extractioner.tick_history_time_and_sales_extractioner import \
    TickHistoryTimeAndSalesRawExtractioner
from connection.utils.condition.condition import TickHistorySummaryInterval

# %% setup a logger:
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')

identifier_type = IdentifierType.ChainRIC

query_start_date = date(2023, 2, 1)
query_end_date = date(2023, 2, 2)

# query_start_date = date(2023, 2, 2)
# query_end_date = date(2023, 2, 3)
# 2023/2/2

identifier = '0#TY:'
output_path = './output/0#TY_2023_2_1_2023_2_2.csv.gz'

content_field_names = [
    IntradaySummariesContentFieldNames.Close.Ask,
    IntradaySummariesContentFieldNames.Close.Bid,
    IntradaySummariesContentFieldNames.Close.MidPrice,
]

extractioner = ExtractionCreator.tick_history(identifier,
                                              identifier_type,
                                              query_start_date,
                                              query_end_date,
                                              content_field_names,
                                              TickHistorySummaryInterval.OneMinute)
extractioner.save_output_file(output_path)
print('Finished')
