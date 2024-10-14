import logging
from datetime import date, datetime

from src.connection.apis.extraction_creator import ExtractionCreator
from src.connection.features.extraction.enums.content_field_names.tick_history.time_and_sales_content_field_names import \
    TimeAndSalesContentFieldNames
from src.connection.features.extraction.enums.extraction_base_enums import IdentifierType
from src.multi_thread.implement.extraction_imp import ExtractionImp

# %% setup a logger:
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')


identifier = 'CLZ24'
identifier_type = IdentifierType.Ric

ask_price = TimeAndSalesContentFieldNames.Trade.AskPrice
ask_size = TimeAndSalesContentFieldNames.Trade.Asksize

bid_price = TimeAndSalesContentFieldNames.Quote.BidPrice

content_filed_names = [ask_price, ask_size, bid_price]

# start_date = date(2023, 11, 10)
# end_date = date(2023,11,11)
#

start_datetime1 = datetime(2023,11,11,10,1,2)
end_datetime1 = datetime(2023,11,11,10,1,3)


start_datetime2 = datetime(2023,11,11,10,1,4)
end_datetime2 = datetime(2023,11,11,10,1,5)




extractioner1 = ExtractionCreator.time_and_sales(
    contract_id=identifier,
    identifier_type=identifier_type,
    query_start_date=start_datetime1,
    query_end_date=end_datetime1,
    content_field_names=content_filed_names

)

extractioner2 = ExtractionCreator.time_and_sales(
    contract_id=identifier,
    identifier_type=identifier_type,
    query_start_date=start_datetime2,
    query_end_date=end_datetime2,
    content_field_names=content_filed_names

)

# extractioners = [extractioner1, extractioner2]


# output_files = ['./testdata1.csv.gz', './testdata2.csv.gz']

# threads = ExtractionImp(extractioners=extractioners)
# threads.save_files(output_files)




extractioner1.save_output_file('./testdata.csv.gz')


print('finished!!!')






