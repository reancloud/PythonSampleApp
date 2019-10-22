"""Config Update tags."""

import logging
import json
from cliff.command import Command
from reantest.utility import Utility

import test_sdk_client


class ConfigUpdateTags(Command):
    """Update Config Tags."""

    log = logging.getLogger(__name__)
    _epilog = 'Example : \n\t rean-test update-tags -f <path_to_tags_json>'

    def get_parser(self, prog_name):
        """get_parser."""
        parser = super(ConfigUpdateTags, self).get_parser(prog_name)

        parser.add_argument('--tag_json_file', '-f',
                            help='JSON file with tags to update',
                            required=False)

        parser.add_argument('--tags', '-t',
                            help='JSON tags string',
                            required=False)

        return parser

    def take_action(self, parsed_args):
        """take_action."""
        self.log.debug(parsed_args)

        try:
            if parsed_args.tag_json_file is None and parsed_args.tags is None:
                self.app.stdout.write("Provide only one parameter")
                exit(1)

            if parsed_args.tag_json_file is not None and parsed_args.tags is not None:
                self.app.stdout.write("Provide only one parameter")
                exit(1)

            if parsed_args.tag_json_file is not None:
                with Utility.open_file(parsed_args.tag_json_file) as handle:
                    input_payload = handle.read()
            else:
                input_payload = parsed_args.tags

            payload = json.loads(input_payload)
            api_instance = test_sdk_client.ConfigurationApi(Utility.set_headers())
            api_response = api_instance.update_tags(payload)
            print(api_response)
        except Exception as exception:
            Utility.print_exception(exception)
