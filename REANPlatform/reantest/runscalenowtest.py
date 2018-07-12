import logging
from . import utility
from cliff.command import Command

import test_sdk_client
from test_sdk_client.rest import ApiException
from ast import literal_eval
import json
import time



class RunScaleNowTest(Command):

    log = logging.getLogger(__name__)


    "runscalenowtest"
    def get_parser(self, prog_name):
        parser = super(RunScaleNowTest, self).get_parser(prog_name)

        # 'app_name': 'str',
        # 'git_url': 'str',
        # 'git_pass': 'int',
        # 'git_encrypted_pwd': 'str',
        # 'git_user': 'str',
        # 'branch_name': 'str',
        # 'command_to_run_test': 'str'
        # 'browser_list': 'BrowsersDto',
        # 'test_url': 'str',
        # 'text_to_search': 'str',
        # 'page_load_time_out': 'int',
        # 'type': 'str',
        # 'execution_strategy': 'str',
        # 'automation_code_type': 'str',
        # 'use_code_upload': 'str'
        # 'code_file_name': 'str',
        # 'pre_script': 'str',
        # 'post_script': 'int',
        # 'report_file': 'str',
        # 'output_dir': 'str',
        # 'delete_vm': 'str',
        # 'run_sequential': 'str'
        # 'run_hours': 'str',
        # 'parrallel_browsers_count': 'int',
        # 'inc_load': 'str',
        # 'inc_with': 'str',
        # 'inc_interval': 'str',

        parser.add_argument('--app_name', '-a', help='Set the name for this Automation Job.', required=True)
        parser.add_argument('--git_url', '-U', help='Set git clone url for Automation code.')
        parser.add_argument('--branch_name', '-b',
                            help='Set git repository branch name. If not specified, master branch will be considered by default.')
        parser.add_argument('--command_to_run_test', '-c',
                            help='Set command to run Automation Testsuite. For e.g. mvn test This option is mandatory.'
                            )
        parser.add_argument('--url', '-u',
                            help='Set url To be used in Automation test. example:http://www.google.com.', required=True
                            )
        parser.add_argument('--automation_code_type', '-T', help='Set automation code type as Ruby, Java, VBScript ')
        parser.add_argument('--use_code_upload', '-UC', help='Set upload code file as true or false')
        parser.add_argument('--code_file_name', '-UF', help='Set upload file name')
        parser.add_argument('--pre_script', '-Pr',
                            help='Set shell script to be executed before test suite runs. For e.g. mvn clean install to build your automation code.')
        parser.add_argument('--post_script', '-Po', help='Set shell script to be executed after test suite runs.')
        parser.add_argument('--report_file', '-r',
                            help='Set test execution report file, preferably in json or xml format.', required=True)
        parser.add_argument('--output_dir', '-o',
                            help='Set test execution reports directory. For e.g. target/testng-report. Path should be relative to your automation code directory'
                            )
        parser.add_argument('--delete_vm', '-d', help='Set delete vm as true or false')
        parser.add_argument('--run_sequential', '-R', help='Set run sequential as true or false')
        parser.add_argument('--run_hours', '-H',
                            help='Set duration in hours for the test suite to continuously run in repetition.')
        parser.add_argument('--parrallel_users_count', '-P', help='Set users count to put load on your application in parallel.')
        parser.add_argument('--inc_load', '-IL', help='Set Incremental Load as true or false')
        parser.add_argument('--inc_with', '-IW',
                            help='Set users count to put load on your application after specified interval in parallel.')
        parser.add_argument('--inc_interval', '-II', help='Set increment interval as integer value')
        parser.add_argument('--chrome', '-C',
                            help='Give the comma separated versions for Chrome to run test on.')
        parser.add_argument('--firefox', '-F',
                            help='Give the comma separated versions for Firefox to run test on.')
        parser.add_argument('--wait', '-w', help='Set to true for wait until job to finish.')

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
        body = test_sdk_client.ScaleNowTestDto(
            parsed_args.app_name,
            parsed_args.git_url,
            "raj@15111990",
            "string",
            "rajashridalavi",
            parsed_args.branch_name,
            parsed_args.command_to_run_test,
            browser_list,
            parsed_args.url,
            "string",
            "10",
            "loadtest",  # type
            "loadTest",
            parsed_args.automation_code_type,
            parsed_args.use_code_upload,
            parsed_args.code_file_name,
            parsed_args.pre_script,
            parsed_args.post_script,
            parsed_args.report_file,
            parsed_args.output_dir,
            parsed_args.delete_vm,
            parsed_args.run_sequential,
            parsed_args.run_hours,
            parsed_args.parrallel_users_count,
            parsed_args.inc_load,
            parsed_args.inc_with,
            parsed_args.inc_interval)


        self.log.debug(body)

        try:
            apiInstance = test_sdk_client.RunJobsApi()
            job_Id = apiInstance.submit_scale_now_test_job(body)
            self.log.debug("Response for Automation Test is------------: %s \n" % job_Id)
            print("The Scale Test submitted successfully. Job Id is : \n", job_Id)

            if (job_Id != None and parsed_args.wait == "true"):
                apiInstance = test_sdk_client.RunTestApi()
                job_status = apiInstance.get_job_status(job_Id)
                while ("RUNNING" in job_status):
                    print("The Status of Job_Id:", job_Id, " is  ", job_status)
                    time.sleep(5)
                print("The Status of Job_Id:", job_Id, " is  ", job_status)

        except Exception as e:
             self.log.error("Exception when calling RunScaleNowTest->submit_scale_now_test_job: %s\n" % e)


class Error(Command):
    "Always raises an error"

    log = logging.getLogger(__name__)

    def take_action(self, parsed_args):
        self.log.info('causing error')
        raise RuntimeError('this is the expected exception')
