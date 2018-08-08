"""Get Validation Param."""
import logging
from cliff.command import Command
import deploy_sdk_client
from deploy_sdk_client.rest import ApiException
from reanplatform.set_header import set_header_parameter
from reanplatform.utility import Utility
from deploy.constants import DeployConstants


class GetValidationParam(Command):
    """Get Validation Param."""

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        """get_parser."""
        # Define parser
        parser = super(GetValidationParam, self).get_parser(prog_name)
        parser.add_argument('--env_id', '-i',
                            help='Environment id',
                            required=True)
        parser.add_argument('--deployment_name', '-n', default='default',
                            help='Deployment name. Please provide this attribute if deployment name is not default.',
                            required=False)
        return parser

    def take_action(self, parsed_args):
        """take_action."""
        # Define parsed_args
        env_id = parsed_args.env_id
        deployment_name = parsed_args.deployment_name

        if env_id:
            GetValidationParam.get_validation_param(env_id, deployment_name)

    @staticmethod
    def get_validation_param(env_id, deployment_name):
        """Get Validation Param."""
        try:
            # Initialise and api_instance
            api_instance = set_header_parameter(deploy_sdk_client.EnvironmentApi(), Utility.get_url(DeployConstants.DEPLOY_URL))
            response = api_instance.get_validation_param_by_env_id_and_deployment_name(env_id, deployment_name)
            print(response)
        except ApiException as api_exception:
            Utility.print_exception(api_exception)
