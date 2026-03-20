from enum import Enum

from src.connection.search.searcher.benchmark_searcher import BenchmarkSearcher
from src.connection.search.searcher.historical_searcher import HistoricalSearcher
from src.connection.search.searcher.otcs_searcher import OtcsSearcher
from src.connection.search.searcher.searcher import Searcher


class SearcherList(Enum):
    """Represents searcher list."""
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
