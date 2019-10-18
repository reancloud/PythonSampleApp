"""Get Users module."""
import re
import logging
from cliff.command import Command
import authnz_sdk_client
from reanplatform.utility import Utility
from auth.utility import AuthnzUtility


class GetUserByNameOrId(Command):
    """Get user by name or id."""

    log = logging.getLogger(__name__)
    _epilog = 'Example : \n\t rean-auth get-user -n <user_name>'

    def get_parser(self, prog_name):
        """get_parser."""
        parser = super(GetUserByNameOrId, self).get_parser(prog_name)
        parser.add_argument('--name', '-n', help='User name. This parameter is not required when --id is specified',
                            required=False)
        parser.add_argument('--id', '-i', help='User id. This parameter is not required when --name is specified',
                            required=False)
        parser.add_argument('--output', '-o', help="Write output to <file> instead of stdout.", required=False)
        return parser

    @staticmethod
    def validate_parameters(parsed_args):
        """validate_parameters."""
        exception_msg = "Specify either --id OR --name"
        if (parsed_args.id and parsed_args.name) or (parsed_args.id is None and parsed_args.name is None):
            raise RuntimeError(re.sub(' +', ' ', exception_msg))

    def take_action(self, parsed_args):
        """take_action."""
        try:
            # Initialise instance and api_instance
            api_instance = authnz_sdk_client.UserControllerApi(AuthnzUtility.set_headers())

            # validate id and name
            GetUserByNameOrId.validate_parameters(parsed_args)
            # Get user by name or id
            if parsed_args.name:
                api_response = api_instance.get_by_username(parsed_args.name)
            else:
                api_response = api_instance.get_user(parsed_args.id)

            if api_response:
                if api_response.name is not None:
                    if parsed_args.output is not None:
                        Utility.print_output_as_dict(api_response, parsed_args.output)
                    else:
                        print(Utility.get_parsed_json(api_response))
                else:
                    print("User not found.")
                    return 1
        except Exception as exception:
            Utility.print_exception(exception)
