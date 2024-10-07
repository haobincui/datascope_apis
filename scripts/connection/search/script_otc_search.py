from src.connection.features.search.enums import IdentifierType, AssetStatus
from connection.features.search.searcher.otcs_searcher import OtcsSearcher

# %% otcsearch example
code = "EDM0"
id_type = IdentifierType.Ric

otc_searcher = OtcsSearcher(identifier=code,
                            identifier_type=id_type,
                            asset_status=AssetStatus.All)

res = otc_searcher.get_table_result()
print(res)

