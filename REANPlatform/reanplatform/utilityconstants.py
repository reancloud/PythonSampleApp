"""Contains constats required for Utility."""


class PlatformConstants(object):
    """Contains constats required for Utility."""

    PLATFORM_CONFIG_FILE_NAME = 'reanplatform'
    REAN_SECRET_KEY = 'UjXnZr4u7x!A%D*G-KaPdSgVkYp3s5v8'
    PLATFORM_REFERENCE = 'platform'
    USER_NAME_REFERENCE = 'username'
    PASSWORD_REFERENCE = 'password'
    BASE_URL_REFERENCE = 'base_url'
    ENV_USER_NAME_REFERENCE = 'USER_NAME'
    ENV_PASSWORD_REFERENCE = 'PASSWORD'
    ENV_BASE_URL_REFERENCE = 'BASE_URL'
    VERIFY_SSL_CERTIFICATE_REFERENCE = 'verify_ssl_certificate'
    DICT_REFERENCE = 'dict'
    TABLE_REFERENCE = 'table'
    STR_REFERENCE = 'str'

    def __setattr__(self, attr, value):
        """__setattr__."""
        if hasattr(self, attr):
            raise Exception("Attempting to alter read-only value")

        self.__dict__[attr] = value
