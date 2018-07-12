"""Utility class contains all common method requried for CLI."""
import os
import base64
import json
from Crypto.Cipher import XOR
import yaml
from reanplatform.utilityconstants import PlatformConstants, EnvironmentVariables


class Utility(object):
    """Utility class contains all common method requried for CLI."""

    @staticmethod
    def get_user_name_password():
        """Get configured username and password."""
        try:
            credentials = Utility.get_env_username_password()
            if credentials:
                if credentials.get('user_name') and credentials.get('password'):
                    credentials = str(credentials.get('user_name')) + ":" + str(credentials.get('password'))
                else:
                    credentials = Utility.get_username_password_from_file()
            else:
                credentials = Utility.get_username_password_from_file()
            return credentials
        except Exception as exception:
            print('Could not get user name and password.')

    @staticmethod
    def get_platform_base_url():
        """Get platform base url."""
        path = os.path.expanduser('~')
        if os.path.exists(path + '/.' + PlatformConstants.PLATFORM_CONFIG_FILE_NAME):
            os.chdir(path + '/.' + PlatformConstants.PLATFORM_CONFIG_FILE_NAME)
            if os.path.isfile(PlatformConstants.PLATFORM_CONFIG_FILE_NAME + '.yaml'):
                with open(PlatformConstants.PLATFORM_CONFIG_FILE_NAME + ".yaml", 'r') as stream:    # noqa: E501
                    data_loaded = yaml.load(stream)

                host = data_loaded[PlatformConstants.PLATFORM_REFERENCE][PlatformConstants.BASE_URL_REFERENCE]
                return host

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
        base_url = Utility.get_platform_base_url()
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
                'user_name': os.environ[EnvironmentVariables.USER_NAME_REFERENCE],
                'password': os.environ[EnvironmentVariables.PASSWORD_REFERENCE]
            }
            return credentials
        except KeyError:
            return False

    @staticmethod
    def get_username_password_from_file():
        """Get user name and password from config file."""
        credentials = ""
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
