import logging
from pprint import pprint
from cliff.command import Command
import swagger_client
from swagger_client.rest import ApiException
from deploy.constants import Constants


class GetProviderByName(Command):

    "GetProvider by name"
    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(GetProviderByName, self).get_parser(prog_name)
        parser.add_argument('--name', '-n', help='Set name to check existance', required=True)
        return parser

    def take_action(self, parsed_args):
        try:
            api_instance = swagger_client.ProviderApi()

            api_instance.api_client.set_default_header(
                Constants.AUTHORIZATION,
                Constants.CREDENTIALS
            )
            api_instance.api_client.host = Constants.HOST_PATH

            api_response = api_instance.get_provider_by_name(parsed_args.name)

            pprint(api_response)
        except ApiException as e:
            self.log.error(e)
