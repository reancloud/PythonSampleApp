"""Delete connection module."""
import os
from pprint import pprint
import logging
from cliff.command import Command
import deploy_sdk_client
from reanplatform.set_header import set_header_parameter
from deploy_sdk_client.rest import ApiException
from reanplatform.utility import Utility


class DeleteConnection(Command):
    """Delete connection."""

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        """get_parser."""
        parser = super(DeleteConnection, self).get_parser(prog_name)
        parser.add_argument('--name', '-n',
                            help='Connection name',
                            required=False
                            )
        parser.add_argument('--id', '-id', help='Connection ID',
                            required=False
                            )
        return parser

    def take_action(self, parsed_args):
        """take_action."""
        # create an instance of the API class
        conn_api_instance = deploy_sdk_client.ConnectionApi()
        api_instance = set_header_parameter(conn_api_instance)
        try:
            con_id = parsed_args.id
            all_vms = api_instance.get_all_vm_connections()
            for vm_conn in all_vms:
                if(vm_conn.name == parsed_args.name):
                    con_id = vm_conn.id
                    break

            if(con_id is None):
                raise RuntimeError("Exception : connection does not exit", parsed_args.name)    # noqa: E501

            # Delete Connection for User
            api_response = api_instance.delete_vm_connection(con_id)
            print("Connection deleted successfully :%s " % str(api_response.name))    # noqa: E501
        except ApiException as e:
            Utility.print_exception(e)
