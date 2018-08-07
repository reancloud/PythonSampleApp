"""Stop Deployment."""
import logging
from cliff.command import Command
import deploy_sdk_client
from deploy_sdk_client.rest import ApiException
from reanplatform.set_header import set_header_parameter
from reanplatform.utility import Utility
from deploy.constants import DeployConstants


class StopDeployment(Command):
    """Stop Deployment."""

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        """get_parser."""
        # Define parser
        parser = super(StopDeployment, self).get_parser(prog_name)
        parser.add_argument('--env_id', '-id',
                            help='Environment id',
                            required=True)
        parser.add_argument('--deployment_name', '-dname', default='default',
                            help='Deployment Name. Please provide this \
                            attribute if deployment name is not default.',
                            required=False)
        return parser

    @staticmethod
    def stop_deployment(env_id, deployment_name):
        """Stop Deployment."""
        try:
            # Initialise instance and api_instance
            instance = deploy_sdk_client.EnvironmentApi()
            api_instance = set_header_parameter(instance, Utility.get_url(DeployConstants.DEPLOY_URL))
            stop_deployment_response = api_instance.stop_deployment_by_env_id_and_deployment_name(env_id, deployment_name)
            return stop_deployment_response
        except ApiException as api_exception:
            Utility.print_exception(api_exception)

    def take_action(self, parsed_args):
        """take_action."""
        # Define parsed_args
        env_id = parsed_args.env_id
        deployment_name = parsed_args.deployment_name

        # Get stop deployment status
        if env_id:
            stop_deployment_status = StopDeployment.stop_deployment(env_id, deployment_name)

        if stop_deployment_status:
            print("Stop Deployment Status : %s" %
                  (stop_deployment_status.status))
