"""Create connection module."""
import os
from pprint import pprint
import logging
from cliff.command import Command
from reanplatform import utility
import deploy_sdk_client
from deploy_sdk_client.rest import ApiException
from reanplatform.set_header import set_header_parameter
from reanplatform.utility import Utility


class SaveConnection(Command):
    """Save connection."""

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        """get_parser."""
        parser = super(SaveConnection, self).get_parser(prog_name)
        parser.add_argument(
                            '--type',
                            '-t', help='Allowed values are: [ SSH, WinRM ]',
                            required=False
                        )
        parser.add_argument(
                            '--name',
                            '-n',
                            help='Connection name',
                            required=False
                        )
        parser.add_argument(
                            '--user',
                            '-u',
                            help='Connection user',
                            required=False
                        )
        parser.add_argument(
                            '--password',
                            '-p',
                            help='Connection password',
                            required=False
                        )
        parser.add_argument(
                            '--securekeypath',
                            '-key', help='Secure key path',
                            required=False
                        )
        return parser

    def get_key(self, parsed_args):
        """get_key."""
        line_stripping = ''
        if os.path.exists(parsed_args.securekeypath):
            with open(parsed_args.securekeypath, 'r') as fin:
                for line in fin.readlines():
                    line_stripping = line_stripping + '\n' + line.strip('\n')
                return line_stripping

    def take_action(self, parsed_args):
        """take_action."""
        conn_api_instance = deploy_sdk_client.ConnectionApi()
        api_instance = set_header_parameter(conn_api_instance)
        try:
            if (parsed_args.securekeypath is not None and
                    parsed_args.password is not None):
                body = deploy_sdk_client.VmConnection(
                    type=parsed_args.type,
                    name=parsed_args.name,
                    user=parsed_args.user,
                    password=parsed_args.password,
                    secure_key=self.get_key(parsed_args)
                )
            elif parsed_args.securekeypath is None:
                body = deploy_sdk_client.VmConnection(
                    type=parsed_args.type,
                    name=parsed_args.name,
                    user=parsed_args.user,
                    password=parsed_args.password
                )
            else:
                body = deploy_sdk_client.VmConnection(
                    type=parsed_args.type,
                    name=parsed_args.name,
                    user=parsed_args.user,
                    password=None,
                    secure_key=self.get_key(parsed_args)
                )

            api_response = api_instance.save_vm_connection(body)
            print("Connection created successfully :%s, id: %s" % (api_response.name, api_response.id))  # noqa: E501

        except ApiException as e:
            Utility.print_exception(e)
