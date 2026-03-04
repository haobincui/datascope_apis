import logging
import os
from datetime import date

from src.connection.apis.extraction_creator import ExtractionCreator
from src.connection.features.extraction.enums.content_field_names.tick_history.time_and_sales_content_field_names import \
    TimeAndSalesContentFieldNames
from src.connection.features.extraction.enums.extraction_base_enums import IdentifierType

# %% setup a logger:
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')





## required fields:

### Quote data:
quote_bid_price = TimeAndSalesContentFieldNames.Quote.BidPrice
quote_bid_size = TimeAndSalesContentFieldNames.Quote.BidSize
quote_bid_acc_size = TimeAndSalesContentFieldNames.Quote.AccBidOrderSize
quote_ask_price = TimeAndSalesContentFieldNames.Quote.AskPrice
quote_ask_size = TimeAndSalesContentFieldNames.Quote.AskSize
quote_acc_ask_size = TimeAndSalesContentFieldNames.Quote.AccAskOrderSize

quote_fields = [quote_ask_price, quote_ask_size, quote_bid_size, quote_bid_price]

### Trade data:
trade_price = TimeAndSalesContentFieldNames.Trade.Price
trade_size = TimeAndSalesContentFieldNames.Trade.Volume
trade_turnover = TimeAndSalesContentFieldNames.Trade.Turnover

trade_fields = [trade_price, trade_size]


## current content
"""
Change the content here to extract different data 
"""
current_content = quote_fields

# ff_output dir

# contract_id = "SPYF132537500.U"
contract_id = "0#SPY*.U"
identifier_type = IdentifierType.ChainRIC
# identifier_type = IdentifierType.Ric
start_date = date(2025, 6, 11)
end_date = date(2025, 6, 12)

output_file = "./test.csv"




# origin_trade_timestamp,series_id,product_code,main_isin,RIC,Company Name


extractioner = ExtractionCreator.time_and_sales(
    contract_id=contract_id,
    identifier_type=identifier_type,
    query_start_date=start_date,
    query_end_date=end_date,
    content_field_names=current_content
)




os.makedirs(os.path.dirname(output_file), exist_ok=True)
extractioner.save_output_file(output_file)





