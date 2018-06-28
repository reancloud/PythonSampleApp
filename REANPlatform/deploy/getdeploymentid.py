"""Get Deployment ID."""
import os
from pprint import pprint
import logging
from cliff.command import Command
import deploy_sdk_client
from deploy_sdk_client.rest import ApiException
from reanplatform.set_header import set_header_parameter
from reanplatform.utility import Utility


class GetDeployments(Command):
    """Get Deployments."""

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        """get_parser."""
        # Define parser
        parser = super(GetDeployments, self).get_parser(prog_name)

        try:
            parser.add_argument('--deployment_name', '-n',
                                help='Deployment Name. Provide this attribute \
                                to get specific deployment.',
                                required=False)
            parser.add_argument('--env_id', '-id',
                                help='Environment Id',
                                required=True)
        except Exception as e:
            Utility.print_exception(e)

        return parser

    @staticmethod
    def get_deployments_by_env_id(env_id):
        """Get Deployments By Env ID."""
        try:
            # Initialise instance and api_instance
            instance = deploy_sdk_client.EnvironmentApi()
            api_instance = set_header_parameter(instance)
            res = api_instance.get_all_deployments_for_environment_by_id(
                env_id
            )
            pprint(res)
        except ApiException as e:
                Utility.print_exception(e)

    @staticmethod
    def get_deployment_by_deployment_name(env_id, deployment_name):
        """Get Deployments by Env ID And Deployment Name."""
        try:
            # Initialise instance and api_instance
            instance = deploy_sdk_client.EnvironmentApi()
            api_instance = set_header_parameter(instance)
            res = api_instance.get_all_deployments_for_environment_by_id_0(
                    env_id,
                    deployment_name
                )
            pprint(res)
        except ApiException as e:
                Utility.print_exception(e)

    def take_action(self, parsed_args):
        """take_action."""
        # Define parsed_args
        env_id = parsed_args.env_id
        deployment_name = parsed_args.deployment_name

        if env_id and deployment_name:
            GetDeployments.get_deployment_by_deployment_name(env_id, deployment_name)  # noqa: E501
        elif env_id:
            GetDeployments.get_deployments_by_env_id(env_id)
