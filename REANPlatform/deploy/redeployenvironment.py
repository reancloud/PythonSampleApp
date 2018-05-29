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
        parser.add_argument('--env_id', '-id',
                            help='Environment id to deploy',
                            required=True)
        parser.add_argument('--name', '-n',
                            help='Environment name to deploy',
                            required=False)
        parser.add_argument('--version', '-v',
                            help='Environment version to deploy',
                            required=False)
        return parser

    def take_action(self, parsed_args):
        """take_action."""
        try:
            if parsed_args.name and parsed_args.version:
                api_instance = deploy_sdk_client.EnvironmentApi()
                env_api_instance = set_header_parameter(api_instance)
                api_response = api_instance.re_deploy_env(parsed_args.env_id, parsed_args.version)
                prin(api_response)
            else:
                print("Environment name and version is required")
        except ApiException as e:
            Utility.print_exception(e)
