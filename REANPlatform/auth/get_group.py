"""Get Users module."""
import re
import logging
from cliff.command import Command
import authnz_sdk_client
from reanplatform.utility import Utility
from auth.utility import AuthnzUtility


class GetGroup(Command):
    """Get group by name or id."""

    log = logging.getLogger(__name__)

    _description = 'Get Group'
    _epilog = 'Example : \n\t rean-auth get-group -n <group_name>'

    # EPILog will get print after commands

    def get_parser(self, prog_name):
        """get_parser."""
        parser = super(GetGroup, self).get_parser(prog_name)
        parser.add_argument('--name', '-n', help='Group name. This parameter is not required when --id is specified',
                            required=False)
        parser.add_argument('--id', '-i', help='Group id. This parameter is not required when --name is specified',
                            required=False)
        parser.add_argument('--output', '-o', help="Write output to <file> instead of stdout.", required=False)
        return parser

    @staticmethod
    def validate_parameters(parsed_args):
        """validate_parameters."""
        exception_msg = "Specify either --id OR --name"
        if parsed_args.id and parsed_args.name:
            raise RuntimeError(re.sub(' +', ' ', exception_msg))
        elif parsed_args.id is None and parsed_args.name is None:
            raise RuntimeError(re.sub(' +', ' ', exception_msg))

    def take_action(self, parsed_args):
        """take_action."""
        # Initialise instance and api_instance

        api_instance = authnz_sdk_client.GroupControllerApi(AuthnzUtility.set_headers())

        try:
            if parsed_args.name:
                api_response = api_instance.get_group_with_name(parsed_args.name)

            else:

                api_response = api_instance.get_group(parsed_args.id)

            if api_response:
                if parsed_args.output is not None:
                    Utility.print_output_as_dict(api_response, parsed_args.output)
                else:
                    print(Utility.get_parsed_json(api_response))

        except ValueError:
            print("Invalid Group name/id.")
            return 1


