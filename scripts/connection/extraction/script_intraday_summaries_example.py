import logging
import time
from datetime import datetime, date

from connection.features.extraction.enums.content_field_names.tick_history.intraday_content_field_names import \
    IntradaySummariesContentFieldNames
from connection.features.extraction.enums.extraction_base_enums import IdentifierType
from connection.features.extraction.on_demand_extractioner.tick_history_intraday_summaries_extractioner import \
    TickHistoryIntradaySummariesExtractioner
from connection.utils.condition.condition import TickHistorySummaryInterval
from connection.utils.condition.tick_history_intraday_summaries_condition import TickHistoryIntradaySummariesCondition
from connection.utils.instrument_identifier_list_base.instrument_identifier_list import InstrumentIdentifier, \
    InstrumentIdentifierList

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')

identifier = '0#CL:'
# identifier = 'EUR='
identifier_type = IdentifierType.ChainRIC
identifier_list = InstrumentIdentifier(identifier=identifier,
                                       identifier_type=identifier_type)

instrument_list = InstrumentIdentifierList(identifier_list=[identifier_list],
                                           preferred_identifier_type=identifier_type)

# content_field_names = [IntradaySummariesContentFieldNames.Open.Open,
#                        IntradaySummariesContentFieldNames.Volume.Volume]
content_field_names = [IntradaySummariesContentFieldNames.Close.Ask,
                       IntradaySummariesContentFieldNames.Close.AskSize,
                       IntradaySummariesContentFieldNames.Close.Bid,
                       IntradaySummariesContentFieldNames.Close.BidSize,
                       IntradaySummariesContentFieldNames.Close.MidPrice,
                       IntradaySummariesContentFieldNames.High.MidPrice,
                       ]

query_start_date = date(2020, 1, 1)
query_end_date = date(2020, 2, 1)

condition = TickHistoryIntradaySummariesCondition(query_start_date=query_start_date, query_end_date=query_end_date,
                                                  summary_interval=TickHistorySummaryInterval.FiveMinutes)

extractioner = TickHistoryIntradaySummariesExtractioner(identifier_list=instrument_list,
                                                        intraday_summaries_content_field_names=content_field_names,
                                                        condition=condition)

logging.info('Created extractioner')

# %% save file:

# output_file_name = f'./output_docs/{identifier}_{view.value}_{nums_of_levels}_{query_start_date.isoformat()}.csv.gz'
output_file_name = f'./output_docs/CL-{query_start_date.isoformat()}-{query_end_date.isoformat()}.csv.gz'
logging.info('start downloading merged_output file')
s = time.time()
extractioner.save_output_file(output_file_name)
e = time.time()
print(f'Save success, use {e - s}s')
