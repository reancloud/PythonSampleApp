"""List all providers."""

import json
import logging
from prettytable import PrettyTable
from cliff.command import Command
import test_sdk_client
from test_sdk_client.rest import ApiException
from reantest.utility import Utility


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
            api_instance = test_sdk_client.ProviderApi()
            api_response = api_instance.get_all_providers()
            if list_provider_format == 'table':
                table = PrettyTable(['Id', 'Name', 'Type', 'Access Key', 'Secret \
                Key', 'Region', 'Bucket Name', 'Instance Profile ARN', 'Default provider', 'KeyPair Name', 'Security \
                group', 'Subnet id', 'Instance Role', 'Use public ip'])
                table.padding_width = 1
                for provider in api_response:
                    table.add_row(
                        [
                            provider.id,
                            provider.name,
                            provider.type,
                            provider.data['access_key'],
                            provider.data['secret_key'],
                            provider.data['region'],
                            provider.bucket_name,
                            provider.instance_profile_arn,
                            provider.default_provider,
                            provider.key_pair_name,
                            provider.security_group_id,
                            provider.subnet_id,
                            provider.test_instance_role,
                            provider.use_public_ip
                        ]
                    )
                print("Provider list ::\n%s" % table)
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
