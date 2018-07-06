"""Contains constats required for Utility."""


class UtilityConstants(object):
    """Contains constats required for Utility."""

    PLATFORM_CONFIG_FILE_NAME = 'reanplatform'
    REAN_SECRET_KEY = 'Rnni%ypUaahh'
    PLATFORM_REFERENCE = 'platform'
    USER_NAME_REFERENCE = 'username'
    PASSWORD_REFERENCE = 'password'
    BASE_URL_REFERENCE = 'base_url'

    def __setattr__(self, attr, value):
        """__setattr__."""
        if hasattr(self, attr):
            raise Exception("Attempting to alter read-only value")

        self.__dict__[attr] = value
