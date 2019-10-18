"""Get Provider module."""
import re
import logging
from cliff.command import Command
import deploy_sdk_client
from deploy_sdk_client.rest import ApiException
from reanplatform.set_header import set_header_parameter
from reanplatform.utility import Utility
from deploy.constants import DeployConstants
from deploy.utility import DeployUtility


class GetProvider(Command):
    """Get Provider."""

    log = logging.getLogger(__name__)

    # EPILog will get print after commands
    _epilog = 'Example : rean-deploy get-provider --provider_name dummyProvider'

    def get_parser(self, prog_name):
        """get_parser."""
        parser = super(GetProvider, self).get_parser(prog_name)
        parser.add_argument('--provider_id', '-i', help='Provider id. This parameter is not required when --provider_name is specified', required=False)
        parser.add_argument('--provider_name', '-n', help='Provider name. This parameter is not required when --provider_id is specified', required=False)
        parser.add_argument('--output', '-o', help="Write output to <file> instead of stdout.", required=False)
        return parser

    @staticmethod
    def validate_parameters(provider_id, provider_name):
        """validate_parameters."""
        exception_msg = "Specify either --provider_id OR --provider_name"
        if (provider_id is None and provider_name is None) or (provider_id is not None and provider_name is not None):
            raise RuntimeError(re.sub(' +', ' ', exception_msg))

    def take_action(self, parsed_args):
        """take_action."""
        # Define parsed argument
        provider_id = parsed_args.provider_id
        provider_name = parsed_args.provider_name
        GetProvider.validate_parameters(provider_id, provider_name)
        # Initialise provider_response
        provider_response = None
        try:
            # Initialise api_client and api_instance
            api_client = set_header_parameter(DeployUtility.create_api_client(), Utility.get_url(DeployConstants.DEPLOY_URL))
            api_instance = deploy_sdk_client.ProviderApi(api_client)
            if provider_id:
                provider_response = api_instance.get_provider(provider_id)
            else:
                provider_response = api_instance.get_provider_by_name(provider_name)
            if provider_response:
                if parsed_args.output is not None:
                    Utility.print_output_as_dict(provider_response, parsed_args.output)
                else:
                    print(Utility.get_parsed_json(provider_response))
        except ApiException as api_exception:
            Utility.print_exception(api_exception)
