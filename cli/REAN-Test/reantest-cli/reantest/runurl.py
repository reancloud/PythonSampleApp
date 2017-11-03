import logging
from . import config
from . import utility 
from cliff.command import Command

import swagger_client
from swagger_client.rest import ApiException
from ast import literal_eval
import json



class RunURL(Command):
    "A simple command that prints a message."

    log = logging.getLogger(__name__)


    "runurltest"
    def get_parser(self, prog_name):
        parser = super(RunURL, self).get_parser(prog_name)
        
        # 'browser_list': 'BrowsersDto',
        # 'test_url': 'str',
        # 'text_to_search': 'str',
        # 'page_load_time_out': 'int',
        # 'type': 'str',
        # 'execution_strategy': 'str',
        # 'run_upa': 'str',
        # 'run_crawl': 'str'

        parser.add_argument('--test_url', '-u', help='Set url To test example:http://www.google.com.This option is mandatory', required=True)
        parser.add_argument('--text_to_search', '-s', help='Set the text to search.This option is mandatory', required=True)
        parser.add_argument('--page_load_time_out', '-p', help='Set the Page load timeout time in secs.This option is not mandatory')
        parser.add_argument('--execution_strategy', '-e', help='Set Execution Statraegy options boost/vmReuse.This option is mandatory', required=True)
        parser.add_argument('--run_upa', '-r', help='Set true if needs UPA test to run with the Test..This option is not mandatory')
        parser.add_argument('--run_crawl', '-c', help='Set true if needs Crawl test to run with the Test.This option is not mandatory')
        
        
        parser.add_argument('--chrome', '-C', help='Give the comma separated versions for Chrome to run test on..This option is not mandatory.')
        parser.add_argument('--firefox', '-F', help='Give the comma separated versions for Firefox to run test on..This option is not mandatory.')
        
        
        #parser.add_argument('--ie', '-I', help='message')
        #parser.add_argument('--opera', '-O', help='message')
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
            parsed_args.test_url,
            parsed_args.text_to_search,
            parsed_args.page_load_time_out,
            "urltest",#type
            parsed_args.execution_strategy,
            parsed_args.run_upa,
            parsed_args.run_crawl)
            

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
