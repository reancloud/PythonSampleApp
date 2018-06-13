"""List Rules."""
import logging
from pprint import pprint
from cliff.command import Command
import deploy_sdk_client
import json
from deploy_sdk_client.rest import ApiException
from reanplatform.set_header import set_header_parameter
from prettytable import PrettyTable
from reanplatform.utility import Utility


class RuleList(Command):
    """List Manage Cloud Rules."""

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        """get_parser."""
        parser = super(RuleList, self).get_parser(prog_name)
        parser.add_argument('--rule_name', '-rule_name',
                            help='Set the rule name',
                            required=False)
        parser.add_argument('--rule_type', '-rule_type',
                            help='Set the rule type',
                            required=False)
        parser.add_argument('--customer_acc', '-customer_acc',
                            help='Set the customer account number',
                            required=False)
        return parser

    @staticmethod
    def list_environment(parsed_args):
        """List Environment."""
        rule_name = parsed_args.rule_name
        rule_type = parsed_args.rule_type
        customer_acc = parsed_args.customer_acc
        try:
            # Initialise instance and api_instance in list_environment
            instance = deploy_sdk_client.EnvironmentApi()
            api_instance = set_header_parameter(instance)

            # Get all environments for user
            api_response = api_instance.get_all_environments()

            table = PrettyTable(['Name', 'Description'])
            table.padding_width = 0
            # Define list for Environment ID's
            env_ids = []

            # Get all envrionment ID's
            for environment in api_response:
                print(environment.name)
                if "_config_rule" in environment.name:
                    env_ids.append(environment.id)

            # For each environment, Print deployment name matched with
            # Parsed arguments
            for id in env_ids:
                res = api_instance.get_all_deployments_for_environment_by_id(
                    id
                )
                for obj in res:
                    if (customer_acc or rule_name) in obj.deployment_name:
                        table.add_row(
                            [
                                obj.environment.name,
                                obj.environment.description,
                            ]
                        )
                    else:
                        return
            return table

        except ApiException as e:
            Utility.print_exception(e)

    def take_action(self, parsed_args):
        """Take action."""
        env_list = RuleList.list_environment(parsed_args)
        if env_list is not None:
            print("Environment list ::\n%s" % (env_list))
