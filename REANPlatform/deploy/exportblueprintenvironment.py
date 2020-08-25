"""Export Blueprint Environment."""
import os
import re
import logging
import requests
import urllib3
from cliff.command import Command
import deploy_sdk_client
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
        parser.add_argument('--env_id', '-i', help='Environment id', required=False)
        parser.add_argument('--env_ids', '-ids', help='Environment ids', required=False)
        parser.add_argument('--blueprint_file_name', '-f', help='Specify filename for blueprint else filename will be environment name with its version', required=False)
        return parser

    def take_action(self, parsed_args):
        """take_action."""
        # Define parsed_args
        env_id = parsed_args.env_id
        env_ids = parsed_args.env_ids
        blueprint_file_name = parsed_args.blueprint_file_name
        # validate env_id, env_ids and blueprint_file_name
        ExportBlueprintEnvironment.validate_parameters(env_id, env_ids, blueprint_file_name)
        # Initialise api_instance
        api_client = set_header_parameter(DeployUtility.create_api_client(), Utility.get_url(DeployConstants.DEPLOY_URL))
        api_instance = deploy_sdk_client.EnvironmentApi(api_client)
        # curl url for export
        curl_url = Constants.PLATFORM_BASE_URL + Constants.DEPLOY_URL + '/env/export/blueprint/'
        response = None
        if env_ids:
            environment_ids = ExportBlueprintEnvironment.get_environment_ids(env_ids)
            response = ExportBlueprintEnvironment.get_post_curl_response(curl_url, environment_ids)
        else:
            curl_url = curl_url + env_id
            response = Utility.get_zip_stream(curl_url)
        if response is not None:
            Utility.handleInvalidResponse(response, 200)
            if blueprint_file_name is None:
                env = api_instance.get_environment(env_id)
                blueprint_file_name = env.name + '-' + env.env_version
            output = blueprint_file_name + '.blueprint.reandeploy'
            Utility.print_output(Utility.get_parsed_serialized_json(response.content), output, PlatformConstants.STR_REFERENCE)
            blueprint_filepath = os.getcwd() + '/' + output
            print("Blueprint file " + blueprint_file_name + " created successfully at " + blueprint_filepath)

    @staticmethod
    def validate_parameters(env_id, env_ids, blueprint_file_name):
        """validate_parameters."""
        exception_msg = "Specify either --env_id OR --env_ids"
        if (env_id is None and env_ids is None) or (env_id is not None and env_ids is not None):
            raise RuntimeError(re.sub(' +', ' ', exception_msg))
        if env_ids is not None and blueprint_file_name is None:
            raise RuntimeError("Please provide --blueprint_file_name.")

    @staticmethod
    def get_environment_ids(env_ids):
        """get_environment_ids."""
        split_environment_ids = env_ids.split(",")
        environment_ids = []
        for x in split_environment_ids:
            environment_id = x.strip()
            environment_ids.append(environment_id)
        return environment_ids

    @staticmethod
    def get_post_curl_response(curl_url, env_ids):
        """Get zip stream."""
        headers = {'Authorization': Utility.get_user_credentials()}
        verify_ssl = Utility.get_config_property(PlatformConstants.VERIFY_SSL_CERTIFICATE_REFERENCE)
        if not verify_ssl:
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        response = requests.post(curl_url, headers=headers, verify=verify_ssl, json=env_ids)
        return response
