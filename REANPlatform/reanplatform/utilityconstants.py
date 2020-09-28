"""Contains constats required for Utility."""


class PlatformConstants(object):
    """Contains constats required for Utility."""

    PLATFORM_CONFIG_FILE_NAME = 'reanplatform'

    PLATFORM_REFERENCE = 'platform'
    USER_NAME_REFERENCE = 'username'
    PASSWORD_REFERENCE = 'password'
    BASE_URL_REFERENCE = 'base_url'
    VERIFY_SSL_CERTIFICATE_REFERENCE = 'verify_ssl_certificate'
    SSL_CERTIFICATE_PATH_REFERENCE = 'ssl_certificate_path'

    # Environment variables references
    ENV_USER_NAME_REFERENCE = 'REAN_PLATFORM_USER_NAME'
    ENV_PASSWORD_REFERENCE = 'REAN_PLATFORM_PASSWORD'
    ENV_BASE_URL_REFERENCE = 'REAN_PLATFORM_BASE_URL'
    ENV_VERIFY_SSL_CERTIFICATE_REFERENCE = 'REAN_PLATFORM_VERIFY_SSL'
    ENV_SSL_CERTIFICATE_PATH_REFERENCE = 'REAN_PLATFORM_SSL_CERTIFICATE_PATH'

    ENV_CONFIG_FILE_PATH_REFERENCE = 'REAN_PLATFORM_CONFIG_FILE_PATH'

    DICT_REFERENCE = 'dict'
    TABLE_REFERENCE = 'table'
    STR_REFERENCE = 'str'

    def __setattr__(self, attr, value):
        """__setattr__."""
        if hasattr(self, attr):
            raise Exception("Attempting to alter read-only value")

        self.__dict__[attr] = value
