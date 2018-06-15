import logging
from cliff.command import Command
from 


class RuleInstall(Command):
    log = logging.getLogger(__name__)

    "Rule Install"

    def get_parser(self, prog_name):
        parser = super(RuleInstall, self).get_parser(prog_name)
        parser.add_argument('--rule_name', '-name',
                            help='Set the rule name for installation',
                            required=True)
        parser.add_argument('--rule_type', '-type',
                            help='Set the rule type for installation',
                            required=False)
        parser.add_argument('--customer_acc', '-acc',
                            help='Set the customer account number',
                            required=True, type=int)
        parser.add_argument('--deploy-provider', '-p',
                            help='Set the REANDeploy provider for customer',
                            required=False)
        parser.add_argument('--customer_email_to', '-email_to',
                            help='Set the TO customer email',
                            required=False)
        parser.add_argument('--customer-email-cc', '-email_cc',
                            help='Set the CC customer email',
                            required=False)
        parser.add_argument('--customer-email-domain', '-email_domain',
                            help='Set the customer email domain',
                            required=False)
        parser.add_argument('--action',
                            help='Set the action',
                            required=False)

        return parser

    def take_action(self, parsed_args):
        return True
