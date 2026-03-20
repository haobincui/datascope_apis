from datetime import date, datetime
from typing import Union, List

from io import StringIO
import pandas as pd

from src.connection.extraction.enums.content_field_names.tick_history.intraday_content_field_names import \
    IntradaySummariesContentFieldNames
from src.connection.extraction.enums.content_field_names.tick_history.time_and_sales_content_field_names import \
    TimeAndSalesContentFieldNames
from src.connection.extraction.enums.extraction_base_enums import IdentifierType
from src.connection.extraction.on_demand_extractor.tick_history_intraday_summaries_extractor import \
    TickHistoryIntradaySummariesExtractor
from src.connection.extraction.on_demand_extractor.tick_history_time_and_sales_extractor import \
    TickHistoryTimeAndSalesRawExtractor
from src.connection.utils.condition.condition import TickHistorySummaryInterval
from src.connection.utils.condition.tick_history_intraday_summaries_condition import TickHistoryIntradaySummariesCondition
from src.connection.utils.condition.tick_history_time_and_sales_condition import TickHistoryTimeAndSalesCondition
from src.connection.utils.instrument_identifier_list_base.instrument_identifier_list import InstrumentIdentifier, \
    InstrumentIdentifierList
from src.error.error import ExtractionError


class ExtractionCreator:
    """Factory for creating extraction request objects."""

    @staticmethod
    def tick_history(
            contract_id: str,
            identifier_type: IdentifierType,
            query_start_date: Union[datetime, date],
            query_end_date: Union[datetime, date],
            content_field_names: List[IntradaySummariesContentFieldNames],
            summary_interval: TickHistorySummaryInterval = TickHistorySummaryInterval.OneSecond
    ) -> TickHistoryIntradaySummariesExtractor:
        """Create a tick-history intraday summaries extractor.

        Args:
            contract_id (str): Contract identifier used in the request.
            identifier_type (IdentifierType): Identifier type used to interpret the instrument code.
            query_start_date (Union[datetime, date]): Inclusive start time for the query range.
            query_end_date (Union[datetime, date]): Inclusive end time for the query range.
            content_field_names (List[IntradaySummariesContentFieldNames]): Intraday summary fields to include in the output.
            summary_interval (TickHistorySummaryInterval): Aggregation interval for the intraday summary bars.

        Returns:
            TickHistoryIntradaySummariesExtractor: Configured extractor ready for execution.
        """
        identifier = InstrumentIdentifier(
            identifier=contract_id,
            identifier_type=identifier_type
        )

        instrument_list = InstrumentIdentifierList(
            identifier_list=[identifier],
            preferred_identifier_type=identifier_type
        )
        condition = TickHistoryIntradaySummariesCondition(
            query_start_date=query_start_date,
            query_end_date=query_end_date,
            summary_interval=summary_interval
        )

        extractor = TickHistoryIntradaySummariesExtractor(
            identifier_list=instrument_list,
            intraday_summaries_content_field_names=content_field_names,
            condition=condition
        )

        return extractor

    @staticmethod
    def time_and_sales(
            contract_id: str,
            identifier_type: IdentifierType,
            query_start_date: Union[datetime, date],
            query_end_date: Union[datetime, date],
            content_field_names: List[TimeAndSalesContentFieldNames]
    ) -> TickHistoryTimeAndSalesRawExtractor:
        """Create a tick-history time-and-sales extractor.

        Args:
            contract_id (str): Contract identifier used in the request.
            identifier_type (IdentifierType): Identifier type used to interpret the instrument code.
            query_start_date (Union[datetime, date]): Inclusive start time for the query range.
            query_end_date (Union[datetime, date]): Inclusive end time for the query range.
            content_field_names (List[TimeAndSalesContentFieldNames]): Tick fields to include in the time-and-sales result.

        Returns:
            TickHistoryTimeAndSalesRawExtractor: Configured extractor ready for execution.
        """
        identifier = InstrumentIdentifier(identifier=contract_id,
                                          identifier_type=identifier_type)

        instrument_list = InstrumentIdentifierList(identifier_list=[identifier],
                                                   preferred_identifier_type=identifier_type)
        condition = TickHistoryTimeAndSalesCondition(query_start_date=query_start_date,
                                                     query_end_date=query_end_date)

        extractor = TickHistoryTimeAndSalesRawExtractor(
            identifier_list=instrument_list,
            times_and_sales_content_field_names=content_field_names,
            condition=condition,
        )

        return extractor

    @staticmethod
    def market_depth():
        """Placeholder for market-depth extraction factory.

        Returns:
            None: No value is returned.
        """
        raise NotImplementedError


def get_intraday_data(
    identifier: str,
    required_fields: List[IntradaySummariesContentFieldNames],
    query_start_date: Union[datetime, date],
    query_end_date: Union[datetime, date],
    *,
    identifier_type: IdentifierType = IdentifierType.Ric,
    summary_interval: TickHistorySummaryInterval = TickHistorySummaryInterval.OneSecond,
    multi_thread: bool = False,
    token=None,
):
    """Fetch intraday data and return it as a DataFrame for legacy scripts.

    Args:
        identifier (str): Contract identifier used in the extraction request.
        required_fields (List[IntradaySummariesContentFieldNames]): Intraday summary fields to request.
        query_start_date (Union[datetime, date]): Inclusive query start date or datetime.
        query_end_date (Union[datetime, date]): Inclusive query end date or datetime.
        identifier_type (IdentifierType): Identifier type for the provided contract.
        summary_interval (TickHistorySummaryInterval): Aggregation interval for summary rows.
        multi_thread (bool): Backward-compatible flag retained for script callers.
        token: Optional auth token object or token string.

    Returns:
        Union[pd.DataFrame, ExtractionError]: Parsed intraday data on success, otherwise the raised extraction error object.
    """
    _ = multi_thread  # keep signature stable for script callers; extraction is single request.
    extractor = ExtractionCreator.tick_history(
        contract_id=identifier,
        identifier_type=identifier_type,
        query_start_date=query_start_date,
        query_end_date=query_end_date,
        content_field_names=required_fields,
        summary_interval=summary_interval,
    )
    try:
        text = extractor.get_text_results(token=token)
        return pd.read_csv(StringIO(text))
    except ExtractionError as exc:
        return exc
