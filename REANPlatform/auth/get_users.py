"""Get Users module."""
import logging
import json
from prettytable import PrettyTable
from cliff.command import Command
from auth.constants import AunthnzConstants
from reanplatform.set_header import set_header_parameter
from reanplatform.utility import Utility
import authnz_sdk_client
from authnz_sdk_client.rest import ApiException


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
        return parser

    @staticmethod
    def get_users(output_format):
        """Get users."""
        try:
            # Initialise instance and api_instance in list_user
            instance = authnz_sdk_client.UsercontrollerApi()
            api_instance = set_header_parameter(instance, Utility.get_url(AunthnzConstants.AUTHNZ_URL))
            # Get all users for user
            api_response = api_instance.get_all_user_using_get()

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
                print("Users list ::\n%s" % (table))

            elif output_format == 'json' or output_format == '':
                parsed_response = GetUsers.parse_response(api_response)
                print(parsed_response)

        except ApiException as e:
            Utility.print_exception(e)

    def take_action(self, parsed_args):
        """take_action."""
        # Define parsed argument
        output_format = parsed_args.format

        # List Users
        GetUsers.get_users(output_format)

    @staticmethod
    def parse_response(api_response):
        """Parse api response."""
        json_response = {}
        user_list = []
        for user in api_response:
            json_response = {
                'id' : user.id,
                'name': user.name,
                'username': user.username,
                'email': user.email,
                'verified': user.verified,
                'disabled': user.disabled
            }
            user_list.append(json_response)

        parsed_response = json.dumps(
            user_list,
            default=lambda o: o.__dict__,
            sort_keys=True, indent=4
        ).replace("\"_", '"')
        return parsed_response
