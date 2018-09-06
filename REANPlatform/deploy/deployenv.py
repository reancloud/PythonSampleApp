"""Depoly/Re-Deploy an Environment."""
import os
import os.path
import logging
import json
import time
from cliff.command import Command
import deploy_sdk_client
from deploy_sdk_client.rest import ApiException
from reanplatform.set_header import set_header_parameter
from reanplatform.utility import Utility
from deploy.constants import DeployConstants
from deploy.utility import DeployUtility
from deploy.getdeploymentstatus import Status


class DepolyEnv(Command):
    """Deploy/Redeploy an Environment."""

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        """get_parser."""
        parser = super(DepolyEnv, self).get_parser(prog_name)
        parser.add_argument('--env_id', '-i', help='Environment id', required=True)
        parser.add_argument('--deployment_name', '-dn', default='default', help='Deployment Name. Please provide this attribute if deployment name is not default.', required=False)
        parser.add_argument('--deployment_description', '-d', help='Description of deployment', required=False)
        parser.add_argument('--provider_name', '-pn', help='Provider Name', required=False)
        parser.add_argument('--region', '-r', help='Region Name', required=False)
        parser.add_argument('--input_json_file', '-in', help='Pass input variable json file with full path', required=False)
        parser.add_argument('--parent_deployment_mappings', '-j',
                            help='Map of parent deployment where key is a name of \"Depends On\" resource and value is \
                            a name/id of the deployment for the parent environment. For example, {\"dependsOnName\" : \"DeploymentName\"}',
                            required=False)
        parser.add_argument('--output', '-o',
                            help="Write output to <file> instead of stdout.",
                            required=False
                           )
        return parser

    @staticmethod
    def read_file_as_json_object(json_file):
        """Convert Json to String."""
        try:
            # check file exists
            if os.path.isfile(json_file) is False:
                print('File not found: ' + json_file)

            # get a file object and read it in as a string
            with open(json_file) as jsonfile:
                json_obj = json.load(jsonfile)
            return json_obj
        except ApiException as api_exception:
            Utility.print_exception(api_exception)

    @staticmethod
    def deploy_environment(environment_id, deployment_name,
                           deployment_description, provider_name,
                           region, child_input_json, depends_on_json):
        """Deploy/Redeploy an Environment."""
        try:
            # Initialise instance and api_instance
            api_client = set_header_parameter(DeployUtility.create_api_client(), Utility.get_url(DeployConstants.DEPLOY_URL))
            api_instance = deploy_sdk_client.EnvironmentApi(api_client)
            status = None
            body = deploy_sdk_client.DeploymentConfigurationDto(
                environment_id=environment_id,
                deployment_name=deployment_name,
                deployment_description=deployment_description,
                region=region,
                provider_name=provider_name,
                input_json=child_input_json,
                parent_deployments=depends_on_json
            )
            response = api_instance.deploy_by_config(
                body=body
            )

            # Get deployment status
            while 1:
                status = Status.deployment_status(environment_id, deployment_name)  # noqa: E501
                status_dict = str(status)
                if "DEPLOYING" in status_dict:
                    time.sleep(1)
                else:
                    break

            return status
        except ApiException as api_exception:
            Utility.print_exception(api_exception)

    def take_action(self, parsed_args):
        """take_action."""
        # Define parsed_args
        environment_id = parsed_args.env_id
        deployment_name = parsed_args.deployment_name
        deployment_description = parsed_args.deployment_description
        region = parsed_args.region
        child_json = parsed_args.input_json_file
        parent_json = parsed_args.parent_deployment_mappings
        provider_name = parsed_args.provider_name
        child_input_json = None
        depends_on_json = None

        if child_json:
            child_input_json = DepolyEnv.read_file_as_json_object(child_json)
        if parent_json:
            depends_on_json = DepolyEnv.read_file_as_json_object(parent_json)

        # Deploy an environment
        result = DepolyEnv.deploy_environment(environment_id, deployment_name, deployment_description, provider_name, region, child_input_json, depends_on_json)
        if result:
            Utility.print_output_as_str("Environment Status : {} ".format(result), parsed_args.output)
