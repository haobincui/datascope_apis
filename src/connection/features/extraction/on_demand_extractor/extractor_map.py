from enum import Enum

from .on_demand_extractor import OnDemandExtractioner
from .tick_history_market_depth_extractor import TickHistoryMarketDepthExtractioner


class ExtractorList(Enum):
    TickHistoryMarketDepthExtractor = 1
    Others = 9


extractor_map = {
    ExtractorList.TickHistoryMarketDepthExtractor: TickHistoryMarketDepthExtractioner,
    ExtractorList.Others: OnDemandExtractioner,
}
