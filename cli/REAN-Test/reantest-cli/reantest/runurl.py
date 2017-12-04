import logging
from . import config
from . import utility 
from cliff.command import Command

import swagger_client
from swagger_client.rest import ApiException
from ast import literal_eval
import json



class RunURLTest(Command):

    log = logging.getLogger(__name__)


    "run-url-test"
    def get_parser(self, prog_name):
        parser = super(RunURLTest, self).get_parser(prog_name)
        
        # 'browser_list': 'BrowsersDto',
        # 'test_url': 'str',
        # 'text_to_search': 'str',
        # 'page_load_time_out': 'int',
        # 'type': 'str',
        # 'execution_strategy': 'str',
        # 'run_upa': 'str',
        # 'run_crawl': 'str'

        parser.add_argument('--url', '-u', help='Set url To test example:http://www.google.com.', required=True)
        parser.add_argument('--text_to_search', '-t', help='Set the text to search.', required=True)
        parser.add_argument('--page_load_time_out', '-p', help='Set the Page load timeout time in secs.')
        parser.add_argument('--upa', '-r', help='Set true if needs UPA test to run with the Test.')
        parser.add_argument('--crawl', '-c', help='Set true if needs Crawl test to run with the Test.')
        
        
        parser.add_argument('--chrome', '-C', help='Give the comma separated versions for Chrome to run test on.')
        parser.add_argument('--firefox', '-F', help='Give the comma separated versions for Firefox to run test on.')
        
        
        parser.add_argument('--ie', '-I', help='Give the comma separated versions for IE to run test on.')
        parser.add_argument('--opera', '-O', help='Give the comma separated versions for Opera to run test on.')
        #parser.add_argument('--safari', '-S', help='message')
        #parser.add_argument('--ios', '-A', help='message')
        #parser.add_argument('--ui_perf_analysis', '-U', help='message')
        #parser.add_argument('--device', '-D', help='message')


        return parser

    def take_action(self, parsed_args):

        # self.log.debug("Inside the take action for runurltest")
        self.log.debug(parsed_args)

        browser_list = utility.Utility.getBrowserDTO(parsed_args)
        self.log.debug(browser_list)

        error_message = utility.Utility.validateInputs(self,parsed_args)
        if(error_message != "") :
            self.app.stdout.write(error_message)
            return
        

        print(parsed_args.firefox)

        #order should be maintained as the constructor takes values as parameter in the same order.  
        body = swagger_client.UrlTestDto(
            browser_list,
            parsed_args.url,
            parsed_args.text_to_search,
            parsed_args.page_load_time_out,
            "urltest",#type
            "boost", #execution_strategy
            parsed_args.upa,
            parsed_args.crawl)
            

        self.log.debug(body)
        
        try:
             apiInstance = swagger_client.RunJobsApi()
             api_response = apiInstance.submit_url_test_job(body)
             self.log.debug(api_response)
             print(api_response)
        except Exception as e:
             self.log.error("Exception when calling RunUrlTest->submit_url_test_job: %s\n" % e)


class Error(Command):
    "Always raises an error"

    log = logging.getLogger(__name__)

    def take_action(self, parsed_args):
        self.log.info('causing error')
        raise RuntimeError('this is the expected exception')
