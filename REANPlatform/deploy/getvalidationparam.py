"""Get Validation Param."""
import os
import logging
from cliff.command import Command
import deploy_sdk_client
from deploy_sdk_client.rest import ApiException
from reanplatform.set_header import set_header_parameter
from reanplatform.utility import Utility
from deploy.constants import DeployConstants
from deploy.utility import DeployUtility


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
        parser.add_argument('--output', '-o',
                            help="Write output to <file> instead of stdout.",
                            required=False
                           )
        return parser

    def take_action(self, parsed_args):
        """take_action."""
        # Define parsed_args
        env_id = parsed_args.env_id
        deployment_name = parsed_args.deployment_name
        file_name = parsed_args.output

        # Get validation param
        validation_param = GetValidationParam.get_validation_param(env_id, deployment_name)

        if validation_param:
            if file_name is not None:
                filepath = os.getcwd() + '/' + file_name + '.json'
                Utility.create_output_file(filepath, validation_param)
                Utility.print_output("Output file " + file_name + " created successfully at " + filepath, parsed_args.output,)
            else:
                Utility.print_output(validation_param, parsed_args.output)

    @staticmethod
    def get_validation_param(env_id, deployment_name):
        """Get Validation Param."""
        try:
            # Initialise api_response
            api_response = None

            # Initialise and api_instance
            api_client = set_header_parameter(DeployUtility.create_api_client(), Utility.get_url(DeployConstants.DEPLOY_URL))
            api_instance = deploy_sdk_client.EnvironmentApi(api_client)
            api_response = api_instance.get_validation_param_by_env_id_and_dep_name(env_id, deployment_name)
            return api_response
        except ApiException as api_exception:
            Utility.print_exception(api_exception)
