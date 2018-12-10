"""List provider module."""
import logging
from prettytable import PrettyTable
from cliff.command import Command
import deploy_sdk_client
from deploy_sdk_client.rest import ApiException
from reanplatform.set_header import set_header_parameter
from reanplatform.utility import Utility
from deploy.constants import DeployConstants
from deploy.utility import DeployUtility


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
        parser.add_argument('--output', '-o',
                            help="Write output to <file> instead of stdout.",
                            required=False
                           )
        return parser

    def take_action(self, parsed_args):
        """take_action of ListProvider."""
        list_provider_format = parsed_args.format
        ListProvider.list_provider(list_provider_format, parsed_args)

    @staticmethod
    def list_provider(list_provider_format, parsed_args):
        """list_provider."""
        try:
            api_client = set_header_parameter(DeployUtility.create_api_client(), Utility.get_url(DeployConstants.DEPLOY_URL))
            provider_api_instance = deploy_sdk_client.ProviderApi(api_client)
            api_response = provider_api_instance.get_all_providers()
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
                Utility.print_output_as_table("Provider list \n{}".format(table), parsed_args.output)
            elif list_provider_format == 'json' or list_provider_format == '':
                Utility.print_output_as_dict(api_response, parsed_args.output)
            else:
                raise RuntimeError("Please specify correct format, Allowed values are: [json, table]")
        except ApiException as api_exception:
            Utility.print_exception(api_exception)
