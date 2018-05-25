"""Delete provider module."""
import logging
from cliff.command import Command
import deploy_sdk_client
from deploy_sdk_client.rest import ApiException
from reanplatform.set_header import set_header_parameter
from reanplatform.utility import Utility


class DeleteProvider(Command):
    """Delete provider."""

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        """get_parser."""
        parser = super(DeleteProvider, self).get_parser(prog_name)
        parser.add_argument('--id', '-id', help='Provider id', required=True)
        return parser

    def take_action(self, parsed_args):
        """Delete provider action."""
        try:
            provider_api_instance = deploy_sdk_client.ProviderApi()
            api_instance = set_header_parameter(provider_api_instance)
            api_response = api_instance.delete_provider(parsed_args.id)
            print("Provider deleted successfully")
        except Exception as e:
            print("======================")
            print(e)
            Utility.print_exception(e)
