import logging
import os
from abc import ABC, abstractmethod

import pandas as pd

from src.connection.infra.http import get_extraction_data_by_job_id, get_extraction_file_by_job_id, get_job_id_by_location, post_extractions_request
from src.connection.extraction.enums.extraction_types import ExtractionTypes
from src.error.error import ExtractionError


class OnDemandExtractor(ABC):
    """
    Abstract class for on-demand extractors.
    """

    _IdentifierList = 'IdentifierList'
    _Condition = 'Condition'
    _UseUserPreferencesForValidationOptions = 'UseUserPreferencesForValidationOptions'
    _ContentFieldNames = 'ContentFieldNames'
    _ExtractionRequest = 'ExtractionRequest'
    _odata_type = '@odata.type'
    _extraction_request_header = "#DataScope.Select.Api.Extractions.ExtractionRequests."

    def __init__(self):
        """Initialize the instance.

        Returns:
            None: No value is returned.
        """
        self.extraction_type = ExtractionTypes.ExtractRaw
        self.body = None
        self.job_id = None
        self.location = None
        self.output_file_path = None

    @abstractmethod
    def get_body(self) -> dict:
        """Return body.

        Returns:
            dict: Requested value for the lookup.
        """
        raise NotImplementedError

    def get_location(self, token=None) -> str:
        """Return location.

        Args:
            token (object): Authentication token used for API requests.

        Returns:
            str: Requested value for the lookup.
        """
        if self.location:
            return self.location

        body = self.body if self.body else self.get_body()
        location = post_extractions_request(self.extraction_type, body, token)

        self.location = location

        return location

    def get_job_id(self, token=None) -> str:
        """Return job id.

        Args:
            token (object): Authentication token used for API requests.

        Returns:
            str: Requested value for the lookup.
        """
        if self.job_id:
            return self.job_id

        location = self.location if self.location else self.get_location(token)

        job_id = get_job_id_by_location(location, token)

        self.job_id = job_id
        return job_id

    def save_output_file(self, output_file_path: str, token=None) -> bool:
        """
        Save the .gz file to local.
        """
        job_id = self.job_id if self.job_id else self.get_job_id(token)

        logging.info('Successfully get the job id, Start download the file')

        res = get_extraction_file_by_job_id(self.extraction_type, job_id, output_file_path, token)
        if res:
            if os.path.getsize(output_file_path) == 0:
                raise ExtractionError(message=f'No file found: [{output_file_path}]')

        self.output_file_path = os.path.abspath(output_file_path)
        logging.info(f'Successfully saved file {output_file_path}')
        print(f'Successfully saved file {output_file_path}')

        return res

    def get_output_file_dir(self) -> str:
        """Return output file dir.

        Returns:
            str: Requested value for the lookup.
        """
        if self.output_file_path:
            return self.output_file_path
        return 'Output File Not Found'

    def get_text_results(self, token=None) -> str:
        """Return text results.

        Args:
            token (object): Authentication token used for API requests.

        Returns:
            str: Requested value for the lookup.
        """
        body = self.body if self.body else self.get_body()
        job_id = self.job_id if self.job_id else self.get_job_id(token)
        text_result = get_extraction_data_by_job_id(self.extraction_type, job_id, token)

        return text_result

    def get_json_results(self, token=None) -> str:
        """Return json results.

        Args:
            token (object): Authentication token used for API requests.

        Returns:
            str: Requested value for the lookup.
        """
        raise NotImplementedError

    def get_dataframe_results(self) -> pd.DataFrame:
        """Return dataframe results.

        Returns:
            pd.DataFrame: Requested value for the lookup.
        """
        return pd.read_csv(
            self.output_file_path if self.output_file_path else self.get_output_file_dir(),
            compression='gzip',
        )
