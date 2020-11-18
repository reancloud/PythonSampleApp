from cliff import command


class Command(command.Command):
    """A basic command."""

    def take_action(self, parsed_args):
        """Command action."""
        return 'Hello World!'