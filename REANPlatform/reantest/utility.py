"""Utilities for Test CLI."""
import logging
import test_sdk_client
from test_sdk_client.rest import ApiException
import validators


class Utility():
    """generate the swagger client in this class."""

    log = logging.getLogger(__name__)

    @staticmethod
    def getUniqueSeq(seq):
        """get_unique_sequence."""
        # order preserving
        checked = list(set(seq))
        return checked

    @staticmethod
    def getBrowserDTO(params):
        """get_browser_DTO."""
        log = logging.getLogger(__name__)
        log.debug(params)
        browser_list = test_sdk_client.BrowsersDto()

        if(params.firefox is not None):
            firefox = Utility.getUniqueSeq(params.firefox.split(","))
            log.debug(firefox)
            browser_list.firefox = firefox
        if(params.chrome is not None):
            chrome = Utility.getUniqueSeq(params.chrome.split(","))
            log.debug(chrome)
            browser_list.chrome = chrome

        # log.debug(browser_list)
        return browser_list

    @staticmethod
    def validateInputs(self, params):
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
    def validateSecurityTestInputs(self, params):
        """validate_security_test_inputs."""
        # All the parameters validations goes in this function
        # log = logging.getLogger(__name__)
        # self.log.debug(params)
        message = ""

        # Validation for Test URL
        if not validators.url(params.url):
            message = "Please enter valid Test URL."

        # Validation for Security test type
        elif (params.security_test_type is None
        ):

            message = "Please Provide security test type."

        return message

    @staticmethod
    def validateAutomationTestInputs(self, params):
        """validate_automation_test_input."""
        # All the parameters validations goes in this function
        # log = logging.getLogger(__name__)
        # self.log.debug(params)
        message = ""

        # Validation for Test URL
        if not validators.url(params.url):
            message = "Please enter valid Application URL."

        # Validation for git url
        elif (params.git_url is None and params.app_name is None and params.command_to_run_test is None and params.automation_code_type is None and params.report_file is None and params.output_dir is None and params.test_suite is None
        ):
            message = "Please enter all requried parameters."

        # Valodation for Browser list
        elif (params.firefox is None and params.chrome is None and params.ie is None and params.opera is None and params.safari is None and params.ios is None and params.ui_perf_analysis is None and params.device is None
        ):

            message = "Please Provide atleast one browser to Test."

        return message
