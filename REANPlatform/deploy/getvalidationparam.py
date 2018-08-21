"""Get Validation Param."""
import os
from os.path import basename
import logging
from cliff.command import Command
import deploy_sdk_client
from deploy_sdk_client.rest import ApiException
from reanplatform.set_header import set_header_parameter
from reanplatform.utility import Utility
from deploy.constants import DeployConstants


class GetValidationParam(Command):
    """Get Validation Param."""

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        """get_parser."""
        # Define parser
        parser = super(GetValidationParam, self).get_parser(prog_name)
        parser.add_argument('--env_id', '-i', help='Environment id', required=True)
        parser.add_argument('--deployment_name', '-n', default='default', help='Deployment name. Please provide this attribute if deployment name is not default.', required=False)
        parser.add_argument('--output', '-f', help='Specify filename for getting validation parameters', required=False)
        return parser

    def take_action(self, parsed_args):
        """take_action."""
        # Define parsed_args
        env_id = parsed_args.env_id
        deployment_name = parsed_args.deployment_name
        file_name = parsed_args.output

        # Get validation param
        if env_id:
            validation_param = GetValidationParam.get_validation_param(env_id, deployment_name)

        if validation_param:
            if file_name is not None:
                filepath = os.getcwd() + '/' + file_name + '.json'
                os.chdir(os.path.dirname(filepath))
                with open(basename(filepath), 'w') as outfile:
                    outfile.write(str(validation_param))
                print("Output file " + file_name + " created successfully at " + filepath)
            else:
                print(validation_param)

    @staticmethod
    def get_validation_param(env_id, deployment_name):
        """Get Validation Param."""
        try:
            # Initialise api_response
            api_response = None

            # Initialise and api_instance
            api_client = set_header_parameter(Utility.create_api_client(), Utility.get_url(DeployConstants.DEPLOY_URL))
            api_instance = deploy_sdk_client.EnvironmentApi(api_client)
            api_response = api_instance.get_validation_param_by_env_id_and_deployment_name(env_id, deployment_name)
            return api_response
        except ApiException as api_exception:
            Utility.print_exception(api_exception)
