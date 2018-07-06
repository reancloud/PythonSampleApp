"""Save provider module."""
import logging
from cliff.command import Command
import deploy_sdk_client
import json
from deploy_sdk_client.rest import ApiException
from reanplatform.set_header import set_header_parameter
from prettytable import PrettyTable
from reanplatform.utility import Utility
from deploy.deploy import DepolyEnv


class RuleInstall(Command):
    """Remove rule."""

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        """get_parser."""
        parser = super(RuleInstall, self).get_parser(prog_name)
        parser.add_argument(
            '--rule_name', help='Rule name for installation', required=False)
        parser.add_argument(
            '--rule_type', help='Rule type for installation', required=False)
        parser.add_argument(
            '--customer_acc', help='Customer account number', required=True, type=int)
        parser.add_argument(
            '--deploy_provider', help='REANDeploy provider',  required=False)
        parser.add_argument(
            '--customer_email_to', help='Customer email', required=False)
        parser.add_argument(
            '--customer_email_cc', help='CC customer email',  required=False)
        parser.add_argument(
            '--customer_email_domain', help='Customer email domain',  required=False)
        parser.add_argument(
            '--action', help='Set the action', action="store_true", required=False) 
        return parser

    def take_action(self, parsed_args):
        """take_action."""
        print("hello world....")
        instance = deploy_sdk_client.EnvironmentApi()
        api_instance = set_header_parameter(instance)
            # Get all environments for user
       # all_env = api_instance.get_all_environments()
        print("response ::")
        env_name = parsed_args.rule_name
        env_version = '00.00.01'
        deployment_name = 'default'
        deployment_description = "testinh"
        region = None
        provider_name = None
        input_json = None
        env_id = None
        env_name = None
        env_version = None
        print("self value=======")
        print(self)
        DepolyEnv.deploy_env(self, deployment_name, deployment_description, region,
                   provider_name, input_json, env_id, env_name, env_version)

       