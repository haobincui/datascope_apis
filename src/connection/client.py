import io
import logging
import os
import time
import urllib.request
from datetime import datetime
from tokenize import Token
from typing import Union
import requests
from src.connection.config import get_config
from src.connection.features.extraction.enums.extraction_types import ExtractionTypes
from src.connection.features.search.enums.search_dictionary_types import SearchDictionary
from src.connection.features.search.enums.search_get_types import GetTypes
from src.connection.features.search.enums.search_types import SearchTypes, HistoricalSearchTypes

from src.error.error import ExtractionError

_config = get_config()

_token = None


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

class Token:
    """
    Token class to store token value, init time and expire time
    :param value: token value.
    :param init_time: token init time, default is current time, in float.
    """
    def __init__(self, value: str, init_time: float = None):
        self.value = value
        if init_time:
            self._init_time = init_time
            self._expire_time = self._init_time + 86400  # expire in 24 hours
            logging.debug(f'Init token at {self._init_time}, with expire time {self._expire_time}')
        else:
            self._init_time = time.time()
            self._expire_time = self._init_time + 86400
            logging.debug(f'Init token at {self._init_time}.'
                          f' use current time as default init time, with expire time {self._expire_time}')


    def is_expired(self) -> bool:
        return time.time() > self._expire_time

    def get_expire_time(self) -> datetime:
        if self._expire_time is not None:
            return datetime.fromtimestamp(self._expire_time)
        else:
            raise ValueError('Token has not been initialized')

    def get_init_time(self) -> datetime:
        if self._init_time is not None:
            return datetime.fromtimestamp(self._init_time)
        else:
            raise ValueError('Token has not been initialized')


    def get_token(self) -> str:
        """return the token value, if the token is expired, get a new token"""
        if self.is_expired() or self.value is None:
            return _get_token().value
        return self.value

    def reset_value(self, new_value: str = None) -> bool:
        self.value = new_value
        logging.debug("Token value reset.")
        return True

    def reset_init_time(self, new_init_time: float = None) -> bool:
        self._init_time = new_init_time
        self._expire_time = self._init_time + 86400
        logging.debug(f"Token init time reset to {self._init_time}, with expire time {self._expire_time}")
        return True

    def clean_token(self) -> bool:
        self.value = None
        self._init_time = None
        self._expire_time = None
        logging.debug('Token cleared')
        return True

    def __exit__(self):
        self.value = None
        self._init_time = None
        self._expire_time = None



def _get_token() -> Token:
    global _token
    if _token:
        return _token
    request_token_url = _config.request_token_url
    request_body = {
        'Credentials': {
            'Username': _config.auth_username,
            'Password': _config.auth_password
        }
    }
    auth = requests.post(request_token_url, json=request_body)
    if auth.status_code == 401:
        raise ValueError('Failed to login: [401 Unauthorized]')
    elif auth.status_code != 200:
        raise ValueError(f'Failed to login: [{auth.json()}]')
    token = auth.json()['value']
    _token = Token(token, time.time())
    logging.debug(f'Get token at {_token.get_init_time().isoformat()}')
    return _token

def process_invalidate_token(token) -> Token:
    # 401 Unauthorized
    global _token
    new_token = token.get_token()
    return new_token



def search(search_type: Union[SearchTypes, GetTypes, HistoricalSearchTypes], body: dict, max_page_size: int = 5, token: Token = None):
    url = _config.search_url + search_type.value
    headers = {
        'Authorization': 'Token ' + (token.value if token else _get_token().value),
        'Prefer': f'odata.maxpagesize={max_page_size}; respond-async',
        'Content-Type': 'application/json'
    }
    if isinstance(search_type, (SearchTypes, HistoricalSearchTypes)):
        r = requests.post(url, json=body, headers=headers).json()
    elif isinstance(search_type, GetTypes):
        r = requests.get(url, json=body, headers=headers).json()
    else:
        raise Exception(f'Unsupport search types {search_type.__class__.name}')
    if 'error' in r:
        raise Exception(f"Failed to search {search_type.name}: [{r['error']['message']}]")
    if r.status_code == 200:
        return r['value']
    elif r.status_code == 401:
        return search(search_type, body, max_page_size, process_invalidate_token(token))
    else:
        raise Exception(f"Failed to search {search_type.name}: [{r['error']['message']}]")


def get_search_dictionaries(search_dictionary: SearchDictionary, max_page_size: int = 5, token: Token = None):
    url = _config.search_url + search_dictionary.value
    headers = {
        'Authorization': 'Token ' + (token.value if token else _get_token().value),
        'Prefer': f'odata.maxpagesize={max_page_size}; respond-async',
        'Content-Type': 'application/json; odata=minimalmetadata'
    }
    body = {}
    r = requests.get(url, json=body, headers=headers).json()
    if 'error' in r:
        raise Exception(f'Failed to get {search_dictionary.name}')
    if r.status_code == 200:
        return r['value']
    elif r.status_code == 401:
        return get_search_dictionaries(search_dictionary, max_page_size, process_invalidate_token(token))
    else:
        raise Exception(f"Failed to get search: [{r['error']['message']}]")



def post_extractions_request(extraction_type: ExtractionTypes, body: dict, token: Token = None):
    """
    Get the location for the extraction request, the start point of getting extractions
    :return: location id or job id (if there is no merged_output data)
    """
    url = _config.extraction_url + extraction_type.name
    headers = {
        'Authorization': 'Token ' + (token.value if token else _get_token().value),
        'Prefer': 'respond-async',  # return the location id in the response, if failed, usually return job id
        'Content-Type': 'application/json; odata=minimalmetadata'
    }
    logging.debug('Start sending extraction request')
    r = requests.post(url, json=body, headers=headers)

    if r.status_code == 401:
        logging.debug('Token expired, re-login')
        return post_extractions_request(extraction_type, body, process_invalidate_token(token))

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
        raise ValueError(f"Failed to send request for {extraction_type.name} with error {res['error']}")


def get_job_id_by_location(location: str, token: Token = None):
    """
    Get JobId via location url
    :param location: location url for target job
    :param token:
    :return: Job Id
    """
    url = location
    headers = {
        'Authorization': 'Token ' + (token.value if token else _get_token().value),
        # 'Prefer': 'respond-async',
    }
    logging.debug('Start getting the Job Id')
    r = requests.get(url, headers=headers)
    if r.status_code == 401:
        logging.debug('Token expired, re-login')
        return get_job_id_by_location(location, process_invalidate_token(token))
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
        raise ValueError(f"Failed to get jod id with error [{r.json()}], [{r.status_code}]")


def get_job_id_by_extraction_request(extraction_type: ExtractionTypes, body: dict, token: Token = None):
    """
    Send the extraction request and Return the job id
    :param extraction_type:
    :param body:
    :param token:
    :return: Job id
    """
    token = token if token else _get_token()

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
        raise ValueError(f'Unsupported extraction type {extraction_type}')

    url = _config.extraction_url + extraction_result_url
    headers = {
        'Authorization': 'Token ' + (token if token else _get_token()),
        'Prefer': 'respond-async',
    }

    r = requests.get(url, headers=headers)
    if r.status_code == 401:
        logging.debug('Token expired, re-login')
        return get_extraction_data_by_job_id(extraction_type, job_id, process_invalidate_token(token))

    if r.status_code == 200:
        res = r.text  # str form, need to convert to dataframe
        return res
    else:
        raise ValueError(f"Failed to get data with error [{r.json()['error']}], [{r.status_code}]")


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

    token = token if token else _get_token()

    headers = {
        "Authorization": "Token " + token,
        "X-Direct-Download": "true",
        "Prefer": "respond-async"
    }

    logging.info('Start downloading the file ')
    r = requests.get(url, headers=headers, stream=True)
    if r.status_code == 401:
        logging.debug('Token expired, re-login')
        return get_extraction_file_by_job_id(extraction_type, job_id, output_file_path, process_invalidate_token(token))
    logging.debug('Successfully get the file, start saving')
    file_dir = os.path.dirname(output_file_path)
    try:
        os.makedirs(file_dir, exist_ok=False)
        logging.debug(f'Created dir {file_dir}')
    except Exception as e:
        logging.debug(f'Dir [{file_dir}] exist, do not need to create')
        pass
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
        'Authorization': 'Token ' + (token if token else _get_token()),
        # 'X-Direct-Download': True
    }
    logging.info('Start downloading the file')

    url_obj = urllib.request.Request(url=url, headers=headers)
    file_dir = os.path.dirname(output_file_path)
    try:
        os.makedirs(file_dir, exist_ok=False)
        logging.debug(f'Created dir {file_dir}')
    except Exception as e:
        logging.debug(f'Dir [{file_dir}] exist, do not need to create')
        pass

    with urllib.request.urlopen(url_obj) as response:
        if response.getcode() == 401:
            logging.debug('Token expired, re-login')
            return get_extraction_file_by_file_id(extraction_file_id, output_file_path, process_invalidate_token(token))
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
        'Authorization': 'Token ' + (token if token else _get_token()),
        'Prefer': 'respond-async,wait=2'  # async wait time, default = 30
    }
    r = requests.get(url, headers=headers)
    if r.status_code == 401:
        logging.debug('Token expired, re-login')
        return get_data_file_id_by_job_id(job_id, process_invalidate_token(token))
    if r.ok:
        res = r.json()
        return res['value'][-1]['FileId']

    else:
        # raise ConnectionError(f'Failed to get file by job id, [{r.status_code}]')
        return ExtractionError(message=f'Failed to get file by job id, [{r.status_code}]')

