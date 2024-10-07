from datetime import datetime

from src.connection.features.search.enums import IdentifierType
from connection.features.search.searcher.historical_searcher import HistoricalSearcher

# %% historical search example
# request example
# {
#     "Request":{
#         "Identifier": "TRI.N",
#         "IdentifierTyper": "Ric",
#         "Range": {
#             "Start": "2015-11-17T00:00:00.000Z",
#             "End": "2015-11-24T00:00:00.00Z"
#         }
#     }
# }

# res example
# res = [
#     {
#         'Identifier': 'TRI.N',
#         'IdentifierType': 'Ric',
#         'Source': '',
#         'Key': 'VjF8MHgzMDAwMDAwMDAwMDAwMDAwfDB4MzAwMDAwMDAwMDAwMDAwMHx8fHx8fHxUUkkuTnw',
#         'Description': 'Historical Instrument',
#         'InstrumentType': 'Unknown',
#         'Status': 'Valid',
#         'DomainCode': '6',
#         'FirstDate': '1996-01-02T00:00:00.000Z',
#         'LastDate': '2023-01-19T00:00:00.000Z',
#         'History': []
#     }
# ]

identifier = 'CLZ24'
identifier_typer = IdentifierType.Ric
start_date = datetime(2011, 11, 17, 0, 0, 0)
end_date = datetime(2014, 11, 24, 0, 0, 0)

searcher = HistoricalSearcher(identifier=identifier,
                              identifier_type=identifier_typer,
                              start=start_date,
                              end=end_date)
res = searcher.get_dict_result()

# print(res)

