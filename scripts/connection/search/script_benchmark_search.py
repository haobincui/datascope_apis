
from src.connection.features.search.enums import IdentifierType
from connection.features.search.searcher.benchmark_searcher import BenchmarkSearcher


# %% Benchmark Search example
identifier = 'A*'
identifier_type = IdentifierType.Ric
preferred_identifier_type = identifier_type

searcher = BenchmarkSearcher(identifier=identifier,
                             identifier_type=identifier_type,
                             preferred_identifier_type=preferred_identifier_type)

res = searcher.get_dict_result()
# print(res)

# results example
# results is a list of dicts:
# [
#     {
#         'Identifier': 'A+FIB3M=KBP',
#      'IdentifierType': 'Ric',
#      'Source': 'REU',
#      'Key': 'VjF8MHgwMDA0MDUwNzI4MzdkN2NlfDB4MDAwNDA1MDcyODNhYjFhNXxSRVV8Qk1SS3xCTVJLfHxLfCB8QStGSUIzTT1LQlB8',
#      'Description': 'KR - A+ Rating KRW Bank Sector 3 Month Point (KBP)',
#      'InstrumentType': 'Benchmark',
#      'Status': 'Valid'
#     },
#     {
#         'Identifier': 'A+FIB6M=KBP',
#      'IdentifierType': 'Ric',
#      'Source': 'REU',
#      'Key': 'VjF8MHgwMDA0MDUwNzI4MzdkN2NlfDB4MDAwNDA1MDcyODNhYjJhNnxSRVV8Qk1SS3xCTVJLfHxLfCB8QStGSUI2TT1LQlB8',
#      'Description': 'KR - A+ Rating KRW Bank Sector 6 Month Point (KBP)',
#      'InstrumentType': 'Benchmark',
#      'Status': 'Valid'
#     }
# ]
