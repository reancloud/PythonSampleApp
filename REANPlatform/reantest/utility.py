"""Utilities for Test CLI."""
import logging
import sys
import time
import itertools
import validators
import test_sdk_client


class Utility():
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
    def validateInputs(params):
        """validate_input."""
        # All the parameters validations goes in this function
        # log = logging.getLogger(__name__)
        # self.log.debug(params)
        message = ""

        # Validation for Test URL
        if not validators.url(params.url):
            message = "Please enter valid Test URL."

        # #Valodation for Browser list
        # elif (params.firefox == None and
        #         params.chrome == None and
        #         params.ie == None and
        #         params.opera == None and
        #         params.safari == None and
        #         params.ios == None and
        #         params.ui_perf_analysis == None and
        #         params.device == None
        #         ):
        #
        #     message = "Please Provide atleast one browser to Test."

        return message

    @staticmethod
    def validateSecurityTestInputs(params):
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
    def validateAutomationTestInputs(params):
        """validate_automation_test_input."""
        # All the parameters validations goes in this function
        # log = logging.getLogger(__name__)
        # self.log.debug(params)
        message = ""

        # Validation for Test URL
        if not validators.url(params.url):
            message = "Please enter valid Application URL."

        # Validation for git url
        elif params.git_url is None and params.app_name is None and params.command_to_run_test is None and params.automation_code_type is None and params.report_file is None and params.output_dir is None and params.test_suite is None:
            message = "Please enter all requried parameters."

        # Valodation for Browser list
        elif params.firefox is None and params.chrome is None and params.ie is None and params.opera is None and params.safari is None and params.ios is None and params.ui_perf_analysis is None and params.device is None:
            message = "Please Provide atleast one browser to Test."

        return message

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
