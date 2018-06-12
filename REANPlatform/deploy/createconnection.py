# pylint: disable=E0202, W0221
"""Create connection module."""
import os
import re
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
                            '-t', help='Connection protocol type. \
                            Allowed values are: [SSH, WinRM]',
                            required=True
                        )
        parser.add_argument(
                            '--name',
                            '-n',
                            help='Connection name',
                            required=True
                        )
        parser.add_argument(
                            '--user',
                            '-u',
                            help='Username to login machine',
                            required=False
                        )
        parser.add_argument(
                            '--password',
                            '-p',
                            help='Password to login machine',
                            required=False
                        )
        parser.add_argument(
                            '--securekeypath',
                            '-key', help='Secure key path. Provide this \
                            attribute only if Connection protocol type is \
                            SSH.',
                            required=False
                        )

        parser.add_argument(
                            '--bastionhost',
                            '-b_host', help='Bastion host',
                            required=False
                        )

        parser.add_argument(
                            '--bastionuser',
                            '-b_user', help='Bastion connection user',
                            required=False
                        )
        parser.add_argument(
                            '--bastionport',
                            '-port', help='Bastion port',
                            required=False
                        )
        parser.add_argument(
                            '--bastionpassword',
                            '-b_pass', help='Bastion connection password',
                            required=False
                        )
        parser.add_argument(
                            '--bastionsecurekeypath',
                            '-b_key', help='Bastion connection secure \
                            key path',
                            required=False
                        )
        return parser

    def validate(self, connection_type, password, securekeypath,
                 bastionhost, bastionuser, bastionsecurekeypath,
                 bastionpassword):
        """Validate parsed arguments."""
        if connection_type == 'WinRM' and securekeypath:
            message = "WinRM Does Not Required SecureKey."
            exception_msg = re.sub(' +', ' ', message)
            raise Exception(exception_msg)
        if password is None and connection_type == 'WinRM':
            message = "password must not be none for 'WinRM'."
            exception_msg = re.sub(' +', ' ', message)
            raise Exception(exception_msg)
        if connection_type == 'SSH' and (password or securekeypath) is None:
            message = "password or securekeypath must not be none for 'SSH'."
            exception_msg = re.sub(' +', ' ', message)
            raise Exception(exception_msg)
        if bastionuser is None and bastionhost:
            message = "bastion user must not be none for bastion connection."
            exception_msg = re.sub(' +', ' ', message)
            raise Exception(exception_msg)
        if bastionuser and (bastionsecurekeypath or bastionpassword) is None:
            message = "bastionpassword or bastionsecurekeypath must not be \
            none for bastion connection."
            exception_msg = re.sub(' +', ' ', message)
            raise Exception(exception_msg)
        if connection_type == 'WinRM' and bastionuser:
            message = "Bastion connection is not allowed in case of WinRM."
            exception_msg = re.sub(' +', ' ', message)
            raise Exception(exception_msg)

    def get_key(self, securekeypath):
        """get_key."""
        line_stripping = ''
        if os.path.exists(securekeypath):
            with open(securekeypath, 'r') as fin:
                for line in fin.readlines():
                    line_stripping = line_stripping + '\n' + line.strip('\n')
                return line_stripping

    def create_connections(self, name, connection_type, user, password,
                           securekeypath, bastionhost, bastionuser,
                           bastionpassword, bastionsecurekeypath,
                           bastionport):
        """Create connections."""
        try:
            # Initialise instance and api_instance
            instance = deploy_sdk_client.ConnectionApi()
            api_instance = set_header_parameter(instance)
            body = None
            bastion_data = None
            if bastionhost:
                bastion_data = {
                        'host': bastionhost,
                        'password': bastionpassword,
                        # 'secure_key': self.get_key(parsed_args),
                        'port':  bastionport,
                        'user': bastionuser
                }
            if(connection_type == 'SSH' and securekeypath and password):    # noqa: E501
                body = deploy_sdk_client.VmConnection(
                    bastion_connection=bastion_data,
                    type=connection_type,
                    name=name,
                    user=user,
                    password=password,
                    secure_key=self.get_key(securekeypath)
                )
            elif(connection_type == 'SSH' and securekeypath):
                body = deploy_sdk_client.VmConnection(
                    bastion_connection=bastion_data,
                    type=connection_type,
                    name=name,
                    user=user,
                    secure_key=self.get_key(securekeypath)
                )
            elif((connection_type == 'WinRM' and password) or
                    (connection_type == 'SSH' and password)):
                    body = deploy_sdk_client.VmConnection(
                        bastion_connection=bastion_data,
                        type=connection_type,
                        name=name,
                        user=user,
                        password=password
                    )
            api_response = api_instance.save_vm_connection(body)
            print("Connection created successfully :%s, id: %s" %
            (api_response.name, api_response.id))  # noqa: E501

        except ApiException as e:
            Utility.print_exception(e)

    def take_action(self, parsed_args):
        """take_action."""
        # Define parsed argument
        bastionhost = parsed_args.bastionhost
        bastionpassword = parsed_args.bastionpassword
        bastionport = parsed_args.bastionport
        bastionuser = parsed_args.bastionuser
        connection_type = parsed_args.type
        securekeypath = parsed_args.securekeypath
        bastionsecurekeypath = parsed_args.bastionsecurekeypath
        name = parsed_args.name
        user = parsed_args.user
        password = parsed_args.password

        self.validate(connection_type, password, securekeypath, bastionhost,
                      bastionuser, bastionpassword, bastionsecurekeypath)
        self.create_connections(name, connection_type, user, password,
                                securekeypath, bastionhost, bastionuser,
                                bastionpassword, bastionsecurekeypath,
                                bastionport)
