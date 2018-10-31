"""List Rules."""
import logging
from prettytable import PrettyTable
from cliff.command import Command
import deploy_sdk_client
from deploy_sdk_client.rest import ApiException
from reanplatform.utility import Utility
from reanplatform.set_header import set_header_parameter
from deploy.constants import DeployConstants
from deploy.utility import DeployUtility


class RuleAvailable(Command):
    """List all the available manage cloud rules in REAN-Deploy. Example: rean-mnc available-rules."""
    # noqa: C0303
    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        """get_parser."""
        parser = super(RuleAvailable, self).get_parser(prog_name)
        return parser

    def take_action(self, parsed_args):
        """List Available Rules."""
        try:
            api_client = set_header_parameter(DeployUtility.create_api_client(), Utility.get_url(DeployConstants.DEPLOY_URL))
            instance = deploy_sdk_client.EnvironmentApi(api_client)
            all_env = instance.get_all_environments()
            table = PrettyTable(['Rule Name', 'Description'])
            table.align['Rule Name'] = "l"
            table.align['Description'] = "l"
            for one_env in all_env:
                if one_env.name.endswith('config_rule_setup'):
                    rule = self.is_rule(all_env, one_env.name.replace('_config_rule_setup', ''))
                    if rule:
                        table.add_row([one_env.name.replace('_config_rule_setup', ''), one_env.description])
                        logging.info(table)

        except ApiException as exception:
            logging.info("Please try again.")
            Utility.print_exception(exception)

    def is_rule(self, all_env, rule_name):
        """Check if manage cloud rule or not."""
        rule = False
        if rule_name + '_assume_role' in str(all_env):
            rule = True
        return rule
