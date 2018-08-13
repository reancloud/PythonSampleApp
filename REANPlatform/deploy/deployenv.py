"""Depoly/Re-Deploy an Environment."""
import os
import os.path
import logging
import json
import time
from cliff.command import Command
import deploy_sdk_client
from deploy_sdk_client.rest import ApiException
from deploy.getdeploymentstatus import Status
from deploy.constants import DeployConstants
from reanplatform.set_header import set_header_parameter
from reanplatform.utility import Utility


class DepolyEnv(Command):
    """Redeploy an environment by name and version."""

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        """get_parser."""
        parser = super(DepolyEnv, self).get_parser(prog_name)
        parser.add_argument('--env_id', '-id',
                            help='Environment id',
                            required=True)
        parser.add_argument('--deployment_name', '-dname', default='default',
                            help='Deployment Name. Please provide this \
                            attribute if deployment name is not default.',
                            required=False)
        parser.add_argument('--deployment_description', '-desc',
                            help='Description of deployment',
                            required=False)
        parser.add_argument('--provider_name', '-pname',
                            help='Provider Name',
                            required=False)
        parser.add_argument('--region', '-region',
                            help='Region Name',
                            required=False)
        parser.add_argument('--input_json_file', '-input_json',
                            help='Pass input variable json file with \
                            full path',
                            required=False)
        parser.add_argument('--parent_deployment_mappings',
                            '-parent_mapping_json',
                            help='Map of parent deployment where key is \
                            a name of \"Depends On\" resource and value is \
                            a name/id of the deployment for the parent \
                            environment. For example, {\"dependsOnName\" : \"DeploymentName\"}',  # noqa: E501
                            required=False)

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
    def re_deploy_environment(environment_id, deployment_name,
                              deployment_description, provider_name,
                              region, child_input_json, depends_on_json):
        """Redeploy An Environment."""
        try:
            # Initialise instance and api_instance and response
            instance = deploy_sdk_client.EnvironmentApi()
            api_instance = set_header_parameter(instance, Utility.get_url(DeployConstants.DEPLOY_URL))
            response = None
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

            return response
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

        # Re Deploy an environment
        result = DepolyEnv.re_deploy_environment(environment_id, deployment_name,         # noqa: E501
                                                 deployment_description, provider_name,  # noqa: E501
                                                 region, child_input_json, depends_on_json
                                                )   # noqa: E501
        if result:
            print(result)
