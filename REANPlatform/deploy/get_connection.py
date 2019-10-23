"""Get Connection module."""
import re
import logging
from cliff.command import Command
import deploy_sdk_client
from deploy_sdk_client.rest import ApiException
from reanplatform.set_header import set_header_parameter
from reanplatform.utility import Utility
from deploy.constants import DeployConstants
from deploy.utility import DeployUtility


class GetConnection(Command):
    """Get Connection."""

    log = logging.getLogger(__name__)

    # EPILog will get print after commands
    _epilog = 'Example : rean-deploy get-connection --connection_id 1'

    def get_parser(self, prog_name):
        """get_parser."""
        parser = super(GetConnection, self).get_parser(prog_name)
        parser.add_argument('--connection_id', '-i', help='Connection id. This parameter is not required when --connection_name is specified', required=False)
        parser.add_argument('--connection_name', '-n', help='Connection name. This parameter is not required when --connection_id is specified', required=False)
        parser.add_argument('--output', '-o', help="Write output to <file> instead of stdout.", required=False)
        return parser

    @staticmethod
    def validate_parameters(connection_id, connection_name):
        """validate_parameters."""
        exception_msg = "Specify either --connection_id OR --connection_name"
        if (connection_id is None and connection_name is None) or (connection_id is not None and connection_name is not None):
            raise RuntimeError(re.sub(' +', ' ', exception_msg))

    def take_action(self, parsed_args):
        """take_action."""
        # Define parsed argument
        connection_id = parsed_args.connection_id
        connection_name = parsed_args.connection_name
        GetConnection.validate_parameters(connection_id, connection_name)
        # Initialise connection_response
        connection_response = None
        try:
            # Initialise api_client and api_instance
            api_client = set_header_parameter(DeployUtility.create_api_client(), Utility.get_url(DeployConstants.DEPLOY_URL))
            api_instance = deploy_sdk_client.ConnectionApi(api_client)
            if connection_id:
                connection_response = api_instance.get_vm_connection(connection_id)
            else:
                connection_response = api_instance.get_vm_connection_by_name(connection_name)
            if connection_response:
                if parsed_args.output is not None:
                    Utility.print_output_as_dict(connection_response, parsed_args.output)
                else:
                    print(Utility.get_parsed_json(connection_response))
        except ApiException as api_exception:
            Utility.print_exception(api_exception)
