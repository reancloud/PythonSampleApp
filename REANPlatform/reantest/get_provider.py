"""Get provider."""
import re
import logging
from cliff.command import Command
from reantest.utility import Utility

import test_sdk_client
from test_sdk_client.rest import ApiException


class GetProvider(Command):
    """Get provider."""

    log = logging.getLogger(__name__)
    _epilog = 'Example : \n\t rean-test get-provider --name <provider_name>'

    def get_parser(self, prog_name):
        """get_parser."""
        parser = super(GetProvider, self).get_parser(prog_name)

        parser.add_argument('--name', '-n', help='Provider name. This parameter is not required when --id is specified',
                            required=False)
        parser.add_argument('--id', '-i', help='Provider id. This parameter is not required when --name is specified',
                            required=False)
        return parser

    @staticmethod
    def validate_parameters(parsed_args):
        """validate_parameters."""
        exception_msg = "Specify either --id OR --name"
        if parsed_args.id and parsed_args.name:
            raise RuntimeError(re.sub(' +', ' ', exception_msg))

        if parsed_args.id is None and parsed_args.name is None:
            raise RuntimeError(re.sub(' +', ' ', exception_msg))

    def take_action(self, parsed_args):
        """take_action."""
        # Initialise instance and api_instance

        api_instance = test_sdk_client.ProviderApi(Utility.set_headers())

        try:
            if parsed_args.name:
                api_response = api_instance.get_provider_by_name(parsed_args.name)
            else:
                api_response = api_instance.get_provider(parsed_args.id)

            print(api_response)

        except ApiException as exception:
            Utility.print_exception(exception)
