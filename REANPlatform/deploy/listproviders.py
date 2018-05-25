"""List provider module."""
import logging
from pprint import pprint
from cliff.command import Command
import deploy_sdk_client
from deploy_sdk_client.rest import ApiException
import json
from reanplatform.set_header import set_header_parameter
from prettytable import PrettyTable
from reanplatform.utility import Utility


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
        try:
            # create an instance of the API class
            provider_api_instance = deploy_sdk_client.ProviderApi()
            api_instance = set_header_parameter(provider_api_instance)

            # Get all providers for user
            api_response = api_instance.get_all_providers()
            if parsed_args.format == 'table':
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

            else:
                print(
                        json.dumps(
                                api_response,
                                default=lambda o: o.__dict__,
                                sort_keys=True, indent=4
                                ).replace("\"_", '"')
                    )
        except ApiException as e:
            Utility.print_exception(e)
