"""Import blueprint module."""
import os
from os.path import basename
import logging
import json
import re
from cliff.command import Command
import authnz_sdk_client
from auth.utility import AuthnzUtility
import solution_sdk_client
from solution_sdk_client.rest import ApiException
from reanplatform.set_header import set_header_parameter
from reanplatform.utility import Utility
from solution.constants import SolutionConstants
from solution.utility import SolutionUtility


class CreateSolution(Command):
    """Create the HCAP Workflow solution package."""

    log = logging.getLogger(__name__)

    # EPILog will get print after commands
    _epilog = 'Example : rean-solution create --solution_file /Users/reanworkflow/solution.json'

    def get_parser(self, prog_name):
        """get_parser."""
        parser = super(CreateSolution, self).get_parser(prog_name)
        parser.add_argument('--solution_file', '-b', help='Solution file. HCAP Workflow solution file path. A path can be absolute path.', required=False)
        parser.add_argument('--name', '-n', help='Solution name. This parameter will override the solution package name given in solution file.', required=False)
        parser.add_argument('--version', '-v', help='Solution version. This parameter will override the solution package version given in solution file.', required=False)
        parser.add_argument('--output', '-o', help="Write output to <file> instead of stdout.", required=False)
        return parser

    def take_action(self, parsed_args):
        """take_action."""
        solution_path = parsed_args.solution_file
        solution_name = parsed_args.name
        solution_version = parsed_args.version

        CreateSolution.validate_parameters(solution_path, solution_name, solution_version)

        CreateSolution.create_solution(solution_path, solution_name, solution_version, parsed_args)    # noqa: E501

    @staticmethod
    def validate_parameters(solution_path, solution_name, solution_version):
        """Validate cli parameters."""
        if solution_path is None:
            raise RuntimeError("Please provide HCAP Workflow solution file absolute path")

    @staticmethod
    def create_solution(solution_path, solution_name, solution_version, parsed_args):
        """create_solution."""
        try:
            api_client = set_header_parameter(SolutionUtility.create_api_client(), Utility.get_url(SolutionConstants.SOLUTION_URL))
            api_solution_instance = solution_sdk_client.Solutionpackagecontrollerv2Api(api_client)

            os.chdir(os.path.dirname(solution_path))
            with open(basename(solution_path), "r") as handle:
                filedata = handle.read()

            jsondata = json.loads(filedata)

            if solution_name is not None;
                jsondata['metadata']['name'] = solution_name
            if solution_version is not None;
                jsondata['metadata']['version'] = solution_version

            saved_solution = api_solution_instance.save_solution_using_post2(jsondata)

        except ApiException as api_exception:
            Utility.print_exception(api_exception)
