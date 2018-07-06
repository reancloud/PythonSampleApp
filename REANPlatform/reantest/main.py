"""Rean-Test main class."""
import sys
from cliff.app import App
from cliff.commandmanager import CommandManager
import time
from pprint import pprint
from reanplatform.constants import Constants

import test_sdk_client
from test_sdk_client.rest import ApiException

from reanplatform.set_header import set_header_parameter

class Test(App):
    """Rean-Deploy CLI."""

    def __init__(self):
        """__init__."""
        super(Test, self).__init__(
            description='CLI for REAN Deploy.',
            version='0.1',
            command_manager=CommandManager('rean.test'),
            deferred_help=True,
            )

    def initialize_app(self, argv):
        """initialize_app."""
        #self.api_instance = test_sdk_client.TestNowUtilityApi()
        # create an instance of the API class
        #api_instance = test_sdk_client.TestNowUtilityApi()

        # Set a relevant user agent so we know which software is actually using ESI
        # api_instance.api_client.set_default_header('Authorization', config.auth_header)
        # api_instance.api_client.host = config.reantest_host # see [1]

        self.LOG.debug('main.Function :: initialize_app')

    def prepare_to_run_command(self, cmd):
        """prepare_to_run_command."""
        self.LOG.debug('prepare_to_run_command %s', cmd.__class__.__name__)

        self.api_instance = test_sdk_client.TestNowUtilityApi()
        set_header_parameter(self.api_instance)

        # self.api_instance.api_client.set_default_header(
        #         Constants.AUTHORIZATION,
        #         Constants.CREDENTIALS
        #     )
        # self.api_instance.api_client.host = Constants.PLATFORM_URL  # see [1]


        self.LOG.debug('Initialize the api_instance in prepare_to_run_command')

    def clean_up(self, cmd, result, err):
        """clean_up."""
        self.LOG.debug('clean_up %s', cmd.__class__.__name__)
        if err:
            self.LOG.debug('got an error: %s', err)


def main(argv=sys.argv[1:]):
    """main."""
    myapp = Test()
    return myapp.run(argv)


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
