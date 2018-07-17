import logging
from . import utility
from cliff.command import Command

import test_sdk_client
from test_sdk_client.rest import ApiException
from ast import literal_eval
import json



class RunSecurityTest(Command):
    """Run security test"""

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(RunSecurityTest, self).get_parser(prog_name)

        # 'browser_list': 'BrowsersDto',
        # 'test_url': 'str',
        # 'ty-tesr
        # 'page_load_time_out': 'int',
        # 'type': 'str',
        # 'execution_strategy': 'str',
        # 'run_upa': 'str',
        # 'run_crawl': 'str'
        # 'securityTest': 'str'
        # 'securityTestType': 'str'

        parser.add_argument('--url', '-u', help='Set url To test example:http://www.google.com.', required=True)
        parser.add_argument('--security_test_type', '-t', help='Set Security test type example:@app_scan/@http_headers.', required=True)

        #parser.add_argument('--chrome', '-C', help='Give the comma separated versions for Chrome to run test on.')
        #parser.add_argument('--firefox', '-F', help='Give the comma separated versions for Firefox to run test on.')

        return parser

    def take_action(self, parsed_args):

        # self.log.debug("Inside the take action for runurltest")
        self.log.debug(parsed_args)

        error_message = utility.Utility.validateSecurityTestInputs(self,parsed_args)
        if(error_message != "") :
            self.app.stdout.write(error_message)
            return

        #order should be maintained as the constructor takes values as parameter in the same order.
        body = test_sdk_client.SecurityTestDto(
            None,
            parsed_args.url,
            "Gmail",#text_to_search
            "10",#page_load_time_out
            "securitytest",#type
            "security",#executionStrategy
            "false",#run_upa
            "false",#run_crawl
            "true",#securityTest
            parsed_args.security_test_type)


        self.log.debug(body)

        try:
             apiInstance = test_sdk_client.RunJobsApi()
             api_response = apiInstance.submit_security_test_job(body)
             self.log.debug(api_response)
             print(api_response)
        except Exception as e:
             self.log.error("Exception when calling RunSecurityTest->submit_security_test_job: %s\n" % e)


class Error(Command):
    "Always raises an error"

    log = logging.getLogger(__name__)

    def take_action(self, parsed_args):
        self.log.info('causing error')
        raise RuntimeError('this is the expected exception')
