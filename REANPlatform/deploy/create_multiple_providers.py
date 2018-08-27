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
from deploy.utility import DeployUtility

class CreateMultipleProviders(Command):
    """Save Multiple providers."""

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        """get_parser."""
        parser = super(CreateMultipleProviders, self).get_parser(prog_name)
        parser.add_argument('--name', '-n', help='Provider name',
                            required=True)
        parser.add_argument('--type', '-t', help='Provider type',
                            required=True)
        parser.add_argument('--provider_details', '-f',
                            help='Json file with applicable key-value pair \
                            for provider type. File absolute path',
                            required=True
                           )
        return parser

    def take_action(self, parsed_args):
        """take_action."""
        prov_name = parsed_args.name
        prov_type = parsed_args.type
        provider_details = parsed_args.provider_details

        CreateMultipleProviders.create_provider(prov_name, prov_type, provider_details)

    @staticmethod
    def create_provider(data, prov_type, file_path):
        """Save Multiple providers."""
        success = []
        failed = []
        json_data = CreateMultipleProviders.fetch_file_data(file_path)
        if isinstance(json_data, list):
            print('Saving list of providers...')
            for data in json_data:
                try:
                    provider = deploy_sdk_client.SaveProvider(
                        name=data.get(DeployConstants.NAME_REEFERENCE),
                        type=prov_type,
                        json=data.get(DeployConstants.PROVIDER_DETAILS_REFERENCE)
                    )
                    api_client = set_header_parameter(DeployUtility.create_api_client(), Utility.get_url(DeployConstants.DEPLOY_URL))
                    provider_api_instance = deploy_sdk_client.ProviderApi(api_client)
                    api_response = provider_api_instance.save_provider(provider)
                    success.append(api_response.name)
                except ApiException as api_exception:
                    failed.append(data.get(DeployConstants.NAME_REEFERENCE))
        else:
            raise RuntimeError('Please provide valid json file.')

        CreateMultipleProviders.print_response(success, failed)
        return success

    @staticmethod
    def fetch_file_data(file_path):
        """Fetch file data."""
        if not os.path.isfile(file_path):
            raise RuntimeError('Provider details file %s does not exists' % file_path)

        with open(file_path, "r") as handle:
            filedata = handle.read()

        jsondata = json.loads(filedata)
        return jsondata

    @staticmethod
    def print_response(success, failed):
        """Print response."""
        success_len = len(success)
        if success_len != 0:
            print('{} providers created successfully: {}'.format(success_len, success))
        print('Failed to create {} providers: {}'.format(len(failed), failed))
