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
        parser.add_argument('--env_id', '-id',
                            help='Environment id',
                            required=True)
        parser.add_argument('--blueprint_name', '-n',
                            help='Specify file name for blueprint',
                            required=False)
        return parser

    def take_action(self, parsed_args):
        """take_action."""
        # Define parsed_args
        env_id = parsed_args.env_id

        if env_id:
            ExportBlueprintEnvironment.export_blueprint_environment(env_id)

    @staticmethod
    def export_blueprint_environment(env_id):
        """Export Blueprint Environment."""
        try:
            # Initialise instance and api_instance
            instance = deploy_sdk_client.EnvironmentApi()
            api_instance = set_header_parameter(instance, Utility.get_url(DeployConstants.DEPLOY_URL))
            blueprint = api_instance.export_blueprint_environment(env_id)
            response = api_instance.export_environment(env_id)
            blueprint_filename = response.name + '-' + response.env_version
            blueprint_filepath = os.getcwd() + '/' + blueprint_filename + '.blueprint.reandeploy'
            os.chdir(os.path.dirname(blueprint_filepath))
            with open(basename(blueprint_filepath), 'w') as outfile:
                outfile.write(str(blueprint))
            print("Blueprint file " + blueprint_filename + " created successfully at " + blueprint_filepath)
        except ApiException as api_exception:
            Utility.print_exception(api_exception)
