"""Contains constats required for commands."""
import os
from reanplatform.utility import Utility


class Constants(object):
    """Contains constats required for CLI."""

    HOST_PATH = Utility.getHost()
    AUTHORIZATION = "Authorization"
    CREDENTIALS = Utility.getUserNameAndPassword()
    PLATFORM_CONFIG_FILE_NAME = 'reanplatform'

    def __setattr__(self, attr, value):
        """__setattr__."""
        if hasattr(self, attr):
            raise Exception("Attempting to alter read-only value")

        self.__dict__[attr] = value
