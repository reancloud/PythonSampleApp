"""Provider set_header module."""
import deploy_sdk_client
from deploy_sdk_client.rest import ApiException
from deploy.constants import Constants


def set_header():
    """Set header to provider API call."""
    provider_api_instance = deploy_sdk_client.ProviderApi()
    provider_api_instance.api_client.set_default_header(
                    Constants.AUTHORIZATION,
                    Constants.CREDENTIALS
    )
    provider_api_instance.api_client.host = Constants.HOST_PATH
    return provider_api_instance
