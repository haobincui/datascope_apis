from enum import Enum

from connection.features.extraction.on_demand_extractioner.on_demand_extractioner import OnDemandExtractioner
from connection.features.extraction.on_demand_extractioner.tick_history_market_depth_extractioner import \
    TickHistoryMarketDepthExtractioner


class ExtractionerList(Enum):
    TickHistoryMarketDepthExtractioner = 1
    Others = 9

extractioner_map = {
    ExtractionerList.TickHistoryMarketDepthExtractioner: TickHistoryMarketDepthExtractioner,
    ExtractionerList.Others: OnDemandExtractioner
}
