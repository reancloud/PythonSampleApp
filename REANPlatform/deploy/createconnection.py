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
        parser.add_argument('--type', '-t', help='Connection protocol type. Allowed values are: [SSH, WinRM]', required=True)
        parser.add_argument('--name', '-n', help='Connection name', required=True)
        parser.add_argument('--user', '-u', help='Username to login machine', required=False)
        parser.add_argument('--password', '-p', help='Password to login machine', required=True)
        parser.add_argument('--securekeypath', '-key', help='Secure key path', required=False)
        parser.add_argument('--bastionhost', '-host', help='Bastion host', required=False)
        parser.add_argument('--bastionuser', '-b_user', help='Bastion connection user', required=False)
        parser.add_argument('--bastionport', '-port', help='Bastion port', required=False)
        parser.add_argument('--bastionpassword', '-b_pass', help='Bastion connection password', required=False)
        parser.add_argument('--bastionsecurekeypath', '-b_key', help='Bastion connection secure key path', required=False)
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
        body = None
        bastion_data = None
        try:
            if parsed_args.bastionhost:
                """For Using Secure Key : secure_key': self.get_key(parsed_args)"""
                bastion_data = {'host': parsed_args.bastionhost, 'password': parsed_args.bastionpassword, 'port': parsed_args.bastionport, 'user': parsed_args.bastionuser}

            if(parsed_args.type == 'SSH' and parsed_args.securekeypath):
                    body = deploy_sdk_client.VmConnection(
                        bastion_connection=bastion_data,
                        type=parsed_args.type,
                        name=parsed_args.name,
                        user=parsed_args.user,
                        secure_key=self.get_key(parsed_args)
                    )
            elif((parsed_args.type == 'WinRM' and parsed_args.password) or (parsed_args.type == 'SSH' and parsed_args.password)):
                    body = deploy_sdk_client.VmConnection(
                        bastion_connection=bastion_data,
                        type=parsed_args.type,
                        name=parsed_args.name,
                        user=parsed_args.user,
                        password=parsed_args.password
                    )
            else:
                raise RuntimeError("Please provide correct\
                         parameters and values:")

            api_response = api_instance.save_vm_connection(body)
            print("Connection created successfully :%s, id: %s" % (api_response.name, api_response.id))  # noqa: E501

        except ApiException as e:
            Utility.print_exception(e)
