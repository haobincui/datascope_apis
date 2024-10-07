import logging
import os
from abc import ABC, abstractmethod

import pandas as pd

from src.connection.client import get_extraction_file_by_job_id, get_job_id_by_location, post_extractions_request, \
    get_extraction_data_by_job_id
from src.connection.features.extraction.enums.extraction_types import ExtractionTypes


class OnDemandExtractioner(ABC):
    """
    abstract class for on demand extractioner
    """
    _IdentifierList = 'IdentifierList'
    _Condition = 'Condition'
    _UseUserPreferencesForValidationOptions = 'UseUserPreferencesForValidationOptions'
    _ContentFieldNames = 'ContentFieldNames'
    _ExtractionRequest = 'ExtractionRequest'
    _odata_type = '@odata.type'
    _extraction_request_header = "#DataScope.Select.Api.Extractions.ExtractionRequests."

    def __init__(self):
        self.extraction_type = ExtractionTypes.ExtractRaw
        self.body = None
        self.job_id = None
        self.location = None
        self.output_file_path = None

    @abstractmethod
    def get_body(self) -> dict:
        raise NotImplemented

    def get_location(self, token=None) -> str:
        if self.location:
            return self.location

        body = self.body if self.body else self.get_body()
        location = post_extractions_request(self.extraction_type, body, token)

        self.location = location

        return location

    def get_job_id(self, token=None) -> str:
        if self.job_id:
            return self.job_id

        location = self.location if self.location else self.get_location(token)

        job_id = get_job_id_by_location(location, token)

        self.job_id = job_id
        return job_id

    def save_output_file(self, output_file_path: str, token=None) -> bool:
        """
        Save the .gz file to local
        :param output_file_path: Output file name need to end with .csv.gz
        :param token:
        :return: True is saved successfully
        """
        job_id = self.job_id if self.job_id else self.get_job_id(token)

        logging.info(f'Successfully get the job id, Start download the file')

        res = get_extraction_file_by_job_id(self.extraction_type, job_id, output_file_path, token)
        if res:
            if os.path.getsize(output_file_path) == 0:
                raise ValueError(f'No file found: [{output_file_path}]')
                # print(f'No file found: [{output_file_path}]')

        self.output_file_path = os.path.abspath(output_file_path)
        logging.info(f'Successfully saved file {output_file_path}')
        print(f'Successfully saved file {output_file_path}')

        return res

    def get_output_file_dir(self) -> str:
        if self.output_file_path:
            return self.output_file_path
        else:
            return 'Output File Not Found'

    def get_text_results(self, token=None) -> str:
        body = self.body if self.body else self.get_body()
        job_id = self.job_id if self.job_id else self.get_job_id(token)
        text_result = get_extraction_data_by_job_id(self.extraction_type, job_id, token)

        return text_result

    def get_json_results(self, token=None) -> str:
        raise NotImplemented

    def get_dataframe_results(self) -> pd.DataFrame:
        res = pd.read_csv(self.output_file_path if self.output_file_path else self.get_output_file_dir(), compression='gzip')

        # dict_res = self.get_text_results(token=token)
        # data_form_converter = DataTypeConverter().from_text_to_dataframe
        return res
