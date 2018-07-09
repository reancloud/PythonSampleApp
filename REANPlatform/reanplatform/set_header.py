"""Set header and URL module."""
from reanplatform.constants import Constants

def set_header_parameter(api_instance, host):
    """Set header."""
    api_instance.api_client.set_default_header(
        Constants.AUTHORIZATION,
        Constants.CREDENTIALS
    )
    api_instance.api_client.host = host
    return api_instance
