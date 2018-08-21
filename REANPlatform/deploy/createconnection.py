"""Create connection module."""
import logging
from cliff.command import Command
import deploy_sdk_client
from deploy_sdk_client.rest import ApiException
from reanplatform.set_header import set_header_parameter
from reanplatform.utility import Utility
from deploy.constants import DeployConstants
from deploy.utility import DeployUtility


class SaveConnection(Command):
    """Save connection."""

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        """Get_parser."""
        parser = super(SaveConnection, self).get_parser(prog_name)
        parser.add_argument('--type', '-t', help='Connection protocol type. Allowed values are: [SSH, WinRM]', required=True)
        parser.add_argument('--name', '-n', help='Connection name', required=True)
        parser.add_argument('--user', '-u', help='Username to login machine', required=False)
        parser.add_argument('--password', '-p', help='Password to login machine', required=False)
        parser.add_argument('--securekeypath', '-k', help='Secure key path', required=False)
        parser.add_argument('--bastionhost', '-bh', help='Bastion host', required=False)
        parser.add_argument('--bastionuser', '-bu', help='Bastion connection user', required=False)
        parser.add_argument('--bastionport', '-bport', help='Bastion port', required=False)
        parser.add_argument('--bastionpassword', '-bp', help='Bastion connection password', required=False)
        parser.add_argument('--bastionsecurekeypath', '-bk', help='Bastion connection secure key path', required=False)
        return parser

    @staticmethod
    def get_key(securekeypath):
        """get_key."""
        line_stripping = ''
        with open(securekeypath, 'r') as fin:
            for line in fin.readlines():
                line_stripping = line_stripping + '\n' + line.strip('\n')
            return line_stripping

    def take_action(self, parsed_args):
        """take_action."""
        api_client = set_header_parameter(DeployUtility.create_api_client(), Utility.get_url(DeployConstants.DEPLOY_URL))
        conn_api_instance = deploy_sdk_client.ConnectionApi(api_client)
        connection_data = None
        bastion_data = None
        try:
            if(parsed_args.bastionhost and parsed_args.type == 'SSH'):
                bastion_data = {
                    'host': parsed_args.bastionhost,
                    'password': parsed_args.bastionpassword,
                    'secureKey': SaveConnection.get_key(parsed_args.bastionsecurekeypath) if parsed_args.bastionsecurekeypath is not None else None,
                    'port': parsed_args.bastionport,
                    'user': parsed_args.bastionuser
                }
            if(parsed_args.type == 'SSH' and parsed_args.securekeypath):
                connection_data = deploy_sdk_client.SaveVmConnection(
                    bastion_connection=bastion_data,
                    type=parsed_args.type,
                    name=parsed_args.name,
                    user=parsed_args.user,
                    secure_key=SaveConnection.get_key(parsed_args.securekeypath)
                )
            elif((parsed_args.type == 'WinRM' and parsed_args.password) or (parsed_args.type == 'SSH' and parsed_args.password)):
                connection_data = deploy_sdk_client.SaveVmConnection(
                    bastion_connection=bastion_data,
                    type=parsed_args.type,
                    name=parsed_args.name,
                    user=parsed_args.user,
                    password=parsed_args.password
                )
            else:
                raise RuntimeError("Please provide correct parameters and values")

            api_response = api_instance.save_vm_connection(connection_data)
            print("Connection created successfully :%s, id: %s" %
                  (api_response.name, api_response.id))

        except ApiException as api_exception:
            Utility.print_exception(api_exception)
