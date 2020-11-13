import os
from configparser import ConfigParser, SectionProxy
from argparse import ArgumentError, ArgumentTypeError

from ibm_watson import SpeechToTextV1
from ibm_cloud_sdk_core.authenticators import BearerTokenAuthenticator, IAMAuthenticator, Authenticator

import logging
LOG = logging.getLogger('watson_stt_tester.utils')

class ConfigError(Exception): pass

class RequiredConfigMissingError(ConfigError):
    def __init__(self, key):
        super(ConfigError).__init__(f'Required config key {key} missing.')

def get_required(s: SectionProxy, key):
    val = s.get(key)
    if key is None:
        raise RequiredConfigMissingError(key)
    return val

def choose_authenticator(config: ConfigParser) -> Authenticator:
    creds = config['CREDENTIALS']
    apikey = get_required(creds, 'api_key')

    if apikey is None:
        raise RequiredConfigMissingError('api_key')

    if creds.get('auth_method', 'iam') == 'bearer':
        LOG.warning('Using bearer token authentication')
        return BearerTokenAuthenticator(apikey)
    else:
        LOG.warning('Using IAM authentication')
        return IAMAuthenticator(
            apikey
        )



def init_stt(config: ConfigParser):
    creds = config['CREDENTIALS']
    url = creds.get('url')
    authenticator = choose_authenticator(config)

    stt = SpeechToTextV1(
        authenticator=authenticator
    )
    stt.set_service_url(url)
    return stt

def load_config(path: str):
    """
    Load the config.ini file
    """
    if not os.path.exists(path):
        raise ArgumentTypeError(f'Config file "{path}" does not exist.')
    c = ConfigParser()
    with open(path, 'r') as config_f:
        c.read_file(config_f)
        return c

