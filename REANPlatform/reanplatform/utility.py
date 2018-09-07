"""Utility class contains all common method requried for CLI."""
import os
from os.path import basename
import base64
import json
from Crypto.Cipher import XOR
import yaml
from reanplatform.utilityconstants import PlatformConstants


class Utility(object):
    """Utility class contains all common method requried for CLI."""

    @staticmethod
    def get_user_credentials():
        """Get configured username and password."""
        try:
            credentials = Utility.get_env_username_password_and_baseurl()
            if credentials and credentials.get('user_name') and credentials.get('password'):
                credentials = str(credentials.get('user_name')) + ":" + str(credentials.get('password'))
            else:
                credentials = Utility.get_username_password_from_file()
            return credentials
        except Exception as exception:
            print('Could not get username and password.')
            return None

    @staticmethod
    def encryptData(val):
        """Encrypts credentials."""
        cipher = XOR.new(PlatformConstants.REAN_SECRET_KEY)
        encoded = base64.b64encode(cipher.encrypt(val))
        return encoded

    @staticmethod
    def decryptData(encoded):
        """Decrypts credentials."""
        cipher = XOR.new(PlatformConstants.REAN_SECRET_KEY)
        decoded = cipher.decrypt(base64.b64decode(encoded))
        return decoded

    @staticmethod
    def print_exception(exception):
        """Print exception method."""
        print("Exception message: ")
        err = json.loads(exception.body)
        print("%s %s" % (err['message'], err['status']))

    @staticmethod
    def get_url(host_url):
        """Get full URL."""
        try:
            base_url = Utility.get_env_username_password_and_baseurl()
            if base_url and base_url.get('base_url'):
                base_url = str(base_url.get('base_url'))
            else:
                base_url = Utility.get_config_property(PlatformConstants.BASE_URL_REFERENCE)
            return base_url + host_url
        except Exception as exception:
            print('Could not get base url.')
            return None

    @staticmethod
    def get_parsed_json(json_object):
        """Get parsed json."""
        return json.dumps(
            json_object,
            default=lambda o: o.__dict__,
            sort_keys=True, indent=4
        ).replace("\"_", '"')

    @staticmethod
    def get_env_username_password_and_baseurl():
        """Get Environment variables."""
        try:
            credentials = {
                'user_name': os.environ[PlatformConstants.ENV_USER_NAME_REFERENCE],
                'password': os.environ[PlatformConstants.ENV_PASSWORD_REFERENCE],
                'base_url': os.environ[PlatformConstants.ENV_BASE_URL_REFERENCE]
            }
            return credentials
        except KeyError:
            return False

    @staticmethod
    def get_username_password_from_file():
        """Get user name and password from config file."""
        path = os.path.expanduser('~')
        if os.path.exists(path + '/.' + PlatformConstants.PLATFORM_CONFIG_FILE_NAME):
            config_file_name = path + '/.' + PlatformConstants.PLATFORM_CONFIG_FILE_NAME + '/' + PlatformConstants.PLATFORM_CONFIG_FILE_NAME + '.yaml'
            if os.path.isfile(config_file_name):
                with open(config_file_name, 'r') as stream:    # noqa: E501
                    data_loaded = yaml.load(stream)
                username = Utility.decryptData(
                    data_loaded[PlatformConstants.PLATFORM_REFERENCE][PlatformConstants.USER_NAME_REFERENCE]).decode('utf-8')
                password = Utility.decryptData(
                    data_loaded[PlatformConstants.PLATFORM_REFERENCE][PlatformConstants.PASSWORD_REFERENCE]).decode('utf-8')
                credentials = str(username) + ":" + str(password)
                return credentials
        return None

    @staticmethod
    def get_config_property(prop):
        """Get ssl verify certification status from config file."""
        path = os.path.expanduser('~')
        if os.path.exists(path + '/.' + PlatformConstants.PLATFORM_CONFIG_FILE_NAME):
            config_file_name = path + '/.' + PlatformConstants.PLATFORM_CONFIG_FILE_NAME + '/' + PlatformConstants.PLATFORM_CONFIG_FILE_NAME + '.yaml'
            if os.path.isfile(config_file_name):
                with open(config_file_name, 'r') as stream:    # noqa: E501
                    data_loaded = yaml.load(stream)
                config_property = data_loaded[PlatformConstants.PLATFORM_REFERENCE][prop]
                return config_property

    @staticmethod
    def create_output_file(filepath, obj):
        """Create Output file."""
        with open(basename(filepath), 'w') as outfile:
            outfile.write(Utility.get_parsed_json(obj))

    @staticmethod
    def print_output_as_str(output, output_file=None):
        """Print output as string."""
        if output_file:
            Utility.print_output(output, output_file, PlatformConstants.STR_REFERENCE)
        else:
            print(output)

    @staticmethod
    def print_output_as_dict(output, output_file=None):
        """Print output as string."""
        Utility.print_output(output, output_file, PlatformConstants.DICT_REFERENCE)

    @staticmethod
    def print_output_as_table(output, output_file=None):
        """Print output as string."""
        if output_file:
            Utility.print_output(output, output_file, PlatformConstants.TABLE_REFERENCE)
        else:
            print(output)

    @staticmethod
    def print_output(output, output_file, output_format):
        """Print output in given format."""
        try:
            if output_file:
                if output_format == PlatformConstants.DICT_REFERENCE:
                    Utility.write_to_file(output_file, Utility.get_parsed_json(output))
                elif output_format == PlatformConstants.TABLE_REFERENCE or output_format == PlatformConstants.STR_REFERENCE:
                    Utility.write_to_file(output_file, output)
            else:
                if isinstance(output, (list, str)):
                    print(Utility.get_parsed_json(output))
                else:
                    print(output)
        except OSError as os_error:
            print(os_error)
        except Exception as exception:
            print(exception)

    @staticmethod
    def write_to_file(output_file, content):
        """Write content to file."""
        with open(output_file, "w") as handle:
            filedata = handle.write(content)
            handle.close()

    @staticmethod
    def extract_json_data(file_path):
        """Extract json value."""
        raw_data = Utility.fetch_file_data(file_path)
        json_data = json.loads(raw_data)
        return json_data

    @staticmethod
    def extract_str_data(file_path):
        """Extract json value."""
        raw_data = Utility.fetch_file_data(file_path)
        return raw_data

    @staticmethod
    def fetch_file_data(file_path):
        """Fetch file data."""
        if file_path.lstrip().startswith('@data:'):
            return file_path.lstrip()[6:]
        else:
            if not os.path.isfile(file_path):
                raise RuntimeError('File %s does not exists' % file_path)

            with open(file_path, "r") as handle:
                raw_data = handle.read()
                return raw_data
            return None
