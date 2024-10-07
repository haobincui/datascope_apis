

import logging
import os
import time
from datetime import date, datetime

from connection.features.extraction.enums.content_field_names.tick_history.intraday_content_field_names import \
    IntradaySummariesContentFieldNames
from error.error import ExtractionError
from connection.apis.extraction_creator import get_intraday_data

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')
# years = np.arange(2020, 2021, 1).tolist()
# months = np.arange(1, 12, 1).tolist()
# need 2002/05/01 - 2003/01/01
years = [2023]
months = [8]
ss = time.time()
for idx, ele in enumerate(years):
    for month in months:
        required_fields = [IntradaySummariesContentFieldNames.Low.Ask,
                           IntradaySummariesContentFieldNames.Low.Bid,
                           IntradaySummariesContentFieldNames.Low.Low,
                           IntradaySummariesContentFieldNames.High.Yield,
                           IntradaySummariesContentFieldNames.Open.Bid,
                           IntradaySummariesContentFieldNames.Close.MidPrice,
                           IntradaySummariesContentFieldNames.Close.BidYield,
                           IntradaySummariesContentFieldNames.Last.Last,
                           IntradaySummariesContentFieldNames.Volume
                           # IntradaySummariesContentFieldNames.
                           ]

        # required_fields = [IntradaySummariesContentFieldNames.Close.Bid,
        #                    IntradaySummariesContentFieldNames.Close.Ask]
        # identifier = 'EURIBOR3MD='
        # identifier = 'GBP3MFSR='
        # identifier = 'SONIAOSR='
        # identifier = '0#FLG+'
        identifier = 'FLGZ3'
        query_start_date = datetime(ele, month, 1, 0, 0, 0)
        # query_start_date =
        if month == 12:
            next_month = 1
            next_year = ele + 1
        else:
            next_month = month + 1
            next_year = ele
        query_end_date = datetime(next_year, next_month, 1, 0, 0, 0)
        if query_end_date.date() > date.today():
            query_end_date = datetime(2023, 9, 7, 0, 0, 0)
        s = time.time()
        res = get_intraday_data(identifier, required_fields, query_start_date, query_end_date, multi_thread=False)
        os.makedirs(f'./output/{identifier}/{ele}/', exist_ok=True)
        if isinstance(res, ExtractionError):
            logging.warning(f'Extraction failed: [{res.message}]')
            continue
        res.to_csv(f'./output/{identifier}/{ele}/{identifier}-{query_start_date.date().isoformat()}-{query_end_date.date().isoformat()}.csv')
        e = time.time()
        print(f'Finished extraction {query_start_date.date().isoformat()} ' + str(e-s))
        time.sleep(2)
ee = time.time()
print('Finished All!! ' + str(ee - ss))


