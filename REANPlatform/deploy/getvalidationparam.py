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
        parser.add_argument('--env_id', '-id',
                            help='Environment Id',
                            required=True)
        return parser

    def take_action(self, parsed_args):
        """take_action."""
        # Define parsed_args
        env_id = parsed_args.env_id

        if env_id:
            GetValidationParam.get_validation_param(env_id)

    @staticmethod
    def get_validation_param(env_id):
        """Get Validation Param."""
        try:
            # Initialise instance and api_instance
            instance = deploy_sdk_client.EnvironmentApi()
            api_instance = set_header_parameter(instance, Utility.get_url(DeployConstants.DEPLOY_URL))
            response = api_instance.get_validation_param(
                env_id
            )
            print(response)
        except ApiException as api_exception:
            Utility.print_exception(api_exception)
