import os
import logging
from cliff.command import Command
import deploy_sdk_client
from pprint import pprint
from deploy.constants import Constants
from deploy_sdk_client.rest import ApiException
from reanplatform.set_header import set_header_parameter
from reanplatform.utility import Utility


class DepolyEnv(Command):

    "DepolyEnv"
    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(DepolyEnv, self).get_parser(prog_name)
        parser.add_argument('--env_id', '-id', help='Environment ID to deploy', required=True)
        parser.add_argument('--deployment_name', '-n', default="default",
                                help='Environment name to deploy',
                                required=False)
        return parser

    def take_action(self, parsed_args):
        try:
            env_api_instance = deploy_sdk_client.EnvironmentApi()
            api_instance = set_header_parameter(env_api_instance)

            body = deploy_sdk_client.DeploymentConfiguration(environment_id=parsed_args.env_id)  # DeploymentConfiguration |  (optional)
            api_response = api_instance.deploy_as_blueprint(parsed_args.env_id)
            print(api_response)
            try:
                env_result = api_instance.get_deploy_status(parsed_args.env_id, parsed_args.deployment_name)
                pprint("Blueprint status is " + env_result.status)
            except:
                print("Your Environment is not yet deployed")
        except ApiException as e:
            print("Exception when calling EnvironmentApi->deploy: %s\n" % e)