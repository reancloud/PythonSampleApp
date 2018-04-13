import logging
from cliff.command import Command


class RuleInstall(Command):
    log = logging.getLogger(__name__)

    "Rule Install"

    def get_parser(self, prog_name):
        parser = super(RuleInstall, self).get_parser(prog_name)

        parser.add_argument(
            '--rule-name', help='Set the rule name for installation', action="append", nargs='*', required=False)
        parser.add_argument(
            '--rule-type', help='Set the rule type for installation', action="append", nargs='*', required=False)
        parser.add_argument(
            '--customer-acc', help='Set the customer account number', action="store", required=True, type=int)
        parser.add_argument(
            '--deploy-provider', help='Set the REANDeploy provider for customer', action="store", required=False)
        parser.add_argument(
            '--customer-email-to', help='Set the TO customer email', action="append", nargs='*', required=False)
        parser.add_argument(
            '--customer-email-cc', help='Set the CC customer email', action="append", nargs='*', required=False)
        parser.add_argument(
            '--customer-email-domain', help='Set the customer email domain', action="store", required=False)
        parser.add_argument(
            '--action', help='Set the action', action="store_true", required=False)

        return parser

    def take_action(self, parsed_args):
        return True
