"""Delete provider module."""
import logging
from cliff.command import Command
import deploy_sdk_client
from deploy_sdk_client.rest import ApiException
from reanplatform.set_header import set_header_parameter
from reanplatform.utility import Utility
from deploy.constants import DeployConstants


class DeleteEnvironment(Command):
    """Delete provider."""

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        """get_parser."""
        parser = super(DeleteEnvironment, self).get_parser(prog_name)
        parser.add_argument('--id', '-id',
                            help='Id of an environment to delete',
                            required=True)
        return parser

    @staticmethod
    def delete_env(env_id):
        """Delete environment action."""
        try:
            # Initialise instance and api_instance
            instance = deploy_sdk_client.EnvironmentApi()
            api_instance = set_header_parameter(instance, Utility.get_url(DeployConstants.DEPLOY_URL))
            api_response = api_instance.delete_environment(env_id)
            print(api_response)
        except ApiException as exception:
            Utility.print_exception(exception)

    def take_action(self, parsed_args):
        """Delete environment action."""
        # Define parsed argument
        env_id = parsed_args.id

        # Delete an environment by ID
        DeleteEnvironment.delete_env(env_id)
