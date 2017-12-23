import os
from pprint import pprint
import logging
from cliff.command import Command
from . import utility
import swagger_client
from swagger_client.rest import ApiException
from deploy.constants import Constants

class DeleteConnection(Command):
    
    "DeleteConnection"
    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(DeleteConnection, self).get_parser(prog_name)
        parser.add_argument('--name', '-n', help='Connection name', required=False)
        parser.add_argument('--id', '-id', help='Connection ID',required=False)
        return parser

    def take_action(self, parsed_args):
          # create an instance of the API class
        api_instance = swagger_client.ConnectionApi()
        api_instance.api_client.set_default_header(
            Constants.AUTHORIZATION,
            Constants.CREDENTIALS
            )
        api_instance.api_client.host = Constants.HOST_PATH
        try:
            if(parsed_args.id is None and parsed_args.name is None):
                raise RuntimeError('Either \'name\' or \'id\'  field is required')
            con_id = None
            if(parsed_args.id is not None):
                con_id = parsed_args.id # int | connection Id
            else:
                all_vms=api_instance.get_all_vm_connections()
                for vm in all_vms:
                    if(vm.name==parsed_args.name):
                        con_id=vm.id
                        break

            if(con_id is None):
               raise RuntimeError('Connection \'name\' or \'id\' does not exit')

            # Delete Connection for User
            api_response = api_instance.delete_vm_connection(con_id)
            pprint("Connection is deleted Successfully")
            pprint(api_response)
        except ApiException as e:
            print("Exception when calling ConnectionApi->delete_vm_connection: %s\n" % e)