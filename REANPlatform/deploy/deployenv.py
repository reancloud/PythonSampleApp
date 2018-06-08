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
            parser.add_argument('--json_file', '-j-file',
                                help='Pass input variable json file with \
                                full path',
                                required=False)
            parser.add_argument('--json_str', '-j-str',
                                help='Pass input variables in a string \
                                like \'{"Key": "Value"}\'',
                                required=False)

            return parser
        except ApiException as e:
            Utility.print_exception(e)

    def validate(self, env_id, env_name, env_version, json_file, json_str):
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
        if json_file and json_str:
            message = "Please provide Input Variable json either in the \
            form of file or in the form if string."
            exception_msg = re.sub(' +', ' ', message)
            raise Exception(exception_msg)

    def convert_json_to_string(self, json_file):
        """Convert Json into String."""
        try:
            # check file exists
            if os.path.isfile(json_file) is False:
                print('File not found: ' + json_file)

            # get a file object and read it in as a string
            fileobj = open(json_file)
            jsonstr = fileobj.read()
            fileobj.close()
            return jsonstr

        except ApiException as e:
            Utility.print_exception(e)

    def deploy_env(self, deployment_name, deployment_description, region,
                   provider_name, input_json, env_id, env_name, env_version):
        """Deploy Environment."""
        # Initialise instance and api_instance
        instance = deploy_sdk_client.EnvironmentApi()
        api_instance = set_header_parameter(instance)
        # Prepare deployment configuration body
        body = deploy_sdk_client.DeploymentConfiguration(
            deployment_name=deployment_name,
            deployment_description=deployment_description,
            region=region,
            provider_name=provider_name,
            input_json=input_json
        )
        # Deploy Environment By ID
        if env_id:
            try:
                api_response = api_instance.deploy(env_id, body=body)
                pprint(api_response)
            except ApiException as e:
                Utility.print_exception(e)
        # Deploy Environment By Name And Version
        elif env_name and env_version:
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
        # Define parsed arguments
        env_id = parsed_args.env_id
        deployment_name = parsed_args.deployment_name
        deployment_description = parsed_args.deployment_description
        region = parsed_args.region
        provider_name = parsed_args.provider_name
        json_file = parsed_args.json_file
        json_str = parsed_args.json_str
        env_name = parsed_args.env_name
        env_version = parsed_args.env_version

        # Valiate parsed arguments
        self.validate(env_id, env_name, env_version, json_file, json_str)

        # Set json format
        if json_str:
            input_json = json_str
        elif json_file:
            input_json = self.convert_json_to_string(json_file)

        self.deploy_env(deployment_name, deployment_description, region,
                        provider_name, input_json, env_id, env_name,
                        env_version)
