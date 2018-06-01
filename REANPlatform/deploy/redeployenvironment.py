import os
import logging
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
                            help='Environment name',
                            required=True)
        parser.add_argument('--env_version', '-env_v',
                            help='Environment version',
                            required=True)
        parser.add_argument('--deployment_name', '-dname', default='default',
                            help='Deployment Name',
                            required=False)
        parser.add_argument('--env_id', '-id',
                            help='environment id',
                            required=False)
        parser.add_argument('--deployment_description', '-desc',
                            help='deployment Description',
                            required=False)
        parser.add_argument('--provider_name', '-pname',
                            help='provider Name',
                            required=False)
        parser.add_argument('--region', '-region',
                            help='Region Name',
                            required=False)
        parser.add_argument('--env_version_id', '-env-ver-id',
                            help='Environment Version ID',
                            required=False)
        parser.add_argument('--input_json', '-json',
                            help='Input Json in a format of string \'{"Key" : "Value"}\'',
                            required=False)

        return parser

    def take_action(self, parsed_args):
        """take_action."""
        try:
            api_instance = deploy_sdk_client.EnvironmentApi()
            env_api_instance = set_header_parameter(api_instance)
            body = deploy_sdk_client.DeploymentConfiguration(environment_id=parsed_args.env_id, deployment_name=parsed_args.deployment_name, deployment_description=parsed_args.deployment_description, region=parsed_args.region, provider_name=parsed_args.provider_name, input_json=parsed_args.input_json)
            api_response = api_instance.re_deploy(parsed_args.env_name, parsed_args.env_version, body=body)
            print(api_response)
        except ApiException as e:
            Utility.print_exception(e)
