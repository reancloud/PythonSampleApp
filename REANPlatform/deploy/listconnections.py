"""List connections module."""
import re
import logging
from prettytable import PrettyTable
from cliff.command import Command
import deploy_sdk_client
from deploy_sdk_client.rest import ApiException
from reanplatform.set_header import set_header_parameter
from reanplatform.utility import Utility
from deploy.constants import DeployConstants
from deploy.utility import DeployUtility


class ListConnections(Command):
    """List connections."""

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        """get_parser."""
        parser = super(ListConnections, self).get_parser(prog_name)
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
        """take_action."""
        list_connection_format = parsed_args.format
        ListConnections.list_connection(list_connection_format, parsed_args)

    @staticmethod
    def list_connection(list_connection_format, parsed_args):
        """list_connection."""
        try:
            api_client = set_header_parameter(DeployUtility.create_api_client(), Utility.get_url(DeployConstants.DEPLOY_URL))
            conn_api_instance = deploy_sdk_client.ConnectionApi(api_client)
            api_response = conn_api_instance.get_all_vm_connections()

            if list_connection_format == 'table':
                table = PrettyTable(['Name', 'Id', 'Type'])
                table.padding_width = 1
                for connection in api_response:
                    table.add_row(
                        [
                            connection.name,
                            connection.id,
                            connection.type
                        ]
                    )
                Utility.print_output_as_table("Connection list \n{}".format(table), parsed_args.output)
            elif list_connection_format == 'json' or list_connection_format == '':
                Utility.print_output_as_dict(api_response, parsed_args.output)
            else:
                exception_msg = "Please specify correct format, Allowed values are: [json, table]"
                raise RuntimeError(re.sub(' +', ' ', exception_msg))

        except ApiException as api_exception:
            Utility.print_exception(api_exception)
