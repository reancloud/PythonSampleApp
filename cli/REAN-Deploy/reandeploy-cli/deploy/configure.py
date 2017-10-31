"Configure REAN-Deploy CLI"
import os
import io
import getpass
import logging
import yaml
from swagger_client.rest import ApiException
from cliff.command import Command
from deploy.constants import Constants
from deploy.utility import Utility


class Configure(Command):

    "Configure REAN-Deploy CLI"
    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(Configure, self).get_parser(prog_name)
        parser.add_argument('--username', '-u', help='Set username', required=True)
        return parser

    def createFile(self, parsed_args, path):
        data = {
            'deploy' : {
                'username' : Utility.encryptData(parsed_args.username),
                'password' : Utility.encryptData(getpass.getpass())
            }
        }
        os.chdir(path + '/.' + Constants.REAN_PLATFORM)
        with io.open(Constants.REAN_PLATFORM + '.yaml', 'w', encoding='utf8') as outputfile:
            yaml.dump(data, outputfile, default_flow_style=False, allow_unicode=True)

    def take_action(self, parsed_args):
        try:
            path = os.path.expanduser('~')
            if os.path.exists(path + '/.' + Constants.REAN_PLATFORM):
                self.createFile(parsed_args, path)
            else:
                os.makedirs(path + '/.' + Constants.REAN_PLATFORM)
                self.createFile(parsed_args, path)

        except ApiException as e:
            self.log.error(e)
