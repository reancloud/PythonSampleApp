"IsEnvironmentExists"
import logging
from pprint import pprint
import swagger_client
from swagger_client.rest import ApiException
from cliff.command import Command
from deploy.constants import Constants


class CheckIfEnvironmentExists(Command):

    "CheckIfEnvironmentExists"
    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(CheckIfEnvironmentExists, self).get_parser(prog_name)
        parser.add_argument('--name', '-n', help='Set name to check existance', required=True)
        return parser

    def take_action(self, parsed_args):

        api_instance = swagger_client.EnvironmentApi()
        api_instance.api_client.set_default_header(
            Constants.AUTHORIZATION,
            Constants.CREDENTIALS
        )
        api_instance.api_client.host = Constants.HOST_PATH
        
        try:
            api_response = api_instance.check_if_environment_exists(parsed_args.name)

            pprint(api_response)
        except ApiException as e:
            self.log.error(e)
