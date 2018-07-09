"""Get Users module."""
import logging
import json
from cliff.command import Command
from prettytable import PrettyTable
from auth.constants import Constants
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
            # Initialise instance and api_instance in list_environment
            instance = authnz_sdk_client.UsercontrollerApi()
            base_url = Utility.get_platform_base_url()
            auth_url = Constants.AUTHNZ_URL
            api_instance = set_header_parameter(instance, base_url + auth_url)
            # Get all environments for user
            api_response = api_instance.get_all_user_using_get()

            if output_format == 'table':
                table = PrettyTable(['Name', 'Id', 'Region', 'Version'])
                table.padding_width = 1
                for environment in api_response:
                    table.add_row(
                        [
                            environment.name,
                            environment.id,
                            environment.region,
                            environment.env_version
                        ]
                    )
                print("Users list ::\n%s" % (table))

            elif output_format == 'json' or output_format == '':
                print(
                    json.dumps(
                        api_response,
                        default=lambda o: o.__dict__,
                        sort_keys=True, indent=4
                        ).replace("\"_", '"')
                    )

        except ApiException as e:
            Utility.print_exception(e)

    def take_action(self, parsed_args):
        """take_action."""
        # Define parsed argument
        output_format = parsed_args.format

        # List Users
        GetUsers.get_users(output_format)
