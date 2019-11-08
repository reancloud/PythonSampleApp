"""Config Update Config Property."""

import logging
from cliff.command import Command
from reantest.utility import Utility

import test_sdk_client


class ConfigUpdateProperty(Command):
    """Update config property."""

    log = logging.getLogger(__name__)
    _epilog = 'Example : \n\t rean-test update-property --property_key <provider_key> --property_value <property_value>'

    def get_parser(self, prog_name):
        """get_parser."""
        parser = super(ConfigUpdateProperty, self).get_parser(prog_name)

        parser.add_argument('--property_key', '-pk',
                            help='property name',
                            required=False)

        parser.add_argument('--property_value', '-pv',
                            help='Property value to update',
                            required=False)

        parser.add_argument('--key_value_string', '-kv',
                            help='Provide this string to update multiple properties. Example: key1=val1,key2=val2',
                            required=False
                            )

        return parser

    def take_action(self, parsed_args):
        """take_action."""
        self.log.debug(parsed_args)

        try:
            if parsed_args.property_key is None and parsed_args.property_value is None and \
                    parsed_args.key_value_string is None:
                raise RuntimeError("Provide either property_name and Property_value or key_value_string")

            if parsed_args.property_key is not None and parsed_args.property_value is not None:
                logging.debug("Using key value property")
                body = {parsed_args.property_key: parsed_args.property_value}
            else:
                logging.debug("Using key_value_string attribute")
                key_values = parsed_args.key_value_string.split(',')
                body = {}
                for kv in key_values:
                    key, val = kv.split('=')
                    body[key] = val

            logging.debug(body)

            api_instance = test_sdk_client.ConfigurationApi(Utility.set_headers())
            api_instance.update_property(body)
            print("Properties updated successfully.")
        except Exception as exception:
            Utility.print_exception(exception)
