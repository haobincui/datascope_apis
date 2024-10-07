from dataclasses import dataclass, field
from enum import Enum


class Condition:
    """
    abstract class for condition
    """
    _RelativeEndTime = 'RelativeEndTime'
    _RelativeStartDaysAgo = 'RelativeStartDaysAgo'
    _RelativeStartDaysTime = 'RelativeStartDaysTime'
    _RelativeEndDaysAgo = 'RelativeEndDaysAgo'
    _RelativeEndDaysTime = 'RelativeEndDaysTime'
    _DateRangeTimeZone = 'DateRangeTimeZone'
    _DaysAgo = 'DaysAgo'
    _DisplaySourceRIC = 'DisplaySourceRIC'
    _ExtractBy = 'ExtractBy'
    _MessageTimeStampIn = 'MessageTimeStampIn'
    _NumberOfLevels = 'NumberOfLevels'
    _Preview = 'Preview'
    _QueryEndDate = 'QueryEndDate'
    _QueryStartDate = 'QueryStartDate'
    _RelativeStartTime = 'RelativeStartTime'
    _ReportDateRangeType = 'ReportDateRangeType'
    _SortBy = 'SortBy'
    _TimeRangeMode = 'TimeRangeMode'
    _View = 'View'
    _ApplyCorrectionsAndCancellations = 'ApplyCorrectionsAndCancellations'
    _SummaryInterval = 'SummaryInterval'
    _TimebarPersistence = 'TimebarPersistence'

    dict_form: dict = field(init=False)


class TickHistoryExtractByMode(Enum):
    Entity = 'Entity'
    Ric = 'Ric'
    NONE = None


class TickHistoryTimeOptions(Enum):
    GmtUtc = 'GmtUtc'
    LocalExchangeTime = 'LocalExchangeTime'
    NONE = None


class PreviewMode(Enum):
    Content = 'Content'
    Instrument = 'Instrument'
    NONE = None


class ReportDateRangeType(Enum):
    Delta = 'Delta'
    Init = 'Init'
    Last = 'Last'
    NoRange = 'NoRange'
    PerIdentifier = 'PerIdentifier'
    Range = 'Range'
    Relative = 'Relative'
    NONE = None


class TickHistorySort(Enum):
    SingleByRic = 'SingleByRic'
    SingleByTimestamp = 'SingleByTimestamp'
    NONE = None


class TickTimeRangeMode(Enum):
    Inclusive = 'Inclusive'
    Window = 'Window'
    NONE = None


class TickHistoryTimeRangeMode(Enum):
    Inclusion = 'Inclusive'
    Window = 'Window'
    NONE = None


class TickHistorySummaryInterval(Enum):
    OneSecond = 'OneSecond'
    FiveSeconds = 'FiveSeconds'
    OneMinute = 'OneMinute'
    FiveMinutes = 'FiveMinutes'
    TenMinutes = 'TenMinutes'
    FifteenMinutes = 'FifteenMinutes'
    OneHour = 'OneHour'
    NONE = None
