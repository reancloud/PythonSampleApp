"""Depoly Environment."""
import os
import re
from pprint import pprint
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
        # Define parser
        parser = super(DepolyEnv, self).get_parser(prog_name)
        try:
            parser.add_argument('--env_name', '-ename',
                                help='Environment name, This parameter is \
                                not required when environmentId is specified',
                                required=False)
            parser.add_argument('--env_version', '-env_v',
                                help='Environment version. This parameter is \
                                not required when environmentId is specified',
                                required=False)
            parser.add_argument('--deployment_name', '-dname',
                                default='default',
                                help='Deployment Name',
                                required=False)
            parser.add_argument('--env_id', '-id',
                                help='Environment Id',
                                required=False)
            parser.add_argument('--deployment_description', '-desc',
                                help='Deployment Description',
                                required=False)
            parser.add_argument('--provider_name', '-pname',
                                help='Provider Name',
                                required=False)
            parser.add_argument('--region', '-region',
                                help='Region Name',
                                required=False)
            parser.add_argument('--env_version_id', '-env-ver-id',
                                help='Environment Version ID',
                                required=False)
            parser.add_argument('--input_json', '-json',
                                help='Input Json in a format of string \
                                \'{"Key": "Value"}\'',
                                required=False)

            return parser
        except ApiException as e:
            Utility.print_exception(e)

    def validate(self, env_id, env_name, env_version):
        """Valiate parsed arguments."""
        if env_id and env_name and env_version:
            message = "Please provide either Environment's ID or Name \
            and Version."
            exception_msg = re.sub(' +', ' ', message)
            raise Exception(exception_msg)
        elif env_id and env_name:
            message = "Please provide either Environment's ID or Name \
            and Version. Do not provide Environment ID and Name both."
            exception_msg = re.sub(' +', ' ', message)
            raise Exception(exception_msg)
        elif env_id and env_version:
            message = "Please provide either Environment's ID or Name \
            and Version. Do not provide Environment ID and Version both."

    def deploy_by_id(self, instance, api_instance, env_id, body):
        """Deploy Environment By ID."""
        try:
            api_response = api_instance.deploy(env_id, body=body)
            pprint(api_response)
        except ApiException as e:
            Utility.print_exception(e)

    def deploy_by_name_and_version(self, instance, api_instance,
                                   env_name, env_version, body):
        """Deploy Environment By Name And Version."""
        try:
            api_response = api_instance.deploy_0(
                env_name,
                env_version,
                body=body
            )
            pprint(api_response)
        except ApiException as e:
            Utility.print_exception(e)

    def take_action(self, parsed_args):
        """Deploy Environment Action."""
        # Create an instance of the API class
        instance = deploy_sdk_client.EnvironmentApi()
        api_instance = set_header_parameter(instance)

        # Define parsed arguments
        env_id = parsed_args.env_id
        deployment_name = parsed_args.deployment_name
        deployment_description = parsed_args.deployment_description
        region = parsed_args.region
        provider_name = parsed_args.provider_name
        input_json = parsed_args.input_json
        env_name = parsed_args.env_name
        env_version = parsed_args.env_version

        # Valiate parsed arguments
        self.validate(env_id, env_name, env_version)

        # Prepare deployment configuration body
        body = deploy_sdk_client.DeploymentConfiguration(
            # environment_id=env_id,
            deployment_name=deployment_name,
            deployment_description=deployment_description,
            region=region,
            provider_name=provider_name,
            input_json=input_json
        )

        # Deploy an environment as per the parsed arguments
        if env_id:
            self.deploy_by_id(instance, api_instance, env_id, body)
        elif env_name and env_version:
            self.deploy_by_name_and_version(instance, api_instance, env_name,
                                            env_version, body)
