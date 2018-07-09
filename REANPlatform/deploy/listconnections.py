"""List connections module."""
import json
import re
import logging
from prettytable import PrettyTable
from cliff.command import Command
import deploy_sdk_client
from deploy_sdk_client.rest import ApiException
from reanplatform.set_header import set_header_parameter
from reanplatform.utility import Utility
from deploy.constants import DeployConstants


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
        return parser

    def take_action(self, parsed_args):
        """take_action."""
        format = parsed_args.format
        ListConnections.list_connection(format)

    @staticmethod
    def list_connection(format):
        """list_connection."""
        try:
            conn_api_instance = deploy_sdk_client.ConnectionApi()
            base_url = Utility.get_platform_base_url()
            deploy_url = DeployConstants.DEPLOY_URL
            api_instance = set_header_parameter(conn_api_instance, base_url + deploy_url)
            api_response = api_instance.get_all_vm_connections()

            if format == 'table':
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
                print("Connection list \n%s" % (table))
            elif format == 'json' or format == '':
                print(
                    json.dumps(
                        api_response,
                        default=lambda o: o.__dict__,
                        sort_keys=True, indent=4
                        ).replace("\"_", '"')
                    )
            else:
                exception_msg = "Please specify correct fromate, Allowed \
                        values are: [json, table]"
                raise RuntimeError(re.sub(' +', ' ', exception_msg))

        except ApiException as e:
            Utility.print_exception(e)
