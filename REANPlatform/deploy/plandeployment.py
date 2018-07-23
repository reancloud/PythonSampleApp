"""Plan Deployment."""
import logging
from cliff.command import Command
import deploy_sdk_client
from deploy_sdk_client.rest import ApiException
from reanplatform.set_header import set_header_parameter
from reanplatform.utility import Utility
from deploy.constants import DeployConstants


class PlanDeployment(Command):
    """Plan Deployment."""

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        """get_parser."""
        # Define parser
        parser = super(PlanDeployment, self).get_parser(prog_name)
        parser.add_argument('--env_id', '-id',
                            help='Environment id',
                            required=True)
        parser.add_argument('--deployment_name', '-dname', default='default',
                            help='Deployment Name. Please provide this \
                            attribute if deployment name is not default.',
                            required=False)
        return parser

    def take_action(self, parsed_args):
        """take_action."""
        # Define parsed_args
        env_id = parsed_args.env_id
        deployment_name = parsed_args.deployment_name
        if env_id:
            PlanDeployment.plan_deployment(env_id, deployment_name)

    @staticmethod
    def plan_deployment(env_id, deployment_name):
        """Plan Deployment."""
        try:
            # Initialise instance and api_instance
            instance = deploy_sdk_client.EnvironmentApi()
            api_instance = set_header_parameter(instance, Utility.get_url(DeployConstants.DEPLOY_URL))
            response = api_instance.plan_deployment(env_id, deployment_name)
            print(response.logs)
        except ApiException as api_exception:
            Utility.print_exception(api_exception)
