"""Configure platform."""
from cliff.command import Command


class HelpDeploy(Command):
    """Details of rean-deploy cli."""

    def get_parser(self, prog_name):
        """get_parser."""
    def take_action(self, parsed_args):
        """take_action."""


class HelpTest(Command):
    """Details of rean-test cli."""

    def get_parser(self, prog_name):
        """get_parser."""
    def take_action(self, parsed_args):
        """take_action."""


class HelpMnc(Command):
    """Details of rean-mnc cli."""

    def get_parser(self, prog_name):
        """get_parser."""
    def take_action(self, parsed_args):
        """take_action."""


class HelpAuth(Command):
    """Details of rean-auth cli."""

    def get_parser(self, prog_name):
        """get_parser."""
    def take_action(self, parsed_args):
        """take_action."""
