"""Get Users module."""
import re
import logging
from cliff.command import Command
from reanplatform.set_header import set_header_parameter
from reanplatform.utility import Utility
from auth.constants import AunthnzConstants
from auth.utility import AuthnzUtility
import authnz_sdk_client
from authnz_sdk_client.rest import ApiException


class GetUserByNameOrId(Command):
    """Get user by name or id."""

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        """get_parser."""
        parser = super(GetUserByNameOrId, self).get_parser(prog_name)
        parser.add_argument('--name', '-n', help='User name. This parameter is not required when --id is specified', required=False)
        parser.add_argument('--id', '-i', help='User id. This parameter is not required when --name is specified', required=False)
        parser.add_argument('--output', '-o', help="Write output to <file> instead of stdout.", required=False)
        return parser

    @staticmethod
    def validate_parameters(id, name):
        """validate_parameters."""
        exception_msg = "Specify either --id OR --name"
        if id and name:
            raise RuntimeError(re.sub(' +', ' ', exception_msg))
        elif id is None and name is None:
            raise RuntimeError(re.sub(' +', ' ', exception_msg))

    def take_action(self, parsed_args):
        """take_action."""
        # Initialise instance and api_instance
        api_client = set_header_parameter(AuthnzUtility.create_api_client(), Utility.get_url(AunthnzConstants.AUTHNZ_URL))
        instance = authnz_sdk_client.UsercontrollerApi(api_client)
        # validate id and name
        GetUserByNameOrId.validate_parameters(parsed_args.id, parsed_args.name)     
        # Get user by name or id
        api_response = None
        if parsed_args.name:
            api_response = instance.get_by_username_using_get(parsed_args.name)
        else:
            api_response = instance.get_user_using_get1(parsed_args.id)

        if api_response:
            if parsed_args.output is not None:
                Utility.print_output_as_dict(api_response, parsed_args.output)
            else:
                print(Utility.get_parsed_json(api_response))
