"""Export Environment."""
import re
import logging
from cliff.command import Command
from reanplatform.constants import Constants
from reanplatform.utility import Utility
from reanplatform.utilityconstants import PlatformConstants


class ExportEnvironment(Command):
    """Export Environment."""

    log = logging.getLogger(__name__)

    # EPILog will get print after commands
    _epilog = 'Example : rean-deploy export-environment --env_id 1'

    def get_parser(self, prog_name):
        """get_parser."""
        # Define parser
        parser = super(ExportEnvironment, self).get_parser(prog_name)
        parser.add_argument('--env_id', '-i', help='Environment id. This parameter is not required when --env_name and --env_version both is specified', required=False)
        parser.add_argument('--env_name', '-n', help='Environment name. This parameter is not required when --env_id is specified', required=False)
        parser.add_argument('--env_version', '-ev', help='Environment version. This parameter is not required when --env_id is specified', required=False)
        parser.add_argument('--output', '-o', help="Write output to <file> instead of stdout.", required=False)
        return parser

    @staticmethod
    def validate_parameters(env_id, env_name):
        """validate_parameters."""
        exception_msg = "Specify either --env_id OR --env_name"
        if env_id is None and env_name is None:
            raise RuntimeError(re.sub(' +', ' ', exception_msg))

    def take_action(self, parsed_args):
        """take_action."""
        # Define parsed_args
        env_id = parsed_args.env_id
        env_name = parsed_args.env_name
        env_version = parsed_args.env_version
        output = parsed_args.output
        # validate env_id and env_name
        ExportEnvironment.validate_parameters(env_id, env_name)
        response = None
        path = None
        if env_id:
            if env_name or env_version:
                raise RuntimeError("Environment name or version not required when id is specified")
            else:
                path = '/env/export/' + env_id
                response = ExportEnvironment.get_api_response(path)
        else:
            if env_name is None:
                raise RuntimeError("Environment name is required")
            elif env_version is None:
                path = '/env/export/envName/' + env_name
                response = ExportEnvironment.get_api_response(path)
            else:
                path = '/env/export/' + env_name + '/' + env_version
                response = ExportEnvironment.get_api_response(path)
        if response is not None:
            Utility.handleInvalidResponse(response, 200)
            if output is not None:
                output = output + '.blueprint.reandeploy'
                Utility.print_output(Utility.get_parsed_serialized_json(response.content), output, PlatformConstants.STR_REFERENCE)
            else:
                print(Utility.get_parsed_serialized_json(response.content))

    @staticmethod
    def get_api_response(path):
        """get_api_response."""
        curl_url = Constants.PLATFORM_BASE_URL + Constants.DEPLOY_URL + path
        return Utility.get_zip_stream(curl_url)
