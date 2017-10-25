"Contains constats required for commands"
import os
from reandeploy.utility import Utility

class Constants(object):
    "Contains constats required for CLI"

    HOST_PATH = "https://deploynow.reancloud.com/DeployNow/rest"
    AUTHORIZATION = "Authorization"
    CREDENTIALS = Utility.get_username_and_password()

    def __setattr__(self, attr, value):
        if hasattr(self, attr):
            raise Exception("Attempting to alter read-only value")

        self.__dict__[attr] = value
