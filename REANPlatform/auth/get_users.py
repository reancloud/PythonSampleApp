"""Get Users module."""
import logging
from prettytable import PrettyTable
from cliff.command import Command
import authnz_sdk_client
from authnz_sdk_client.rest import ApiException
from reanplatform.set_header import set_header_parameter
from reanplatform.utility import Utility
from auth.constants import AunthnzConstants
from auth.utility import AuthnzUtility


class GetUsers(Command):
    """Get Users."""

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        """get_parser."""
        parser = super(GetUsers, self).get_parser(prog_name)
        parser.add_argument('--format', '-f',
                            help='Allowed values are: [json, table]',
                            type=str, default='json',
                            nargs='?',
                            required=False)
        parser.add_argument('--output', '-o', help="Write output to <file> instead of stdout.", required=False)
        return parser

    @staticmethod
    def get_users(output_format, parsed_args):
        """Get users."""
        try:
            # Initialise instance and api_instance in list_user
            api_client = set_header_parameter(AuthnzUtility.create_api_client(), Utility.get_url(AunthnzConstants.AUTHNZ_URL))
            instance = authnz_sdk_client.UsercontrollerApi(api_client)
            # Get all users
            api_response = instance.get_all_user_using_get()
            if output_format == 'table':
                table = PrettyTable(['Id', 'Name', 'Username', 'Email', 'Verified', 'Disabled'])
                table.padding_width = 1
                for user in api_response:
                    table.add_row(
                        [
                            user.id,
                            user.name,
                            user.username,
                            user.email,
                            user.verified,
                            user.disabled
                        ]
                    )
                Utility.print_output_as_table("Users list \n{}".format(table), parsed_args.output)

            elif output_format == 'json' or output_format == '':
                users_list = GetUsers.parse_response(api_response)
                Utility.print_output_as_dict(users_list, parsed_args.output)

        except ApiException as e:
            Utility.print_exception(e)

    def take_action(self, parsed_args):
        """take_action."""
        # Define parsed argument
        output_format = parsed_args.format

        # List Users
        GetUsers.get_users(output_format, parsed_args)

    @staticmethod
    def parse_response(api_response):
        """Parse api response."""
        json_response = {}
        users_list = []
        for user in api_response:
            json_response = AuthnzUtility.get_user_dict(user)
            users_list.append(json_response)
        return users_list
