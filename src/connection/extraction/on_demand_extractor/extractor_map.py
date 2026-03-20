from enum import Enum

from .on_demand_extractor import OnDemandExtractor
from .tick_history_market_depth_extractor import TickHistoryMarketDepthExtractor


class ExtractorList(Enum):
    """Represents extractor list."""
    TickHistoryMarketDepthExtractor = 1
    Others = 9


extractor_map = {
    ExtractorList.TickHistoryMarketDepthExtractor: TickHistoryMarketDepthExtractor,
    ExtractorList.Others: OnDemandExtractor,
}
