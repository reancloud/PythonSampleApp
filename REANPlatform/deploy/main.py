import sys
from cliff.app import App
from cliff.commandmanager import CommandManager
import time
import deploy_sdk_client
from deploy_sdk_client.rest import ApiException
from pprint import pprint


class Deploy(App):
    def __init__(self):
        super(Deploy, self).__init__(
            description='CLI for REAN Deploy.',
            version='0.1',
            command_manager=CommandManager('rean.deploy'),
            deferred_help=True,
            )

    def initialize_app(self, argv):
        self.LOG.debug('main.Function :: initialize_app')

    def prepare_to_run_command(self, cmd):
        self.LOG.debug('prepare_to_run_command %s', cmd.__class__.__name__)
        self.LOG.debug('Initialize the api_instance in prepare_to_run_command')

    def clean_up(self, cmd, result, err):
        self.LOG.debug('clean_up %s', cmd.__class__.__name__)
        if err:
            self.LOG.debug('got an error: %s', err)


def main(argv=sys.argv[1:]):
    myapp = Deploy()
    return myapp.run(argv)


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
