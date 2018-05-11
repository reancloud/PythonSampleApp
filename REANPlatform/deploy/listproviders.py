"""List provider module."""
import logging
from pprint import pprint
from cliff.command import Command
import deploy_sdk_client
from deploy_sdk_client.rest import ApiException
from deploy.constants import Constants


class ListProvider(Command):
    """List of providers."""

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        """Parser of ListProviders."""
        parser = super(ListProvider, self).get_parser(prog_name)
        return parser

    def take_action(self, parsed_args):
        """take_action ListProvider."""
        try:
            # create an instance of the API class
            api_instance = deploy_sdk_client.ProviderApi()
            api_instance.api_client.set_default_header(
                Constants.AUTHORIZATION,
                Constants.CREDENTIALS
            )
            api_instance.api_client.host = Constants.HOST_PATH

            # Get all providers for user
            api_response = api_instance.get_all_providers()
            pprint(api_response)
        except ApiException as e:
            print("Exception when calling ProviderApi->\
                    get_all_providers: %s\n" % e)
