"""Utility class contains all common method requried for CLI."""
import os
from reanplatform.utilityconstants import Constants
import yaml
from Crypto.Cipher import XOR
import base64
import json


class Utility(object):
    """Utility class contains all common method requried for CLI."""

    @staticmethod
    def getUserNameAndPassword():
        """Get configured username and password."""
        path = os.path.expanduser('~')
        if os.path.exists(path + '/.' + Constants.PLATFORM_CONFIG_FILE_NAME):
            os.chdir(path + '/.' + Constants.PLATFORM_CONFIG_FILE_NAME)
            if os.path.isfile(Constants.PLATFORM_CONFIG_FILE_NAME + '.yaml'):
                with open(Constants.PLATFORM_CONFIG_FILE_NAME + ".yaml", 'r') as stream:    # noqa: E501
                    data_loaded = yaml.load(stream)

                username = Utility.decryptData(data_loaded['deploy']['username']).decode('utf-8')
                password = Utility.decryptData(data_loaded['deploy']['password']).decode('utf-8')
                credentials = str(username) + ":" + str(password)
                return credentials

    @staticmethod
    def getPlatformUrl():
        """Get configured username and password."""
        path = os.path.expanduser('~')
        if os.path.exists(path + '/.' + Constants.PLATFORM_CONFIG_FILE_NAME):
            os.chdir(path + '/.' + Constants.PLATFORM_CONFIG_FILE_NAME)
            if os.path.isfile(Constants.PLATFORM_CONFIG_FILE_NAME + '.yaml'):
                with open(Constants.PLATFORM_CONFIG_FILE_NAME + ".yaml", 'r') as stream:    # noqa: E501
                    data_loaded = yaml.load(stream)

                host = data_loaded['deploy']['host']
                return host

    @staticmethod
    def encryptData(val):
        """Encrypts credentials."""
        cipher = XOR.new(Constants.REAN_SECRET_KEY)
        encoded = base64.b64encode(cipher.encrypt(val))
        return encoded

    @staticmethod
    def decryptData(encoded):
        """Decrypts credentials."""
        cipher = XOR.new(Constants.REAN_SECRET_KEY)
        decoded = cipher.decrypt(base64.b64decode(encoded))
        return decoded

    def print_exception(e):
        """Print exception method."""
        print("Exception message: ")
        err = json.loads(e.body)
        print("%s %s" % (err['message'], err['status']))
