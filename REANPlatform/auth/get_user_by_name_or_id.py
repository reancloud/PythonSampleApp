"""Get Users module."""
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
        parser.add_argument('--name', '-n', help='User name', required=False)
        parser.add_argument('--id', '-i', help='User ID', required=False)
        return parser

    @staticmethod
    def get_user_by_name(name):
        """Get user by name."""
        try:
            # Initialise instance and api_instance
            instance = authnz_sdk_client.UsercontrollerApi()
            api_instance = set_header_parameter(instance, Utility.get_url(AunthnzConstants.AUTHNZ_URL))
            # Get user details by name
            api_response = api_instance.get_by_username_using_get(name)
            json_object = AuthnzUtility.get_user_dict(api_response)
            parsed_json = Utility.get_parsed_json(json_object)
            print(parsed_json)

        except ApiException as e:
            Utility.print_exception(e)

    @staticmethod
    def get_user_by_id(user_id):
        """Get user by user id."""
        try:
            # Initialise instance and api_instance
            instance = authnz_sdk_client.UsercontrollerApi()
            api_instance = set_header_parameter(instance, Utility.get_url(AunthnzConstants.AUTHNZ_URL))
            # Get user details by name
            api_response = api_instance.get_user_using_get1(user_id)
            json_object = AuthnzUtility.get_user_dict(api_response)
            parsed_json = Utility.get_parsed_json(json_object)
            print(parsed_json)

        except ApiException as e:
            Utility.print_exception(e)

    def take_action(self, parsed_args):
        """take_action."""
        # Get user by name or id
        if parsed_args.name:
            GetUserByNameOrId.get_user_by_name(parsed_args.name)
        elif parsed_args.id:
            GetUserByNameOrId.get_user_by_id(parsed_args.id)
        else:
            print('Please provide either username or id. Both can not be empty.')
