import logging
import time
from typing import Optional, Union

import requests

from src.connection.extraction.enums.extraction_types import ExtractionTypes
from src.connection.infra.http.auth import Token, build_auth_header, get_token
from src.connection.shared.settings import get_settings
from src.error.error import ExtractionError


def post_extractions_request(
    extraction_type: ExtractionTypes,
    body: dict,
    token: Optional[Union[Token, str]] = None,
):
    """Submit an extraction request and return the polling location/result URL.

    Args:
        extraction_type (ExtractionTypes): Extraction output format requested from DataScope.
        body (dict): Serialized extraction request payload.
        token (Optional[Union[Token, str]]): Authentication token used for API requests.

    Returns:
        object: Result location URL or direct result URL for follow-up requests.
    """
    settings = get_settings()
    url = settings.extraction_url + extraction_type.name
    headers = {
        'Authorization': build_auth_header(token),
        'Prefer': 'respond-async',
        'Content-Type': 'application/json; odata=minimalmetadata',
    }

    logging.debug('Start sending extraction request')
    response = requests.post(url, json=body, headers=headers, timeout=settings.request_timeout_seconds)

    if response.status_code == 202:
        return response.headers['location']

    if response.status_code == 200:
        payload = response.json()
        job_id = payload['JobId']
        return url + "Result" + f"(ExtractionId='{job_id}')"

    payload = response.json()
    raise ExtractionError(
        message=f"Failed to send request for {extraction_type.name} with error {payload['error']}",
        details={'status_code': response.status_code, 'url': url},
    )


def get_job_id_by_location(location: str, token: Optional[Union[Token, str]] = None):
    """Poll a location endpoint until the extraction job id is available.

    Args:
        location (str): Polling URL returned by a prior extraction submission.
        token (Optional[Union[Token, str]]): Authentication token used for API requests.

    Returns:
        object: Extraction job id from the polling response.
    """
    settings = get_settings()
    headers = {'Authorization': build_auth_header(token)}
    logging.debug('Start getting the Job Id')

    response = requests.get(location, headers=headers, timeout=settings.request_timeout_seconds)
    if response.status_code == 200:
        payload = response.json()
        return payload['JobId']

    if response.status_code == 408:
        time.sleep(0.1)
        return get_job_id_by_location(location, token)

    raise ExtractionError(
        message=f"Failed to get job id with error [{response.json()}], [{response.status_code}]",
        details={'status_code': response.status_code, 'url': location},
    )


def get_job_id_by_extraction_request(
    extraction_type: ExtractionTypes,
    body: dict,
    token: Optional[Union[Token, str]] = None,
):
    """Submit an extraction request and resolve its resulting job id.

    Args:
        extraction_type (ExtractionTypes): Extraction output format requested from DataScope.
        body (dict): Serialized extraction request payload.
        token (Optional[Union[Token, str]]): Authentication token used for API requests.

    Returns:
        object: Extraction job id associated with the submitted request.
    """
    actual_token = get_token() if token is None else token
    location = post_extractions_request(extraction_type, body, actual_token)
    return get_job_id_by_location(location, actual_token)


def get_extraction_data_by_job_id(
    extraction_type: ExtractionTypes,
    job_id: str,
    token: Optional[Union[Token, str]] = None,
) -> str:
    """Fetch extraction result text for a completed job id.

    Args:
        extraction_type (ExtractionTypes): Extraction output format requested from DataScope.
        job_id (str): Job identifier returned by the extraction service.
        token (Optional[Union[Token, str]]): Authentication token used for API requests.

    Returns:
        str: Raw extraction text content returned by DataScope.
    """
    settings = get_settings()

    def _result_url(result_name: str) -> str:
        """Build the extraction result URL suffix for a job id.

        Args:
            result_name (str): Extraction result type prefix expected by the API.

        Returns:
            str: URL suffix that points to the extraction `$value` endpoint.
        """
        return f"{result_name}Results('{job_id}')/$value"

    if extraction_type == ExtractionTypes.ExtractRaw:
        extraction_result_url = _result_url('RawExtraction')
    elif extraction_type == ExtractionTypes.ExtractWithNotes:
        extraction_result_url = _result_url('ExtractionRawWithNotes')
    else:
        raise ExtractionError(message=f'Unsupported extraction type {extraction_type}')

    url = settings.extraction_url + extraction_result_url
    headers = {
        'Authorization': build_auth_header(token),
        'Prefer': 'respond-async',
    }

    response = requests.get(url, headers=headers, timeout=settings.request_timeout_seconds)
    if response.status_code == 200:
        return response.text

    raise ExtractionError(
        message=f"Failed to get data with error [{response.json().get('error')}], [{response.status_code}]",
        details={'status_code': response.status_code, 'url': url, 'job_id': job_id},
    )


def get_extraction_result_value(
    extraction_type: ExtractionTypes,
    body: dict,
    token: Optional[Union[Token, str]] = None,
):
    """Submit an extraction and return the resolved text result.

    Args:
        extraction_type (ExtractionTypes): Extraction output format requested from DataScope.
        body (dict): Serialized extraction request payload.
        token (Optional[Union[Token, str]]): Authentication token used for API requests.

    Returns:
        object: Extraction text payload returned by DataScope.
    """
    actual_token = get_token() if token is None else token
    location = post_extractions_request(extraction_type, body, actual_token)
    job_id = get_job_id_by_location(location, actual_token)
    return get_extraction_data_by_job_id(extraction_type, job_id, actual_token)


def get_data_file_id_by_job_id(job_id: str, token: Optional[Union[Token, str]] = None):
    """Resolve the extracted file id for a completed job.

    Args:
        job_id (str): Job identifier returned by the extraction service.
        token (Optional[Union[Token, str]]): Authentication token used for API requests.

    Returns:
        object: File id associated with the completed extraction job.
    """
    settings = get_settings()
    url = settings.extraction_url + f"ExtractedFileByJobId(JobId='{job_id}')"
    headers = {
        'Authorization': build_auth_header(token),
        'Prefer': 'respond-async,wait=2',
    }

    response = requests.get(url, headers=headers, timeout=settings.request_timeout_seconds)
    if response.ok:
        payload = response.json()
        return payload['value'][-1]['FileId']

    raise ExtractionError(
        message=f'Failed to get file by job id, [{response.status_code}]',
        details={'status_code': response.status_code, 'url': url, 'job_id': job_id},
    )
