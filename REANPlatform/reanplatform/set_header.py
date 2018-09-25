"""Set header and URL module."""

from reanplatform.constants import Constants
from reanplatform.utility import Utility
from reanplatform.utilityconstants import PlatformConstants

def set_header_parameter(api_client, host):
    """Set header."""
    api_client.set_default_header(
        Constants.AUTHORIZATION,
        Constants.CREDENTIALS
    )
    api_client.host = host
    api_client.verify_ssl = Utility.get_config_property(PlatformConstants.VERIFY_SSL_CERTIFICATE_REFERENCE)
    return api_client
