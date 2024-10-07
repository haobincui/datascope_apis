import logging
from datetime import datetime

from connection.features.extraction.enums.content_field_names.tick_history.time_and_sales_content_field_names import \
    TimeAndSalesContentFieldNames
from connection.features.extraction.enums.extraction_base_enums import IdentifierType
from connection.features.extraction.on_demand_extractioner.tick_history_time_and_sales_extractioner import \
    TickHistoryTimeAndSalesRawExtractioner
from connection.utils.condition.tick_history_time_and_sales_condtion import TickHistoryTimeAndSalesCondition
from connection.utils.instrument_identifier_list_base.instrument_identifier_list import InstrumentIdentifier, \
    InstrumentIdentifierList

# %% setup a logger:
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')




# identifier = 'FLG9400L3' # FLG DEC3 94 C
identifier = '0#FLG'

# identifier = 'GBP10YSOCATM=ICAP' # chain: GBPSOCAPV=ICAP
identifier_type = IdentifierType.ChainRIC


query_start_date = datetime(2023, 2, 1, 0, 0, 0)
query_end_date = datetime(2023, 3, 1, 0, 0, 0)

condition = TickHistoryTimeAndSalesCondition(query_start_date=query_start_date,
                                             query_end_date=query_end_date)

# trade_ask_price = TimeAndSalesContentFieldNames.Trade.AskPrice
quote_bid_price = TimeAndSalesContentFieldNames.Quote.BidPrice
quote_ask_price = TimeAndSalesContentFieldNames.Quote.AskPrice
quote_ask_size = TimeAndSalesContentFieldNames.Quote.AskSize
quote_bid_size = TimeAndSalesContentFieldNames.Quote.BidSize
quote_ask_vol = TimeAndSalesContentFieldNames.Quote.AskImpliedVolatility
quote_bid_vol = TimeAndSalesContentFieldNames.Quote.BidImpliedVolatility


content_field_names = [quote_bid_price,
                       quote_ask_price,
                       quote_bid_size,
                       quote_ask_size,
                       quote_bid_vol,
                       quote_ask_vol,
                       # trade_ask_price
                       ]

identifier_list = InstrumentIdentifier(identifier=identifier,
                                       identifier_type=identifier_type)

instrument_list = InstrumentIdentifierList(identifier_list=[identifier_list],
                                           preferred_identifier_type=identifier_type)

extractioner = TickHistoryTimeAndSalesRawExtractioner(identifier_list=instrument_list,
                                                      times_and_sales_content_field_names=content_field_names,
                                                      condition=condition)

output_path = f'./output_docs/test_{identifier}.csv.gz'
extractioner.save_output_file(output_path)
# res = extractioner.get_text_results()

