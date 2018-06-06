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
                                required=False)
            parser.add_argument('--deployment_name', '-dname',
                                default='default',
                                help='Deployment Name. This parameter \
                                is not required when -run_id is specified',
                                required=False)
            parser.add_argument('--run_id', '-run_id',
                                help='Terraform Run ID,
                                required=False)
        except Exception as e:
            Utility.print_exception(e)

        return parser

    def validate(self, env_id, deployment_name, run_id):
        """Validate Parsed Arguments."""
        if env_id and deployment_name and run_id:
            message = "Please Provide either Run ID or Environment ID and \
            Deployment Name. Do Not Provide All Of Them."
            exception_msg = re.sub(' +', ' ', message)
            raise Exception(exception_msg)
        if env_id and run_id:
            message = "Please Provide either Run ID or Environment ID and \
            Deployment Name. Do Not Provide Environment ID and Run ID Both."
            exception_msg = re.sub(' +', ' ', message)
            raise Exception(exception_msg)
        if deployment_name and run_id:
            message = "Please Provide either Run ID or Environment ID and \
            Deployment Name. Do Not Provide Deployment Name and Run ID Both."
            exception_msg = re.sub(' +', ' ', message)
            raise Exception(exception_msg)

    def deployment_status(self, instance, api_instance,
                          env_id, deployment_name, run_id):
        """Get Deployment Status."""
        try:
            if env_id:
                api_response = api_instance.get_deploy_status_0(
                    env_id,
                    deployment_name
                )
                pprint(api_response)
            elif run_id:
                api_response = api_instance.get_deployment_status(
                    run_id
                )
                pprint(api_response)
        except ApiException as e:
            Utility.print_exception(e)

    def take_action(self, parsed_args):
        """take_action."""
        # Define parsed arguments
        env_id = parsed_args.env_id
        deployment_name = parsed_args.deployment_name
        run_id = parsed_args.run_id

        # Create an instance for REAN Deploy API
        instance = deploy_sdk_client.EnvironmentApi()
        api_instance = set_header_parameter(instance)
        # Validate parsed agruments
        self.validate(env_id, deployment_name, run_id)
        # Get deployment status
        self.deployment_status(instance, api_instance,
                               env_id, deployment_name, run_id)
