"""Export Blueprint Environment."""
import os
import logging
from cliff.command import Command
import deploy_sdk_client
from deploy_sdk_client.rest import ApiException
from reanplatform.constants import Constants
from reanplatform.set_header import set_header_parameter
from reanplatform.utility import Utility
from reanplatform.utilityconstants import PlatformConstants
from deploy.constants import DeployConstants
from deploy.utility import DeployUtility


class ExportBlueprintEnvironment(Command):
    """Export Blueprint Environment."""

    log = logging.getLogger(__name__)

    # EPILog will get print after commands
    _epilog = 'Example : rean-deploy export-blueprint-environment --env_id 1'

    def get_parser(self, prog_name):
        """get_parser."""
        # Define parser
        parser = super(ExportBlueprintEnvironment, self).get_parser(prog_name)
        parser.add_argument('--env_id', '-i', help='Environment id', required=True)
        parser.add_argument('--blueprint_file_name', '-f', help='Specify filename for blueprint else filename will be environment name with its version', required=False)
        return parser

    def take_action(self, parsed_args):
        """take_action."""
        # Define parsed_args
        env_id = parsed_args.env_id
        blueprint_file_name = parsed_args.blueprint_file_name

        ExportBlueprintEnvironment.export_blueprint_environment(env_id, blueprint_file_name)

    @staticmethod
    def export_blueprint_environment(env_id, blueprint_file_name):
        """Export Blueprint Environment."""
        try:
            # Initialise api_instance
            api_client = set_header_parameter(DeployUtility.create_api_client(), Utility.get_url(DeployConstants.DEPLOY_URL))
            api_instance = deploy_sdk_client.EnvironmentApi(api_client)
            filename = blueprint_file_name
            path = '/env/export/blueprint/' + env_id
            response = ExportBlueprintEnvironment.get_api_response(path)
            if response is not None:
                Utility.handleInvalidResponse(response, 200)
                if filename is not None:
                    output = filename + '.blueprint.reandeploy'
                else:
                    env = api_instance.get_environment(env_id)
                    filename = env.name + '-' + env.env_version
                    output = filename + '.blueprint.reandeploy'
                Utility.print_output(Utility.get_parsed_serialized_json(response.content), output, PlatformConstants.STR_REFERENCE)
                blueprint_filepath = os.getcwd() + '/' + filename + '.blueprint.reandeploy'
                print("Blueprint file " + filename + " created successfully at " + blueprint_filepath)
        except ApiException as api_exception:
            Utility.print_exception(api_exception)

    @staticmethod
    def get_api_response(path):
        """get_api_response."""
        curl_url = Constants.PLATFORM_BASE_URL + Constants.DEPLOY_URL + path
        return Utility.get_zip_stream(curl_url)
