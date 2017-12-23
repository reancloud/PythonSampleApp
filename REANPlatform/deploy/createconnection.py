import os
from pprint import pprint
import logging
from cliff.command import Command
from . import utility
import swagger_client
from swagger_client.rest import ApiException
from deploy.constants import Constants

class SaveConnection(Command):

    "SaveConnection"
    log = logging.getLogger(__name__)


    def get_parser(self, prog_name):
        parser = super(SaveConnection, self).get_parser(prog_name)
        parser.add_argument('--type', '-t', help='Set type of connection', required=False)
        parser.add_argument('--name', '-n', help='Set name of connection', required=False)
        parser.add_argument('--user', '-u', help='Set user of connection', required=False)
        parser.add_argument('--password', '-p', help='Set password of connection', required=False)
        parser.add_argument('--securekeypath', '-k', help='Set secure key path of connection',
                            required=False
                           )
        return parser

    def get_key(self, parsed_args):
        line_stripping = ''
        if os.path.exists(parsed_args.securekeypath):
            with open(parsed_args.securekeypath, 'r') as fin:
                for line in fin.readlines():
                    line_stripping = line_stripping + '\n' +line.strip('\n')
                return line_stripping

    def take_action(self, parsed_args):

        api_instance = swagger_client.ConnectionApi()

        api_instance.api_client.set_default_header(
           Constants.AUTHORIZATION,
           Constants.CREDENTIALS
        )
        api_instance.api_client.host = Constants.HOST_PATH
        try:
            if parsed_args.securekeypath is None and parsed_args.password is None:
                raise RuntimeError('Either \'password\' or \'secureKey\' String type field is required')
            elif parsed_args.securekeypath is not None and parsed_args.password is not None:
                body = swagger_client.VmConnection(
                    type=parsed_args.type,
                    name=parsed_args.name,
                    user=parsed_args.user,
                    password=parsed_args.password,
                    self.get_key(parsed_args)
                )
            elif parsed_args.securekeypath is None:
                body = swagger_client.VmConnection(
                    type=parsed_args.type,
                    name=parsed_args.name,
                    user=parsed_args.user,
                    password=parsed_args.password
                )
            else:
                body = swagger_client.VmConnection(
                    type=parsed_args.type,
                    name=parsed_args.name,
                    user=arsed_args.user,
                    passwprd=None,
                    self.get_key(parsed_args)
                )

            def callback_function(response):
                pprint(response)         

            api_response = api_instance.save_vm_connection(body,callback=callback_function)
           
        except ApiException as e:
            self.log.error(e)
