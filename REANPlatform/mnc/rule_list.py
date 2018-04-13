import logging
import json
from cliff.command import Command


class RuleList(Command):
    log = logging.getLogger(__name__)

    "Rule"

    def get_parser(self, prog_name):
        parser = super(RuleList, self).get_parser(prog_name)

        parser.add_argument(
            '--rule-name', help='Set the rule name', action="append", required=False)
        parser.add_argument(
            '--rule-type', help='Set the rule type', action="append", required=False)
        parser.add_argument(
            '--customer-acc', help='Set the customer account number', action="store", required=False, type=int)

        return parser

    def take_action(self, parsed_args):
        return True
