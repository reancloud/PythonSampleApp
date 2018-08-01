"""List Rules."""
import logging
from cliff.command import Command
from prettytable import PrettyTable
from mnc.parameters_constants import MncConstats
import deploy_sdk_client
from deploy_sdk_client.rest import ApiException
from reanplatform.utility import Utility
from reanplatform.set_header import set_header_parameter
from deploy.constants import DeployConstants


class RuleAvailable(Command):        # noqa: D203.
    """List all the available Manage cloud rules in REAN-Deploy.

    Example: rean-mnc rule-available --all.
    """

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        """get_parser."""
        parser = super(RuleAvailable, self).get_parser(prog_name)
        parser.add_argument('--' + MncConstats.OPTIONAL, MncConstats.OPTIONAL_INITIAL,
                            help='List all the available rules',
                            required=False)
        return parser

    def take_action(self, parsed_args):
        """List Available Rules."""
        try:
            instance = deploy_sdk_client.EnvironmentApi()
            api_instance = set_header_parameter(instance, Utility.get_url(DeployConstants.DEPLOY_URL))
            all_env = api_instance.get_all_environments()
            table = PrettyTable(['Rule Name', 'Description'])
            table.align['Rule Name'] = "l"
            table.align['Description'] = "l"
            for one_env in all_env:
                if one_env.name.endswith('config_rule_setup'):
                    table.add_row([one_env.name.replace('_config_rule_setup', ''), one_env.description])
            logging.info(table)

        except ApiException as exception:
            logging.info("Please try again.")
            Utility.print_exception(exception)
