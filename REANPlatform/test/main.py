import sys

from cliff.app import App
from cliff.commandmanager import CommandManager
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint
from . import config



class Test(App):

    def __init__(self):
        super(Test, self).__init__(
            description='CLI for REAN Test.',
            version='0.1',
            command_manager=CommandManager('rean.test'),
            deferred_help=True,
            )

    def initialize_app(self, argv):
        # create an instance of the API class
        # api_instance = swagger_client.TestNowUtilityApi()

        # Set a relevant user agent so we know which software is actually using ESI
        # api_instance.api_client.set_default_header('Authorization', config.auth_header)
        # api_instance.api_client.host = config.reantest_host # see [1]

        self.LOG.debug('main.Function :: initialize_app')

    def prepare_to_run_command(self, cmd):
        self.LOG.debug('prepare_to_run_command %s', cmd.__class__.__name__)
        self.LOG.debug('Initialize the api_instance in prepare_to_run_command')

        self.api_instance = swagger_client.TestNowUtilityApi()
        self.api_instance.api_client.set_default_header('Authorization', config.auth_header)
        self.api_instance.api_client.host = config.host  # see [1]

    def clean_up(self, cmd, result, err):
        self.LOG.debug('clean_up %s', cmd.__class__.__name__)
        if err:
            self.LOG.debug('got an error: %s', err)


def main(argv=sys.argv[1:]):
    myapp = Test()
    return myapp.run(argv)


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
