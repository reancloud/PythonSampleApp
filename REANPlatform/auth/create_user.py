"""Get Users module."""
import logging
import re
from cliff.command import Command
import authnz_sdk_client
from authnz_sdk_client.rest import ApiException
from reanplatform.utility import Utility
from auth.utility import AuthnzUtility


class CreateUser(Command):
    """create user."""

    log = logging.getLogger(__name__)
    _epilog = 'Example : \n\t rean-auth create-user --name <name> --username <user_name> --email <email_id> ' \
              '--password <password>'

    def get_parser(self, prog_name):
        """get_parser."""
        parser = super(CreateUser, self).get_parser(prog_name)
        parser.add_argument('--name', '-n', help='Users name', required=True)
        parser.add_argument('--username', '-u', help='Users username ', required=True)
        parser.add_argument('--email', '-e', help='User email', required=True)
        parser.add_argument('--password', '-p', help='password', required=True)
        parser.add_argument('--output', '-o', help="Write output to <file> instead of stdout.",
                            required=False)
        return parser

    @staticmethod
    def validate_input(parsed_args):
        """Validate input."""
        message = ""
        if len(parsed_args.password) < 8 or len(parsed_args.password) > 50:
            message = "Make sure your password lenghth is between 8 to 50 letters"
        elif re.search('[0-9]', parsed_args.password) is None:
            message = "Make sure your password has a number in it"
        elif re.search('[A-Z]', parsed_args.password) is None:
            message = "Make sure your password has a capital letter in it"
        elif re.search('[a-z]', parsed_args.password) is None:
            message = "Make sure your password has a LowerCase letter in it"

        elif not parsed_args.name:
            message = "Name Cannot be empty."
        elif not parsed_args.username:
            message = "username Cannot be empty."
        elif not parsed_args.email or not CreateUser.validate_email(parsed_args.email):
            message = "Error with email."
        if message:
            raise RuntimeError(message)

    @staticmethod
    def validate_email(parsed_args):
        """Validate email."""
        return bool(re.match(r"[^@]+@[^@]+\.[^@]+", parsed_args))

    def take_action(self, parsed_args):
        """Take action."""
        try:
            CreateUser.validate_input(parsed_args)
            api_instance = authnz_sdk_client.UserControllerApi(AuthnzUtility.set_headers())

            userdto = authnz_sdk_client.UserDto(name=parsed_args.name, email=parsed_args.email,
                                                username=parsed_args.username)
            userauthenticationDto = authnz_sdk_client.UserAuthenticationDto(
                password=parsed_args.password)
            userdto.user_authentication = userauthenticationDto

            api_response = api_instance.create(body=userdto)
            print(api_response)
            Utility.print_output_as_str("User saved successfully :{}, id: {}"
                                        .format(api_response.name, api_response.id), parsed_args.output)
        except ApiException as api_exception:
            Utility.print_exception(api_exception)
