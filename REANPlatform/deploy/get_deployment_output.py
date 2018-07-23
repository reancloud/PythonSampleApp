"""Get Deployment Details."""
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
        parser.add_argument('--env_id', '-id',
                            help='Environment ID.',
                            required=True)
        parser.add_argument('--deployment_name', '-dname',
                            default='default',
                            help='Deployment Name.',
                            required=False)
        return parser

    @staticmethod
    def get_deployment_details(env_id, deployment_name):
        """Get Deployment Status."""
        try:
            # Initialise api_response
            api_response = None

            # Initialise instance and api_instance to get deployment details
            instance = deploy_sdk_client.EnvironmentApi()
            api_instance = set_header_parameter(instance, Utility.get_url(DeployConstants.DEPLOY_URL))
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

        # Get deployment details
        deployment_output = GetDeploymentOutput.get_deployment_details(
            env_id, deployment_name)

        if deployment_output:
            print(deployment_output)
