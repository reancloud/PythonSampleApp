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
        parser.add_argument('--provider_details', '-f',
                            help="An array of Provider in JSON format. Sample value for this attribute is:\n[{\n  'name': 'provider_name',\n  'type': 'provider_type',\n  'provider_details': provider_json\n}]",
                            required=True
                           )
        return parser

    def take_action(self, parsed_args):
        """take_action."""
        provider_details = parsed_args.provider_details

        CreateMultipleProviders.create_provider(provider_details)

    @staticmethod
    def create_provider(file_path):
        """Save Multiple providers."""
        success = []
        failed = []
        exists = []
        json_data = CreateMultipleProviders.fetch_file_data(file_path)

        if isinstance(json_data, list):
            print('Saving list of providers...')
            for data in json_data:
                try:
                    api_client = set_header_parameter(DeployUtility.create_api_client(), Utility.get_url(DeployConstants.DEPLOY_URL))
                    provider_api_instance = deploy_sdk_client.ProviderApi(api_client)
                    flag = CreateMultipleProviders.check_if_provider_exists(data.get(DeployConstants.NAME_REFERENCE), provider_api_instance)
                    if not flag:
                        provider = deploy_sdk_client.SaveProvider(
                            name=data.get(DeployConstants.NAME_REFERENCE),
                            type=data.get(DeployConstants.PROVIDER_TYPE_REFERENCE),
                            json=data.get(DeployConstants.PROVIDER_DETAILS_REFERENCE)
                        )
                        api_response = provider_api_instance.save_provider(provider)
                        success.append(api_response.name)
                    else:
                        exists.append(data.get(DeployConstants.NAME_REFERENCE))
                except ApiException as api_exception:
                    failed.append(data.get(DeployConstants.NAME_REFERENCE))
        else:
            raise RuntimeError('Please provide valid json file.')

        CreateMultipleProviders.print_response(success, exists, failed)

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
    def print_response(success, exists, failed):
        """Print response."""
        success_len = len(success)
        if success_len != 0:
            print('{} providers created successfully: {}'.format(success_len, success))

        exists_len = len(exists)
        if exists_len != 0:
            print('{} providers already exists: {}'.format(exists_len, exists))

        failed_len = len(failed)
        if failed_len != 0:
            print('Failed to create {} providers: {}'.format(failed_len, failed))

    @staticmethod
    def check_if_provider_exists(prov_name, provider_api_instance):
        """Check if provider exists."""
        try:
            api_response = provider_api_instance.get_provider_by_name(prov_name)
            return True
        except ApiException as api_exception:
            err = json.loads(api_exception.body)
            if err['status'] == 404:
                return False
