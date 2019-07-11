"""Utility class for authnz."""
import urllib3
from reanplatform.utilityconstants import PlatformConstants
from reanplatform.set_header import set_header_parameter
from reanplatform.utility import Utility as PlatformUtility
from auth.constants import AunthnzConstants
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
        verify_ssl = PlatformUtility.get_config_property(PlatformConstants.VERIFY_SSL_CERTIFICATE_REFERENCE)
        if not verify_ssl:
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        Configuration().verify_ssl = verify_ssl
        api_client = ApiClient()
        return api_client

    @staticmethod
    def set_headers():
        """Set headers."""
        return set_header_parameter(AuthnzUtility.create_api_client(), PlatformUtility.get_url(AunthnzConstants.AUTHNZ_URL))
