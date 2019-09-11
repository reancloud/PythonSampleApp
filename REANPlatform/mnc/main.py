"""Rean-MNC main class."""
import sys
from cliff.app import App
from cliff.commandmanager import CommandManager


class MNC(App):            # noqa: D203
    """Rean-MNC CLI."""

    def __init__(self):
        """__init__."""
        super(MNC, self).__init__(
            description='CLI for REAN Managed Cloud',
            version='2.17.0',
            command_manager=CommandManager('rean.mnc'),
            deferred_help=True,
        )

    def initialize_app(self, argv):
        """initialize_app."""
        self.LOG.debug('main.Function :: initialize_app')

    def prepare_to_run_command(self, cmd):
        """prepare_to_run_command."""
        self.LOG.debug('prepare_to_run_command %s', cmd.__class__.__name__)
        self.LOG.debug('Initialize the api_instance in prepare_to_run_command')

    def clean_up(self, cmd, result, err):
        """clean_up."""
        self.LOG.debug('clean_up %s', cmd.__class__.__name__)
        if err:
            self.LOG.debug('got an error: %s', err)


def main(argv=sys.argv[1:]):
    """main."""
    mnc = MNC()
    return mnc.run(argv)


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
