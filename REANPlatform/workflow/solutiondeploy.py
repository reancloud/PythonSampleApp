"""Deploy Workflow Solution module deployments."""
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
from workflow.getsolution import GetSolution
from workflow.getsolutiondeployment import GetSolutionDeployment


class SolutionDeploy(Command):
    """Deploy Solution Package"""

    log = logging.getLogger(__name__)

    # EPILog will get print after commands
    _epilog = 'Example : rean-workflow solution-deploy --solution-name cli-create --solution-version 00.03.00 --deployment-name demo --package_details /Users/reandeploy/package.json'

    def get_parser(self, prog_name):
        """get_parser."""
        parser = super(SolutionDeploy, self).get_parser(prog_name)
        parser.add_argument('--solution-name', '-n', help='Solution package name.', required=True)
        parser.add_argument('--solution-version', '-sv', help='Solution package version.', required=True)
        parser.add_argument('--deployment-name', '-dn', help='Solution package deployment name.', required=True)
        parser.add_argument('--update-if-exists', '-u', action="store", default="False", help='This parameter will update the existing solution package based on solution name and solution version.', required=False)
        parser.add_argument('--deployment-description', '-dd', help='Solution package description.', required=False)
        parser.add_argument('--wait', '-w', action="store", default="False", help='Wait flag for explicitly waiting to destroy the deployment', required=False)
        parser.add_argument('--package-details', '-f',
                            help='Json file with applicable key-value pair \
                            for solution package deployment. File absolute path',
                            required=True
                           )
        parser.add_argument('--output', '-o',
                            help="Write output to <file> instead of stdout.",
                            required=False
                           )
        return parser

    def take_action(self, parsed_args):
        """take_action."""
        package_details = parsed_args.package_details
        solution_wait = bool(parsed_args.wait)
        update_if_exists = bool(parsed_args.update_if_exists)
        SolutionDeploy.validate_parameters(parsed_args)
        SolutionDeploy.deploy_solution_package(package_details, parsed_args, solution_wait, update_if_exists)

    @staticmethod
    def validate_parameters(parsed_args):
        """Validate cli parameters."""
        if parsed_args.solution_name is None:
            raise RuntimeError("Please provide HCAP Workflow Solution Package Name")

        if parsed_args.solution_version is None:
            raise RuntimeError("Please provide HCAP Workflow Solution Package Version")

        if parsed_args.deployment_name is None:
            raise RuntimeError("Please provide HCAP Workflow Solution Package Deployment Name")

    @staticmethod
    def deploy_solution_package(package_details, parsed_args, solution_wait, update_if_exists):
        """create_provider."""
        api_client = set_header_parameter(WorkflowUtility.create_api_client(), Utility.get_url(WorkflowConstants.WORKFLOW_URL))
        workflow_api_instance = workflow_sdk_client.DeploymentcontrollerApi(api_client)
        try:
            file_path = package_details
            if not os.path.isfile(file_path):
                raise RuntimeError('Solution deployment file %s does not exists' % file_path)
            # Parse parameters
            with open(file_path, "r") as handle:
                filedata = handle.read()

            jsondata = json.loads(filedata)
            solution_deployment = SolutionDeploy.create_input_json(jsondata, parsed_args)
            if update_if_exists is True:
                SolutionDeploy.update_solution_package(workflow_api_instance, solution_wait, parsed_args, solution_deployment)
            else:
                SolutionDeploy.deploy_solution(workflow_api_instance, solution_wait, parsed_args, solution_deployment)

        except ApiException as api_exception:
            Utility.print_exception(api_exception)

    def create_input_json(jsondata, parsed_args):
        """ create deployment input json """
        try:
            if parsed_args.solution_name is not None and parsed_args.solution_version is not None:
                solution_package = GetSolution.getsolution(parsed_args.solution_name, parsed_args.solution_version)
                if solution_package.id is not None:
                    jsondata['solutionPackageId'] = solution_package.id

            if parsed_args.deployment_name is not None:
                jsondata['name'] = parsed_args.deployment_name

            if parsed_args.deployment_description is not None:
                jsondata['description'] = parsed_args.deployment_description

            return jsondata
        except ApiException as api_exception:
            Utility.print_exception(api_exception)

    def deploy_solution(workflow_api_instance, solution_wait, parsed_args, solution_deployment):
        """ method is used to deploy the solution """
        try:
            api_response = workflow_api_instance.deploy_using_post(solution_deployment)
            if solution_wait is True and api_response.id is not None:
                solution_status = SolutionDeploy.wait_for_status(solution_wait, workflow_api_instance, api_response.id)
                Utility.print_output_as_str("Solution Package Deployed Succesfully: {}".format(solution_status), parsed_args.output)
            else:
                Utility.print_output_as_str("Solution Package Deployment Succesfully: {}".format(api_response), parsed_args.output)
        except ApiException as api_exception:
            Utility.print_exception(api_exception)

    def update_solution_package(workflow_api_instance, solution_wait, parsed_args, solution_deployment):
        """ method for update solution package """
        try:
            solution_package_dep = SolutionDeploy.get_solution_package_deployment(parsed_args.solution_name, parsed_args.solution_version, parsed_args.deployment_name)
            if solution_package_dep is not None:
                solution_deployment['id'] = solution_package_dep.id
                redeploy_response = workflow_api_instance.redeploy_using_put(solution_deployment)
                if solution_wait is True and redeploy_response.id is not None:
                    redeploy_status = SolutionDeploy.wait_for_status(solution_wait, workflow_api_instance, redeploy_response.id)
                    Utility.print_output_as_str("Solution Package ReDeployed Succesfully: {}".format(redeploy_status), parsed_args.output)
                else:
                    Utility.print_output_as_str("Solution Package Redeploy Succesfully: {}".format(redeploy_response), parsed_args.output)
        except ApiException as api_exception:
            return SolutionDeploy.deploy_solution(workflow_api_instance, solution_wait, parsed_args, solution_deployment)

    def wait_for_status(solution_wait, workflow_api_instance, solution_id):
        """ method used for wait status """
        try:
            while 1:
                deployment_status = workflow_api_instance.get_solution_package_deploy_status_using_get(solution_id)
                if deployment_status.status != 'FAILED' and deployment_status.status != 'DEPLOYED':
                    time.sleep(10)
                else:
                    return deployment_status
        except ApiException as api_exception:
            Utility.print_exception(api_exception)

    def get_solution_package_deployment(solution_name, solution_version, deployment_name):
        """get solution package ."""
        solution_package = GetSolution.getsolution(solution_name, solution_version)
        if solution_package.id is not None:
            api_client = set_header_parameter(WorkflowUtility.create_api_client(), Utility.get_url(WorkflowConstants.WORKFLOW_URL))
            workflow_api_instance = workflow_sdk_client.DeploymentcontrollerApi(api_client)
            api_response = workflow_api_instance.get_solution_package_deploy_status_by_name_using_get(deployment_name, solution_package.id)
            return api_response
