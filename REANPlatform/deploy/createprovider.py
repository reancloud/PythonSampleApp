"""Save provider module."""
import os
import json
import logging
from cliff.command import Command
import deploy_sdk_client
from deploy_sdk_client.rest import ApiException
from reanplatform.set_header import set_header_parameter
from reanplatform.utility import Utility
from deploy.constants import DeployConstants


class SaveProvider(Command):
    """Save provider."""

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        """get_parser."""
        parser = super(SaveProvider, self).get_parser(prog_name)
        parser.add_argument('--name', '-n', help='Provider name', required=True)
        parser.add_argument('--type', '-t', help='Provider type', required=True)
        parser.add_argument('--provider_details', '-f', help='Json file with applicable key-value pair for provider type. File absolute path', required=True)
        return parser

    def take_action(self, parsed_args):
        """take_action."""
        prov_name = parsed_args.name
        prov_type = parsed_args.type
        provider_details = parsed_args.provider_details

        SaveProvider.create_provider(prov_name, prov_type, provider_details)

    @staticmethod
    def create_provider(prov_name, prov_type, provider_details):
        """create_provider."""
        api_client = set_header_parameter(Utility.create_api_client(), Utility.get_url(DeployConstants.DEPLOY_URL))
        api_instance = deploy_sdk_client.ProviderApi(api_client)
        try:
            file_path = provider_details

            if not os.path.isfile(file_path):
                raise RuntimeError('Provider details file %s does not exists' % file_path)

            # Parse parameters
            with open(file_path, "r") as handle:
                filedata = handle.read()

            jsondata = json.loads(filedata)
            provider = deploy_sdk_client.SaveProvider(
                name=prov_name,
                type=prov_type,
                json=jsondata
            )
            api_response = api_instance.save_provider(provider)
            print("Provider created successfully :%s, id: %s" % (api_response.name, api_response.id))
        except ApiException as api_exception:
            Utility.print_exception(api_exception)
