"""Create Workflow Solution module."""
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


class CreateSolution(Command):
    """Create the HCAP Workflow solution package."""

    log = logging.getLogger(__name__)

    # EPILog will get print after commands
    _epilog = 'Example : rean-workflow create --solution-file /Users/reanworkflow/solution.json'

    def get_parser(self, prog_name):
        """get_parser."""
        parser = super(CreateSolution, self).get_parser(prog_name)
        parser.add_argument('--solution-file', '-s', help='Solution file. HCAP Workflow solution file path. A path can be absolute path.', required=True)
        parser.add_argument('--update-if-exists', '-u', action="store", default="False", help='This parameter will update the existing solution package based on solution name and solution version.', required=False)
        parser.add_argument('--output', '-o', help="Write output to <file> instead of stdout.", required=False)
        return parser

    def take_action(self, parsed_args):
        """take_action."""
        solution_path = parsed_args.solution_file

        CreateSolution.validate_parameters(solution_path)

        CreateSolution.create_solution(solution_path, parsed_args)    # noqa: E501

    @staticmethod
    def validate_parameters(solution_path):
        """Validate cli parameters."""
        if solution_path is None:
            raise RuntimeError("Please provide HCAP Workflow solution file absolute path")

    @staticmethod
    def create_solution(solution_path, parsed_args):
        """Create Solution."""
        try:
            os.chdir(os.path.dirname(solution_path))
            with open(basename(solution_path), "r") as handle:
                filedata = handle.read()

            jsondata = json.loads(filedata)
            api_solution_instance = CreateSolution.get_api_instance(jsondata['schemaVersion'])
            update_if_exists = bool(parsed_args.update_if_exists)

            if update_if_exists is True:
                saved_solution = CreateSolution.update_solution(api_solution_instance, jsondata)
            else:
                saved_solution = CreateSolution.save_solution(api_solution_instance, jsondata)
            Utility.print_output_as_str("Solution Package Added Succesfully: {}".format(saved_solution), parsed_args.output)
        except ApiException as api_exception:
            Utility.print_exception(api_exception)

    @staticmethod
    def get_api_instance(schema_version):
        """Get API instance."""
        if schema_version == "1.0":
            api_client = set_header_parameter(SolutionUtility.create_api_client(), Utility.get_url(WorkflowConstants.SOLUTION_URL))
            api_solution_instance = solution_sdk_client.Solutionpackagecontrollerv1Api(api_client)
            return api_solution_instance

        if schema_version == "2.0":
            api_client = set_header_parameter(SolutionUtility.create_api_client(), Utility.get_url(WorkflowConstants.SOLUTION_URL))
            api_solution_instance = solution_sdk_client.Solutionpackagecontrollerv2Api(api_client)
            return api_solution_instance

    @staticmethod
    def save_solution(api_solution_instance, jsondata):
        """Save Solution."""
        if jsondata['schemaVersion'] == "1.0":
            return api_solution_instance.save_solution_using_post1(jsondata)

        if jsondata['schemaVersion'] == "2.0":
            return api_solution_instance.save_solution_using_post2(jsondata)

    @staticmethod
    def update_solution(api_solution_instance, jsondata):
        """Update Solution."""
        try:
            if jsondata['schemaVersion'] == "1.0":
                solution = api_solution_instance.get_solution_by_name_and_version_using_get1(jsondata['metadata']['name'], jsondata['metadata']['version'])
                jsondata['id'] = solution.id
                return api_solution_instance.update_solution_using_put1(jsondata)

            if jsondata['schemaVersion'] == "2.0":
                solution = api_solution_instance.get_solution_by_name_and_version_using_get2(jsondata['metadata']['name'], jsondata['metadata']['version'])
                jsondata['id'] = solution.id
                return api_solution_instance.update_solution_using_put2(jsondata)
        except ApiException as api_exception:
            return CreateSolution.save_solution(api_solution_instance, jsondata)
