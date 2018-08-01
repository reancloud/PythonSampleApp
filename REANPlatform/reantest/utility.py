"""Utilities for Test CLI."""
import os
import logging
import sys
import time
import itertools
import validators
import test_sdk_client


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
        elif params.security_test_type is None:
            message = "Please Provide security test type."

        return message

    @staticmethod
    def validate_automation_test_inputs(params):
        """validate_automation_test_input."""
        # All the parameters validations goes in this function
        # log = logging.getLogger(__name__)
        # self.log.debug(params)
        message = ""

        # Validation for Test URL
        if not validators.url(params.url):
            message = "Please enter valid Application URL."

        # Validation for git url
        elif params.git_repository_url is None:
            message = "Please enter git_url parameters."
        elif params.app_name is None:
            message = "Please enter app_name parameters."
        elif params.command_to_run_test is None:
            message = "Please enter command_to_run_test parameters."
        elif params.automation_code_type is None:
            message = "Please enter automation_code_type parameters."
        elif params.report_file_name is None:
            message = "Please enter report_file parameters."
        elif params.output_directory_path is None:
            message = "Please enter output_dir parameters."
        elif params.test_suite is None:
            message = "Please enter test_suite parameters."

        # Validation for Browser list
        elif params.chrome is None and params.firefox is None and params.ie is None:
            message = "Please Provide at least one browser to Test."

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
        print("The request submitted successfully. Job Id is : ", job_id)

        if job_id is not None and hasattr(parsed_args, 'wait') and parsed_args.wait == "true":
            api_instance = test_sdk_client.RunTestApi()
            Utility.wait_while_job_running(api_instance, job_id)
