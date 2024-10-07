import logging
import time
from datetime import datetime, date

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
n = 2

# %% ids:
identifier = 'CLZ24'
identifier_type = IdentifierType.Ric
identifier_list = InstrumentIdentifier(identifier=identifier,
                                       identifier_type=identifier_type)

instrument_list = InstrumentIdentifierList(identifier_list=[identifier_list],
                                           preferred_identifier_type=identifier_type)
start = datetime(2022, 10, 1, 0, 0, 0)
end = datetime(2022, 11, 1, 0, 0, 0)
dt = (end - start) / n
starts = [start + dt * i for i in range(n)]
ends = starts[1:] + [end]

content_field_name = MarketDepthContentFieldNames.BidPrice
content_field_names = [content_field_name]
nums_of_levels = 2
view = TickHistoryMarketDepthViewOptions.NormalizedLL2
conditions = [TickHistoryMarketDepthCondition(query_start_date=starts[i],
                                              query_end_date=ends[i],
                                              view=view,
                                              number_of_levels=nums_of_levels) for i in range(n)]

extractioners = [TickHistoryMarketDepthExtractioner(instrument_list,
                                                    content_field_names,
                                                    condition) for condition in conditions]

logging.info('Successfully created extractioners')

# %% multi threads obj:
extractioners_imp = ExtractionImp(extractioners)

# %% name of the dir for the files

output_file_paths = [f'./output_docs/{identifier}_{n}_test/{start_time.isoformat()}.csv.gz' for start_time in starts]

# %% send the requests and download files
logging.info('Start downloading file')
s = time.time()
file_dirs = extractioners_imp.save_files(output_file_paths)
e = time.time()

print(f'Save successfully, time usage {e - s}')
