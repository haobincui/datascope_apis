import configparser
import os
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from typing import Optional


@dataclass(frozen=True)
class DataScopeSettings:
    """Represents data scope settings."""
    gateway_ip: str
    auth_service: str
    username: Optional[str]
    password: Optional[str]
    search_service: str = 'Search'
    extraction_service: str = 'Extractions'
    request_timeout_seconds: float = 600.0
    max_retries: int = 6
    retry_backoff_seconds: float = 0.2

    @property
    def base_url(self) -> str:
        """Base url.

        Returns:
            str: Computed result of the operation.
        """
        return f'https://{self.gateway_ip}/'

    @property
    def request_token_url(self) -> str:
        """Request token url.

        Returns:
            str: Computed result of the operation.
        """
        return f'{self.base_url}{self.auth_service}/RequestToken'

    @property
    def search_url(self) -> str:
        """Search url.

        Returns:
            str: Computed result of the operation.
        """
        return f'{self.base_url}{self.search_service}/'

    @property
    def extraction_url(self) -> str:
        """Extraction url.

        Returns:
            str: Computed result of the operation.
        """
        return f'{self.base_url}{self.extraction_service}/'


def _read_ini(path: Path) -> configparser.ConfigParser:
    """Read ini.

    Args:
        path (Path): Input value for path.

    Returns:
        configparser.ConfigParser: Computed result of the operation.
    """
    conf = configparser.ConfigParser()
    if path.exists():
        conf.read(path, encoding='utf-8')
    return conf


def _ini_value(conf: configparser.ConfigParser, section: str, key: str, default: Optional[str] = None) -> Optional[str]:
    """Ini value.

    Args:
        conf (configparser.ConfigParser): Input value for conf.
        section (str): Input value for section.
        key (str): Input value for key.
        default (Optional[str]): Input value for default.

    Returns:
        Optional[str]: Computed result of the operation.
    """
    if conf.has_section(section):
        return conf[section].get(key, default)
    return default


@lru_cache(maxsize=1)
def get_settings(config_file: str = 'application.ini') -> DataScopeSettings:
    """Return settings.

    Args:
        config_file (str): Input value for config file.

    Returns:
        DataScopeSettings: Requested value for the lookup.
    """
    config_path = Path(__file__).resolve().parents[2] / config_file
    conf = _read_ini(config_path)

    gateway_ip = os.getenv(
        'DATASCOPE_GATEWAY_IP',
        _ini_value(conf, 'gateway', 'ip', 'selectapi.datascope.refinitiv.com/RestApi/v1'),
    )
    auth_service = os.getenv(
        'DATASCOPE_AUTH_SERVICE',
        _ini_value(conf, 'auth', 'service', 'Authentication'),
    )

    username = os.getenv('DATASCOPE_USERNAME', _ini_value(conf, 'auth', 'username'))
    password = os.getenv('DATASCOPE_PASSWORD', _ini_value(conf, 'auth', 'password'))

    timeout = float(os.getenv('DATASCOPE_TIMEOUT_SECONDS', '600'))
    max_retries = int(os.getenv('DATASCOPE_MAX_RETRIES', '3'))
    backoff = float(os.getenv('DATASCOPE_RETRY_BACKOFF_SECONDS', '0.2'))

    return DataScopeSettings(
        gateway_ip=gateway_ip,
        auth_service=auth_service,
        username=username,
        password=password,
        request_timeout_seconds=timeout,
        max_retries=max_retries,
        retry_backoff_seconds=backoff,
    )
