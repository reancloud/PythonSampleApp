"""Plan Deployment."""
import logging
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
        parser.add_argument('--output', '-o',
                            help="Write output to <file> instead of stdout.",
                            required=False
                           )
        return parser

    def take_action(self, parsed_args):
        """take_action."""
        # Define parsed_args
        env_id = parsed_args.env_id
        deployment_name = parsed_args.deployment_name
        plan_response = None

        if env_id and deployment_name:
            plan_response = PlanDeployment.plan_deployment(env_id, deployment_name)
        else:
            plan_response = PlanDeployment.plan(env_id)

        if plan_response:
            if parsed_args.output is not None:
                Utility.print_output_as_str(plan_response.logs, parsed_args.output)
            else:
                Utility.print_output_as_str(plan_response.logs)

    @staticmethod
    def plan_deployment(env_id, deployment_name):
        """Plan Deployment."""
        try:
            # Initialise api_instance
            api_client = set_header_parameter(DeployUtility.create_api_client(), Utility.get_url(DeployConstants.DEPLOY_URL))
            env_instance = deploy_sdk_client.EnvironmentApi(api_client)
            response = env_instance.plan_deployment(env_id, deployment_name)
            return response
        except ApiException as api_exception:
            Utility.print_exception(api_exception)

    @staticmethod
    def plan(env_id):
        """Plan."""
        try:
            # Initialise api_instance
            api_client = set_header_parameter(DeployUtility.create_api_client(), Utility.get_url(DeployConstants.DEPLOY_URL))
            env_instance = deploy_sdk_client.EnvironmentApi(api_client)
            response = env_instance.plan(env_id)
            return response
        except ApiException as api_exception:
            Utility.print_exception(api_exception)
