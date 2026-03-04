import io
import logging
import os
import time
import urllib.request
from dataclasses import dataclass
from datetime import datetime, timedelta
from threading import Lock
from typing import Optional, Union

import requests
from src.connection.config import get_config
from src.connection.features.extraction.enums.extraction_types import ExtractionTypes
from src.connection.features.search.enums.search_dictionary_types import SearchDictionary
from src.connection.features.search.enums.search_get_types import GetTypes
from src.connection.features.search.enums.search_types import SearchTypes, HistoricalSearchTypes

from src.error.error import DataScopeAuthError, DataScopeInputError, ExtractionError, SearchError

_config = get_config()


@dataclass
class Token:
    value: str
    acquired_at: datetime


_token: Optional[Token] = None
_token_lock = Lock()
_token_ttl = timedelta(hours=24)


def _ensure_parent_dir(file_path: str) -> None:
    file_dir = os.path.dirname(file_path)
    if file_dir:
        os.makedirs(file_dir, exist_ok=True)


# def get_html(url, retry_count=0):
#     """
#     # https://stackoverflow.com/questions/39287669/handling-connectionreseterror
# https://stackoverflow.com/questions/20568216/python-handling-socket-error-errno-104-connection-reset-by-peer
#     :param url:
#     :param retry_count:
#     :return:
#     """
#     try:
#         request = urllib.Request(url)
#         response = urllib.urlopen(request)
#         html = response.read()
#     except ConectionResetError as e:
#         if retry_count == MAX_RETRIES:
#             raise e
#         time.sleep(for_some_time)
#         get_html(url, retry_count + 1)

# def 

def _is_token_expired(token: Token) -> bool:
    return datetime.utcnow() - token.acquired_at >= _token_ttl


def _request_new_token() -> Token:
    request_token_url = _config.request_token_url
    request_body = {
        'Credentials': {
            'Username': _config.auth_username,
            'Password': _config.auth_password
        }
    }
    auth = requests.post(request_token_url, json=request_body)
    if not auth.ok:
        raise DataScopeAuthError(
            message=f'failed to login [{auth.status_code}]',
            details={'status_code': auth.status_code, 'url': request_token_url},
        )
    try:
        token_value = auth.json().get('value')
        if not token_value:
            raise DataScopeAuthError(
                message='missing token in login response',
                details={'status_code': auth.status_code, 'url': request_token_url},
            )
        return Token(value=token_value, acquired_at=datetime.utcnow())
    except Exception as exc:
        raise DataScopeAuthError(
            message='failed to login',
            details={'status_code': auth.status_code, 'url': request_token_url},
        ) from exc


def _refresh_token(token: Token) -> Token:
    global _token
    with _token_lock:
        if _is_token_expired(token):
            refreshed = _request_new_token()
            token.value = refreshed.value
            token.acquired_at = refreshed.acquired_at
            if _token is None or _token is token:
                _token = token
    return token


def _get_token() -> Token:
    global _token
    with _token_lock:
        if _token is None or _is_token_expired(_token):
            _token = _request_new_token()
        return _token


def _get_token_value(token=None) -> str:
    if token is None:
        return _get_token().value
    if isinstance(token, Token):
        return _refresh_token(token).value
    if isinstance(token, str):
        return token
    raise DataScopeInputError(message=f'Unsupported token type: {type(token)}')


def _build_auth_header(token=None) -> str:
    return 'Token ' + _get_token_value(token)


def search(search_type: Union[SearchTypes, GetTypes, HistoricalSearchTypes], body: dict, max_page_size=5, token=None):
    url = _config.search_url + search_type.value
    headers = {
        'Authorization': _build_auth_header(token),
        'Prefer': f'odata.maxpagesize={max_page_size}; respond-async',
        'Content-Type': 'application/json'
    }
    if isinstance(search_type, (SearchTypes, HistoricalSearchTypes)):
        r = requests.post(url, json=body, headers=headers).json()
    elif isinstance(search_type, GetTypes):
        r = requests.get(url, json=body, headers=headers).json()
    else:
        raise SearchError(message=f'Unsupported search type [{search_type}]')
    if 'error' in r:
        raise SearchError(
            message=f"Failed to search {search_type.name} [{r['error']['message']}]",
            details={'url': url, 'search_type': search_type.name},
        )
    return r['value']


def get_search_dictionaries(search_dictionary: SearchDictionary, max_page_size=5, token=None):
    url = _config.search_url + search_dictionary.value
    headers = {
        'Authorization': _build_auth_header(token),
        'Prefer': f'odata.maxpagesize={max_page_size}; respond-async',
        'Content-Type': 'application/json; odata=minimalmetadata'
    }
    body = {}
    r = requests.get(url, json=body, headers=headers).json()
    if 'error' in r:
        raise SearchError(
            message=f'Failed to get {search_dictionary.name}',
            details={'url': url, 'dictionary': search_dictionary.name},
        )
    return r['value']


def post_extractions_request(extraction_type: ExtractionTypes, body: dict, token=None):
    """
    Get the location for the extraction request, the start point of getting extractions
    :return: location id or job id (if there is no merged_output data)
    """
    url = _config.extraction_url + extraction_type.name
    headers = {
        'Authorization': _build_auth_header(token),
        'Prefer': 'respond-async',  # return the location id in the response, if failed, usually return job id
        'Content-Type': 'application/json; odata=minimalmetadata'
    }
    logging.debug('Start sending extraction request')
    r = requests.post(url, json=body, headers=headers)

    if r.status_code == 202:
        location = r.headers['location']
        return location

    if r.status_code == 200:
        res = r.json()
        logging.debug(f"get JobId [{res['JobId']}] with Notes [{res['Notes']}]")
        job_id = res['JobId']
        location = url + "Result" + f"(ExtractionId='{job_id}')"
        return location
    else:
        res = r.json()
        raise ExtractionError(
            message=f"Failed to send request for {extraction_type.name} with error {res['error']}",
            details={'status_code': r.status_code, 'url': url},
        )


def get_job_id_by_location(location: str, token=None):
    """
    Get JobId via location url
    :param location: location url for target job
    :param token:
    :return: Job Id
    """
    url = location
    headers = {
        'Authorization': _build_auth_header(token),
        # 'Prefer': 'respond-async',
    }
    logging.debug('Start getting the Job Id')
    r = requests.get(url, headers=headers)
    if r.status_code == 200:
        res = r.json()
        job_id = res['JobId']
        notes = res['Notes']
        logging.debug(f'Successful get Job Id [{job_id}] with notes [{notes}]')
        return job_id
    elif r.status_code == 408:
        time.sleep(0.1)
        return get_job_id_by_location(location, token)
    else:
        raise ExtractionError(
            message=f"Failed to get job id with error [{r.json()}], [{r.status_code}]",
            details={'status_code': r.status_code, 'url': url},
        )


def get_job_id_by_extraction_request(extraction_type: ExtractionTypes, body: dict, token=None):
    """
    Send the extraction request and Return the job id
    :param extraction_type:
    :param body:
    :param token:
    :return: Job id
    """
    token = _get_token() if token is None else token

    location = post_extractions_request(extraction_type, body, token)
    job_id = get_job_id_by_location(location, token)

    return job_id


def get_extraction_data_by_job_id(extraction_type: ExtractionTypes, job_id: str, token=None) -> str:
    """
    Get requested extraction data (in str) by job id
    :param extraction_type: ExtractionRaw / ExtractWithNotes
    :param job_id: job_id
    :param token: token
    :return: Data， as a str
    """

    def _get_extraction_result_url(result_name: str) -> str:
        return f"{result_name}Results('{job_id}')/$value"

    if extraction_type == ExtractionTypes.ExtractRaw:
        extraction_result_url = _get_extraction_result_url('RawExtraction')
    elif extraction_type == ExtractionTypes.ExtractWithNotes:
        extraction_result_url = _get_extraction_result_url('ExtractionRawWithNotes')
    else:
        raise ExtractionError(message=f'Unsupported extraction type {extraction_type}')

    url = _config.extraction_url + extraction_result_url
    headers = {
        'Authorization': _build_auth_header(token),
        'Prefer': 'respond-async',
    }

    r = requests.get(url, headers=headers)
    if r.status_code == 200:
        res = r.text  # str form, need to convert to dataframe
        return res
    else:
        raise ExtractionError(
            message=f"Failed to get data with error [{r.json()['error']}], [{r.status_code}]",
            details={'status_code': r.status_code, 'url': url, 'job_id': job_id},
        )


def get_extraction_file_by_job_id(extraction_type: ExtractionTypes, job_id: str, output_file_path: str,
                                  token=None) -> bool:
    """
    Download the file (in .gz) by job id
    :param extraction_type:
    :param output_file_path:
    :param job_id:
    :param token:
    :return:
    """

    def get_extraction_result_url(result_name: str) -> str:
        return f"{result_name}Results('{job_id}')/$value"

    if extraction_type == ExtractionTypes.ExtractRaw:
        extraction_result_url = get_extraction_result_url('RawExtraction')
    elif extraction_type == ExtractionTypes.ExtractWithNotes:
        extraction_result_url = get_extraction_result_url('ExtractionRawWithNotes')
    else:
        # raise ValueError(f'Unsupport extraction type {extraction_type}')
        raise ExtractionError(message=f'Unsupported extraction type {extraction_type}')

    url = _config.extraction_url + extraction_result_url

    headers = {
        "Authorization": _build_auth_header(token),
        "X-Direct-Download": "true",
        "Prefer": "respond-async"
    }

    logging.info('Start downloading the file ')
    r = requests.get(url, headers=headers, stream=True)
    if not r.ok:
        raise ExtractionError(
            message=f'Failed to download file by job id [{job_id}], [{r.status_code}]',
            details={'status_code': r.status_code, 'url': url, 'job_id': job_id},
        )
    logging.debug('Successfully get the file, start saving')
    _ensure_parent_dir(output_file_path)
    with open(output_file_path, 'wb') as output_file:
        output_file.write(r.content)

    if output_file.closed:
        logging.info('Finished downloading')
        return True


def get_extraction_file_by_file_id(extraction_file_id: str, output_file_path: str,
                                   token=None) -> bool:
    """
    download the file (in .gz) by file id
    :param extraction_file_id:
    :param output_file_path:
    :param token:
    :return:
    """
    url = _config.extraction_url + f"ExtractedFiles('{extraction_file_id}')" + "/$value"
    headers = {
        'Authorization': _build_auth_header(token),
        # 'X-Direct-Download': True
    }
    logging.info('Start downloading the file')

    url_obj = urllib.request.Request(url=url, headers=headers)
    _ensure_parent_dir(output_file_path)

    with urllib.request.urlopen(url_obj) as response:
        compressed_file = io.BytesIO(response.read())
        with open(output_file_path, 'wb') as outfile:
            outfile.write(compressed_file.read())

    if outfile.closed:
        logging.info('Successfully download the file')
        return True


def get_extraction_result_value(extraction_type: ExtractionTypes, body: dict, token=None):
    """
    Get extraction results value in one function
    :param extraction_type:  ExtractionRaw/ExtractionWithNotes
    :param body:  Input Json, OnDemandExtractioner
    :param token: token
    :return: str form data
    """
    token = _get_token() if token is None else token

    location = post_extractions_request(extraction_type, body, token)

    job_id = get_job_id_by_location(location, token)

    data = get_extraction_data_by_job_id(extraction_type, job_id, token)

    return data


def get_data_file_id_by_job_id(job_id: str, token=None):
    """
    Return the File id
    :param job_id:
    :param token:
    :return:
    """
    url = _config.extraction_url + f"ExtractedFileByJobId(JobId='{job_id}')"
    headers = {
        'Authorization': _build_auth_header(token),
        'Prefer': 'respond-async,wait=2'  # async wait time, default = 30
    }
    r = requests.get(url, headers=headers)
    if r.ok:
        res = r.json()
        return res['value'][-1]['FileId']

    else:
        raise ExtractionError(
            message=f'Failed to get file by job id, [{r.status_code}]',
            details={'status_code': r.status_code, 'url': url, 'job_id': job_id},
        )
