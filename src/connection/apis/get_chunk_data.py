import os
from datetime import datetime, date
from typing import List, Union

from src.connection.apis.extraction_creator import ExtractionCreator
from src.connection.extraction.enums.content_field_names.tick_history.intraday_content_field_names import \
    IntradaySummariesContentFieldNames
from src.connection.extraction.enums.content_field_names.tick_history.time_and_sales_content_field_names import \
    TimeAndSalesContentFieldNames
from src.connection.extraction.enums.extraction_base_enums import IdentifierType
from src.connection.utils.condition.condition import TickHistorySummaryInterval
from src.calendar import plus_period, Period, TimeUnit, EomConvention


class ChunkDataCreator:
    """Build chunked extraction requests and output paths."""

    @staticmethod
    def tick_history(
            contract_id: str,
            identifier_type: IdentifierType,
            content_field_names: List[IntradaySummariesContentFieldNames],
            summary_interval: TickHistorySummaryInterval,
            output_path: str,
            query_start_date: Union[datetime, date], query_end_date: Union[datetime, date],
            num_of_chunks: int
    ) -> (List[List[ExtractionCreator]], List[List[str]]):
        """Build chunked tick-history extraction jobs and output file paths.

        Args:
            contract_id (str): Contract identifier used in all extraction requests.
            identifier_type (IdentifierType): Identifier type used to interpret the instrument code.
            content_field_names (List[IntradaySummariesContentFieldNames]): Intraday summary fields requested for each chunk.
            summary_interval (TickHistorySummaryInterval): Aggregation interval for each intraday result set.
            output_path (str): Output directory or file path.
            query_start_date (Union[datetime, date]): Inclusive start time for the query range.
            query_end_date (Union[datetime, date]): Inclusive end time for the query range.
            num_of_chunks (int): Number of chunk groups used to partition the total date range.

        Returns:
            (List[List[ExtractionCreator]], List[List[str]]): Chunked extraction objects and their target output paths.
        """
        output_paths = []
        extractions = []

        query_start_dates = [query_start_date]

        while query_start_dates[-1] < query_end_date:
            query_start_dates.append(
                plus_period(query_start_dates[-1], Period(1, TimeUnit.MONTH), eom=EomConvention.LAST_DAY))
        #
        if query_start_dates[-1] == query_end_date:
            query_start_dates.remove(query_end_date)
        query_end_dates = query_start_dates[1:] + [query_end_date]

        total_files = len(query_start_dates)
        files_for_each_chunk = total_files // num_of_chunks + 1

        for i in range(0, num_of_chunks):
            start = i * files_for_each_chunk
            end = (i + 1) * files_for_each_chunk
            start_dates = query_start_dates[start: end]
            end_dates = query_end_dates[start: end]
            current_chunk_extractions = []
            current_chunk_output_paths = []
            for idx in range(len(start_dates)):
                extractioner = ExtractionCreator.tick_history(
                    contract_id, identifier_type, start_dates[idx], end_dates[idx],
                    content_field_names, summary_interval
                )
                output_file_id = contract_id + '_' + start_dates[idx].isoformat() + '_' + end_dates[idx].isoformat()
                current_file_output_path = f'{output_path}/{contract_id}/{start_dates[idx].year}'
                current_chunk_extractions.append(extractioner)
                current_chunk_output_paths.append(f'{current_file_output_path}/{output_file_id}.csv.gz')
                os.makedirs(current_file_output_path, exist_ok=True)

            extractions.append(current_chunk_extractions)
            output_paths.append(current_chunk_output_paths)
        return extractions, output_paths

    @staticmethod
    def time_and_sales(
            contract_id: str,
            identifier_type: IdentifierType,
            content_field_names: List[TimeAndSalesContentFieldNames],
            output_path: str,
            query_start_date: Union[datetime, date], query_end_date: Union[datetime, date],
            num_of_chunks: int
    ) -> (List[List[ExtractionCreator]], List[List[str]]):
        """Build chunked time-and-sales extraction jobs and output file paths.

        Args:
            contract_id (str): Contract identifier used in all extraction requests.
            identifier_type (IdentifierType): Identifier type used to interpret the instrument code.
            content_field_names (List[TimeAndSalesContentFieldNames]): Tick fields requested for each chunk.
            output_path (str): Output directory or file path.
            query_start_date (Union[datetime, date]): Inclusive start time for the query range.
            query_end_date (Union[datetime, date]): Inclusive end time for the query range.
            num_of_chunks (int): Number of chunk groups used to partition the total date range.

        Returns:
            (List[List[ExtractionCreator]], List[List[str]]): Chunked extraction objects and their target output paths.
        """
        output_paths = []
        extractions = []

        query_start_dates = [query_start_date]

        while query_start_dates[-1] < query_end_date:
            query_start_dates.append(
                plus_period(query_start_dates[-1], Period(1, TimeUnit.MONTH), eom=EomConvention.LAST_DAY))
        #
        if query_start_dates[-1] == query_end_date:
            query_start_dates.remove(query_end_date)
        query_end_dates = query_start_dates[1:] + [query_end_date]

        total_files = len(query_start_dates)
        files_for_each_chunk = total_files // num_of_chunks + 1

        for i in range(0, num_of_chunks):
            start = i * files_for_each_chunk
            end = (i + 1) * files_for_each_chunk
            start_dates = query_start_dates[start: end]
            end_dates = query_end_dates[start: end]
            current_chunk_extractions = []
            current_chunk_output_paths = []
            for idx in range(len(start_dates)):
                extractioner = ExtractionCreator.time_and_sales(
                    contract_id, identifier_type, start_dates[idx], end_dates[idx],
                    content_field_names
                )
                output_file_id = contract_id + '_' + start_dates[idx].isoformat() + '_' + end_dates[idx].isoformat()
                current_file_output_path = f'{output_path}/{contract_id}/{start_dates[idx].year}'
                current_chunk_extractions.append(extractioner)
                current_chunk_output_paths.append(f'{current_file_output_path}/{output_file_id}.csv.gz')
                os.makedirs(current_file_output_path, exist_ok=True)

            extractions.append(current_chunk_extractions)
            output_paths.append(current_chunk_output_paths)
        return extractions, output_paths
