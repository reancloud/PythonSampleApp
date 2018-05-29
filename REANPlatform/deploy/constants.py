"Contains constats required for commands"
import os
from reanplatform.utility import Utility

class Constants(object):
    "Contains constats required for CLI"

    HOST_PATH = Utility.getPlatformUrl()
    AUTHORIZATION = "Authorization"
    CREDENTIALS = Utility.getUserNameAndPassword()
    REAN_PLATFORM = 'reanplatform'

    def __setattr__(self, attr, value):
        if hasattr(self, attr):
            raise Exception("Attempting to alter read-only value")

        self.__dict__[attr] = value