import logging
from cliff.command import Command


class RuleRemove(Command):
    log = logging.getLogger(__name__)

    "Rule Remove"

    def get_parser(self, prog_name):
        parser = super(RuleRemove, self).get_parser(prog_name)

        parser.add_argument(
            '--rule-name', help='Set the rule name for removal', action="append", nargs='*', required=False)
        parser.add_argument(
            '--rule-type', help='Set the rule type for removal', action="append", nargs='*', required=False)
        parser.add_argument(
            '--customer-acc', help='Set the customer account number', action="store", required=True, type=int)
        parser.add_argument(
            '--force-yes', help='Set the rule type for removal', action="store_true", required=False)

        return parser

    def take_action(self, parsed_args):
        return True
