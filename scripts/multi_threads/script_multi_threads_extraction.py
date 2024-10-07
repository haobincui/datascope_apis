import logging
import time
from datetime import datetime

from connection.features.extraction.enums.extraction_base_enums import IdentifierType
from connection.features.extraction.on_demand_extractioner.tick_history_market_depth_extractioner import \
    TickHistoryMarketDepthExtractioner
from connection.features.extraction.enums.content_field_names.tick_history.market_depth_content_field_name import \
    MarketDepthContentFieldNames
from connection.utils.condition.tick_history_market_depth_condition import TickHistoryMarketDepthCondition, \
    TickHistoryMarketDepthViewOptions
from connection.utils.instrument_identifier_list_base.instrument_identifier_list import InstrumentIdentifier, \
    InstrumentIdentifierList
from src.multi_thread import ExtractionImp

# %% setup logger
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')

# %% ids:
identifier = 'CLZ24'
identifier_type = IdentifierType.Ric
identifiers = []
for i in range(10):
    identifier = f'CLZ{int(i)}'
    identifiers.append(identifier)
identifier_list = [InstrumentIdentifier(identifier=identifier,
                                        identifier_type=identifier_type) for identifier in identifiers]

instrument_list = [InstrumentIdentifierList(identifier_list=[identifier_l],
                                           preferred_identifier_type=identifier_type) for identifier_l in identifier_list]

# %% start date and end date for 1st extraction:
query_start_date = datetime(2010, 1, 2, 0, 0, 0)
query_end_date = datetime(2023, 3, 1, 0, 0, 0)

content_field_name = MarketDepthContentFieldNames.BidPrice
content_field_names = [content_field_name, MarketDepthContentFieldNames.AskPrice]
nums_of_levels = 10
view = TickHistoryMarketDepthViewOptions.NormalizedLL2
condition = TickHistoryMarketDepthCondition(query_start_date, query_end_date, view=view,
                                            number_of_levels=nums_of_levels)
# condition = TickHistoryMarketDepthCondition(query_start_date=query_start_date_1,
#                                             query_end_date=query_end_date_1,
#                                             view=view,
#                                             number_of_levels=nums_of_levels)
extractioners = [TickHistoryMarketDepthExtractioner(instrument, content_field_names, condition) for instrument in
                 instrument_list]

# extractioner_1 = TickHistoryMarketDepthExtractioner(instrument_list,
#                                                     content_field_names,
#                                                     condition)

# %% start date and end date for 2nd extraction:
# query_start_date_2 = datetime(2022, 11, 22, 0, 0, 0)
# query_end_date_2 = datetime(2022, 11, 23, 0, 0, 0)
#
#
# condition = TickHistoryMarketDepthCondition(query_start_date=query_start_date_2,
#                                             query_end_date=query_end_date_2,
#                                             view=view,
#                                             number_of_levels=nums_of_levels)
#
# extractioner_2 = TickHistoryMarketDepthExtractioner(instrument_list,
#                                                     content_field_names,
#                                                     condition)


# %% start date and end date for 3rd extraction:
# query_start_date_3 = datetime(2022, 11, 23, 0, 0, 0)
# query_end_date_3 = datetime(2022, 11, 24, 0, 0, 0)
#
#
# condition = TickHistoryMarketDepthCondition(query_start_date=query_start_date_3,
#                                             query_end_date=query_end_date_3,
#                                             view=view,
#                                             number_of_levels=nums_of_levels)
#
# extractioner_3 = TickHistoryMarketDepthExtractioner(instrument_list,
#                                                     content_field_names,
#                                                     condition)

# %% list of extractioner:
# extractioners = [extractioner_1, extractioner_2, extractioner_3]


logging.info('Successfully created extractioners')

# %% multi threads obj:
extractioners_imp = ExtractionImp(extractioners)

# %% name of the dir for the files
# start_date = date(2022, 11, 21)

# start_datetimes = [query_start_date_1, query_start_date_2, query_start_date_3]

output_file_paths = [f'./output_docs/oil_data/{str(identifier)}.csv.gz' for identifier in identifiers]

# %% send the requests and download files
logging.info('Start downloading file')
s = time.time()
file_dirs = extractioners_imp.save_files(output_file_paths)
e = time.time()

print(f'Save successfully, time usage {e - s}')

