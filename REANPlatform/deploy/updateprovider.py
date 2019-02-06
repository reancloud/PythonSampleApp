"""Update provider module."""
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


class UpdateProvider(Command):
    """Update provider."""

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        """get_parser."""
        parser = super(UpdateProvider, self).get_parser(prog_name)
        parser.add_argument('--id', '-i', help='Provider id to update',
                            required=True)
        parser.add_argument('--name', '-n', help='Provider name',
                            required=True)
        parser.add_argument('--type', '-t', help='Provider type',
                            required=True)
        parser.add_argument('--provider_details', '-f',
                            help='Json file with applicable key-value pair \
                            for provider type. File absolute path',
                            required=True)
        parser.add_argument('--output', '-o',
                            help="Write output to <file> instead of stdout.",
                            required=False)
        return parser

    def take_action(self, parsed_args):
        """take_action."""
        UpdateProvider.update_provider(parsed_args)

    @staticmethod
    def update_provider(parsed_args):
        """update_provider."""
        api_client = set_header_parameter(DeployUtility.create_api_client(), Utility.get_url(DeployConstants.DEPLOY_URL))
        provider_api_instance = deploy_sdk_client.ProviderApi(api_client)
        try:
            file_path = parsed_args.provider_details
            if not os.path.isfile(file_path):
                raise RuntimeError('Provider details file %s does not exists' % file_path)
            with open(file_path, "r") as handle:
                filedata = handle.read()
            jsondata = json.loads(filedata)
            provider = deploy_sdk_client.SaveProvider(
                id=parsed_args.id,
                name=parsed_args.name,
                type=parsed_args.type,
                json=jsondata
            )
            api_response = provider_api_instance.update_provider(provider)
            Utility.print_output_as_str("Provider created successfully Name: {},  Id: {}".format(parsed_args.name, parsed_args.id), parsed_args.output)
        except ApiException as api_exception:
            Utility.print_exception(api_exception)
