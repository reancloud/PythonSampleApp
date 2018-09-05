"""Delete provider module."""
import logging
from cliff.command import Command
import deploy_sdk_client
from deploy_sdk_client.rest import ApiException
from reanplatform.set_header import set_header_parameter
from reanplatform.utility import Utility
from reanplatform.utilityconstants import PlatformConstants
from deploy.constants import DeployConstants
from deploy.utility import DeployUtility


class DeleteEnvironment(Command):
    """Delete Environment."""

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        """get_parser."""
        parser = super(DeleteEnvironment, self).get_parser(prog_name)
        parser.add_argument('--env_id', '-i', help='Id of an environment to be deleted', required=True)
        parser.add_argument('--output', '-o',
                            help="Write output to <file> instead of stdout.",
                            required=False
                           )
        return parser

    @staticmethod
    def delete_env(env_id, parsed_args):
        """Delete environment action."""
        try:
            # Initialise api_client and api_instance
            api_client = set_header_parameter(DeployUtility.create_api_client(), Utility.get_url(DeployConstants.DEPLOY_URL))
            api_instance = deploy_sdk_client.EnvironmentApi(api_client)
            api_response = api_instance.delete_environment(env_id)
            Utility.print_output("Environment deleted successfully : {}".format(api_response.id), parsed_args.output, PlatformConstants.STR_REFERENCE)
        except ApiException as exception:
            Utility.print_exception(exception)

    def take_action(self, parsed_args):
        """Delete environment action."""
        # Define parsed argument
        env_id = parsed_args.env_id

        # Delete an environment by ID
        DeleteEnvironment.delete_env(env_id)
