"""Plan Deployment."""
import os
import os.path
import logging
import json
from cliff.command import Command
import deploy_sdk_client
from deploy_sdk_client.rest import ApiException
from reanplatform.set_header import set_header_parameter
from reanplatform.utility import Utility
from deploy.constants import DeployConstants
from deploy.utility import DeployUtility


class PlanDeployment(Command):
    """Plan Deployment."""

    log = logging.getLogger(__name__)

    # EPILog will get print after commands
    _epilog = 'Example : rean-deploy plan-deployment --env_id 1 --deployment_name dummyDeployment'

    def get_parser(self, prog_name):
        """get_parser."""
        # Define parser
        parser = super(PlanDeployment, self).get_parser(prog_name)
        parser.add_argument('--env_id', '-i', help='Environment id', required=True)
        parser.add_argument('--deployment_name', '-dn', help='Deployment name.', required=False)
        parser.add_argument('--output', '-o', help="Write output to <file> instead of stdout.", required=False)
        parser.add_argument('--resource_connection', '-f', help="Json file with applicable resouce name-connection name pair. File absolute path \nExample:\n\"[{\"resourceName\" : \"connectionName\"}]", required=False)
        parser.add_argument('--chef_environment', '-ce', help="Chef Environment Name(Only when REAN Deploy is configured for Chefserver)", required=False)
        parser.add_argument('--provider_name', '-pn', help='Provider Name', required=False)
        parser.add_argument('--region', '-r', help='Region Name', required=False)
        parser.add_argument('--input_json_file', '-in', help='Pass input variable json file with full path', required=False)
        parser.add_argument('--parent_deployment_mappings', '-j',
                            help='Map of parent deployment where key is a name of \"Depends On\" resource and value is \
                            a name/id of the deployment for the parent environment. For example, {\"dependsOnName\" : \"DeploymentName\"}',
                            required=False)
        return parser

    def take_action(self, parsed_args):
        """take_action."""
        # Define parsed_args
        env_id = parsed_args.env_id
        deployment_name = parsed_args.deployment_name
        plan_response = None
        child_input_json = None
        depends_on_json = None

        if parsed_args.input_json_file:
            child_input_json = PlanDeployment.read_file_as_json_object(parsed_args.input_json_file)
        if parsed_args.parent_deployment_mappings:
            depends_on_json = PlanDeployment.read_file_as_json_object(parsed_args.parent_deployment_mappings)
        if parsed_args.resource_connection:
            connections = PlanDeployment.read_file_as_json_object(parsed_args.resource_connection)

        deploy_config = deploy_sdk_client.DeploymentConfigurationDto(
            environment_id=parsed_args.env_id,
            deployment_name=parsed_args.deployment_name,
            region=parsed_args.region,
            provider_name=parsed_args.provider_name,
            input_json=child_input_json,
            parent_deployments=depends_on_json,
            chef_environment=parsed_args.chef_environment
        )

        try:
            # Initialise api_instance
            api_client = set_header_parameter(DeployUtility.create_api_client(), Utility.get_url(DeployConstants.DEPLOY_URL))
            env_instance = deploy_sdk_client.EnvironmentApi(api_client)
            plan_response = env_instance.plan_by_deploy_config_dto(deploy_config)
        except ApiException as api_exception:
            Utility.print_exception(api_exception)

        if plan_response:
            if parsed_args.output is not None:
                Utility.print_output_as_str(plan_response.logs, parsed_args.output)
            else:
                Utility.print_output_as_str(plan_response.logs)

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
