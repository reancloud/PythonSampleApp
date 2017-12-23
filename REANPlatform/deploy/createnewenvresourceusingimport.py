"CreateNewEnvResourceUsingImport"
import logging
from pprint import pprint
import swagger_client
from swagger_client.rest import ApiException
from cliff.command import Command
from deploy.constants import Constants


class CreateNewEnvResourceUsingImport(Command):

    "CheckIfEnvironmentExists"
    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(CreateNewEnvResourceUsingImport, self).get_parser(prog_name)
        parser.add_argument('--envid', '-id', help='Set id to import environment', required=True)
        return parser

    def take_action(self, parsed_args):
        api_instance = swagger_client.EnvironmentApi()

        api_instance.api_client.set_default_header(
            Constants.AUTHORIZATION,
            Constants.CREDENTIALS
        )
        api_instance.api_client.host = Constants.HOST_PATH

        try:
            api_response = api_instance.create_new_env_resource_using_import(env_id=parsed_args.envid)
            pprint(api_response)
        except ApiException as e:
            self.log.error(e)
