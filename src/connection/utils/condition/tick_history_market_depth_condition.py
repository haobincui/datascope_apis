import copy
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from src.connection.utils.condition.condition import Condition, TickHistoryExtractByMode, TickHistoryTimeOptions, \
    PreviewMode, ReportDateRangeType, TickHistorySort, TickTimeRangeMode

from enum import Enum

from src.calendar.datetime_converter import DatetimeConverter


class TickHistoryMarketDepthViewOptions(Enum):
    LegacyLevel2 = 'LegacyLevel2'
    NormalizedLL2 = 'NormalizedLL2'
    RawMarketByOrder = 'RawMarketByOrder'
    RawMarketByPrice = 'RawMarketByPrice'
    RawMarketMaker = 'RawMarketMaker'
    NONE = None


@dataclass()
class TickHistoryMarketDepthCondition(Condition):
    query_start_date: datetime
    query_end_date: datetime
    display_source_ric: bool = True
    date_range_time_zone: Optional[str] = None
    days_ago: Optional[int] = None
    extract_by: Optional[TickHistoryExtractByMode] = TickHistoryExtractByMode.Ric
    message_time_stamp_in: Optional[TickHistoryTimeOptions] = TickHistoryTimeOptions.GmtUtc
    number_of_levels: Optional[int] = 2
    preview: Optional[PreviewMode] = PreviewMode.NONE  # NONE => return .csv.gz, CONTENT => return .csv
    relative_end_days_ago: Optional[int] = None
    relative_end_time: Optional[str] = None
    relative_start_day_ago: Optional[int] = None
    relative_start_time: Optional[str] = None
    report_date_range_type: Optional[ReportDateRangeType] = ReportDateRangeType.Range
    sort_by: Optional[TickHistorySort] = TickHistorySort.SingleByRic
    time_range_mode: Optional[TickTimeRangeMode] = TickTimeRangeMode.NONE
    view: Optional[TickHistoryMarketDepthViewOptions] = TickHistoryMarketDepthViewOptions.NormalizedLL2

    def __post_init__(self):
        datetime_converter_to_input = DatetimeConverter().from_datetime_to_searcher_input
        self.dict_form = {
            self._QueryEndDate: datetime_converter_to_input(self.query_end_date),
            self._QueryStartDate: datetime_converter_to_input(self.query_start_date),
            self._NumberOfLevels: self.number_of_levels,
            self._View: self.view.value,
            self._DateRangeTimeZone: self.date_range_time_zone,
            self._DaysAgo: self.days_ago,
            self._RelativeEndDaysAgo: self.relative_end_days_ago,
            self._RelativeEndTime: self.relative_end_time,
            self._RelativeStartDaysAgo: self.relative_start_day_ago,
            self._RelativeStartTime: self.relative_start_time,
            self._DisplaySourceRIC: self.display_source_ric,
            self._ExtractBy: self.extract_by.value,
            self._MessageTimeStampIn: self.message_time_stamp_in.value,
            self._Preview: self.preview.value,
            self._ReportDateRangeType: self.report_date_range_type.value,
            self._SortBy: self.sort_by.value,
            self._TimeRangeMode: self.time_range_mode.value,
        }

        temp_dict = copy.deepcopy(self.dict_form)

        for key in temp_dict.keys():
            if temp_dict.get(key) is None:
                self.dict_form.pop(key)

