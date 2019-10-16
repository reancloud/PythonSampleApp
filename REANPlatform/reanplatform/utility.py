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
    """Utility class contains all common method required for CLI."""

    @staticmethod
    def get_user_credentials():
        """Get configured username and password."""
        try:
            configuration_details = Utility.get_configuration_details()

            if configuration_details and configuration_details.get(PlatformConstants.USER_NAME_REFERENCE) \
                    and configuration_details.get(PlatformConstants.PASSWORD_REFERENCE):
                return str(configuration_details.get(PlatformConstants.USER_NAME_REFERENCE)) + ":" + \
                       str(configuration_details.get(PlatformConstants.PASSWORD_REFERENCE))
            else:
                print("CLI is not configured")
        except Exception as exception:
            Utility.print_exception(exception)

    @staticmethod
    def get_configuration_details():
        """Get configuration details"""

        configuration_details = Utility.get_config_details_from_environment()
        if Utility.is_valid_configuration(configuration_details):
            return configuration_details

        configuration_details = Utility.get_configuration_details_from_path()
        if Utility.is_valid_configuration(configuration_details):
            return configuration_details

        configuration_details = Utility.get_configuration_details_from_file()
        if Utility.is_valid_configuration(configuration_details):
            return configuration_details

    @staticmethod
    def is_valid_configuration(configuration_details):
        if configuration_details and configuration_details[PlatformConstants.USER_NAME_REFERENCE] \
                and configuration_details[PlatformConstants.PASSWORD_REFERENCE] \
                and configuration_details[PlatformConstants.BASE_URL_REFERENCE] \
                and configuration_details[PlatformConstants.VERIFY_SSL_CERTIFICATE_REFERENCE]:
            # Validate certificate path if verify ssl is enable
            return True
        else:
            return False

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
            configuration_details = Utility.get_configuration_details()
            return configuration_details[PlatformConstants.BASE_URL_REFERENCEt] + host_url
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
    def get_config_details_from_environment():
        """Get Environment variables."""
        try:
            credentials = {
                PlatformConstants.USER_NAME_REFERENCE: os.environ[PlatformConstants.ENV_USER_NAME_REFERENCE],
                PlatformConstants.PASSWORD_REFERENCE: os.environ[PlatformConstants.ENV_PASSWORD_REFERENCE],
                PlatformConstants.BASE_URL_REFERENCE: os.environ[PlatformConstants.ENV_BASE_URL_REFERENCE],
                PlatformConstants.VERIFY_SSL_CERTIFICATE_REFERENCE: os.environ[
                    PlatformConstants.ENV_VERIFY_SSL_CERTIFICATE_REFERENCE]
            }
            return credentials
        except KeyError:
            return False

    @staticmethod
    def get_configuration_details_from_path():
        """Get credentials from provided config file."""
        try:
            if os.environ[PlatformConstants.ENV_VERIFY_SSL_CERTIFICATE_REFERENCE]:
                if os.path.exists(PlatformConstants.ENV_VERIFY_SSL_CERTIFICATE_REFERENCE):

                    with open(os.environ[PlatformConstants.ENV_VERIFY_SSL_CERTIFICATE_REFERENCE], "r") as f:
                        yaml_object = yaml.safe_load(f)

                    for k, v in yaml_object.items():
                        actual_yaml = v

                    credentials = {
                        PlatformConstants.USER_NAME_REFERENCE: actual_yaml[PlatformConstants.USER_NAME_REFERENCE],
                        PlatformConstants.PASSWORD_REFERENCE: actual_yaml[PlatformConstants.PASSWORD_REFERENCE],
                        PlatformConstants.BASE_URL_REFERENCE: actual_yaml[PlatformConstants.BASE_URL_REFERENCE],
                        PlatformConstants.VERIFY_SSL_CERTIFICATE_REFERENCE: actual_yaml[PlatformConstants.VERIFY_SSL_CERTIFICATE_REFERENCE]
                    }
                    return credentials
        except Exception:
            print("Failed to read credential from provided configuration file path")

    @staticmethod
    def get_configuration_details_from_file():
        """Get user name and password from config file."""
        path = os.path.expanduser('~')
        if os.path.exists(path + '/.' + PlatformConstants.PLATFORM_CONFIG_FILE_NAME):
            config_file_name = path + '/.' + PlatformConstants.PLATFORM_CONFIG_FILE_NAME + '/' + PlatformConstants.PLATFORM_CONFIG_FILE_NAME + '.yaml'
            if os.path.isfile(config_file_name):
                with open(config_file_name, 'r') as stream:  # noqa: E501
                    data_loaded = yaml.load(stream, Loader=yaml.FullLoader)
                username = ''
                password = ''
                try:
                    username = Utility.decryptData(
                        data_loaded[PlatformConstants.PLATFORM_REFERENCE][PlatformConstants.USER_NAME_REFERENCE]).decode('utf-8')
                    password = Utility.decryptData(
                        data_loaded[PlatformConstants.PLATFORM_REFERENCE][PlatformConstants.PASSWORD_REFERENCE]).decode('utf-8')
                except base64.binascii.Error:
                    username = data_loaded[PlatformConstants.PLATFORM_REFERENCE][PlatformConstants.USER_NAME_REFERENCE]
                    password = data_loaded[PlatformConstants.PLATFORM_REFERENCE][PlatformConstants.PASSWORD_REFERENCE]

                credentials = {
                    PlatformConstants.USER_NAME_REFERENCE: username,
                    PlatformConstants.PASSWORD_REFERENCE: password,
                    PlatformConstants.BASE_URL_REFERENCE: data_loaded[PlatformConstants.BASE_URL_REFERENCE],
                    PlatformConstants.VERIFY_SSL_CERTIFICATE_REFERENCE: data_loaded[PlatformConstants.VERIFY_SSL_CERTIFICATE_REFERENCE]
                }

                return credentials
        return None

    @staticmethod
    def get_config_property(prop):
        """Get ssl verify certification status from config file."""
        configuration_details = Utility.get_configuration_details()
        return configuration_details.get(prop)

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
    def handleInvalidResponse(response, expectedStatus):
        """validate_api_response."""
        if response.status_code is not expectedStatus:
            serialized_json = Utility.get_serialized_json(response.content)
            raise RuntimeError(serialized_json["message"])
