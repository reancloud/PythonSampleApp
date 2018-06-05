"""Get Deployment Status By Env ID and Deployment Name."""
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
                                required=False)
            parser.add_argument('--deployment_name', '-dname',
                                default='default',
                                help='Deployment Name',
                                required=False)
            parser.add_argument('--run_id', '-run_id',
                                help='Terraform Run ID',
                                required=False)
        except Exception as e:
            Utility.print_exception(e)

        return parser

    def take_action(self, parsed_args):
        """take_action."""
        instance = deploy_sdk_client.EnvironmentApi()
        api_instance = set_header_parameter(instance)

        # Check the deployment status
        try:
            if parsed_args.env_id:
                api_response = api_instance.get_deploy_status_0(
                    parsed_args.env_id,
                    parsed_args.deployment_name
                )
                pprint(api_response)
            elif parsed_args.run_id:
                api_response = api_instance.get_deployment_status(
                    parsed_args.run_id
                )
                pprint(api_response)
        except ApiException as e:
            Utility.print_exception(e)
