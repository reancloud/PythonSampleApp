"""List connections module."""
import logging
from cliff.command import Command
import deploy_sdk_client
import json
import os
from deploy_sdk_client.rest import ApiException
from reanplatform.set_header import set_header_parameter
from prettytable import PrettyTable
from reanplatform.utility import Utility


class Connection(Command):
    """List connections."""

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        """get_parser."""
        parser = super(Connection, self).get_parser(prog_name)

        connection_parser = parser.add_subparsers(help='Connection sub-commands')  # noqa: E501

        list_connection_parser = connection_parser.add_parser(
                                                        "list",
                                                        help='List connection\
                                                        Usage: [rean-deploy\
                                                        connection list\
                                                        --format json/table]'
                                                    )
        list_connection_parser.add_argument(
                            '--format', '-f',
                            help='Allowed values are: [json, table]',
                            type=str, default='json',
                            nargs='?',
                            required=False
                            )
        list_connection_parser.add_argument(
                                    'action', nargs='?',
                                    type=str,
                                    default='list',
                                    help='List command default action'
                                    )

        del_connection_parser = connection_parser.add_parser(
                                                        "delete",
                                                        help='Delete connections\
                                                        Usage: [rean-deploy\
                                                        connection delete\
                                                        --id conn_id/--name conn_name]'    # noqa: E501
                                                    )

        del_connection_parser.add_argument(
                            '--name', '-n',
                            help='Connection name',
                            required=False
                            )
        del_connection_parser.add_argument(
                            '--id', '-id',
                            help='Connection ID',
                            required=False
                            )
        del_connection_parser.add_argument(
                                    'action', nargs='?',
                                    type=str,
                                    default='delete',
                                    help='Delete command default action'
                                )

        create_connection_parser = connection_parser.add_parser(
                                                        "create",
                                                        help='Create connections\
                                                        Usage: [rean-deploy\
                                                        connection create\
                                                        --name con_name\
                                                        --type type\
                                                        --user user]'
                                                    )

        create_connection_parser.add_argument(
                            '--name',
                            '-n',
                            help='Connection name',
                            required=True
                        )

        create_connection_parser.add_argument(
                            '--type',
                            '-t', help='Connection protocol type. Allowed values \
                            are: [SSH, WinRM]',
                            required=True
                        )

        create_connection_parser.add_argument(
                            '--user',
                            '-u',
                            help='Username to login machine',
                            required=True
                        )
        create_connection_parser.add_argument(
                            '--password',
                            '-p',
                            help='Password to login machine',
                            required=False
                        )
        create_connection_parser.add_argument(
                            '--securekeypath',
                            '-key', help='Secure key path',
                            required=False
                        )

        create_connection_parser.add_argument(
                            '--bastionhost',
                            '-host', help='Bastion host',
                            required=False
                        )

        create_connection_parser.add_argument(
                            '--bastionuser',
                            '-b_user', help='Bastion connection user',
                            required=False
                        )
        create_connection_parser.add_argument(
                            '--bastionport',
                            '-port', help='Bastion port',
                            required=False
                        )
        create_connection_parser.add_argument(
                            '--bastionpassword',
                            '-b_pass', help='Bastion connection password',
                            required=False
                        )
        create_connection_parser.add_argument(
                            '--bastionsecurekeypath',
                            '-b_key', help='Bastion connection secure \
                            key path',
                            required=False
                        )
        create_connection_parser.add_argument(
                                    'action', nargs='?',
                                    type=str,
                                    default='create',
                                    help='Create command default action'
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
        self.connection_opration(parsed_args, api_instance)

    def connection_opration(self, parsed_args, api_instance):
        """connection_opration."""
        try:
            if parsed_args.action == 'list':
                api_response = api_instance.get_all_vm_connections()
                if parsed_args.format == 'table':
                    table = PrettyTable(['Name', 'Id', 'Type'])
                    table.padding_width = 1
                    for connection in api_response:
                        table.add_row(
                                    [
                                        connection.name,
                                        connection.id,
                                        connection.type
                                    ]
                            )
                    print("Connection list \n%s" % (table))
                elif parsed_args.format == 'json' or parsed_args.format == '':
                    print(
                            json.dumps(
                                    api_response,
                                    default=lambda o: o.__dict__,
                                    sort_keys=True, indent=4
                                    ).replace("\"_", '"')
                        )
                else:
                    raise RuntimeError("Please specify correct fromate, Allowed \
                            values are: [json, table]")

            elif parsed_args.action == 'delete':
                con_id = parsed_args.id

                if parsed_args.name and parsed_args.id is None:
                    all_vms = api_instance.get_all_vm_connections()
                    for vm_conn in all_vms:
                        if(vm_conn.name == parsed_args.name):
                            con_id = vm_conn.id
                            break

                if(con_id is None):
                    raise RuntimeError("Exception : connection does not exit", parsed_args.name)    # noqa: E501

            # Delete Connection for User
                api_response = api_instance.delete_vm_connection(con_id)
                print("Connection deleted successfully :%s " % str(api_response.name))    # noqa: E501

            elif parsed_args.action == 'create':
                body = None
                bastion_data = None
                if parsed_args.bastionhost:
                    bastion_data = {
                            'host': parsed_args.bastionhost,
                            'password': parsed_args.bastionpassword,
                            # 'secure_key': self.get_key(parsed_args),
                            'port':  parsed_args.bastionport,
                            'user': parsed_args.bastionuser
                        }

                if(parsed_args.type == 'SSH' and parsed_args.securekeypath and parsed_args.password):    # noqa: E501
                    body = deploy_sdk_client.VmConnection(
                        bastion_connection=bastion_data,
                        type=parsed_args.type,
                        name=parsed_args.name,
                        user=parsed_args.user,
                        password=parsed_args.password,
                        secure_key=self.get_key(parsed_args)
                    )
                elif(parsed_args.type == 'SSH' and parsed_args.securekeypath):
                        body = deploy_sdk_client.VmConnection(
                            bastion_connection=bastion_data,
                            type=parsed_args.type,
                            name=parsed_args.name,
                            user=parsed_args.user,
                            secure_key=self.get_key(parsed_args)
                        )
                elif((parsed_args.type == 'WinRM' and parsed_args.password) or
                        (parsed_args.type == 'SSH' and parsed_args.password)):
                        if(parsed_args.type == 'WinRM' and parsed_args.securekeypath):     # noqa: E501
                            raise RuntimeError("WinRM does not require\
                            securekey:")
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
