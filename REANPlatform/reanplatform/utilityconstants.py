"""Contains constats required for Utility."""


class PlatformConstants(object):
    """Contains constats required for Utility."""

    PLATFORM_CONFIG_FILE_NAME = 'reanplatform'
    REAN_SECRET_KEY = 'Rnni%ypUaahh'
    PLATFORM_REFERENCE = 'platform'
    USER_NAME_REFERENCE = 'username'
    PASSWORD_REFERENCE = 'password'
    ENV_BASE_URL_REFERENCE = 'BASE_URL'
    ENV_USER_NAME_REFERENCE = 'USER_NAME'
    ENV_PASSWORD_REFERENCE = 'PASSWORD'
    VERIFY_SSL_CERTIFICATE_REFERENCE = 'verify_ssl_certificate'

    def __setattr__(self, attr, value):
        """__setattr__."""
        if hasattr(self, attr):
            raise Exception("Attempting to alter read-only value")

        self.__dict__[attr] = value
