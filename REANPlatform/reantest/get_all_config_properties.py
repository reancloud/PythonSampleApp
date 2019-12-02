"""List all Config Properties."""

import json
import logging
from prettytable import PrettyTable
from cliff.command import Command
import test_sdk_client
from reantest.utility import Utility
from reanplatform.utility import Utility as PlatformUtility


class ConfigListProperties(Command):
    """List Config Properties."""

    log = logging.getLogger(__name__)
    _epilog = 'Example : \n\t rean-test list-config-properties -t <tags/properties> -f <json/table>'

    def get_parser(self, prog_name):
        """Parser of Properties."""
        parser = super(ConfigListProperties, self).get_parser(prog_name)
        parser.add_argument('--format', '-f',
                            help='Allowed values are: [json, table]',
                            type=str, default='json',
                            choices=['json', 'table'],
                            nargs='?',
                            required=False)
        parser.add_argument('--output', '-o', help="Write output to <file> instead of stdout.", required=False)
        parser.add_argument('--type', '-t', help="Specific property type. Default Value is Tag",
                            choices=['tags', 'properties'], default='tags')
        return parser

    def take_action(self, parsed_args):
        """take_action of ListProvider."""
        try:
            api_instance = test_sdk_client.ConfigurationApi(Utility.set_headers())
            api_response = api_instance.get_all_configurations()

            if parsed_args.type == 'tags':
                ConfigListProperties.list_tags(parsed_args, api_response)
            elif parsed_args.type == 'properties':
                ConfigListProperties.list_porperties(parsed_args, api_response)

        except Exception as exception:
            Utility.print_exception(exception)

    @staticmethod
    def list_tags(parsed_args, api_response):
        """List configuration tags."""
        tags_data = api_response.tags
        if parsed_args.format == 'table':
            tag_table = PrettyTable(['Key', 'Value'])
            tag_table.padding_width = 1

            for key in tags_data:
                tag_table.add_row(
                    [
                        key,
                        tags_data[key]
                    ]
                )

            PlatformUtility.print_output_as_str("{}".format(tag_table), parsed_args.output)
        elif parsed_args.format == 'json' or parsed_args.format == '':
            PlatformUtility.print_output_as_str(
                json.dumps(
                    tags_data,
                    default=lambda o: o.__dict__,
                    sort_keys=True, indent=4
                ).replace("\"_", '"'), parsed_args.output
            )
        else:
            raise RuntimeError("Please specify correct format, Allowed \
                    values are: [json, table]")

    @staticmethod
    def list_porperties(parsed_args, api_response):
        """List Config Properties."""
        properties_data = api_response.properties
        if parsed_args.format == 'table':
            for title in properties_data:
                print(title)
                porperties_table = PrettyTable(['Display Name', 'Key', 'Value'])
                porperties_table.padding_width = 1

                for property_data in properties_data[title]:
                    porperties_table.add_row(
                        [
                            property_data.display_name,
                            property_data.key,
                            property_data.value,

                        ]
                    )

                PlatformUtility.print_output_as_str("{}".format(porperties_table), parsed_args.output)

        elif parsed_args.format == 'json' or parsed_args.format == '':
            PlatformUtility.print_output_as_str(
                json.dumps(
                    properties_data,
                    default=lambda o: o.__dict__,
                    sort_keys=True, indent=4
                ).replace("\"_", '"'), parsed_args.output
            )
        else:
            raise RuntimeError("Please specify correct format, Allowed \
                        values are: [json, table]")
