"""Get Deployment Logs By Deployment ID."""
import logging
from cliff.command import Command
import deploy_sdk_client
from deploy_sdk_client.rest import ApiException
from reanplatform.set_header import set_header_parameter
from reanplatform.utility import Utility
from deploy.constants import DeployConstants
from deploy.utility import DeployUtility
from reanplatform.utilityconstants import PlatformConstants


class GetDeploymentLogs(Command):
    """Get Deployment Logs."""

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        """get_parser."""
        # Define parser
        parser = super(GetDeploymentLogs, self).get_parser(prog_name)
        parser.add_argument('--deployment_id', '-di', help='Deployment id.', required=True)
        parser.add_argument('--output', '-o',
                            help="Write output to <file> instead of stdout.",
                            required=False)
        return parser

    @staticmethod
    def get_deployment_logs(deployment_id):
        """Get Deployment Logs."""
        try:
            # Initialise api_response
            api_response = None

            # Initialise api_client and api_instance to get deployment logs
            api_client = set_header_parameter(DeployUtility.create_api_client(), Utility.get_url(DeployConstants.DEPLOY_URL))
            api_instance = deploy_sdk_client.EnvironmentApi(api_client)
            api_response = api_instance.get_deploy_resource_log(deployment_id, '-1')
            return api_response
        except ApiException as api_exception:
            Utility.print_exception(api_exception)

    def take_action(self, parsed_args):
        """take_action."""
        # Define parsed arguments
        deployment_id = parsed_args.deployment_id
        output = parsed_args.output

        # Get deployment logs
        deployment_logs = GetDeploymentLogs.get_deployment_logs(deployment_id)

        if deployment_logs:
            if output is not None:
                Utility.print_output(deployment_logs, output, PlatformConstants.STR_REFERENCE)
            else:
                Utility.print_output_as_str(deployment_logs) 
