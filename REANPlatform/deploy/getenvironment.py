"""Get Environment module."""
import os
import logging
from cliff.command import Command
import deploy_sdk_client
from deploy_sdk_client.rest import ApiException
from reanplatform.set_header import set_header_parameter
from reanplatform.utility import Utility
from deploy.constants import DeployConstants
from deploy.utility import DeployUtility


class GetEnvironment(Command):
    """Get Environment."""

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        """get_parser."""
        parser = super(GetEnvironment, self).get_parser(prog_name)
        parser.add_argument('--env_name', '-n', help='Environment name', required=True)
        parser.add_argument('--env_version', '-ev', help='Environment version.', required=False)
        parser.add_argument('--output', '-o', help="Write output to <file> instead of stdout.", required=False)
        return parser

    @staticmethod
    def get_environment_by_name_and_version(name, version):
        """Get Environment By Name And Version."""
        try:
            # Initialise api_client and api_instance
            api_client = set_header_parameter(DeployUtility.create_api_client(), Utility.get_url(DeployConstants.DEPLOY_URL))
            api_instance = deploy_sdk_client.EnvironmentApi(api_client)
            # Get environment by name and version
            api_response = api_instance.get_environment_by_version_and_name(name, version)
            return api_response
        except ApiException as api_exception:
            Utility.print_exception(api_exception)

    @staticmethod
    def get_environment_by_env_name(name):
        """Get Environment By Name."""
        try:
            # Initialise api_client and api_instance
            api_client = set_header_parameter(DeployUtility.create_api_client(), Utility.get_url(DeployConstants.DEPLOY_URL))
            api_instance = deploy_sdk_client.EnvironmentApi(api_client)
            # Get environment by name
            api_response = api_instance.get_environment_by_name_with_latest_version(name)
            return api_response
        except ApiException as api_exception:
            Utility.print_exception(api_exception)

    def take_action(self, parsed_args):
        """take_action of GetEnvironment."""
        # Define parsed argument
        name = parsed_args.env_name
        version = parsed_args.env_version
        # Initialise env_response
        env_response = None
        # Get Environment
        if version:
            env_response = GetEnvironment.get_environment_by_name_and_version(name, version)
        else:
            env_response = GetEnvironment.get_environment_by_env_name(name)

        if env_response:
            if parsed_args.output is not None:
                Utility.print_output_as_dict(env_response, parsed_args.output)
            else:
                print(Utility.get_parsed_json(env_response))
