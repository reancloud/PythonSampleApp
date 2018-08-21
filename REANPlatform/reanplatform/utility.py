"""Utility class contains all common method requried for CLI."""
import os
import base64
import json
import yaml
import urllib3
from Crypto.Cipher import XOR
from reanplatform.utilityconstants import PlatformConstants
from deploy_sdk_client.api_client import ApiClient
from deploy_sdk_client.configuration import Configuration


class Utility(object):
    """Utility class contains all common method requried for CLI."""

    @staticmethod
    def get_user_credentials():
        """Get configured username and password."""
        try:
            credentials = Utility.get_env_username_password()
            if credentials and credentials.get('user_name') and credentials.get('password'):
                credentials = str(credentials.get('user_name')) + ":" + str(credentials.get('password'))
            else:
                credentials = Utility.get_username_password_from_file()
            return credentials
        except Exception as exception:
            print('Could not get username and password.')
            return None

    @staticmethod
    def encryptData(val):
        """Encrypts credentials."""
        cipher = XOR.new(PlatformConstants.REAN_SECRET_KEY)
        encoded = base64.b64encode(cipher.encrypt(val))
        return encoded

    @staticmethod
    def decryptData(encoded):
        """Decrypts credentials."""
        cipher = XOR.new(PlatformConstants.REAN_SECRET_KEY)
        decoded = cipher.decrypt(base64.b64decode(encoded))
        return decoded

    @staticmethod
    def print_exception(exception):
        """Print exception method."""
        print("Exception message: ")
        err = json.loads(exception.body)
        print("%s %s" % (err['message'], err['status']))

    @staticmethod
    def get_url(host_url):
        """Get full URL."""
        base_url = Utility.get_config_property(PlatformConstants.BASE_URL_REFERENCE)
        return base_url + host_url

    @staticmethod
    def get_parsed_json(json_object):
        """Get parsed json."""
        return json.dumps(
            json_object,
            default=lambda o: o.__dict__,
            sort_keys=True, indent=4
        ).replace("\"_", '"')

    @staticmethod
    def get_env_username_password():
        """Get Environment variables."""
        try:
            credentials = {
                'user_name': os.environ[PlatformConstants.ENV_USER_NAME_REFERENCE],
                'password': os.environ[PlatformConstants.ENV_PASSWORD_REFERENCE]
            }
            return credentials
        except KeyError:
            return False

    @staticmethod
    def get_username_password_from_file():
        """Get user name and password from config file."""
        path = os.path.expanduser('~')
        if os.path.exists(path + '/.' + PlatformConstants.PLATFORM_CONFIG_FILE_NAME):
            os.chdir(path + '/.' + PlatformConstants.PLATFORM_CONFIG_FILE_NAME)
            if os.path.isfile(PlatformConstants.PLATFORM_CONFIG_FILE_NAME + '.yaml'):
                with open(PlatformConstants.PLATFORM_CONFIG_FILE_NAME + ".yaml", 'r') as stream:    # noqa: E501
                    data_loaded = yaml.load(stream)

                username = Utility.decryptData(
                    data_loaded[PlatformConstants.PLATFORM_REFERENCE][PlatformConstants.USER_NAME_REFERENCE]).decode('utf-8')
                password = Utility.decryptData(
                    data_loaded[PlatformConstants.PLATFORM_REFERENCE][PlatformConstants.PASSWORD_REFERENCE]).decode('utf-8')
                credentials = str(username) + ":" + str(password)
                return credentials
        return None

    @staticmethod
    def get_config_property(prop):
        """Get ssl verify certification status from config file."""
        path = os.path.expanduser('~')
        if os.path.exists(path + '/.' + PlatformConstants.PLATFORM_CONFIG_FILE_NAME):
            os.chdir(path + '/.' + PlatformConstants.PLATFORM_CONFIG_FILE_NAME)
            if os.path.isfile(PlatformConstants.PLATFORM_CONFIG_FILE_NAME + '.yaml'):
                with open(PlatformConstants.PLATFORM_CONFIG_FILE_NAME + ".yaml", 'r') as stream:    # noqa: E501
                    data_loaded = yaml.load(stream)

                config_property = data_loaded[PlatformConstants.PLATFORM_REFERENCE][prop]
                return config_property
