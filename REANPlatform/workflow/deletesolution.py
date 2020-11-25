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
from workflow.constants import WorkflowConstants
from workflow.solution_utility import SolutionUtility


class DeleteSolution(Command):
    """Delete the HCAP Workflow solution package."""

    log = logging.getLogger(__name__)

    # EPILog will get print after commands
    _epilog = 'Example : rean-solution create --id AXX0g1s0VcpUxUfs1-B_'

    def get_parser(self, prog_name):
        """get_parser."""
        parser = super(DeleteSolution, self).get_parser(prog_name)
        parser.add_argument('--id', help='Solution package id', required=True)
        parser.add_argument('--output', '-o', help="Write output to <file> instead of stdout.", required=False)
        return parser

    def take_action(self, parsed_args):
        """take_action."""
        solution_id = parsed_args.id

        DeleteSolution.validate_parameters(solution_id)

        DeleteSolution.delete_solution(solution_id, parsed_args)    # noqa: E501

    @staticmethod
    def validate_parameters(solution_id):
        """Validate cli parameters."""
        if solution_id is None:
            raise RuntimeError("Please provide HCAP Workflow solution package id")

    @staticmethod
    def delete_solution(solution_id, parsed_args):
        """delete_solution."""
        try:
            api_client = set_header_parameter(SolutionUtility.create_api_client(), Utility.get_url(WorkflowConstants.SOLUTION_URL))
            api_solution_instance = solution_sdk_client.Solutionpackagecontrollerv2Api(api_client)
            deleted_solution = api_solution_instance.delete_using_delete2(solution_id)
            Utility.print_output_as_str("Solution Package Added Succesfully: {}".format(deleted_solution), parsed_args.output)
        except ApiException as api_exception:
            Utility.print_exception(api_exception)
