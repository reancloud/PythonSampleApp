"""Destroy deployment module."""
import logging
from pprint import pprint
from cliff.command import Command
import deploy_sdk_client
from deploy_sdk_client.rest import ApiException
from reanplatform.set_header import set_header_parameter
import json
import re
from reanplatform.utility import Utility


class DestroyDeployment(Command):
    """Destroy deployment."""

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        """get_parser."""
        parser = super(DestroyDeployment, self).get_parser(prog_name)
        parser.add_argument(
            '--deployment_id', '-d_id',
            help='Deployment id. This parameter is\
                            not required when --env_id OR --deployment_name\
                            and --env_id are specified',
            required=False
        )
        parser.add_argument('--env_id', '-id',
                            help='Environment id. This parameter is\
                            not required when --deployment_id is specified',
                            required=False
                            )
        parser.add_argument(
            '--deployment_name', '-d_name',
            help='Deployment name. This parameter is\
                            not required when --deployment_id is specified',
            required=False
        )
        return parser

    @staticmethod
    def validate_parameters(env_id, deployment_name, deployment_id):
        """Validate cli parameter."""
        exception_msg = "Specify either ---env_id OR --deployment_id OR\
                --env_id and --deployment_name"
        if env_id and deployment_id:
            raise RuntimeError(re.sub(' +', ' ', exception_msg))
        elif deployment_name and deployment_id:
            raise RuntimeError(re.sub(' +', ' ', exception_msg))
        elif deployment_name and env_id is None:
            raise RuntimeError(re.sub(' +', ' ', exception_msg))

    def take_action(self, parsed_args):
        """take_action."""
        env_id = parsed_args.env_id
        deployment_name = parsed_args.deployment_name
        deployment_id = parsed_args.deployment_id

        DestroyDeployment.validate_parameters(
            env_id, deployment_name, deployment_id)

        if env_id and deployment_name:
            DestroyDeployment.destroy_by_envid_deploymentname(
                env_id, deployment_name)
        elif env_id:
            DestroyDeployment.destroy_env_by_envid(env_id)
        elif deployment_id:
            DestroyDeployment.destroy_by_deploymentid(deployment_id)

    @staticmethod
    def destroy_env_by_envid(env_id):
        """destroy_env_by_envid."""
        try:
            api_instance = deploy_sdk_client.EnvironmentApi()
            env_api_instance = set_header_parameter(api_instance)
            response = env_api_instance.destroy(env_id)
            print("Environment status for %s: %s" %
                  (response.environment.name, response.status))
        except ApiException as e:
            Utility.print_exception(e)

    @staticmethod
    def destroy_by_deploymentid(deployment_id):
        """destroy_deployment_id."""
        try:
            api_instance = deploy_sdk_client.EnvironmentApi()
            env_api_instance = set_header_parameter(api_instance)
            deployment_response = env_api_instance.destroy_deployment_by_id(
                deployment_id)
            print("Environment status for %s: %s" % (
                deployment_response.environment.name, deployment_response.status))
        except ApiException as e:
            Utility.print_exception(e)

    @staticmethod
    def destroy_by_envid_deploymentname(env_id, deployment_name):
        """destroy_by_envid_deploymentname."""
        try:
            api_instance = deploy_sdk_client.EnvironmentApi()
            env_api_instance = set_header_parameter(api_instance)
            get_env_name = api_instance.get_environment(env_id)
            deployment_response = env_api_instance.destroy_deployment_by_env_name_and_deployment_name(
                get_env_name.name, deployment_name)
            print("Environment status for %s: %s" % (
                deployment_response.environment.name, deployment_response.status))
        except ApiException as e:
            Utility.print_exception(e)
