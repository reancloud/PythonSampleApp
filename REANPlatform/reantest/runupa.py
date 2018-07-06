import logging
from . import config
from . import utility 
from cliff.command import Command

import test_sdk_client
from test_sdk_client.rest import ApiException
from ast import literal_eval
import json
import time



class RunUPA(Command):

    log = logging.getLogger(__name__)


    "runupatest"
    def get_parser(self, prog_name):
        parser = super(RunUPA, self).get_parser(prog_name)
        
        # 'browser_list': 'BrowsersDto',
        # 'test_url': 'str',
        # 'text_to_search': 'str',
        # 'page_load_time_out': 'int',
        # 'type': 'str',
        # 'execution_strategy': 'str',
        # 'run_upa': 'str',
        # 'run_crawl': 'str'

        parser.add_argument('--url', '-u', help='Set upa To test example:http://www.google.com.', required=True)
        parser.add_argument('--text_to_search', '-s', help='Set the text to search.', required=True)
        parser.add_argument('--page_load_time_out', '-p', help='Set the Page load timeout time in secs.')
        parser.add_argument('--upa', '-r', help='Set true if needs UPA test to run with the Test.')
        parser.add_argument('--crawl', '-c', help='Set true if needs Crawl test to run with the Test.')
        
        
        parser.add_argument('--chrome', '-C', help='Give the comma separated versions for Chrome to run test on..This option is not mandatory.')
        parser.add_argument('--firefox', '-F', help='Give the comma separated versions for Firefox to run test on..This option is not mandatory.')
        parser.add_argument('--wait', '-w', help='Set to true for wait until job to finish.')
        #parser.add_argument('--ie', '-I', help='Give the comma separated versions for IE to run test on.')
        #parser.add_argument('--opera', '-O', help='Give the comma separated versions for Opera to run test on.')

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
        body = swagger_client.UpaTestDto(
            browser_list,
            parsed_args.url,
            parsed_args.text_to_search,
            parsed_args.page_load_time_out,
            "upatest",#type
            "boost",  # execution_strategy
            parsed_args.upa,
            parsed_args.crawl)
            

        self.log.debug(body)
        
        try:
             apiInstance = test_sdk_client.RunJobsApi()
             job_Id = apiInstance.submit_upa_test_job(body)
             self.log.debug("Response for UPA Test is------------: %s \n" % job_Id)
             print("The UPA Test submitted successfully. Job Id is : ", job_Id)

             if (job_Id != None and parsed_args.wait =="true"):
                 apiInstance = test_sdk_client.RunTestApi()
                 job_status = apiInstance.get_job_status(job_Id)
                 while ("RUNNING" in job_status):
                    print("The Status of Job_Id:",job_Id," is  ", job_status)
                    time.sleep(5)
                 print("The Status of Job_Id:", job_Id, " is  ", job_status)

        except Exception as e:
             self.log.error("Exception when calling RunUpaTest->submit_upa_test_job: %s\n" % e)


class Error(Command):
    "Always raises an error"

    log = logging.getLogger(__name__)

    def take_action(self, parsed_args):
        self.log.info('causing error')
        raise RuntimeError('this is the expected exception')
