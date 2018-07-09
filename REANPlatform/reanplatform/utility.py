"""Utility class contains all common method requried for CLI."""
import os
import base64
import json
import yaml
from Crypto.Cipher import XOR
from reanplatform.utilityconstants import PlatformConstants


class Utility(object):
    """Utility class contains all common method requried for CLI."""

    @staticmethod
    def getUserNameAndPassword():
        """Get configured username and password."""
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

    @staticmethod
    def get_platform_base_url():
        """Get configured username and password."""
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
