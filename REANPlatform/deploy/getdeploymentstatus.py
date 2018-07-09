"""Get Deployment Status By Env ID and Deployment Name."""
import os
import re
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
                                help='Environment ID. This parameter \
                                is not required when -run_id is specified',
                                required=True)
            parser.add_argument('--deployment_name', '-dname',
                                default='default',
                                help='Deployment Name. This parameter \
                                is not required when -run_id is specified',
                                required=False)
        except Exception as e:
            Utility.print_exception(e)

        return parser

    @staticmethod
    def deployment_status(env_id, deployment_name):
        """Get Deployment Status."""
        try:
            # Initialise api_response
            api_response = None

            # Initialise instance and api_instance to get deployment status
            instance = deploy_sdk_client.EnvironmentApi()
            api_instance = set_header_parameter(instance)
            if (env_id and deployment_name):
                api_response = api_instance.get_deploy_status_by_env_id_and_deployment_name(
                    env_id,
                    deployment_name
                )
            elif env_id:
                api_response = api_instance.get_deploy_status_by_env_id(
                    env_id
                )
            return api_response.status
        except ApiException as e:
            Utility.print_exception(e)

    def take_action(self, parsed_args):
        """take_action."""
        # Define parsed arguments
        env_id = parsed_args.env_id
        deployment_name = parsed_args.deployment_name

        # Get deployment status
        status = Status.deployment_status(env_id, deployment_name)

        if status:
            print("Environment Status : %s " % (status))
