"""Utility class contains all common method requried for CLI."""
import os
from os.path import basename
import base64
from base64 import b64decode
import json
import requests
import boto3
from Crypto import Random
from Crypto.Cipher import AES
import urllib3
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
                password = str(credentials.get('password'))
                if "AWS_LAMBDA_FUNCTION_NAME" in os.environ:
                    password = boto3.client('kms').decrypt(CiphertextBlob=b64decode(password))['Plaintext'].decode('utf-8')

                credentials = str(credentials.get('user_name')) + ":" + str(password)
            else:
                credentials = Utility.get_username_password_from_file()
            return credentials
        except Exception as exception:
            Utility.print_exception(exception)

    @staticmethod
    def encryptData(val):
        """Encrypts credentials."""
        raw = val.encode('utf-8')
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(PlatformConstants.REAN_SECRET_KEY.encode('utf-8'), AES.MODE_CFB, iv)
        encoded = base64.b64encode(iv + cipher.encrypt(raw))
        return encoded

    @staticmethod
    def decryptData(encoded):
        """Decrypts credentials."""
        enc = base64.b64decode(encoded)
        iv = enc[:16]
        cipher = AES.new(PlatformConstants.REAN_SECRET_KEY.encode('utf-8'), AES.MODE_CFB, iv)
        decoded = cipher.decrypt(enc[16:])
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
            Utility.print_exception(exception)

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
                    data_loaded = yaml.load(stream, Loader=yaml.FullLoader)
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
                    data_loaded = yaml.load(stream, Loader=yaml.FullLoader)
                config_property = data_loaded[PlatformConstants.PLATFORM_REFERENCE][prop]
                return config_property
        return None

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
            Utility.print_exception(exception)

    @staticmethod
    def write_to_file(output_file, content):
        """Write content to file."""
        with open(output_file, "w") as handle:
            handle.write(content)
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

    @staticmethod
    def get_zip_stream(curl_url):
        """Get zip stream."""
        headers = {'Authorization': Utility.get_user_credentials()}
        verify_ssl = Utility.get_config_property(PlatformConstants.VERIFY_SSL_CERTIFICATE_REFERENCE)
        if not verify_ssl:
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

        response = requests.get(curl_url, headers=headers, verify=verify_ssl)
        return response

    @staticmethod
    def get_serialized_json(content):
        """get_serialized_json."""
        return json.loads(content.decode('utf-8'))

    @staticmethod
    def get_parsed_serialized_json(content):
        """parse_serialized_json."""
        return json.dumps(Utility.get_serialized_json(content), indent=4, sort_keys=True)

    @staticmethod
    def validate_api_response(response):
        """validate_api_response."""
        err_codes = [500,403,404]
        for code in err_codes:
            if code == response.status_code:
                serialized_json = Utility.get_serialized_json(response.content)
                raise RuntimeError(serialized_json["message"])
