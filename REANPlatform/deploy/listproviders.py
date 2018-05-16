"""List provider module."""
import logging
from pprint import pprint
from cliff.command import Command
import deploy_sdk_client
from deploy_sdk_client.rest import ApiException
from deploy.constants import Constants
import json
from deploy import set_provider_header
from prettytable import PrettyTable


class ListProvider(Command):
    """List of providers for current user."""

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        """Parser of ListProviders."""
        parser = super(ListProvider, self).get_parser(prog_name)
        parser.add_argument('--formate', '-f',
                            help='List formate eg. json Or table',
                            type=str, default='json',
                            nargs='?',
                            required=False)
        return parser

    def take_action(self, parsed_args):
        """take_action of ListProvider."""
        try:
            # create an instance of the API class
            api_instance = set_provider_header.set_header()

            # Get all providers for user
            api_response = api_instance.get_all_providers()
            if parsed_args.formate == 'table':
                table = PrettyTable(['Name', 'Id', 'Type', 'Created by'])
                table.padding_width = 1
                for provider in api_response:
                    table.add_row(
                                [
                                    provider.name,
                                    provider.id,
                                    provider.type,
                                    provider.created_by
                                ]
                            )
                print("Provider list ::\n%s" % (table))

            else:
                print(
                        json.dumps(
                                api_response,
                                default=lambda o: o.__dict__,
                                sort_keys=True, indent=4
                                )
                    )
        except ApiException as e:
            print("Exception when calling ProviderApi->\
                    get_all_providers: %s\n" % e)
