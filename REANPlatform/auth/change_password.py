"""Change Password module."""
import logging
from cliff.command import Command
from reanplatform.set_header import set_header_parameter
from reanplatform.utility import Utility
import authnz_sdk_client
from authnz_sdk_client.rest import ApiException
from auth.constants import AunthnzConstants


class ChangePassword(Command):
    """Change Password"""

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        """get_parser."""
        parser = super(ChangePassword, self).get_parser(prog_name)
        parser.add_argument('--user_id', '-id',
                            help='User Id',
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
        """Change Password"""
        try:
            # Initialise instance and api_instance in list_environment
            if parsed_args.new_password == parsed_args.confirm_password:
                instance = authnz_sdk_client.UsercontrollerApi()
                change_user_password_object = authnz_sdk_client.ChangeUserPassword(
                    id=parsed_args.user_id,
                    old_password=parsed_args.old_password,
                    new_password=parsed_args.new_password,
                    confirm_password=parsed_args.confirm_password
                )
                api_instance = set_header_parameter(instance, Utility.get_url(AunthnzConstants.AUTHNZ_URL))

                api_response = api_instance.change_password_using_put(change_user_password_object)
                print(api_response)
            else:
                print('New password and confirm password does not match.')

        except ApiException as e:
            Utility.print_exception(e)

    def take_action(self, parsed_args):
        """take_action."""
        # Change Password
        ChangePassword.change_password(parsed_args)
