"""Export Environment."""
import re
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
        parser.add_argument('--env_id', '-i', help='Environment id. This parameter is not required when --env_name and --env_version both is specified', required=False)
        parser.add_argument('--env_name', '-n', help='Environment name. This parameter is not required when --env_id is specified', required=False)
        parser.add_argument('--env_version', '-ev', help='Environment version. This parameter is not required when --env_id is specified', required=False)
        parser.add_argument('--output', '-o', help="Write output to <file> instead of stdout.", required=False)
        return parser

    @staticmethod
    def validate_parameters(env_id, env_name, env_version):
        """validate_parameters."""
        exception_msg = "Specify either --env_id OR --env_name"
        if env_id is None and (env_name is None and env_version is None):
            raise RuntimeError(re.sub(' +', ' ', exception_msg))

    def take_action(self, parsed_args):
        """take_action."""
        try:
            # Define parsed_args
            env_id = parsed_args.env_id
            env_name = parsed_args.env_name
            env_version = parsed_args.env_version
            output = parsed_args.output
            # validate env_id and env_name
            ExportEnvironment.validate_parameters(env_id, env_name, env_version)
            # Initialise instance and api_instance
            api_client = set_header_parameter(DeployUtility.create_api_client(), Utility.get_url(DeployConstants.DEPLOY_URL))
            api_instance = deploy_sdk_client.EnvironmentApi(api_client)
            response = None
            if env_id:
                if env_name or env_version:
                    raise RuntimeError("Environment name or version not required when id is specified")
                else:
                    response = api_instance.export_environment(env_id)
            else:
                if env_name is None:
                    raise RuntimeError("Environment name is required")
                elif env_version is None:
                    response = api_instance.export_environment_by_name(env_name)
                else:
                    response = api_instance.export_environment_by_name_and_version(env_name, env_version)
            if response:
                if output is not None:
                    Utility.print_output_as_dict(response, output)
                else:
                    print(Utility.get_parsed_json(response))
        except ApiException as api_exception:
            Utility.print_exception(api_exception)
