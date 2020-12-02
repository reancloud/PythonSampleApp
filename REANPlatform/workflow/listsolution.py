"""List all Workflow Solutions module."""
import os
from os.path import basename
import logging
from prettytable import PrettyTable
from cliff.command import Command
import authnz_sdk_client
from auth.utility import AuthnzUtility
import solution_sdk_client
from solution_sdk_client.rest import ApiException
from reanplatform.set_header import set_header_parameter
from reanplatform.utility import Utility
from workflow.constants import WorkflowConstants
from workflow.solution_utility import SolutionUtility


class ListSolutions(Command):
    """List the solution package."""

    log = logging.getLogger(__name__)

    # EPILog will get print after commands
    _epilog = 'Example : rean-workflow list-solution'

    def get_parser(self, prog_name):
        """get_parser."""
        parser = super(ListSolutions, self).get_parser(prog_name)
        parser.add_argument('--format', '-f',
                            help='Allowed values are: [json, table]',
                            type=str, default='json',
                            nargs='?',
                            required=False)
        parser.add_argument('--output', '-o', help="Write output to <file> instead of stdout.", required=False)
        return parser

    def take_action(self, parsed_args):
        """take_action."""
        # Define parsed argument
        output_format = parsed_args.format

        ListSolutions.get_solutions(output_format, parsed_args)    # noqa: E501

    @staticmethod
    def get_solutions(output_format, parsed_args):
        """List solutions."""
        try:
            api_client = set_header_parameter(SolutionUtility.create_api_client(), Utility.get_url(WorkflowConstants.SOLUTION_URL))
            api_solution_instance = solution_sdk_client.Solutionpackagecontrollerv2Api(api_client)
            allSolutions = api_solution_instance.get_all_solution_by_owner_using_get2()
            if output_format == 'table':
                table = PrettyTable(['Id', 'Name', 'Version'])
                table.padding_width = 1
                for sol in allSolutions:
                    table.add_row(
                        [
                            sol.id,
                            sol.metadata.name,
                            sol.metadata.version
                        ]
                    )
                Utility.print_output_as_table("Solution Package list \n{}".format(table), parsed_args.output)
            elif output_format in 'json' or output_format in '':
                Utility.print_output_as_dict(allSolutions, parsed_args.output)
            else:
                raise RuntimeError("Please specify correct format, Allowed values are: [json, table]")
        except ApiException as api_exception:
            Utility.print_exception(api_exception)
