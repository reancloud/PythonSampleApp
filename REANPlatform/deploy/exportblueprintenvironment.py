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
        parser.add_argument('--b_name', '-n',
                            help='Specify file name for blueprint',
                            required=False)
        return parser

    def take_action(self, parsed_args):
        """take_action."""
        # Define parsed_args
        env_id = parsed_args.env_id
        blueprint_filename = parsed_args.b_name
        blueprint_path = None

        if blueprint_filename is None:
            blueprint_path = os.getcwd() + '/' + \
                'environment.blueprint.reandeploy'
        else:
            blueprint_path = os.getcwd() + '/' + blueprint_filename + \
                '.blueprint.reandeploy'

        ExportBlueprintEnvironment.validate_parameter(blueprint_path)

        if env_id:
            ExportBlueprintEnvironment.export_blueprint_environment(
                env_id, blueprint_path)

    @staticmethod
    def validate_parameter(blueprint_path):
        """Validate parameter."""
        if blueprint_path is None:
            raise RuntimeError("Please provide valid path")

    @staticmethod
    def export_blueprint_environment(env_id, blueprint_path):
        """Export Blueprint Environment."""
        try:
            # Initialise instance and api_instance
            instance = deploy_sdk_client.EnvironmentApi()
            api_instance = set_header_parameter(instance, Utility.get_url(DeployConstants.DEPLOY_URL))
            response = api_instance.export_blueprint_environment(env_id)
            os.chdir(os.path.dirname(blueprint_path))
            with open(basename(blueprint_path), 'w') as outfile:
                outfile.write(str(response))
            print("Blueprint file created successfully at " + blueprint_path)

        except ApiException as api_exception:
            Utility.print_exception(api_exception)
