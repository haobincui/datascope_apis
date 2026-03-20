from typing import Optional, Union

import requests

from src.connection.infra.http.auth import Token, build_auth_header
from src.connection.search.enums.search_dictionary_types import SearchDictionary
from src.connection.search.enums.search_get_types import GetTypes
from src.connection.search.enums.search_types import HistoricalSearchTypes, SearchTypes
from src.connection.shared.settings import get_settings
from src.error.error import SearchError


def search(
    search_type: Union[SearchTypes, GetTypes, HistoricalSearchTypes],
    body: dict,
    max_page_size: int = 5,
    token: Optional[Union[Token, str]] = None,
):
    """Execute a search request against the DataScope search API.

    Args:
        search_type (Union[SearchTypes, GetTypes, HistoricalSearchTypes]): Search endpoint selector.
        body (dict): Request payload for the target search endpoint.
        max_page_size (int): OData page size hint sent in the `Prefer` header.
        token (Optional[Union[Token, str]]): Authentication token used for API requests.

    Returns:
        object: Parsed `value` payload returned by the search API.
    """
    settings = get_settings()
    url = settings.search_url + search_type.value
    headers = {
        'Authorization': build_auth_header(token),
        'Prefer': f'odata.maxpagesize={max_page_size}; respond-async',
        'Content-Type': 'application/json',
    }

    if isinstance(search_type, (SearchTypes, HistoricalSearchTypes)):
        response = requests.post(url, json=body, headers=headers, timeout=settings.request_timeout_seconds)
    elif isinstance(search_type, GetTypes):
        response = requests.get(url, json=body, headers=headers, timeout=settings.request_timeout_seconds)
    else:
        raise SearchError(message=f'Unsupported search type [{search_type}]')

    payload = response.json()
    if 'error' in payload:
        raise SearchError(
            message=f"Failed to search {search_type.name} [{payload['error']['message']}]",
            details={'url': url, 'search_type': search_type.name},
        )
    return payload['value']


def get_search_dictionaries(
    search_dictionary: SearchDictionary,
    max_page_size: int = 5,
    token: Optional[Union[Token, str]] = None,
):
    """Fetch dictionary values for search filters and request metadata.

    Args:
        search_dictionary (SearchDictionary): Dictionary endpoint to query.
        max_page_size (int): OData page size hint sent in the `Prefer` header.
        token (Optional[Union[Token, str]]): Authentication token used for API requests.

    Returns:
        object: Parsed dictionary entries from the API response.
    """
    settings = get_settings()
    url = settings.search_url + search_dictionary.value
    headers = {
        'Authorization': build_auth_header(token),
        'Prefer': f'odata.maxpagesize={max_page_size}; respond-async',
        'Content-Type': 'application/json; odata=minimalmetadata',
    }

    response = requests.get(url, json={}, headers=headers, timeout=settings.request_timeout_seconds)
    payload = response.json()
    if 'error' in payload:
        raise SearchError(
            message=f'Failed to get {search_dictionary.name}',
            details={'url': url, 'dictionary': search_dictionary.name},
        )
    return payload['value']
