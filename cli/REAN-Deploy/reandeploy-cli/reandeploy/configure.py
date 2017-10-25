"Configure REAN-Deploy CLI"
import os
import logging
from pprint import pprint
import swagger_client
from swagger_client.rest import ApiException
from cliff.command import Command


class Configure(Command):

    "Configure REAN-Deploy CLI"
    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(Configure, self).get_parser(prog_name)
        parser.add_argument('--username', '-u', help='Set username', required=True)
        parser.add_argument('--password', '-p', help='Set username', required=True)
        return parser

    def create_file(self, parsed_args, path):
        os.chdir(path +'/.deploy')
        file_obj = open("credentials", "w+")
        file_obj.write("[default]")
        file_obj.write('\n')
        username = 'username=' + parsed_args.username
        password = 'password=' + parsed_args.password
        file_obj.write(username)
        file_obj.write('\n')
        file_obj.write(password)
        file_obj.close()
   
    def take_action(self, parsed_args):
        try:
            path = os.path.expanduser('~')
            if os.path.exists(path+'/.deploy'):
                self.create_file(parsed_args, path)
            else:
                os.makedirs(path+'/.deploy')
                self.create_file(parsed_args, path)

        except ApiException as e:
            self.log.error(e)


class Error(Command):
    "Always raises an error"

    log = logging.getLogger(__name__)

    def take_action(self, parsed_args):
        self.log.info('causing error')
        raise RuntimeError('this is the expected exception')
