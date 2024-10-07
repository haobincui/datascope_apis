import copy
from dataclasses import dataclass
from datetime import datetime, date
from typing import Union

from src.connection.utils.condition.condition import Condition, TickHistoryExtractByMode, TickHistoryTimeOptions, \
    PreviewMode, ReportDateRangeType, TickHistorySort, TickHistorySummaryInterval, TickHistoryTimeRangeMode
from src.calendar.datetime_converter import DatetimeConverter


@dataclass()
class TickHistoryIntradaySummariesCondition(Condition):
    query_start_date: Union[datetime, date]
    query_end_date: Union[datetime, date]
    display_source_ric: bool = True
    date_range_time_zone: str = None
    days_ago: int = None
    relative_start_days_ago: int = None
    relative_start_time: str = None
    relative_end_days_ago: int = None
    relative_end_time: str = None
    preview: PreviewMode = PreviewMode.NONE
    extract_by: TickHistoryExtractByMode = TickHistoryExtractByMode.Ric
    message_time_stamp_in: TickHistoryTimeOptions = TickHistoryTimeOptions.GmtUtc
    report_date_range_type: ReportDateRangeType = ReportDateRangeType.Range
    sort_by: TickHistorySort = TickHistorySort.SingleByRic
    summary_interval: TickHistorySummaryInterval = TickHistorySummaryInterval.OneMinute
    time_bar_persistence: bool = False
    time_range_mode: TickHistoryTimeRangeMode = TickHistoryTimeRangeMode.NONE

    def __post_init__(self):
        datetime_converter_to_input = DatetimeConverter().from_datetime_to_searcher_input
        self.dict_form = {
            self._QueryStartDate: datetime_converter_to_input(self.query_start_date),
            self._QueryEndDate: datetime_converter_to_input(self.query_end_date),
            self._DisplaySourceRIC: self.display_source_ric,
            self._DateRangeTimeZone: self.date_range_time_zone,
            self._DaysAgo: self.days_ago,
            self._RelativeStartDaysAgo: self.relative_start_days_ago,
            self._RelativeStartTime: self.relative_start_time,
            self._RelativeEndDaysAgo: self.relative_end_days_ago,
            self._RelativeEndTime: self.relative_end_time,
            self._Preview: self.preview.value,
            self._MessageTimeStampIn: self.message_time_stamp_in.value,
            self._ReportDateRangeType: self.report_date_range_type.value,
            self._ExtractBy: self.extract_by.value,
            self._SortBy: self.sort_by.value,
            self._SummaryInterval: self.summary_interval.value,
            self._TimebarPersistence: self.time_bar_persistence,
            self._TimeRangeMode: self.time_range_mode.value,
        }

        temp_dict = copy.deepcopy(self.dict_form)

        for key in temp_dict.keys():
            if temp_dict.get(key) is None:
                self.dict_form.pop(key)




