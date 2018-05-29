"""List connections module."""
import logging
from cliff.command import Command
import deploy_sdk_client
import json
from deploy_sdk_client.rest import ApiException
from reanplatform.set_header import set_header_parameter
from prettytable import PrettyTable
from reanplatform.utility import Utility


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
        try:
            conn_api_instance = deploy_sdk_client.ConnectionApi()
            api_instance = set_header_parameter(conn_api_instance)
            api_response = api_instance.get_all_vm_connections()

            if parsed_args.format == 'table':
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
            elif parsed_args.format == 'json' or parsed_args.format == '':
                print(
                        json.dumps(
                                api_response,
                                default=lambda o: o.__dict__,
                                sort_keys=True, indent=4
                                ).replace("\"_", '"')
                    )
            else:
                raise RuntimeError("Please specify correct formate, Allowed \
                        values are: [json, table]")

        except ApiException as e:
            Utility.print_exception(e)
