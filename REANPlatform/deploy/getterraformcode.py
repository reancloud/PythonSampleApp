"""Get Terraform Files."""
import os
from pathlib import Path
import logging
import requests
from reanplatform.constants import Constants
from cliff.command import Command
import deploy_sdk_client
from deploy_sdk_client.rest import ApiException
from reanplatform.set_header import set_header_parameter
from reanplatform.utility import Utility
from deploy.constants import DeployConstants
from deploy.utility import DeployUtility


class GetTerraformCode(Command):
    """Get Terraform Files."""

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        """get_parser."""
        # Define parser
        parser = super(GetTerraformCode, self).get_parser(prog_name)
        parser.add_argument('--env_id', '-i', help='Environment id', required=True)
        parser.add_argument('--output_directory', '-o', help='Set Output directory to store terraform files.')
        return parser

    def take_action(self, parsed_args):
        """take_action."""
        # Define parsed_args
        env_id = parsed_args.env_id

        try:            
            path = '/env/download/terraform/' + env_id   
            curl_url = Constants.PLATFORM_BASE_URL + Constants.DEPLOY_URL + path
            api_response = Utility.get_zip_stream(curl_url)
            file_name = 'tf_files-' + env_id + '.tar.gz'
            if parsed_args.output_directory is not None and os.path.isdir(parsed_args.output_directory):
                if parsed_args.output_directory.endswith('/'):
                    open(parsed_args.output_directory + file_name, 'wb').write(api_response.content)
                    print("Terraform Files downloaded successfully at " + parsed_args.output_directory + file_name)
                else:
                    open(parsed_args.output_directory + '/' + file_name, 'wb').write(api_response.content)
                    print("Terraform Files downloaded successfully at " + parsed_args.output_directory + '/' + file_name)
            else:
                open(str(Path.home()) + "/" + file_name, 'wb').write(api_response.content)
                print("Terraform Files downloaded successfully at " + str(Path.home()) + "/" + file_name)
        except ApiException as api_exception:
            Utility.print_exception(api_exception)
