"""Destroy environment module."""
import logging
from pprint import pprint
from cliff.command import Command
import deploy_sdk_client
from deploy_sdk_client.rest import ApiException
from reanplatform.set_header import set_header_parameter
import json
from reanplatform.utility import Utility


class DestroyEnvironment(Command):
    """Destroy environment."""

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        """get_parser."""
        parser = super(DestroyEnvironment, self).get_parser(prog_name)
        parser.add_argument('--env_name', '-name',
                            help='Environment name. This parameter\
                            is not required when env_id is specified',
                            required=False
                            )
        parser.add_argument('--env_id', '-id',
                            help='Environment id. This parameter is\
                            not required when env_name and\
                            env_version is specified',
                            required=False
                            )
        parser.add_argument('--env_version', '-env_v',
                            help='Environment version. This parameter\
                            is not required when env_id is specified',
                            required=False
                            )
        return parser

    def take_action(self, parsed_args):
        """take_action."""
        env_id = parsed_args.env_id
        env_name = parsed_args.env_name
        env_version = parsed_args.env_version

        self.validate_parameters(env_id, env_name, env_version)

        api_instance = deploy_sdk_client.EnvironmentApi()
        env_api_instance = set_header_parameter(api_instance)
        if env_id:
            self.destroy_env_by_envid(env_id, env_api_instance)
        elif env_name and env_version:
            self.destroy_env_by_envname(env_name, env_version, env_api_instance)    # noqa: E501

    def validate_parameters(self, env_id, env_name, env_version):
        """Validate cli parameter."""
        if env_id:
            if env_name or env_version:
                raise RuntimeError("Environment id is specified. Do not\
                provide environment name, environment version")
        elif env_name and env_version:
            if env_id:
                raise RuntimeError("Environment name and version is\
                    specified. Do not provide environment id")
        else:
            raise RuntimeError("Destroy environment. Usage: [rean-deploy\
                environment destroy --env_id Or --env_name\
                env_name --env_version env_version")

    def destroy_env_by_envid(self, env_id, env_api_instance):
        """destroy_env_by_envid."""
        try:
            response = env_api_instance.destroy(env_id)
            print("Environment status %s: %s" % (response.environment.name, response.status))  # noqa: E501
        except ApiException as e:
            Utility.print_exception(e)

    def destroy_env_by_envname(self, env_name, env_version, env_api_instance):
        """destroy_env_by_envname."""
        try:
            get_env_resp = env_api_instance.get_environment_by_version_and_name(env_name=env_name, env_version=env_version)  # noqa: E501
            environment_id = get_env_resp.config.env_id
            response = env_api_instance.destroy(environment_id)
            print("Environment status %s: %s" % (response.environment.name, response.status))  # noqa: E501
        except ApiException as e:
            Utility.print_exception(e)
