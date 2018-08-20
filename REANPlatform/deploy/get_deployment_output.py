"""Get Deployment Details."""
import os
from os.path import basename
import logging
from cliff.command import Command
import deploy_sdk_client
from deploy_sdk_client.rest import ApiException
from reanplatform.set_header import set_header_parameter
from reanplatform.utility import Utility
from deploy.constants import DeployConstants


class GetDeploymentOutput(Command):
    """Get Deployment Details."""

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        """get_parser."""
        # Define parser
        parser = super(GetDeploymentOutput, self).get_parser(prog_name)
        parser.add_argument('--env_id', '-i', help='Environment id', required=True)
        parser.add_argument('--deployment_name', '-n', default='default', help='Deployment name', required=False)
        parser.add_argument('--output', '-f', help='Specify filename for getting deployment output', required=False)
        return parser

    @staticmethod
    def get_deployment_details(env_id, deployment_name):
        """Get Deployment Details."""
        try:
            # Initialise api_response
            api_response = None

            # Initialise api_instance to get deployment details
            api_client = set_header_parameter(Utility.create_api_client(), Utility.get_url(DeployConstants.DEPLOY_URL))
            api_instance = deploy_sdk_client.EnvironmentApi(api_client)
            if env_id:
                api_response = api_instance.get_deployment_details(env_id, deployment_name)
            return api_response
        except ApiException as api_exception:
            Utility.print_exception(api_exception)

    def take_action(self, parsed_args):
        """take_action."""
        # Define parsed arguments
        env_id = parsed_args.env_id
        deployment_name = parsed_args.deployment_name
        file_name = parsed_args.output

        # Get deployment details
        deployment_output = GetDeploymentOutput.get_deployment_details(
            env_id, deployment_name)

        if deployment_output:
            if file_name is not None:
                filepath = os.getcwd() + '/' + file_name + '.json'
                os.chdir(os.path.dirname(filepath))
                with open(basename(filepath), 'w') as outfile:
                    outfile.write(str(deployment_output))
                print("Deployment output file " + file_name + " created successfully at " + filepath)
            else:
                print(deployment_output)