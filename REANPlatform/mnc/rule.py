import logging
from cliff.command import Command


class Rule(Command):
    log = logging.getLogger(__name__)

    "Rule"

    def get_parser(self, prog_name):
        parser = super(Rule, self).get_parser(prog_name)
        subparser = parser.add_subparsers()

        subparser.add_parser('install', help='Installation of Managed Cloud rules from customer account')
        subparser.add_parser('remove', help='Removal of Managed Cloud rules from customer account')
        subparser.add_parser('list', help='Lits Managed Cloud rules')

        parser.print_help()
        return parser

    def take_action(self, parsed_args):
        return True
