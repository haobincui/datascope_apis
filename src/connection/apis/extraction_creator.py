from datetime import date, datetime
from typing import Union, List

from connection.features.extraction.enums.content_field_names.tick_history.intraday_content_field_names import \
    IntradaySummariesContentFieldNames
from connection.features.extraction.enums.extraction_base_enums import IdentifierType
from connection.features.extraction.on_demand_extractioner.tick_history_intraday_summaries_extractioner import \
    TickHistoryIntradaySummariesExtractioner
from connection.features.extraction.on_demand_extractioner.tick_history_time_and_sales_extractioner import \
    TickHistoryTimeAndSalesRawExtractioner
from connection.utils.condition.condition import TickHistorySummaryInterval
from connection.utils.condition.tick_history_intraday_summaries_condition import TickHistoryIntradaySummariesCondition
from connection.utils.condition.tick_history_time_and_sales_condtion import TickHistoryTimeAndSalesCondition
from connection.utils.instrument_identifier_list_base.instrument_identifier_list import InstrumentIdentifier, \
    InstrumentIdentifierList


class ExtractionCreator:
    @staticmethod
    def tick_history(
            contract_id: str,
            identifier_type: IdentifierType,
            query_start_date: Union[datetime, date],
            query_end_date: Union[datetime, date],
            content_field_names: List[IntradaySummariesContentFieldNames],
            summary_interval: TickHistorySummaryInterval = TickHistorySummaryInterval.OneSecond
    ) -> TickHistoryIntradaySummariesExtractioner:
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

        extractioner = TickHistoryIntradaySummariesExtractioner(
            identifier_list=instrument_list,
            intraday_summaries_content_field_names=content_field_names,
            condition=condition
        )

        return extractioner

    @staticmethod
    def time_and_sales(
            contract_id: str,
            identifier_type: IdentifierType,
            query_start_date: Union[datetime, date],
            query_end_date: Union[datetime, date],
            content_field_names: List[IntradaySummariesContentFieldNames]
    ) -> TickHistoryTimeAndSalesRawExtractioner:
        identifier = InstrumentIdentifier(identifier=contract_id,
                                          identifier_type=identifier_type)

        instrument_list = InstrumentIdentifierList(identifier_list=[identifier],
                                                   preferred_identifier_type=identifier_type)
        condition = TickHistoryTimeAndSalesCondition(query_start_date=query_start_date,
                                                     query_end_date=query_end_date)

        extractioner = TickHistoryTimeAndSalesRawExtractioner(identifier_list=instrument_list,
                                                              times_and_sales_content_field_names=content_field_names,
                                                              condition=condition)

        return extractioner

    @staticmethod
    def market_depth():
        raise NotImplemented
