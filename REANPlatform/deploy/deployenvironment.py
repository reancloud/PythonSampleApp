import os
from pprint import pprint
import logging
from cliff.command import Command
from . import utility
import swagger_client
from swagger_client.rest import ApiException
from deploy.constants import Constants


class DepolyEnv(Command):

    "DepolyEnv"
    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(DepolyEnv, self).get_parser(prog_name)
        parser.add_argument('--env_id', '-id', help='Environment ID to deploy', required=True)
        return parser

    def take_action(self, parsed_args):
        # create an instance of the API class
        api_instance = swagger_client.EnvironmentApi()

        api_instance.api_client.set_default_header(
            Constants.AUTHORIZATION,
            Constants.CREDENTIALS
        )
        api_instance.api_client.host = Constants.HOST_PATH
        try:
            body = swagger_client.DeploymentConfiguration(environment_id=parsed_args.env_id)  # DeploymentConfiguration |  (optional)
            api_response = api_instance.deploy(parsed_args.env_id, body=body)
            pprint(api_response)
        except ApiException as e:
            print("Exception when calling EnvironmentApi->deploy: %s\n" % e)
