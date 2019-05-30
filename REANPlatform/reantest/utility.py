"""Utilities for Test CLI."""
import os
import json
import logging
import sys
import time
import itertools
import uuid
import urllib3
import requests
import validators

import test_sdk_client
from test_sdk_client.api_client import ApiClient
from test_sdk_client.configuration import Configuration
from test_sdk_client.rest import ApiException

from reanplatform.set_header import set_header_parameter
from reanplatform.utility import Utility as PlatformUtility
from reanplatform.utilityconstants import PlatformConstants

from reantest.constants import TestConstants


class Utility:
    """generate the swagger client in this class."""

    log = logging.getLogger(__name__)

    @staticmethod
    def get_unique_seq(seq):
        """get_unique_sequence."""
        # order preserving
        checked = list(set(seq))
        return checked

    @staticmethod
    def get_browser_dto(params):
        """get_browser_DTO."""
        log = logging.getLogger(__name__)
        log.debug(params)
        browser_list = test_sdk_client.BrowsersDto()

        if params.firefox is not None:
            firefox = Utility.get_unique_seq(params.firefox.split(","))
            log.debug(firefox)
            browser_list.firefox = firefox
        if params.chrome is not None:
            chrome = Utility.get_unique_seq(params.chrome.split(","))
            log.debug(chrome)
            browser_list.chrome = chrome

        # log.debug(browser_list)
        return browser_list

    @staticmethod
    def validate_url_test_inputs(params):
        """Validate url and browsers input."""
        # All the parameters validations goes in this function

        message = ""
        # Validation for Test URL
        if not validators.url(params.url):
            message = "Please enter valid Test URL."

        # Validation for Browser list
        if params.chrome is None and params.firefox is None and params.ie is None:
            message = "Please Provide at least one browser to Test."
        return message

    @staticmethod
    def validate_scale_test_inputs(params):
        """Validate url and browsers input."""
        # All the parameters validations goes in this function

        message = ""
        # # Validation for Test URL
        # if not validators.url(params.url):
        #     message = "Please enter valid Test URL."

        # Validation for Browser list
        if params.chrome is None and params.firefox is None:
            message = "Please Provide at least one browser to Test."

        if params.use_code_upload == 'true':
            if params.code_file_name == "test":
                message = "Please provide valid file path to upload code."
        else:
            if params.git_repository_url is None:
                message = "Please provide valid git credentials"

        return message

    @staticmethod
    def validate_url(params):
        """Validate URL."""
        message = ""
        if not validators.url(params.url):
            message = "Please enter valid Test URL."
        return message

    @staticmethod
    def validate_security_test_inputs(params):
        """validate_security_test_inputs."""
        # All the parameters validations goes in this function
        # log = logging.getLogger(__name__)
        # self.log.debug(params)
        message = ""

        # Validation for Test URL
        if not validators.url(params.url):
            message = "Please enter valid Test URL."

        # Validation for Security test type
        elif params.security_test_type != '@app_scan' and params.security_test_type != '@http_headers' and params.security_test_type != '@app_scan,@http_headers' and params.security_test_type != '@http_headers,@app_scan':
            message = "Please Provide valid security test type."

        return message

    @staticmethod
    def validate_path(params):
        """Validate system path."""
        return os.path.isdir(params.output_directory)

    @staticmethod
    def open_file(path):
        """Validate system path and open file."""
        if not os.path.isfile(path):
            raise RuntimeError('file %s does not exists' % path)

        return open(path, "r")

    @staticmethod
    def wait_while_job_running(api_instance, job_id):
        """Wait while job running."""
        job_status = api_instance.get_job_status(job_id)
        spinner = itertools.cycle(['-', '/', '|', '\\'])
        print("The Status of Job_Id:", job_id, " is ", job_status)
        while "RUNNING" in job_status:
            for _ in range(50):
                sys.stdout.write(next(spinner))
                sys.stdout.flush()
                time.sleep(0.1)
                sys.stdout.write('\b')
            job_status = api_instance.get_job_status(job_id)
        print("The Status of Job_Id:", job_id, " is ", job_status)

    @staticmethod
    def execute_test(body, parsed_args, log, method_to_execute):
        """Execute Test."""
        job_id = method_to_execute(body)
        log.debug("Response is------------: %s ", job_id)
        print("The request Job/test submitted successfully. Job Id is : ", job_id)

        if job_id is not None and hasattr(parsed_args, 'wait') and parsed_args.wait == "true":
            api_instance = test_sdk_client.RunTestApi(Utility.set_headers())
            Utility.wait_while_job_running(api_instance, job_id)

    @staticmethod
    def print_exception(exception):
        """Print exception method."""
        print("Exception message: ")
        if isinstance(exception, RuntimeError):
            print(exception)
        elif isinstance(exception, ApiException):
            if isinstance(exception.body, str):
                err = json.loads(exception.body)
            if isinstance(exception.body, bytes):
                err = json.loads(exception.body.decode("utf-8"))
            print("Status : %s ,Message : %s" % (err['status'], err['message']))
        elif isinstance(exception, Exception):
            print(exception)

    @staticmethod
    def set_headers():
        """Set headers."""
        return set_header_parameter(Utility.create_api_client(), PlatformUtility.get_url(TestConstants.TEST_URL))

    @staticmethod
    def create_api_client():
        """Create API client."""
        verify_ssl = PlatformUtility.get_config_property(PlatformConstants.VERIFY_SSL_CERTIFICATE_REFERENCE)
        if not verify_ssl:
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        Configuration().verify_ssl = verify_ssl
        api_client = ApiClient()
        return api_client

    @staticmethod
    def upload_code(file_path, app_name):
        """Servlet API call to upload automation code manually."""
        # This module will call REANTest upload servlet.
        # This servlet upload code file to s3 bucket of provider and that s3 object name will get used for test.

        file_name = 'code-' + app_name + '-' + uuid.uuid4().hex

        if not os.path.isfile(file_path):
            raise RuntimeError('file %s does not exists' % file_path)

        file_extension = os.path.splitext(file_path)[1].lower()

        # REANTest only support zip file to upload
        if file_extension != ".zip":
            raise RuntimeError('Invalid file type %s, test only support zip file upload' % file_path)

        file = {'file': open(file_path, 'rb')}

        credentials = PlatformUtility.get_user_credentials()
        HEADERS = {'Authorization': credentials}
        params = {'filename': file_name, 'userId': credentials.split(':')[0], 'awspecIO': 'null'}

        responce = requests.post(PlatformUtility.get_url('/api/reantest/TestNow/uploadCode'),
                                 headers=HEADERS, files=file, data=params)

        if responce.status_code != 200:
            raise RuntimeError('Failed to upload file, %s' % file_path)

        return file_name
