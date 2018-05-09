import logging
from pprint import pprint
from cliff.command import Command
import deploy_sdk_client
from deploy_sdk_client.rest import ApiException
from deploy.constants import Constants
import os
import json


class SaveProvider(Command):
    "SaveProvider"
    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(SaveProvider, self).get_parser(prog_name)
        parser.add_argument('--name', '-n', help='Set name for Provider',
                            required=True)
        parser.add_argument('--type', '-t', help='Type of provider',
                            required=True)
        parser.add_argument('--input_json_file', '-f',
                            help='Json File with applicable key-value pair \
                            for provider type', required=True)
        return parser

    def take_action(self, parsed_args):
        api_instance = deploy_sdk_client.ProviderApi()

        api_instance.api_client.set_default_header(
            Constants.AUTHORIZATION,
            Constants.CREDENTIALS
        )
        api_instance.api_client.host = Constants.HOST_PATH

        try:
            file_path = parsed_args.input_json_file

            if not os.path.isfile(file_path):
                raise RuntimeError('No such file or directory')

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

            pprint(api_response)
        except ApiException as e:
            self.log.error(e)
