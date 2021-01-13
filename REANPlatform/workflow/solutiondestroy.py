"""Destroy Workflow Solution module deployments."""
import os
import json
import time
import logging
from cliff.command import Command
import workflow_sdk_client
from workflow_sdk_client.rest import ApiException
from reanplatform.set_header import set_header_parameter
from reanplatform.utility import Utility
from workflow.constants import WorkflowConstants
from workflow.workflow_utility import WorkflowUtility
from workflow.getsolutiondeployment import GetSolutionDeployment


class SolutionDestroy(Command):
    """Destroy the solution package."""

    log = logging.getLogger(__name__)

    # EPILog will get print after commands
    _epilog = 'Example : rean-workflow solution-destroy --solution-name cli-create --solution-version 00.03.00 --deployment-name demo'

    def get_parser(self, prog_name):
        """get_parser."""
        parser = super(SolutionDestroy, self).get_parser(prog_name)
        parser.add_argument('--solution-name', '-n', help='Solution package name. This parameter is required to get the solution package.', required=True)
        parser.add_argument('--solution-version', '-sv', help='Solution package version. This parameter is required to get the solution package.', required=True)
        parser.add_argument('--deployment-name', '-dn', help='Solution package deployment name. This parameter is required to get the solution package deployment.', required=True)
        parser.add_argument('--wait', '-w', action="store_true", default="False", help='Wait flag for explicitly waiting to destroy the deployment', required=False)
        parser.add_argument('--output', '-o',
                            help="Write output to <file> instead of stdout.",
                            required=False
                           )
        return parser

    def take_action(self, parsed_args):
        """take_action."""
        solution_name = parsed_args.solution_name
        solution_version = parsed_args.solution_version
        deployment_name = parsed_args.deployment_name
        solution_wait = parsed_args.wait
        SolutionDestroy.validate_parameters(solution_name, solution_version, deployment_name)
        SolutionDestroy.destroy_solution_package(solution_name, solution_version, deployment_name, solution_wait, parsed_args)

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
    def destroy_solution_package(solution_name, solution_version, deployment_name, solution_wait, parsed_args):
        """destroy solution package"""
        try:
            solution_deployment = GetSolutionDeployment.get_solution_package(solution_name, solution_version, deployment_name)
            if solution_deployment is not None and solution_deployment.id is not None:
                api_client = set_header_parameter(WorkflowUtility.create_api_client(), Utility.get_url(WorkflowConstants.WORKFLOW_URL))
                workflow_api_instance = workflow_sdk_client.DeploymentcontrollerApi(api_client)
                api_response = workflow_api_instance.destroy_using_delete(solution_deployment.id)
                if solution_wait is True and api_response.id is not None:
                    while 1:
                        deployment_status = workflow_api_instance.get_solution_package_deploy_status_using_get(api_response.id)
                        if deployment_status.status != "FAILED" and deployment_status.status != "DESTROYED":
                            time.sleep(10)
                        else:
                            Utility.print_output_as_str("Solution Package Destroy status")
                            Utility.print_output_as_dict(deployment_status, parsed_args.output)
                            break
                else:
                    Utility.print_output_as_str("Solution Package Destroy Successfully")
                    Utility.print_output_as_dict(api_response, parsed_args.output)
        except ApiException as api_exception:
            Utility.print_exception(api_exception)
