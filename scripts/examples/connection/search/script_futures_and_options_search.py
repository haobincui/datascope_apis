from src.connection.search.enums import IdentifierType
from src.connection.search.searcher.futures_and_options_searcher import FuturesAndOptionSearcher

# exchange_codes = ['IMM']
identifier_type = IdentifierType.Ric
# identifier = 'FLG9400L3'
identifier = 'EDM20'

searcher = FuturesAndOptionSearcher(identifier=identifier,
                                    identifier_type=identifier_type,
                                    # exchange_codes=exchange_codes,
                                    max_page_size=10
                                    )

res = searcher.get_dict_result()
print(res)




