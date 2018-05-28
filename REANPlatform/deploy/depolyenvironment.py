import os
import logging
from cliff.command import Command
import deploy_sdk_client
from deploy_sdk_client.rest import ApiException
from reanplatform.set_header import set_header_parameter
from reanplatform.utility import Utility


class DepolyEnv(Command):
    """Depoly Environment."""
    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        """get_parser."""
        parser = super(DepolyEnv, self).get_parser(prog_name)
        parser.add_argument('--env_id', '-id', help='Environment id to deploy', required=True)
        return parser

    def take_action(self, parsed_args):
        """take_action."""
        api_instance = deploy_sdk_client.EnvironmentApi()
        env_api_instance = set_header_parameter(api_instance)
        api_instance = deploy_sdk_client.EnvironmentApi()
        try:
            body = deploy_sdk_client.DeploymentConfiguration(environment_id=parsed_args.env_id)
            api_response = api_instance.deploy(parsed_args.env_id, body=body)
            print(api_response)
        except ApiException as e:
            Utility.print_exception(e)
