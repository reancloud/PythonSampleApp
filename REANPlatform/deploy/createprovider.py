"""Save provider module."""
import logging
from pprint import pprint
from cliff.command import Command
import deploy_sdk_client
from deploy_sdk_client.rest import ApiException
from deploy import set_provider_header
import os
import json


class SaveProvider(Command):
    """Save the provider."""

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        """get_parser."""
        parser = super(SaveProvider, self).get_parser(prog_name)
        parser.add_argument('--name', '-n', help='Provider name',
                            required=True)
        parser.add_argument('--type', '-t', help='Type of provider',
                            required=True)
        parser.add_argument('--provider_details', '-f',
                            help='Json file with applicable key-value pair \
                            for provider type', required=True)
        return parser

    def take_action(self, parsed_args):
        """take_action."""
        api_instance = set_provider_header.set_header()
        try:
            file_path = parsed_args.provider_details

            if not os.path.isfile(file_path):
                raise RuntimeError('Provider details file %s \
                                does not exists' % file_path)

            # Parse parameters
            with open(file_path, "r") as handle:
                filedata = handle.read()

            jsondata = json.loads(filedata)
            provider = deploy_sdk_client.SaveProvider(
                            name=parsed_args.name,
                            type=parsed_args.type,
                            json=jsondata
                        )
            api_response = api_instance.save_provider(provider)
            pprint("Provider created successfully : %s" % (parsed_args.name))
        except ApiException as e:
            self.log.error(e)
