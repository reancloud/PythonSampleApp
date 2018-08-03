"""Contains constats required for commands."""
from reanplatform.utility import Utility
from reanplatform.utilityconstants import PlatformConstants


class Constants(object):
    """Contains constats required for CLI."""

    PLATFORM_BASE_URL = Utility.get_config_property(PlatformConstants.BASE_URL_REFERENCE)
    # PLATFORM_URL_WITH_HOST = Utility.get_host_url()
    AUTHNZ_URL = '/api'
    DEPLOY_URL = '/api/reandeploy/DeployNow/rest'
    TEST_URL = '/api/reantest/TestNow/rest'
    MNC_URL = '/api/'
    AUTHORIZATION = "Authorization"
    CREDENTIALS = Utility.get_user_credentials()
    PLATFORM_CONFIG_FILE_NAME = 'reanplatform'

    def __setattr__(self, attr, value):
        """__setattr__."""
        if hasattr(self, attr):
            raise Exception("Attempting to alter read-only value")

        self.__dict__[attr] = value
