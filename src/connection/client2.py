import asyncio
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import TypedDict

import requests
from aiohttp import ClientSession

from connection.util import status_code

"""
API Request objects,
[post] request -> location id,
[get] location -> job id,
[get] job id -> extraction file id,
[get] extraction file id -> extraction file
"""

_status_code = status_code


class RequestHeader(TypedDict):
    """request header"""
    Authorization: str
    Prefer: str
    Content_Type: str


@dataclass()
class APIRequest(ABC):
    """abstract method for all API requests"""
    task_id: str
    request_url: str
    request_header: RequestHeader
    token: str = None


# @dataclass()
# class GetLocation(APIRequest):
#     """send request, get location """
#
@dataclass()
class JobIdRequest(APIRequest):
    def __post_init__(self):
        self.request_header = {
            'Authorization': self.token,
            'Prefer': 'respond-async',
            'Content_Type': 'application/json'
        }




class SaveFile(APIRequest):
    pass


@dataclass()
class ExtractionRequest(APIRequest):
    """post extraction request, get location id or job id"""
    pass
