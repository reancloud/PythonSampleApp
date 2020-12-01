"""Utility class contains all common method requried for CLI."""
import os
import urllib3
from reanplatform.utilityconstants import PlatformConstants
from reanplatform.utility import Utility
from workflow_sdk_client.api_client import ApiClient
from workflow_sdk_client.configuration import Configuration


class WorkflowUtility:
    """Utility class contains all common method requried for CLI."""

    @staticmethod
    def create_api_client():
        """Create API client."""
        verify_ssl = Utility.get_config_property(PlatformConstants.VERIFY_SSL_CERTIFICATE_REFERENCE)
        if not verify_ssl:
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

        if verify_ssl:
            ssl_ca_cert = Utility.get_config_property(PlatformConstants.SSL_CERTIFICATE_PATH_REFERENCE)
            if os.path.exists(ssl_ca_cert):
                Configuration().ssl_ca_cert = ssl_ca_cert
            else:
                RuntimeError('Configured SSL path is invalid.')

        Configuration().verify_ssl = verify_ssl
        api_client = ApiClient()
        return api_client
