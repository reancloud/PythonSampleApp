"""Set header and URL module."""
import reanplatform
from reanplatform.constants import Constants


def set_header_parameter(api_instance):
    """Set header."""
    api_instance.api_client.set_default_header(Constants.AUTHORIZATION, Constants.CREDENTIALS)
    api_instance.api_client.host = Constants.PLATFORM_URL
    return api_instance
