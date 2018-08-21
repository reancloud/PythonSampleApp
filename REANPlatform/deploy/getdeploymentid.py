"""Get Deployment ID."""
import logging
from cliff.command import Command
import deploy_sdk_client
from deploy_sdk_client.rest import ApiException
from reanplatform.set_header import set_header_parameter
from reanplatform.utility import Utility
from deploy.constants import DeployConstants
from deploy.utility import DeployUtility


class GetDeployments(Command):
    """Get Deployment Id."""

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        """get_parser."""
        # Define parser
        parser = super(GetDeployments, self).get_parser(prog_name)
        parser.add_argument('--deployment_name', '-n', default='default', help='Deployment name. Provide this attribute to get specific deployment else deployment name will be default', required=False)
        parser.add_argument('--env_id', '-i', help='Environment id', required=True)
        return parser

    @staticmethod
    def get_deployment_by_id_and_name(env_id, deployment_name):
        """Get Deployments by Env ID And Deployment Name."""
        try:
            # Initialise api_client and api_instance
            api_client = set_header_parameter(DeployUtility.create_api_client(), Utility.get_url(DeployConstants.DEPLOY_URL))
            api_instance = deploy_sdk_client.EnvironmentApi(api_client)
            api_response = api_instance.get_all_deployments_for_environment_by_id_and_deployment_name(env_id, deployment_name)
            print("Deployment id : %s " % (api_response.id))
        except ApiException as api_exception:
            Utility.print_exception(api_exception)

    def take_action(self, parsed_args):
        """take_action."""
        # Define parsed_args
        env_id = parsed_args.env_id
        deployment_name = parsed_args.deployment_name

        if env_id:
            GetDeployments.get_deployment_by_id_and_name(env_id, deployment_name)
