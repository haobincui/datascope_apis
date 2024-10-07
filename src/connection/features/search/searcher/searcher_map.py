from enum import Enum

from connection.features.search.searcher.benchmark_searcher import BenchmarkSearcher
from connection.features.search.searcher.historical_searcher import HistoricalSearcher
from connection.features.search.searcher.otcs_searcher import OtcsSearcher
from connection.features.search.searcher.searcher import Searcher


class SearcherList(Enum):
    OtcsSearcher = 0
    BenchmarkSearcher = 1
    HistoricalSearcher = 2
    Others = 9


searcher_map = {
    SearcherList.OtcsSearcher: OtcsSearcher,
    SearcherList.BenchmarkSearcher: BenchmarkSearcher,
    SearcherList.HistoricalSearcher: HistoricalSearcher,
    SearcherList.Others: Searcher
}
