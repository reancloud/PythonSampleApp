"""Delete connection module."""
import logging
import re
from cliff.command import Command
import deploy_sdk_client
from deploy_sdk_client.rest import ApiException
from reanplatform.set_header import set_header_parameter
from reanplatform.utility import Utility
from reanplatform.utilityconstants import PlatformConstants
from deploy.constants import DeployConstants
from deploy.utility import DeployUtility


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
            This parameter is not required when --conn_name is specified',
                            required=False
                           )
        parser.add_argument('--output', '-o',
                            help="Write output to <file> instead of stdout.",
                            required=False
                           )
        return parser

    @staticmethod
    def validate_parameters(conn_id, conn_name):
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

        DeleteConnection.validate_parameters(conn_id, conn_name)

        if conn_id:
            DeleteConnection.delete_connection_by_id(conn_id, parsed_args)
        elif conn_name:
            DeleteConnection.delete_connection_by_name(conn_name, parsed_args)

    @staticmethod
    def delete_connection_by_id(conn_id, parsed_args):
        """delete_connection."""
        try:
            api_client = set_header_parameter(DeployUtility.create_api_client(), Utility.get_url(DeployConstants.DEPLOY_URL))
            conn_api_instance = deploy_sdk_client.ConnectionApi(api_client)
            api_response = conn_api_instance.delete_vm_connection(conn_id)
            Utility.print_output("Connection deleted successfully : {}".format(conn_id), parsed_args.output, PlatformConstants.STR_REFERENCE)
        except ApiException as api_exception:
            Utility.print_exception(api_exception)

    @staticmethod
    def delete_connection_by_name(conn_name, parsed_args):
        """delete_connection_by_name."""
        api_client = set_header_parameter(DeployUtility.create_api_client(), Utility.get_url(DeployConstants.DEPLOY_URL))
        conn_api_instance = deploy_sdk_client.ConnectionApi(api_client)
        conn_id = None
        try:
            all_vms = conn_api_instance.get_all_vm_connections()
            for vm_conn in all_vms:
                if vm_conn.name == conn_name:
                    conn_id = vm_conn.id
                    break

            if conn_id is None:
                raise RuntimeError("Exception : connection does not exit", conn_name)    # noqa: E501
            DeleteConnection.delete_connection_by_id(conn_id, parsed_args)

        except ApiException as api_exception:
            Utility.print_exception(api_exception)
