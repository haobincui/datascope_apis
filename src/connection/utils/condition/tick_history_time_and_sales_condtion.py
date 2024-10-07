import copy
from dataclasses import dataclass
from datetime import datetime, date
from typing import Union

from src.connection.utils.condition.condition import Condition, TickHistoryExtractByMode, TickHistoryTimeOptions, \
    PreviewMode, ReportDateRangeType, TickHistorySort, TickHistoryTimeRangeMode
from src.calendar.datetime_converter import DatetimeConverter


@dataclass()
class TickHistoryTimeAndSalesCondition(Condition):
    query_start_date: Union[datetime, date]
    query_end_date: Union[datetime, date]
    apply_corrections_and_cancellations: bool = True
    date_range_time_zone: str = None
    days_ago: int = None
    display_source_ric: bool = True
    extract_by: TickHistoryExtractByMode = TickHistoryExtractByMode.Ric
    message_time_stamp_in: TickHistoryTimeOptions = TickHistoryTimeOptions.LocalExchangeTime
    preview: PreviewMode = PreviewMode.NONE
    relative_start_days_ago: int = None
    relative_start_time: str = None
    relative_end_days_ago: int = None
    relative_end_time: str = None
    report_date_range_type: ReportDateRangeType = ReportDateRangeType.Range
    sort_by: TickHistorySort = TickHistorySort.SingleByRic
    time_range_mode: TickHistoryTimeRangeMode = TickHistoryTimeRangeMode.Inclusion

    def __post_init__(self):
        datetime_converter_to_input = DatetimeConverter().from_datetime_to_searcher_input
        self.dict_form = {
            self._QueryStartDate: datetime_converter_to_input(self.query_start_date),
            self._QueryEndDate: datetime_converter_to_input(self.query_end_date),
            self._MessageTimeStampIn: self.message_time_stamp_in.value,
            self._TimeRangeMode: self.time_range_mode.value,
            self._ReportDateRangeType: self.report_date_range_type.value,
            self._Preview: self.preview.value,
            self._ExtractBy: self.extract_by.value,
            self._ApplyCorrectionsAndCancellations: self.apply_corrections_and_cancellations,
            self._DaysAgo: self.days_ago,
            self._RelativeStartDaysAgo: self.relative_start_days_ago,
            self._RelativeStartTime: self.relative_start_time,
            self._RelativeEndDaysAgo: self.relative_end_days_ago,
            self._RelativeEndTime: self.relative_end_time,
            self._DisplaySourceRIC: self.display_source_ric
        }

        temp_dict = copy.deepcopy(self.dict_form)

        for key in temp_dict.keys():
            if temp_dict.get(key) is None:
                self.dict_form.pop(key)

