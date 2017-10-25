import logging
from pprint import pprint
from cliff.command import Command
import swagger_client
from swagger_client.rest import ApiException
from reandeploy.constants import Constants


class GetALLVMConnections(Command):

    "GetALLVMConnections"
    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(GetALLVMConnections, self).get_parser(prog_name)

        return parser

    def take_action(self, parsed_args):
        try:
            api_instance = swagger_client.ConnectionApi()

            api_instance.api_client.set_default_header(
                Constants.AUTHORIZATION,
                Constants.CREDENTIALS
            )
            api_instance.api_client.host = Constants.HOST_PATH

            api_response = api_instance.get_all_vm_connections()

            pprint(api_response)
        except ApiException as e:
            self.log.error(e)


class Error(Command):
    "Always raises an error"

    log = logging.getLogger(__name__)

    def take_action(self, parsed_args):
        self.log.info('causing error')
        raise RuntimeError('this is the expected exception')
