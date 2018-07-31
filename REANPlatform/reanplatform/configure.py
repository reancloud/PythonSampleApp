"""Configure platform."""
import os
import io
import getpass
import logging
import yaml
from cliff.command import Command
from deploy_sdk_client.rest import ApiException
from reanplatform.constants import Constants
from reanplatform.utilityconstants import PlatformConstants
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
        parser.add_argument('--platform_base_url',
                            '-url',
                            help='Platform Base URL(e.g https://reanplatform.com)',
                            required=True
                           )
        parser.add_argument('--password',
                            '-p',
                            help='Platform password',
                            required=False
                           )
        parser.add_argument('--auto_approve',
                            '-y',
                            help='Skip interactive approval before updating user credentials.',
                            required=False,
                            action='store_true'
                           )
        parser.add_argument('--disable_verify_ssl',
                            '-d',
                            help='Verifying SSL certificate when calling API from https server.',
                            required=False,
                            action='store_false'
                           )
        return parser

    def createFile(self, parsed_args, path):
        """Create file of credentials."""
        os.chdir(path + '/.' + Constants.PLATFORM_CONFIG_FILE_NAME)
        if os.path.exists(path + '/.' + Constants.PLATFORM_CONFIG_FILE_NAME + '/' + Constants.PLATFORM_CONFIG_FILE_NAME + '.yaml'):
            if parsed_args.auto_approve:
                self.__update_credentials(parsed_args)
            else:
                user_input = input('REAN CLI is already configured. Are you sure you want to update existing credentials (y/n): ')
                if user_input == 'y' or user_input == 'Y':
                    self.__update_credentials(parsed_args)
        else:
            self.__update_credentials(parsed_args)

    def take_action(self, parsed_args):
        """take_action."""
        try:
            path = os.path.expanduser('~')
            if os.path.exists(path + '/.' + Constants.PLATFORM_CONFIG_FILE_NAME):
                self.createFile(parsed_args, path)
            else:
                os.makedirs(path + '/.' + Constants.PLATFORM_CONFIG_FILE_NAME)
                self.createFile(parsed_args, path)

        except ApiException as exception:
            self.log.error(exception)

    def __parse_base_url(self, base_url):
        """Parse base url.

        Removes extra '/' if any from url.
        """
        if base_url[-1] == '/':
            return base_url[:-1]
        return base_url

    def __update_credentials(self, parsed_args):
        """Update credentials."""
        data = self.__get_data(parsed_args)
        with io.open(Constants.PLATFORM_CONFIG_FILE_NAME + '.yaml', 'w', encoding='utf8') as outputfile:  # noqa: E501
            yaml.dump(data, outputfile, default_flow_style=False, allow_unicode=True)   # noqa: E501

    def __get_data(self, parsed_args):
        """Get file data."""
        if parsed_args.password:
            password = parsed_args.password
        else:
            password = getpass.getpass()

        data = {
            PlatformConstants.PLATFORM_REFERENCE: {
                PlatformConstants.BASE_URL_REFERENCE: self.__parse_base_url(parsed_args.platform_base_url),
                PlatformConstants.USER_NAME_REFERENCE: Utility.encryptData(parsed_args.username),
                PlatformConstants.PASSWORD_REFERENCE: Utility.encryptData(password),
                PlatformConstants.VERIFY_SSL_CERTIFICATE_REFERENCE: parsed_args.disable_verify_ssl
            }
        }
        return data
