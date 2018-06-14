"""Depoly/Re-Deploy an Environment."""
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


class DepolyEnv(Command):
    """Redeploy an environment by name and version."""

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        """get_parser."""
        parser = super(DepolyEnv, self).get_parser(prog_name)
        parser.add_argument('--env_id', '-id',
                            help='Environment id',
                            required=True)
        parser.add_argument('--deployment_name', '-dname', default='default',
                            help='Deployment Name. Please provide this \
                            attribute if deployment name is not default.',
                            required=False)
        parser.add_argument('--deployment_description', '-desc',
                            help='Description of deployment',
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
        parser.add_argument('--json_file', '-json',
                            help='Pass input variable json file with \
                            full path',
                            required=False)

        return parser

    @staticmethod
    def pass_json_as_object(json_file):
        """Convert Json to String."""
        try:
            # check file exists
            if os.path.isfile(json_file) is False:
                print('File not found: ' + json_file)

            # get a file object and read it in as a string
            with open(json_file) as jsonfile:
                json_obj = json.load(jsonfile)
            return json_obj
        except ApiException as e:
            Utility.print_exception(e)

    @staticmethod
    def re_deploy_environment(environment_id, deployment_name,
                              deployment_description, env_version_id,
                              provider_name, input_json, region):
        """Redeploy An Environment."""
        try:
            # Initialise instance and api_instance
            instance = deploy_sdk_client.EnvironmentApi()
            api_instance = set_header_parameter(instance)
            body = deploy_sdk_client.DeploymentConfiguration(
                environment_id=environment_id,
                deployment_name=deployment_name,
                deployment_description=deployment_description,
                env_version_id=env_version_id,
                region=region,
                provider_name=provider_name,
                input_json=input_json
            )
            api_response = api_instance.deploy_1(
                body=body
            )
            print(api_response)
        except ApiException as e:
            Utility.print_exception(e)

    def take_action(self, parsed_args):
        """take_action."""
        # Define parsed_args
        environment_id = parsed_args.env_id
        deployment_name = parsed_args.deployment_name
        deployment_description = parsed_args.deployment_description
        env_version_id= parsed_args.env_version_id
        region = parsed_args.region
        json_file = parsed_args.json_file
        provider_name = parsed_args.provider_name
        input_json = None

        input_json = DepolyEnv.pass_json_as_object(json_file)
        print(input_json)

        # Re Deploy an environment
        DepolyEnv.re_deploy_environment(environment_id, deployment_name,
                                        deployment_description, env_version_id,
                                        provider_name, input_json, region)
