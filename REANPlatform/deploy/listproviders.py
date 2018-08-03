"""List provider module."""
import json
import logging
from prettytable import PrettyTable
from cliff.command import Command
import deploy_sdk_client
from deploy_sdk_client.rest import ApiException
from reanplatform.set_header import set_header_parameter
from reanplatform.utility import Utility
from deploy.constants import DeployConstants


class ListProvider(Command):
    """List providers."""

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        """Parser of ListProviders."""
        parser = super(ListProvider, self).get_parser(prog_name)
        parser.add_argument('--format', '-f',
                            help='Allowed values are: [json, table]',
                            type=str, default='json',
                            nargs='?',
                            required=False)
        return parser

    def take_action(self, parsed_args):
        """take_action of ListProvider."""
        list_provider_format = parsed_args.format
        ListProvider.list_provider(list_provider_format)

    @staticmethod
    def list_provider(list_provider_format):
        """list_provider."""
        try:
            provider_api_instance = deploy_sdk_client.ProviderApi()
            api_instance = set_header_parameter(provider_api_instance, Utility.get_url(DeployConstants.DEPLOY_URL))
            api_response = api_instance.get_all_providers()
            if list_provider_format == 'table':
                table = PrettyTable(['Name', 'Id', 'Type'])
                table.padding_width = 1
                for provider in api_response:
                    table.add_row(
                        [
                            provider.name,
                            provider.id,
                            provider.type
                        ]
                    )
                print("Provider list ::\n%s" % (table))
            elif list_provider_format == 'json' or list_provider_format == '':
                print(
                    json.dumps(
                        api_response,
                        default=lambda o: o.__dict__,
                        sort_keys=True, indent=4
                        ).replace("\"_", '"')
                    )
            else:
                raise RuntimeError("Please specify correct fromate, Allowed \
                        values are: [json, table]")
        except ApiException as api_exception:
            Utility.print_exception(api_exception)
