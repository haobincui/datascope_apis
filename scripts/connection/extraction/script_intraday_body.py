import logging
from datetime import datetime

from connection.client import get_extraction_file_by_job_id, get_extraction_file_by_file_id
from connection.features.extraction.enums.content_field_names.tick_history.intraday_content_field_names import \
    IntradaySummariesContentFieldNames
from connection.features.extraction.enums.extraction_base_enums import IdentifierType
from connection.features.extraction.on_demand_extractioner.tick_history_intraday_summaries_extractioner import \
    TickHistoryIntradaySummariesExtractioner
from connection.utils.condition.tick_history_intraday_summaries_condition import TickHistoryIntradaySummariesCondition
from connection.utils.instrument_identifier_list_base.instrument_identifier_list import InstrumentIdentifier, \
    InstrumentIdentifierList

# %% setup a logger:
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')


identifier = 'EURIBOR3MD='
# identifier = 'EUR='
identifier_type = IdentifierType.Ric
identifier_list = InstrumentIdentifier(identifier=identifier,
                                       identifier_type=identifier_type)

instrument_list = InstrumentIdentifierList(identifier_list=[identifier_list],
                                           preferred_identifier_type=identifier_type)

query_start_date = datetime(2022, 10, 15, 0, 0, 0)
query_end_date = datetime(2023, 2, 7, 0, 0, 0)

# close_ask = IntradaySummariesContentFieldNames.Close.Ask
# close_bid = IntradaySummariesContentFieldNames.Close.Bid
# high = IntradaySummariesContentFieldNames.Volume.Volume
# d = IntradaySummariesContentFieldNames.Domain.Domain
# low = IntradaySummariesContentFieldNames.Low.Low
# open_ask = IntradaySummariesContentFieldNames.Open.Yield
# open_bid = IntradaySummariesContentFieldNames.Open.AskYield
# t = IntradaySummariesContentFieldNames.
open = IntradaySummariesContentFieldNames.Open.Open
# t =IntradaySummariesContentFieldNames.Close.Ask
# t2 = IntradaySummariesContentFieldNames.Close.Bid
# t3 = IntradaySummariesContentFieldNames.High.High
# t4 = IntradaySummariesContentFieldNames.High.Ask
t5 = IntradaySummariesContentFieldNames.Last.Last

content_field_names = [open]

condition = TickHistoryIntradaySummariesCondition(query_start_date=query_start_date, query_end_date=query_end_date)

extractioner = TickHistoryIntradaySummariesExtractioner(identifier_list=instrument_list,
                                                        intraday_summaries_content_field_names=content_field_names,
                                                        condition=condition)
# body = extractioner.get_body()
# path = './intraday_test3.csv'
# only can download 4-day data??????
# extractioner.save_output_file(path)
# print('finished')
# res = extractioner.get_dataframe_results()
# get_extraction_file_by_job_id(extraction_type, job_id, output_file_path, token)
file_id = 'VjF8MHgwODVhY2Y3ODgzNTg4OGM5fA'
path = './text2333.csv.gz'
get_extraction_file_by_file_id(file_id, path)
