"""Delete Workflow Solution module."""
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
from workflow.constants import WorkflowConstants
from workflow.solution_utility import SolutionUtility
from workflow.getsolution import GetSolution


class DeleteSolution(Command):
    """Delete the solution package."""

    log = logging.getLogger(__name__)

    # EPILog will get print after commands
    _epilog = 'Example : rean-workflow delete-solution --solution-name solutionName --solution-version 00.00.01'

    def get_parser(self, prog_name):
        """get_parser."""
        parser = super(DeleteSolution, self).get_parser(prog_name)
        parser.add_argument('--solution-name', '-n', help='Solution name. This parameter is required to get the solution package.', required=True)
        parser.add_argument('--solution-version', '-sv', help='Solution version. This parameter is required to get the solution package.', required=True)
        parser.add_argument('--output', '-o', help="Write output to <file> instead of stdout.", required=False)
        return parser

    def take_action(self, parsed_args):
        """take_action."""
        solution_name = parsed_args.solution_name
        solution_version = parsed_args.solution_version
        DeleteSolution.validate_parameters(solution_name, solution_version)
        DeleteSolution.delete_solution(solution_name, solution_version, parsed_args)    # noqa: E501

    @staticmethod
    def validate_parameters(solution_name, solution_version):
        """Validate cli parameters."""
        if solution_name is None:
            raise RuntimeError("Please provide HCAP Workflow solution name")

        if solution_version is None:
            raise RuntimeError("Please provide HCAP Workflow solution version")

    @staticmethod
    def delete_solution(solution_name, solution_version, parsed_args):
        """delete_solution."""
        try:
            solution_package = GetSolution.getsolution(solution_name, solution_version)
            if solution_package.id is not None:
                api_client = set_header_parameter(SolutionUtility.create_api_client(), Utility.get_url(WorkflowConstants.SOLUTION_URL))
                api_solution_instance = solution_sdk_client.Solutionpackagecontrollerv2Api(api_client)
                deleted_solution = api_solution_instance.delete_using_delete2(solution_package.id)
                Utility.print_output_as_str("Solution Package deleted Successfully")
                Utility.print_output_as_dict(deleted_solution, parsed_args.output)
        except ApiException as api_exception:
            Utility.print_exception(api_exception)
