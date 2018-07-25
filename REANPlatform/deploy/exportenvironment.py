"""Export Environment."""
import os
from os.path import basename
import logging
from cliff.command import Command
import deploy_sdk_client
from deploy_sdk_client.rest import ApiException
from reanplatform.set_header import set_header_parameter
from reanplatform.utility import Utility
from deploy.constants import DeployConstants


class ExportEnvironment(Command):
    """Export Environment."""

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        """get_parser."""
        # Define parser
        parser = super(ExportEnvironment, self).get_parser(prog_name)
        parser.add_argument('--env_id', '-id',
                            help='Environment id',
                            required=True)
        return parser

    def take_action(self, parsed_args):
        """take_action."""
        # Define parsed_args
        env_id = parsed_args.env_id

        if env_id:
            ExportEnvironment.export_environment(env_id)

    @staticmethod
    def export_environment(env_id):
        """Export Environment."""
        try:
            # Initialise instance and api_instance
            instance = deploy_sdk_client.EnvironmentApi()
            api_instance = set_header_parameter(instance, Utility.get_url(DeployConstants.DEPLOY_URL))
            response = api_instance.export_environment(env_id)
            filename = response.name + '-' + response.env_version
            filepath = os.getcwd() + '/' + filename + '.blueprint.reandeploy'

            os.chdir(os.path.dirname(filepath))
            with open(basename(filepath), 'w') as outfile:
                outfile.write(str(response))
            print("Export Environment file " + filename + " created successfully at " + filepath)

        except ApiException as api_exception:
            Utility.print_exception(api_exception)
