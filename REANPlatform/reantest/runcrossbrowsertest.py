import logging
from . import config
from . import utility
from cliff.command import Command

import test_sdk_client
from test_sdk_client.rest import ApiException
from ast import literal_eval
import json
import time



class RunCrossBrowserTest(Command):

    log = logging.getLogger(__name__)


    "runcrossbrowsertest"
    def get_parser(self, prog_name):
        parser = super(RunCrossBrowserTest, self).get_parser(prog_name)

        # 'browser_list': 'BrowsersDto',
        # "testURL": "http://34.199.118.11/",
        #  "textToSearch": "string",
        # "pageLoadTimeOut": "10",
        # "executionStrategy": "boost",

        # "appName": "magento_test",
        # "gitURL": "https://github.com/reancloud/testnowrubyexample.git",
        # "gitPass": "test",
        # "gitEncryptedPwd": "string",
        # "gitUser": "test",
        # "branchName": "master/develop",
        # "commandToRunTest": "cucumber features / mvn test",

        # "type": "functionaltest",
        # "automationCodeType": "Ruby/Java/VBScript",
        # "isPresrveIfFailed": "true/false",
        # "useCodeUpload": "true/false",
        # "codeFileName": "test",
        # "preScript": "echo 'Executing PreScript'",
        # "postScript": "echo 'Executing PostScript'",
        # "reportFile": "magento_report.json",
        # "outputDir": "reports",
        # "deletevm": "true/false",
        # "runSequential": "true/false",
        # "sampleCodeType": "ruby/java/HP-UFT",
        # "testSuite": "Selenium/UFT/NA"

        parser.add_argument('--app_name', '-a', help='Set the name for this Automation Job.', required=True)
        parser.add_argument('--url', '-u', help='Set url To be used in Automation test. example:http://www.google.com.', required=True)
        parser.add_argument('--git_url', '-U', help='Set git clone url for Automation code.', required=True)
        parser.add_argument('--git_user', '-Us', help='Set user id in case of private git repository.')
        parser.add_argument('--git_pass', '-P', help='Set user password in case of private git repository')
        parser.add_argument('--branch_name', '-b', help='Set git repository branch name. If not specified, master branch will be considered by default.')
        parser.add_argument('--command_to_run_test', '-c', help='Set command to run Automation Testsuite. For e.g. mvn test ', required=True)
        parser.add_argument('--automation_code_type', '-T', help='Set automation code type as Ruby, Java, VBScript ', required=True)
        parser.add_argument('--is_presrve_if_failed', '-p', help='Set true for preserve machine if test fails.')
        parser.add_argument('--pre_script', '-Pr', help='Set shell script to be executed before test suite runs. For e.g. mvn clean install to build your automation code.')
        parser.add_argument('--post_script', '-Po', help='Set shell script to be executed after test suite runs.')
        parser.add_argument('--report_file', '-r', help='Set test execution report file, preferably in json or xml format.', required=True)
        parser.add_argument('--output_dir', '-o', help='Set test execution reports directory. For e.g. target/testng-report. Path should be relative to your automation code directory.', required=True)
        parser.add_argument('--delete_vm', '-d', help='Set delete vm as true or false')
        parser.add_argument('--run_sequential', '-R', help='Set run sequential as true or false')
        parser.add_argument('--sample_code_type', '-t', help='Set sample code type as Ruby, Java, HP-UFT, TestComplete ')
        parser.add_argument('--test_suite', '-s', help='Set test suite as Selenium, UFT, TestComplete, NA', required=True)

        parser.add_argument('--chrome', '-C', help='Give the comma separated versions for Chrome to run test on..This option is not mandatory.')
        parser.add_argument('--firefox', '-F', help='Give the comma separated versions for Firefox to run test on..This option is not mandatory.')

        parser.add_argument('--ie', '-I', help='Give the comma separated versions for IE to run test on.')
        parser.add_argument('--opera', '-O', help='Give the comma separated versions for Opera to run test on.')
        parser.add_argument('--wait', '-w', help='Set to true for wait until job to finish.')

        return parser

    def take_action(self, parsed_args):

        self.log.debug(parsed_args)

        browser_list = utility.Utility.getBrowserDTO(parsed_args)
        self.log.debug(browser_list)

        error_message = utility.Utility.validateInputs(self,parsed_args)
        if(error_message != "") :
            self.app.stdout.write(error_message)
            return


        print(parsed_args.firefox)

        #order should be maintained as the constructor takes values as parameter in the same order.
        body = test_sdk_client.CrossBrowserTestDto(
            parsed_args.app_name,
            parsed_args.git_url,
            parsed_args.git_pass,
            "",
            parsed_args.git_user,
            parsed_args.branch_name,
            parsed_args.command_to_run_test,
            browser_list,
            parsed_args.url,
            "string",#git_encrypted_pwd
            "10",
            "functionaltest",  # type
            "boost",
            parsed_args.automation_code_type,
            parsed_args.is_presrve_if_failed,
            "false",#use_code_upload,
            "test",#code_file_name,
            parsed_args.pre_script,
            parsed_args.post_script,
            parsed_args.report_file,
            parsed_args.output_dir,
            parsed_args.delete_vm,
            parsed_args.run_sequential,
            parsed_args.sample_code_type,
            parsed_args.test_suite)

        self.log.debug(body)

        try:
            apiInstance = test_sdk_client.RunJobsApi()
            job_Id = apiInstance.submit_cross_browser_test_job(body)
            self.log.debug("Response for Automation Test is------------: %s \n" % job_Id)
            print("The Automation Test submitted successfully. Job Id is : ", job_Id)

            if (job_Id != None and parsed_args.wait == "true"):
                apiInstance = test_sdk_client.RunTestApi()
                job_status = apiInstance.get_job_status(job_Id)
                while ("RUNNING" in job_status):
                    print("The Status of Job_Id:", job_Id, " is  ", job_status)
                    time.sleep(5)
                print("The Status of Job_Id:", job_Id, " is  ", job_status)
        except Exception as e:
             self.log.error("Exception when calling RunAutomationTest->submit_cross_browser_test_job: %s\n" % e)


class Error(Command):
    "Always raises an error"

    log = logging.getLogger(__name__)

    def take_action(self, parsed_args):
        self.log.info('causing error')
        raise RuntimeError('this is the expected exception')
