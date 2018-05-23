"""Configure platform."""
import os
import io
import getpass
import logging
import yaml
from deploy_sdk_client.rest import ApiException
from cliff.command import Command
from reanplatform.constants import Constants
from reanplatform.utility import Utility


class Configure(Command):
    """Configure platform."""

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        """get_parser."""
        parser = super(Configure, self).get_parser(prog_name)
        parser.add_argument('--username', '-u',
                            help='Platform username',
                            required=True
                            )
        parser.add_argument('--platform_url',
                            '-url',
                            help='Platform URL',
                            required=True
                            )
        parser.add_argument('--password',
                            '-p',
                            help='Platform password',
                            required=False
                            )
        return parser

    def createFile(self, parsed_args, path):
        """Create file of credentials."""
        if parsed_args.password:
            password = parsed_args.password
        else:
            password = getpass.getpass()

        data = {
            'deploy': {
                'host': parsed_args.platform_url,
                'username': Utility.encryptData(parsed_args.username),
                'password': Utility.encryptData(password)
            }
        }
        os.chdir(path + '/.' + Constants.PLATFORM_CONFIG_FILE_NAME)
        with io.open(Constants.PLATFORM_CONFIG_FILE_NAME + '.yaml', 'w', encoding='utf8') as outputfile:  # noqa: E501
            yaml.dump(data, outputfile, default_flow_style=False, allow_unicode=True)   # noqa: E501

    def take_action(self, parsed_args):
        """take_action."""
        try:
            path = os.path.expanduser('~')
            if os.path.exists(path + '/.\
                            ' + Constants.PLATFORM_CONFIG_FILE_NAME):
                self.createFile(parsed_args, path)
            else:
                os.makedirs(path + '/.' + Constants.PLATFORM_CONFIG_FILE_NAME)
                self.createFile(parsed_args, path)

        except ApiException as e:
            self.log.error(e)
