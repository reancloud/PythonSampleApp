"""Change Password module."""
import logging
from cliff.command import Command
from reanplatform.utility import Utility
import authnz_sdk_client
from authnz_sdk_client.rest import ApiException
from auth.utility import AuthnzUtility


class ChangePassword(Command):
    """Change Password."""

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        """get_parser."""
        parser = super(ChangePassword, self).get_parser(prog_name)
        parser.add_argument('--user_id', '-i',
                            help='User id',
                            required=True)
        parser.add_argument('--old_password', '-op',
                            help='Old Password',
                            required=True)
        parser.add_argument('--new_password', '-np',
                            help='New Password',
                            required=True)
        parser.add_argument('--confirm_password', '-cp',
                            help='Confirm Password',
                            required=True)
        return parser

    @staticmethod
    def change_password(parsed_args):
        """Change Password."""
        try:
            # Initialise instance and api_instance in list_environment
            api_instance = authnz_sdk_client.UserControllerApi(AuthnzUtility.set_headers())

            change_user_password_object = authnz_sdk_client.ChangeUserPassword(
                id=parsed_args.user_id,
                old_password=parsed_args.old_password,
                new_password=parsed_args.new_password,
                confirm_password=parsed_args.confirm_password
            )
            api_response = api_instance.change_password(body=change_user_password_object)
            if api_response is True:
                print('Password changed successfully.')
        except ApiException as e:
            Utility.print_exception(e)

    def take_action(self, parsed_args):
        """take_action."""
        # Change Password
        ChangePassword.change_password(parsed_args)
