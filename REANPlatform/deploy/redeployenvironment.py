"""Re-Deploy an Environment."""
import os
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
                            version of same environmen',
                            required=False)
        parser.add_argument('--json_file', '-file',
                            help='Input Json file with full path',
                            required=False)
        parser.add_argument('--json_str', '-json',
                            help='Input Json in a format of string \'{"Key" \
                            : "Value"}\'',
                            required=False)

        return parser

    def take_action(self, parsed_args):
        """take_action."""
        try:
            instance = deploy_sdk_client.EnvironmentApi()
            api_instance = set_header_parameter(instance)
            body = deploy_sdk_client.DeploymentConfiguration(
                deployment_name=parsed_args.deployment_name,
                deployment_description=parsed_args.deployment_description,
                region=parsed_args.region,
                provider_name=parsed_args.provider_name,
                input_json=parsed_args.json_str
            )
            if parsed_args.env_name and parsed_args.env_version:
                api_response = api_instance.re_deploy(
                    parsed_args.env_name,
                    parsed_args.env_version,
                    body=body
                )
                print(api_response)
            if parsed_args.deployment_id:
                api_response= api_instance.re_deploy_0(
                    parsed_args.deployment_id,
                    body=body
                )
                print(api_response)
        except ApiException as e:
            Utility.print_exception(e)
