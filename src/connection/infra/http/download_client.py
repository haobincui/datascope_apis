import io
import logging
import os
import urllib.request
from typing import Optional, Union

import requests

from src.connection.extraction.enums.extraction_types import ExtractionTypes
from src.connection.infra.http.auth import Token, build_auth_header
from src.connection.shared.settings import get_settings
from src.error.error import ExtractionError


def _ensure_parent_dir(file_path: str) -> None:
    """Create parent directories for an output path when needed.

    Args:
        file_path (str): Destination file path.

    Returns:
        None: No value is returned.
    """
    file_dir = os.path.dirname(file_path)
    if file_dir:
        os.makedirs(file_dir, exist_ok=True)


def get_extraction_file_by_job_id(
    extraction_type: ExtractionTypes,
    job_id: str,
    output_file_path: str,
    token: Optional[Union[Token, str]] = None,
) -> bool:
    """Download extraction output to a local file using a job id.

    Args:
        extraction_type (ExtractionTypes): Extraction output format requested from DataScope.
        job_id (str): Job identifier returned by the extraction service.
        output_file_path (str): Path to the output file.
        token (Optional[Union[Token, str]]): Authentication token used for API requests.

    Returns:
        bool: True when the output file exists and is non-empty.
    """
    settings = get_settings()

    def result_url(result_name: str) -> str:
        """Build the extraction result URL suffix for a job id.

        Args:
            result_name (str): Extraction result type prefix expected by the API.

        Returns:
            str: URL suffix that points to the extraction `$value` endpoint.
        """
        return f"{result_name}Results('{job_id}')/$value"

    if extraction_type == ExtractionTypes.ExtractRaw:
        extraction_result_url = result_url('RawExtraction')
    elif extraction_type == ExtractionTypes.ExtractWithNotes:
        extraction_result_url = result_url('ExtractionRawWithNotes')
    else:
        raise ExtractionError(message=f'Unsupported extraction type {extraction_type}')

    url = settings.extraction_url + extraction_result_url
    headers = {
        'Authorization': build_auth_header(token),
        'X-Direct-Download': 'true',
        'Prefer': 'respond-async',
    }

    logging.info('Start downloading the file')
    response = requests.get(url, headers=headers, stream=True, timeout=settings.request_timeout_seconds)
    if not response.ok:
        raise ExtractionError(
            message=f'Failed to download file by job id [{job_id}], [{response.status_code}]',
            details={'status_code': response.status_code, 'url': url, 'job_id': job_id},
        )

    _ensure_parent_dir(output_file_path)
    with open(output_file_path, 'wb') as output_file:
        output_file.write(response.content)

    return os.path.exists(output_file_path) and os.path.getsize(output_file_path) > 0


def get_extraction_file_by_file_id(
    extraction_file_id: str,
    output_file_path: str,
    token: Optional[Union[Token, str]] = None,
) -> bool:
    """Download extraction output to a local file using a file id.

    Args:
        extraction_file_id (str): Extracted file id returned by DataScope.
        output_file_path (str): Path to the output file.
        token (Optional[Union[Token, str]]): Authentication token used for API requests.

    Returns:
        bool: True when the output file exists and is non-empty.
    """
    settings = get_settings()
    url = settings.extraction_url + f"ExtractedFiles('{extraction_file_id}')/$value"
    headers = {'Authorization': build_auth_header(token)}

    logging.info('Start downloading the file by file id')
    request = urllib.request.Request(url=url, headers=headers)
    _ensure_parent_dir(output_file_path)

    with urllib.request.urlopen(request) as response:
        compressed_file = io.BytesIO(response.read())
        with open(output_file_path, 'wb') as outfile:
            outfile.write(compressed_file.read())

    return os.path.exists(output_file_path) and os.path.getsize(output_file_path) > 0
