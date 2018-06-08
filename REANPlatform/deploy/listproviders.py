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
        format = parsed_args.format
        self.list_provider(format)

    def list_provider(self, format):
        """list_provider."""
        try:
            provider_api_instance = deploy_sdk_client.ProviderApi()
            api_instance = set_header_parameter(provider_api_instance)
            api_response = api_instance.get_all_providers()
            if format == 'table':
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
            elif format == 'json' or format == '':
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
        except ApiException as e:
            Utility.print_exception(e)
