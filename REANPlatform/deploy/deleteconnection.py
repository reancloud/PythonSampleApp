"""Delete connection module."""
import os
from pprint import pprint
import logging
import re
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
        parser.add_argument('--conn_name', '-n',
                            help='Connection name. This parameter is\
                            not required when --conn_id is specified',
                            required=False
                            )
        parser.add_argument('--conn_id', '-id', help='Connection ID.\
                            This parameter is not required\
                            when --conn_name is specified',
                            required=False
                            )
        return parser

    def validate_parameters(self, conn_id, conn_name):
        """validate_parameters."""
        exception_msg = "Specify either --conn_name OR --conn_id"
        if conn_id and conn_name:
            raise RuntimeError(re.sub(' +', ' ', exception_msg))
        elif conn_id is None and conn_name is None:
            raise RuntimeError(re.sub(' +', ' ', exception_msg))

    def take_action(self, parsed_args):
        """take_action."""
        conn_name = parsed_args.conn_name
        conn_id = parsed_args.conn_id

        self.validate_parameters(conn_id, conn_name)
        self.delete_connection(conn_name, conn_id)

    def delete_connection(self, conn_name, conn_id):
        """delete_connection."""
        # create an instance of the API class
        conn_api_instance = deploy_sdk_client.ConnectionApi()
        api_instance = set_header_parameter(conn_api_instance)
        try:
            if conn_name:
                all_vms = api_instance.get_all_vm_connections()
                for vm_conn in all_vms:
                    if(vm_conn.name == conn_name):
                        conn_id = vm_conn.id
                        break

            if(conn_id is None):
                raise RuntimeError("Exception : connection does not exit", conn_name)    # noqa: E501

            api_response = api_instance.delete_vm_connection(conn_id)
            print("Connection deleted successfully :%s " % str(api_response.name))    # noqa: E501
        except ApiException as e:
            Utility.print_exception(e)
