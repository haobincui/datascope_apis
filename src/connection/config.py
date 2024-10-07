import configparser
import errno
import os
from os import strerror


def _get_url(conf, service):
    ip = conf[service].get('ip', 'localhost')
    port = conf[service].get('port', '16016')
    prefix = conf[service].get('service', None)
    return f'http://{ip}:{port}/' if prefix is None else f'http://{ip}:{port}/{prefix}/'


class Config:
    def __init__(self, f = 'application.ini'):

        file = os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(__file__)), f))
        conf = configparser.ConfigParser()
        r = conf.read(file, encoding='utf-8')
        if not r:
            raise FileNotFoundError(errno.ENOENT, strerror(errno.ENOENT), file)
        ip = conf['gateway'].get('ip', 'localhost')
        port = conf['gateway'].get('port', '16016')
        self.ip = ip
        self.base_url = f'https://{ip}/'
        self.auth_base_url = self.base_url + conf['auth'].get('service', 'Authentication')
        # self.auth_url = self.auth_base_url + 'users/login'
        self.request_token_url = self.auth_base_url + '/RequestToken'
        self.auth_username = conf['auth'].get('username')
        self.auth_password = conf['auth'].get('password')
        self.search_url = self.base_url + 'Search/'
        self.extraction_url = self.base_url + 'Extractions/'
        self.output_docs_path = conf['docs'].get('output_docs_path')
        self.input_docs_path = conf['docs'].get('input_docs_path')


_config = None


def get_config(f='application.ini'):
    global _config
    if _config is None:
        _config = Config(f)
    return _config
