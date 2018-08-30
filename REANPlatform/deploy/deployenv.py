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
        parser.add_argument('--resource_connection', '-f',
                            help="Json file with applicable resoucename-connectionname pair. File absolute path \nExample:\n\"[{\"resourceName\" : \"connectionName\"}]",
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
    def deploy_environment(parsed_args):
        """Deploy/Redeploy an Environment."""
        try:
            # Initialise instance and api_instance
            api_client = set_header_parameter(DeployUtility.create_api_client(), Utility.get_url(DeployConstants.DEPLOY_URL))
            api_instance = deploy_sdk_client.EnvironmentApi(api_client)
            status = None

            child_input_json = None
            depends_on_json = None
            connections = None

            if parsed_args.input_json_file:
                child_input_json = DepolyEnv.read_file_as_json_object(parsed_args.input_json_file)
            if parsed_args.parent_deployment_mappings:
                depends_on_json = DepolyEnv.read_file_as_json_object(parsed_args.parent_deployment_mappings)
            if parsed_args.resource_connection:
                connections = DepolyEnv.read_file_as_json_object(parsed_args.resource_connection)

            body = deploy_sdk_client.DeploymentConfigurationDto(
                environment_id=parsed_args.env_id,
                deployment_name=parsed_args.deployment_name,
                deployment_description=parsed_args.deployment_description,
                region=parsed_args.region,
                provider_name=parsed_args.provider_name,
                input_json=child_input_json,
                parent_deployments=depends_on_json,
                connections=connections
            )
            response = api_instance.deploy_by_config(
                body=body
            )

            # Get deployment status
            while 1:
                status = Status.deployment_status(parsed_args.env_id, parsed_args.deployment_name)  # noqa: E501
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
        # Deploy an environment
        result = DepolyEnv.deploy_environment(parsed_args)
        if result:
            print("Environment Status : %s " % (result))
