import os
import logging
from cliff.command import Command
import deploy_sdk_client
from deploy_sdk_client.rest import ApiException
from reanplatform.set_header import set_header_parameter
from reanplatform.utility import Utility


class ReDepoly(Command):
    """Redeploy an environment by name and version."""
    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        """get_parser."""
        parser = super(ReDepoly, self).get_parser(prog_name)
        parser.add_argument('--name', '-n',
                            help='Environment name to deploy',
                            required=False)
        parser.add_argument('--version', '-v', type=str,
                            help='Environment version to deploy',
                            required=False)
        return parser

    def take_action(self, parsed_args):
        """take_action."""
        try:
            api_instance = deploy_sdk_client.EnvironmentApi()
            env_api_instance = set_header_parameter(api_instance)
            api_response = api_instance.re_deploy(parsed_args.env_name, parsed_args.version)
            prin(api_response)
        except ApiException as e:
            Utility.print_exception(e)
