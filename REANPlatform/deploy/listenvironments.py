"""List environment module."""
import logging
from prettytable import PrettyTable
from cliff.command import Command
import deploy_sdk_client
from deploy_sdk_client.rest import ApiException
from reanplatform.set_header import set_header_parameter
from reanplatform.utility import Utility
from reanplatform.utilityconstants import PlatformConstants
from deploy.constants import DeployConstants
from deploy.utility import DeployUtility


class ListEnvironments(Command):
    """List Environments."""

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        """get_parser."""
        parser = super(ListEnvironments, self).get_parser(prog_name)
        parser.add_argument('--format', '-f',
                            help='Allowed values are: [json, table]',
                            type=str, default='json',
                            nargs='?',
                            required=False)
        parser.add_argument('--output', '-o',
                            help="Write output to <file> instead of stdout.",
                            required=False
                           )
        return parser

    @staticmethod
    def list_environment(output_format, parsed_args):
        """List Environment."""
        try:
            # Initialise instance and api_instance in list_environment
            api_client = set_header_parameter(DeployUtility.create_api_client(), Utility.get_url(DeployConstants.DEPLOY_URL))
            instance = deploy_sdk_client.EnvironmentApi(api_client)
            # Get all environments for user
            api_response = instance.get_all_environments()
            if output_format == 'table':
                table = PrettyTable(['Name', 'Id', 'Region', 'Version'])
                table.padding_width = 1
                for environment in api_response:
                    table.add_row(
                        [
                            environment.name,
                            environment.id,
                            environment.region,
                            environment.env_version
                        ]
                    )
                Utility.print_output("Environment list \n{}".format(table), parsed_args.output, PlatformConstants.TABLE_REFERENCE)
            elif output_format == 'json' or output_format == '':
                Utility.print_output(api_response, parsed_args.output)
            else:
                raise RuntimeError("Please specify correct format, Allowed values are: [json, table]")
        except ApiException as api_exception:
            Utility.print_exception(api_exception)

    def take_action(self, parsed_args):
        """take_action of ListEnvironment."""
        # Define parsed argument
        output_format = parsed_args.format

        # List Environments
        ListEnvironments.list_environment(output_format, parsed_args)
