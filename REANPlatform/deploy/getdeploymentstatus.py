"""Get Deployment Status By Env ID and Deployment Name."""
import logging
from cliff.command import Command
import deploy_sdk_client
from deploy_sdk_client.rest import ApiException
from reanplatform.set_header import set_header_parameter
from reanplatform.utility import Utility
from deploy.constants import DeployConstants
from deploy.utility import DeployUtility


class Status(Command):
    """Get Deployment Status."""

    log = logging.getLogger(__name__)

    # EPILog will get print after commands
    _epilog = 'Example : rean-deploy get-status --env_id 1 --deployment_name dummyDeployment'

    def get_parser(self, prog_name):
        """get_parser."""
        # Define parser
        parser = super(Status, self).get_parser(prog_name)
        parser.add_argument('--env_id', '-i', help='Environment id.', required=True)
        parser.add_argument('--deployment_name', '-dn', default='default', help='Deployment Name. Please provide this attribute if deployment name is not given Default deployment name will be default.', required=False)
        parser.add_argument('--output', '-o',
                            help="Write output to <file> instead of stdout.",
                            required=False
                           )
        return parser

    @staticmethod
    def deployment_status(env_id, deployment_name):
        """Get Deployment Status."""
        try:
            # Initialise api_response
            api_response = None

            # Initialise api_client and api_instance to get deployment status
            api_client = set_header_parameter(DeployUtility.create_api_client(), Utility.get_url(DeployConstants.DEPLOY_URL))
            api_instance = deploy_sdk_client.EnvironmentApi(api_client)
            api_response = api_instance.get_deployment_details(env_id, deployment_name)
            return api_response.status

        except ApiException as api_exception:
            Utility.print_exception(api_exception)

    def take_action(self, parsed_args):
        """take_action."""
        # Define parsed arguments
        env_id = parsed_args.env_id
        deployment_name = parsed_args.deployment_name

        # Get deployment status
        status = Status.deployment_status(env_id, deployment_name)

        if status:
            Utility.print_output_as_str("Environment Status : {} ".format(status), parsed_args.output)
