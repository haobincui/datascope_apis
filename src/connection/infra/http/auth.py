import time
from dataclasses import dataclass
from datetime import datetime, timedelta
from threading import Lock
from typing import Optional, Union

import requests

from src.connection.shared.settings import get_settings
from src.error.error import DataScopeAuthError, DataScopeInputError


@dataclass
class Token:
    """Authentication token and acquisition timestamp."""
    value: str
    acquired_at: datetime


_token: Optional[Token] = None
_token_lock = Lock()
_token_ttl = timedelta(hours=24)


def _is_token_expired(token: Token) -> bool:
    """Check whether a cached token has exceeded the configured TTL.

    Args:
        token (Token): Authentication token used for API requests.

    Returns:
        bool: True when the token is expired; otherwise False.
    """
    return datetime.utcnow() - token.acquired_at >= _token_ttl


def _require_credentials(username: Optional[str], password: Optional[str]) -> None:
    """Validate that username and password credentials are present.

    Args:
        username (Optional[str]): DataScope account username.
        password (Optional[str]): DataScope account password.

    Returns:
        None: No value is returned.
    """
    if not username or not password:
        raise DataScopeInputError(
            message='Missing DataScope credentials. Set DATASCOPE_USERNAME and DATASCOPE_PASSWORD.',
        )


def _request_new_token() -> Token:
    """Request a fresh token from the DataScope authentication endpoint.

    Returns:
        Token: Fresh token payload with acquisition time.
    """
    settings = get_settings()
    _require_credentials(settings.username, settings.password)

    request_body = {
        'Credentials': {
            'Username': settings.username,
            'Password': settings.password,
        }
    }

    last_error: Optional[Exception] = None
    for attempt in range(settings.max_retries + 1):
        try:
            auth = requests.post(
                settings.request_token_url,
                json=request_body,
                timeout=settings.request_timeout_seconds,
            )
            if not auth.ok:
                raise DataScopeAuthError(
                    message=f'failed to login [{auth.status_code}]',
                    details={'status_code': auth.status_code, 'url': settings.request_token_url},
                )

            token_value = auth.json().get('value')
            if not token_value:
                raise DataScopeAuthError(
                    message='missing token in login response',
                    details={'status_code': auth.status_code, 'url': settings.request_token_url},
                )
            return Token(value=token_value, acquired_at=datetime.utcnow())
        except Exception as exc:
            last_error = exc
            if attempt >= settings.max_retries:
                break
            time.sleep(settings.retry_backoff_seconds * (attempt + 1))

    raise DataScopeAuthError(
        message='failed to login',
        details={'url': settings.request_token_url},
    ) from last_error


def refresh_token(token: Token) -> Token:
    """Refresh a token in place when it is expired.

    Args:
        token (Token): Authentication token used for API requests.

    Returns:
        Token: Valid (possibly refreshed) token object.
    """
    global _token
    with _token_lock:
        if _is_token_expired(token):
            refreshed = _request_new_token()
            token.value = refreshed.value
            token.acquired_at = refreshed.acquired_at
            if _token is None or _token is token:
                _token = token
    return token


def get_token() -> Token:
    """Get a process-wide shared token, refreshing it when needed.

    Returns:
        Token: Cached token object ready for authorized requests.
    """
    global _token
    with _token_lock:
        if _token is None or _is_token_expired(_token):
            _token = _request_new_token()
        return _token


def get_token_value(token: Optional[Union[Token, str]] = None) -> str:
    """Resolve a token input into a raw bearer token string.

    Args:
        token (Optional[Union[Token, str]]): Authentication token used for API requests.

    Returns:
        str: Raw token value suitable for HTTP authorization headers.
    """
    if token is None:
        return get_token().value
    if isinstance(token, Token):
        return refresh_token(token).value
    if isinstance(token, str):
        return token
    raise DataScopeInputError(message=f'Unsupported token type: {type(token)}')


def build_auth_header(token: Optional[Union[Token, str]] = None) -> str:
    """Build the `Authorization` header value for DataScope requests.

    Args:
        token (Optional[Union[Token, str]]): Authentication token used for API requests.

    Returns:
        str: Header value in the form `Token <value>`.
    """
    return f'Token {get_token_value(token)}'
