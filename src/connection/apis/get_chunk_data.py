import os
from datetime import datetime, date
from typing import List, Union

from connection.apis.extraction_creator import ExtractionCreator
from connection.features.extraction.enums.content_field_names.tick_history.intraday_content_field_names import \
    IntradaySummariesContentFieldNames
from connection.features.extraction.enums.extraction_base_enums import IdentifierType
from connection.utils.condition.condition import TickHistorySummaryInterval
from src.calendar import plus_period, Period, TimeUnit, EomConvention


class ChunkDataCreator:

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
            content_field_names: List[IntradaySummariesContentFieldNames],
            output_path: str,
            query_start_date: Union[datetime, date], query_end_date: Union[datetime, date],
            num_of_chunks: int
    ) -> (List[List[ExtractionCreator]], List[List[str]]):

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
