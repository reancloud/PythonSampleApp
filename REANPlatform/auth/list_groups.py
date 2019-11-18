"""List all groups."""

import json
from prettytable import PrettyTable
from reanplatform.utility import Utility as PlatformUtility
import logging
from cliff.command import Command
import authnz_sdk_client
from reanplatform.utility import Utility
from auth.utility import AuthnzUtility


class ListGroups(Command):
    """List Groups."""

    log = logging.getLogger(__name__)
    _epilog = 'Example : \n\t rean-auth list-groups -f <json/table>'

    def get_parser(self, prog_name):
        """Parser of ListGroups."""
        parser = super(ListGroups, self).get_parser(prog_name)
        parser.add_argument('--format', '-f',
                            help='Allowed values are: [json, table]',
                            type=str, default='json',
                            nargs='?',
                            choices=['json', 'table'],
                            required=False)
        parser.add_argument('--output', '-o', help="Write output to <file> instead of stdout.", required=False)
        return parser

    def take_action(self, parsed_args):
        """take_action of ListGroups."""
        list_groups_format = parsed_args.format
        """list_groups."""
        try:
            api_instance = authnz_sdk_client.GroupControllerApi(AuthnzUtility.set_headers())
            api_response = api_instance.get_groups()
            if not api_response:
                print("Group list is empty.")
            else:
                if list_groups_format == 'table':
                    table = PrettyTable(['Id', 'Name', 'Description', 'Policies', 'Group Level Sharing'])
                    table.padding_width = 1
                    for group in api_response:
                        policies_name = ""
                        for policy in group.policies:
                            policies_name += policy["name"] + ', '
                        table.add_row(
                            [
                                group.id,
                                group.name,
                                group.description,
                                policies_name[:-2],
                                group.group_level_sharing
                            ]
                        )
                    PlatformUtility.print_output_as_str("{}".format(table), parsed_args.output)
                elif list_groups_format == 'json' or list_groups_format == '':
                    PlatformUtility.print_output_as_str(
                        json.dumps(
                            api_response,
                            default=lambda o: o.__dict__,
                            sort_keys=True, indent=4
                        ).replace("\"_", '"'), parsed_args.output
                    )
                else:
                    raise RuntimeError("Please specify correct format, Allowed \
                            values are: [json, table]")
        except Exception as exception:
            Utility.print_exception(exception)
