"""Get Group Users module."""
import logging
from cliff.command import Command
import authnz_sdk_client
from reanplatform.utility import Utility
from auth.utility import AuthnzUtility


class GetGroupUsers(Command):
    """Get group users."""

    log = logging.getLogger(__name__)

    _description = 'Get Group Users'
    _epilog = 'Example : \n\t rean-auth get-group-users -i <group_id>'

    # EPILog will get print after commands

    def get_parser(self, prog_name):
        """get_parser."""
        parser = super(GetGroupUsers, self).get_parser(prog_name)
        parser.add_argument('--group_id', '-i', help='Group id.', required=True)
        parser.add_argument('--output', '-o', help="Write output to <file> instead of stdout.", required=False)
        return parser

    def take_action(self, parsed_args):
        """take_action."""
        # Initialise instance and api_instance
        api_instance = authnz_sdk_client.GroupControllerApi(AuthnzUtility.set_headers())
        api_response = None
        try:
            if parsed_args.group_id:
                api_response = api_instance.get_users_from_group(parsed_args.group_id)
            if api_response:
                if parsed_args.output is not None:
                    Utility.print_output_as_dict(api_response, parsed_args.output)
                else:
                    print(Utility.get_parsed_json(api_response))
        except ValueError:
            print("Invalid Group id.")
            exit(1)
