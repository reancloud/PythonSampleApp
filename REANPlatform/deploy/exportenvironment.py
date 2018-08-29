"""Export Environment."""
import os
import logging
from cliff.command import Command
import deploy_sdk_client
from deploy_sdk_client.rest import ApiException
from reanplatform.set_header import set_header_parameter
from reanplatform.utility import Utility
from deploy.constants import DeployConstants
from deploy.utility import DeployUtility


class ExportEnvironment(Command):
    """Export Environment."""

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        """get_parser."""
        # Define parser
        parser = super(ExportEnvironment, self).get_parser(prog_name)
        parser.add_argument('--env_id', '-i', help='Environment id', required=True)
        parser.add_argument('--environment_file_name', '-f', help='Specify filename for exporting an environment else filename will be environment name with its version', required=False)
        return parser

    def take_action(self, parsed_args):
        """take_action."""
        # Define parsed_args
        env_id = parsed_args.env_id
        environment_file_name = parsed_args.environment_file_name

        ExportEnvironment.export_environment(env_id, environment_file_name)

    @staticmethod
    def export_environment(env_id, environment_file_name):
        """Export Environment."""
        try:
            # Initialise instance and api_instance
            api_client = set_header_parameter(DeployUtility.create_api_client(), Utility.get_url(DeployConstants.DEPLOY_URL))
            api_instance = deploy_sdk_client.EnvironmentApi(api_client)
            response = api_instance.export_environment(env_id)
            filename = environment_file_name

            if filename is None:
                filename = response.name + '-' + response.env_version

            filepath = os.getcwd() + '/' + filename + '.blueprint.reandeploy'
            Utility.create_output_file(filepath, response)
            print("Export Environment file " + filename + " created successfully at " + filepath)

        except ApiException as api_exception:
            Utility.print_exception(api_exception)
