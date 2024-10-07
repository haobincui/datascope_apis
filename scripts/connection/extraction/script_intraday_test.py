import logging
from datetime import datetime

from connection.features.extraction.enums.content_field_names.tick_history.intraday_content_field_names import \
    IntradaySummariesContentFieldNames
from connection.apis.extraction_creator import get_intraday_data


logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')


required_fields = [IntradaySummariesContentFieldNames.Open.Open]
identifier = 'EURIBOR3MD='
query_start_date = datetime(2000, 2, 2, 0, 0, 0)
query_end_date = datetime(2023, 2, 8, 0, 0, 0)

res = get_intraday_data(identifier, required_fields, query_start_date, query_end_date, multi_thread=True)
res.to_csv(f'./{identifier}-{query_start_date.date().isoformat()}-{query_end_date.date().isoformat()}.csv')

