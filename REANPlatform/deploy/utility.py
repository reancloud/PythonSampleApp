"""Utility class contains all common method requried for CLI."""
import urllib3
from reanplatform.utilityconstants import PlatformConstants
from reanplatform.utility import Utility
from deploy_sdk_client.api_client import ApiClient
from deploy_sdk_client.configuration import Configuration


class DeployUtility:
    """Utility class contains all common method requried for CLI."""

    @staticmethod
    def create_api_client():
        """Create API client."""
        verify_ssl = Utility.get_config_property(PlatformConstants.VERIFY_SSL_CERTIFICATE_REFERENCE)
        if not verify_ssl:
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        Configuration().verify_ssl = verify_ssl
        api_client = ApiClient()
        return api_client
