"""Get Terraform Files."""
from pathlib import Path
import logging
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
        parser.add_argument('--output_directory', '-o', help='Set Output directory to store reports.')
        return parser

    def take_action(self, parsed_args):
        """take_action."""
        # Define parsed_args
        env_id = parsed_args.env_id

        try:
            # Initialise api_client and api_instance
            api_client = set_header_parameter(DeployUtility.create_api_client(), Utility.get_url(DeployConstants.DEPLOY_URL))
            print(api_client)
            api_instance = deploy_sdk_client.EnvironmentApi(api_client)
            print(api_instance)
            api_response = api_instance.download_terraform_files(env_id)
            print(api_response)

            file_name = 'terraform_files.zip'
            if parsed_args.output_directory is not None and Utility.validate_path(parsed_args):
                self.log.debug("File path Exists")
                if parsed_args.output_directory.endswith('/'):
                    open(parsed_args.output_directory + file_name, 'wb').write(api_response.data)
                    print("Terraform Files downloaded successfully at " + parsed_args.output_directory + file_name)
                else:
                    open(parsed_args.output_directory + '/' + file_name, 'wb').write(api_response.data)
                    print("Terraform Files downloaded successfully at " + parsed_args.output_directory + '/' + file_name)
            else:
                self.log.debug("File path not exists")
                open(str(Path.home()) + "/" + file_name, 'wb').write(api_response.data)
                print("Terraform Files downloaded successfully at " + str(Path.home()) + "/" + file_name)
        except ApiException as api_exception:
            Utility.print_exception(api_exception)
