"""List environment module."""
import logging
from cliff.command import Command
import deploy_sdk_client
import json
from deploy_sdk_client.rest import ApiException
from reanplatform.set_header import set_header_parameter
from prettytable import PrettyTable
from reanplatform.utility import Utility

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
        return parser

    def take_action(self, parsed_args):
        """take_action of ListEnvironment."""
        try:
            # create an instance of the API class 
            environment_api_instance = deploy_sdk_client.EnvironmentApi()
            api_instance = set_header_parameter(environment_api_instance)

            # Get all environments for user
            api_response = api_instance.get_all_environments()
            if parsed_args.format == 'table':
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
                print("Environment list ::\n%s" % (table))

            elif parsed_args.format == 'json' or parsed_args.format == '':
                print(
                        json.dumps(
                                api_response,
                                default=lambda o: o.__dict__,
                                sort_keys=True, indent=4
                                ).replace("\"_", '"')
                    )
            else:
                raise RuntimeError("Please specify correct fromate, Allowed \
                        values are: [json, table]")
        except ApiException as e:
            Utility.print_exception(e)