import os
from pprint import pprint
import logging
from cliff.command import Command
import deploy_sdk_client
from deploy_sdk_client.rest import ApiException
from reanplatform.set_header import set_header_parameter
from reanplatform.utility import Utility


class Status(Command):
    """Get Deployment Status."""
    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        """get_parser."""
        # Define parser
        parser = super(Status, self).get_parser(prog_name)

        try:
            parser.add_argument('--env_id', '-id',
                                help='Environment id',
                                required=True)
        except Exception:
            print("Please provide required arguments")

        return parser

    def take_action(self, parsed_args):
        """take_action."""
        instance = deploy_sdk_client.EnvironmentApi()
        api_instance = set_header_parameter(instance)

        # Check the deployment status
        try:
            api_response = api_instance.get_deploy_status(parsed_args.env_id)
            pprint("Deployment status is " + api_response.status)
        except ApiException as e:
            Utility.print_exception(e)
            pprint("Environment is not deployed yet")
