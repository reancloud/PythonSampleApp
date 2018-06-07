"""Delete provider module."""
import logging
from cliff.command import Command
import deploy_sdk_client
from deploy_sdk_client.rest import ApiException
from reanplatform.set_header import set_header_parameter
from reanplatform.utility import Utility


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

    def delete_env(self, instance, api_instance, env_id):
        """Delete environment action."""
        try:
            api_response = api_instance.delete_environment(env_id)
            print(api_response)
        except Exception as e:
            print(e)
            Utility.print_exception(e)

    def take_action(self, parsed_args):
        """Delete environment action."""
        # Initialise instance and api_instance in delete_env environment method
        instance = deploy_sdk_client.EnvironmentApi()
        api_instance = set_header_parameter(instance)

        # Define parsed argument
        env_id = parsed_args.id

        # Delete an environment by ID
        self.delete_env(instance, api_instance, env_id)
