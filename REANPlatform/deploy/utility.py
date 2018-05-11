"""Utility class contains all common method requried for CLI."""
import os
from deploy.utilityconstants import Constants
import yaml
from Crypto.Cipher import XOR
import base64


class Utility(object):
    """Utility class contains all common method requried for CLI."""

    @staticmethod
    def getUserNameAndPassword():
        """Get configured username and password."""
        path = os.path.expanduser('~')
        if os.path.exists(path + '/.' + Constants.REAN_PLATFORM):
            os.chdir(path + '/.' + Constants.REAN_PLATFORM)
            if os.path.isfile(Constants.REAN_PLATFORM + '.yaml'):
                with open(Constants.REAN_PLATFORM + ".yaml", 'r') as stream:
                    data_loaded = yaml.load(stream)

                username = Utility.decryptData(
                            data_loaded['deploy']['username']).decode('utf-8')
                password = Utility.decryptData(
                            data_loaded['deploy']['password']).decode('utf-8')
                credentials = str(username) + ":" + str(password)
                return credentials

    @staticmethod
    def getHost():
        """Get configured username and password."""
        path = os.path.expanduser('~')
        if os.path.exists(path + '/.' + Constants.REAN_PLATFORM):
            os.chdir(path + '/.' + Constants.REAN_PLATFORM)
            if os.path.isfile(Constants.REAN_PLATFORM + '.yaml'):
                with open(Constants.REAN_PLATFORM + ".yaml", 'r') as stream:
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
