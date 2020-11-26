"""Save provider module."""
import os
import json
import logging
from cliff.command import Command
import workflow_sdk_client
from workflow_sdk_client.rest import ApiException
from reanplatform.set_header import set_header_parameter
from reanplatform.utility import Utility
from workflow.constants import WorkflowConstants
from workflow.workflow_utility import WorkflowUtility
from workflow.getsolution import GetSolution


class GetSolutionDeployment(Command):
    """Deploy Solution Package"""

    log = logging.getLogger(__name__)

    # EPILog will get print after commands
    _epilog = 'Example : rean-workflow --solution-name solutionpackagedeployment --solution-version 1.0.2 --deployment-name solutionpackagedeployment'

    def get_parser(self, prog_name):
        """get_parser."""
        parser = super(GetSolutionDeployment, self).get_parser(prog_name)
        parser.add_argument('--solution_name', '-n', help='Solution package name.', required=True)
        parser.add_argument('--solution_version', '-sv', help='Solution package version.', required=True)
        parser.add_argument('--deployment_name', '-dn', help='Solution package deployment name.', required=True)
        parser.add_argument('--output', '-o', help="Write output to <file> instead of stdout.", required=False)
        return parser

    def take_action(self, parsed_args):
        """take_action."""
        try:
            solution_name = parsed_args.solution_name
            solution_version = parsed_args.solution_version
            deployment_name = parsed_args.deployment_name
            GetSolutionDeployment.validate_parameters(solution_name, solution_version, deployment_name)
            solutio_deployment = GetSolutionDeployment.get_solution_package(solution_name, solution_version, deployment_name)
            Utility.print_output_as_str("Solution Package Deployment Status: {}".format(solutio_deployment), parsed_args.output)
        except ApiException as api_exception:
            Utility.print_exception(api_exception)


    @staticmethod
    def validate_parameters(solution_name, solution_version, deployment_name):
        """Validate cli parameters."""
        if solution_name is None:
            raise RuntimeError("Please provide HCAP Workflow Solution Package Name")

        if solution_version is None:
            raise RuntimeError("Please provide HCAP Workflow Solution Package Version")

        if deployment_name is None:
            raise RuntimeError("Please provide HCAP Workflow Solution Package Deployment Name")

    @staticmethod
    def get_solution_package(solution_name, solution_version, deployment_name):
        """get solution package ."""
        try:
            solution_package = GetSolution.getsolution(solution_name, solution_version)
            if solution_package.id is not None:
                api_client = set_header_parameter(WorkflowUtility.create_api_client(), Utility.get_url(WorkflowConstants.WORKFLOW_URL))
                workflow_api_instance = workflow_sdk_client.DeploymentcontrollerApi(api_client)
                api_response = workflow_api_instance.get_solution_package_deploy_status_by_name_using_get(deployment_name, solution_package.id)
                return api_response
        except ApiException as api_exception:
            Utility.print_exception(api_exception)
