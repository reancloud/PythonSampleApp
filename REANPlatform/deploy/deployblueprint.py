import os
from pprint import pprint
import logging
from cliff.command import Command
import deploy_sdk_client
from deploy_sdk_client.rest import ApiException
from reanplatform.set_header import set_header_parameter
from reanplatform.utility import Utility


class DeployBlueprint(Command):
    """Depoly Environment As Blueprint ."""
    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        """get_parser."""
        # Define parser
        parser = super(DeployBlueprint, self).get_parser(prog_name)

        parser.add_argument('--env_name', '-ename',
                            help='Environment name',
                            required=False)
        parser.add_argument('--env_version', '-env_v',
                            help='Environment version',
                            required=False)
        parser.add_argument('--deployment_name', '-dname', default='default',
                            help='Deployment Name',
                            required=False)
        parser.add_argument('--env_id', '-id',
                            help='environment id',
                            required=True)
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
                            help='Input Json File With Full Path',
                            required=False)

        return parser

    def take_action(self, parsed_args):
        """take_action."""
        try:
            instance = deploy_sdk_client.EnvironmentApi()
            api_instance = set_header_parameter(instance)  
            body = deploy_sdk_client.DeploymentConfiguration(environment_id=parsed_args.env_id, deployment_name=parsed_args.deployment_name, deployment_description=parsed_args.deployment_description, region=parsed_args.region, provider_name=parsed_args.provider_name, input_json='{\"Key\" : \"Value\"}')
            api_response = api_instance.deploy_as_blueprint(parsed_args.env_id)
            pprint(api_response) 
        except ApiException as e:
            Utility.print_exception(e)
