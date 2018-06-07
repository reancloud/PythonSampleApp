"""Destroy deployment module."""
import logging
from pprint import pprint
from cliff.command import Command
import deploy_sdk_client
from deploy_sdk_client.rest import ApiException
from reanplatform.set_header import set_header_parameter
import json
from reanplatform.utility import Utility


class DestroyDeployment(Command):
    """Destroy deployment."""

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        """get_parser."""
        parser = super(DestroyDeployment, self).get_parser(prog_name)
        parser.add_argument(
                            '--env_name', '-name',
                            help='Environment name. This parameter is\
                            not required when deployment_id provided',
                            required=False
                            )
        parser.add_argument(
                            '--deployment_name', '-d_name',
                            help='Deployment name. This parameter is\
                            not required when deployment_id provided',
                            required=False
                            )
        parser.add_argument(
                            '--deployment_id', '-d_id',
                            help='Deployment id. This parameter is\
                            not required when env_name and\
                            deployment_name are provided',
                            required=False
                            )
        return parser

    def take_action(self, parsed_args):
        """take_action."""
        env_name = parsed_args.env_name
        deployment_name = parsed_args.deployment_name
        deployment_id = parsed_args.deployment_id

        self.validate(env_name, deployment_name, deployment_id)

        api_instance = deploy_sdk_client.EnvironmentApi()
        env_api_instance = set_header_parameter(api_instance)
        if deployment_id:
            self.destroy_deployment_id(deployment_id, api_instance)
        elif env_name and deployment_name:
            self.destroy_by__envname_deployment_name(env_name, deployment_name, api_instance)   # noqa: E501

    def validate(self, env_name, deployment_name, deployment_id):
        """Validate cli parameter."""
        if deployment_id:
            if deployment_name or env_name:
                raise RuntimeError("Deployment id is specified. Do not\
                    provide environment name and deployment name")
        elif env_name and deployment_name:
            if deployment_id:
                raise RuntimeError("Environment name and deployment\
                    name is specified. Do not provide deployment id")
        else:
            raise RuntimeError('Destroy deployment, Usage: [rean-deploy\
                destroy-deployment --deployment_id id Or --env_name env_name\
                --deployment_name deployment_name')

    def destroy_deployment_id(self, deployment_id, env_api_instance):
        """destroy_deployment_id."""
        try:
            deployment_response = env_api_instance.destroy_deployment(deployment_id)     # noqa: E501
            print("Deployment status %s: %s" % (deployment_response.environment.name, deployment_response.status))  # noqa: E501
        except ApiException as e:
            Utility.print_exception(e)

    def destroy_by__envname_deployment_name(self, env_name, deployment_name, env_api_instance):     # noqa: E501
        """destroy_by__envname_deployment_name."""
        try:
            deployment_response = env_api_instance.destroy_deployment_0(env_name, deployment_name)  # noqa: E501
            print("Deployment status %s: %s" % (deployment_response.environment.name, deployment_response.status))  # noqa: E501
        except ApiException as e:
            Utility.print_exception(e)
