"""Export Blueprint Environment."""
import os
from os.path import basename
import logging
from cliff.command import Command
import deploy_sdk_client
from deploy_sdk_client.rest import ApiException
from reanplatform.set_header import set_header_parameter
from reanplatform.utility import Utility
from deploy.constants import DeployConstants


class ExportBlueprintEnvironment(Command):
    """Export Blueprint Environment."""

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        """get_parser."""
        # Define parser
        parser = super(ExportBlueprintEnvironment, self).get_parser(prog_name)
        parser.add_argument('--env_id', '-i',
                            help='Environment id',
                            required=True)
        parser.add_argument('--blueprint_file_name', '-f',
                            help='Specify filename for blueprint else filename will be environment name with its version',
                            required=False)
        return parser

    def take_action(self, parsed_args):
        """take_action."""
        # Define parsed_args
        env_id = parsed_args.env_id
        blueprint_file_name = parsed_args.blueprint_file_name

        if env_id:
            ExportBlueprintEnvironment.export_blueprint_environment(env_id, blueprint_file_name)

    @staticmethod
    def export_blueprint_environment(env_id, blueprint_file_name):
        """Export Blueprint Environment."""
        try:
            # Initialise api_instance
            api_instance = set_header_parameter(deploy_sdk_client.EnvironmentApi(), Utility.get_url(DeployConstants.DEPLOY_URL))
            blueprint = api_instance.export_blueprint_environment(env_id)
            filename = blueprint_file_name

            if filename is None:
                response = api_instance.export_environment(env_id)
                filename = response.name + '-' + response.env_version

            blueprint_filepath = os.getcwd() + '/' + filename + '.blueprint.reandeploy'
            os.chdir(os.path.dirname(blueprint_filepath))
            with open(basename(blueprint_filepath), 'w') as outfile:
                outfile.write(str(blueprint))
            print("Blueprint file " + filename + " created successfully at " + blueprint_filepath)
        except ApiException as api_exception:
            Utility.print_exception(api_exception)
