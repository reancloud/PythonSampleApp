"""Re-Deploy an Environment."""
import os
import re
import os.path
import logging
import json
from cliff.command import Command
import deploy_sdk_client
from deploy_sdk_client.rest import ApiException
from reanplatform.set_header import set_header_parameter
from reanplatform.utility import Utility


class ReDepoly(Command):
    """Redeploy an environment by name and version."""

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        """get_parser."""
        parser = super(ReDepoly, self).get_parser(prog_name)
        parser.add_argument('--env_name', '-ename',
                            help='Environment name. This parameter is not \
                            required when deploymentId is specified',
                            required=False)
        parser.add_argument('--env_version', '-env_v',
                            help='Environment version. This parameter is \
                            not required when deploymentId is specified',
                            required=False)
        parser.add_argument('--deployment_id', '-id',
                            help='Deployment id',
                            required=False)
        parser.add_argument('--deployment_name', '-dname', default='default',
                            help='Deployment Name',
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
                            help='Please provide this attribute only if you \
                            want to upgrade existing deployment with newer \
                            version of an environment. A value should be the \
                            version of same environment',
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

    def validate(self, env_name, env_version,
                 deployment_id, json_file, json_str):
        """Validate Parsed Arguments."""
        if env_name and env_version and deployment_id:
            message = "Please Provide either Deployment ID or Environment \
            Name and Version."
            exception_msg = re.sub(' +', ' ', message)
            raise Exception(exception_msg)
        elif env_version and deployment_id:
            message = "Please Provide either Deployment ID or Environment \
            Name and Version. Do Not Provide Environment Version and \
            Deployment ID Both."
            exception_msg = re.sub(' +', ' ', message)
            raise Exception(exception_msg)
        elif env_name and deployment_id:
            message = "Please Provide either Deployment ID or Environment \
            Name and Version. Do Not Provide Environment Name and \
            Deployment ID Both."
            exception_msg = re.sub(' +', ' ', message)
            raise Exception(exception_msg)
        if json_file and json_str:
            message = "Please provide Input Variable json either in the \
            form of file or in the form if string."
            exception_msg = re.sub(' +', ' ', message)
            raise Exception(exception_msg)

    def convert_json_to_string(self, json_file):
        """Convert Json to String."""
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

    def re_deploy_environment(self, instance, api_instance, env_name,
                              env_version, deployment_id, json_str,
                              input_json, deployment_description, region,
                              provider_name, deployment_name):
        """Redeploy An Environment."""
        try:
            body = deploy_sdk_client.DeploymentConfiguration(
                deployment_name=deployment_name,
                deployment_description=deployment_description,
                region=region,
                provider_name=provider_name,
                input_json=input_json
            )
            if env_name and env_version:
                api_response = api_instance.re_deploy(
                    env_name,
                    env_version,
                    body=body
                )
                print(api_response)
            if deployment_id:
                api_response = api_instance.re_deploy_0(
                    deployment_id,
                    body=body
                )
                print(api_response)
        except ApiException as e:
            Utility.print_exception(e)

    def take_action(self, parsed_args):
        """take_action."""
        # Define parsed_args
        env_name = parsed_args.env_name
        env_version = parsed_args.env_version
        deployment_name = parsed_args.deployment_name
        deployment_id = parsed_args.deployment_id
        deployment_description = parsed_args.deployment_description
        region = parsed_args.region
        json_file = parsed_args.json_file
        json_str = parsed_args.json_str
        provider_name = parsed_args.provider_name

        # Define an instance for REAN Deploy API
        instance = deploy_sdk_client.EnvironmentApi()
        api_instance = set_header_parameter(instance)

        # Validate parsed agruments
        self.validate(env_name, env_version, deployment_id,
                      json_file, json_str)

        # Set json format
        if json_str:
            input_json = json_str
        elif json_file:
            input_json = self.convert_json_to_string(json_file)

        # Re Deploy an environment
        self.re_deploy_environment(instance, api_instance, env_name,
                                   env_version, deployment_id, json_str,
                                   input_json, deployment_description, region,
                                   provider_name, deployment_name)
