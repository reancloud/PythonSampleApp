"""Get Terraform Files."""
import os
import logging
from cliff.command import Command
from deploy_sdk_client.rest import ApiException
from reanplatform.constants import Constants
from reanplatform.utility import Utility


class GetTerraformCode(Command):
    """Get Terraform Code."""

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        """get_parser."""
        # Define parser
        parser = super(GetTerraformCode, self).get_parser(prog_name)
        parser.add_argument('--env_id', '-i', help='Environment id', required=True)
        parser.add_argument('--output_directory', '-o',
                            help='Set Output directory to store terraform code else it will get downloaded at current working directory.')
        return parser

    def take_action(self, parsed_args):
        """take_action."""
        # Define parsed_args
        env_id = parsed_args.env_id
        output_directory = parsed_args.output_directory
        try:
            path = '/env/download/terraform/' + env_id
            curl_url = Constants.PLATFORM_BASE_URL + Constants.DEPLOY_URL + path
            api_response = Utility.get_zip_stream(curl_url)
            file_name = 'tf_files-' + env_id + '.tar.gz'
            if output_directory is not None:
                if os.path.isdir(output_directory):
                    if parsed_args.output_directory.endswith('/'):
                        output_directory = output_directory + file_name
                    else:
                        output_directory = output_directory + '/' + file_name
                else:
                    raise RuntimeError("Invalid path! Please provide a valid path")
            else:
                output_directory = os.path.abspath(file_name)
            open(output_directory, 'wb').write(api_response.content)
            print("Terraform Code downloaded successfully at " + output_directory)
        except ApiException as api_exception:
            Utility.print_exception(api_exception)
