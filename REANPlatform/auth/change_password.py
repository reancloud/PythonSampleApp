"""Change Password module."""
import logging
from cliff.command import Command
from reanplatform.set_header import set_header_parameter
from reanplatform.utility import Utility
import authnz_sdk_client
from authnz_sdk_client.rest import ApiException
from auth.constants import AunthnzConstants
from auth.utility import AuthnzUtility


class ChangePassword(Command):
    """Change Password."""

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
        parser.add_argument('--output', '-o',
                            help="Write output to <file> instead of stdout.",
                            required=False
                           )
        return parser

    @staticmethod
    def change_password(parsed_args):
        """Change Password."""
        try:
            # Initialise instance and api_instance in list_environment
            if parsed_args.new_password == parsed_args.confirm_password:
                api_client = set_header_parameter(AuthnzUtility.create_api_client(), Utility.get_url(AunthnzConstants.AUTHNZ_URL))
                instance = authnz_sdk_client.UsercontrollerApi(api_client)
                change_user_password_object = authnz_sdk_client.ChangeUserPassword(
                    id=parsed_args.user_id,
                    old_password=parsed_args.old_password,
                    new_password=parsed_args.new_password,
                    confirm_password=parsed_args.confirm_password
                )

                api_response = instance.change_password_using_put(change_user_password_object)
                Utility.print_output_as_dict(api_response, parsed_args.output)
            else:
                print('New password and confirm password does not match.')

        except ApiException as e:
            Utility.print_exception(e)

    def take_action(self, parsed_args):
        """take_action."""
        # Change Password
        ChangePassword.change_password(parsed_args)
