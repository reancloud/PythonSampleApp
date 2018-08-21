"""Utility class for authnz."""
import urllib3
from reanplatform.utilityconstants import PlatformConstants
from reanplatform.utility import Utility
from authnz_sdk_client.api_client import ApiClient
from authnz_sdk_client.configuration import Configuration


class AuthnzUtility(object):
    """Utility class contains all common method requried for Authnz CLI."""

    @staticmethod
    def get_user_dict(user):
        """Return dictionary of user details."""
        dict_object = {
            'id': user.id,
            'name': user.name,
            'username': user.username,
            'email': user.email,
            'verified': user.verified,
            'disabled': user.disabled
        }
        return dict_object

    @staticmethod
    def create_api_client():
        """Create API client."""
        verify_ssl = Utility.get_config_property(PlatformConstants.VERIFY_SSL_CERTIFICATE_REFERENCE)
        if not verify_ssl:
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        Configuration().verify_ssl = verify_ssl
        api_client = ApiClient()
        return api_client
