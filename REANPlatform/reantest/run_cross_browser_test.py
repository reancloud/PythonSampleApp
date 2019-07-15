"""Run Cross Browser Test."""
import logging
import validators
from cliff.command import Command
import test_sdk_client
from reantest.utility import Utility


class RunCrossBrowserTest(Command):
    """Run cross browser test."""

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        """get_parser."""
        parser = super(RunCrossBrowserTest, self).get_parser(prog_name)

        parser.add_argument('--app_name', '-a',
                            help='Set the name for this Automation Job.',
                            required=True)
        parser.add_argument('--url', '-u',
                            help='Set url To be used in Automation test. Example:http://www.google.com.')
        parser.add_argument('--code_file_name', '-cf',
                            help='Set upload file name',
                            default="test")
        parser.add_argument('--git_repository_url', '-gr',
                            help='Set git clone url for Automation code.')
        parser.add_argument('--git_username', '-gu',
                            help='Set user id in case of private git repository.')
        parser.add_argument('--git_password', '-gp',
                            help='Set user password in case of private git repository')
        parser.add_argument('--git_branch_name', '-gb',
                            help='Set git repository branch name. '
                                 'If not specified, master branch will be considered by default.',
                            default='master')
        parser.add_argument('--command_to_run_test', '-rc',
                            help='Set command to run Automation Testsuite. For e.g. mvn test ')
        parser.add_argument('--automation_code_type', '-at',
                            help='Set automation code type as Ruby, Java, VBScript ')
        parser.add_argument('--preserve_machine', '-p',
                            help='Set true for preserve machine if test fails.')
        parser.add_argument('--pre_script', '-pr',
                            help='Set shell script to be executed before test suite runs.'
                                 'For e.g. mvn clean install to build your automation code.')
        parser.add_argument('--post_script', '-po',
                            help='Set shell script to be executed after test suite runs.')
        parser.add_argument('--report_file_name', '-rf',
                            help='Set test execution report file, preferably in json or xml format.')
        parser.add_argument('--output_directory_path', '-od',
                            help='Set test execution reports directory.'
                                 'Example target/testng-report,'
                                 'Path should be relative to your automation code directory.')
        parser.add_argument('--delete_virtual_machine', '-d',
                            help='Set delete vm as true or false')
        parser.add_argument('--run_sequential', '-rs',
                            help='Set run sequential as true or false')
        parser.add_argument('--sample_code_type', '-ct',
                            choices=['Ruby', 'Java', 'HP-UFT', 'TestComplete'],
                            help='Set sample code type')
        parser.add_argument('--test_suite', '-ts',
                            choices=['Selenium', 'UFT', 'TestComplete', 'NA'],
                            help='Set test suite')

        parser.add_argument('--chrome', '-c',
                            help='Give the comma separated versions for Chrome to run test on.')
        parser.add_argument('--firefox', '-f',
                            help='Give the comma separated versions for Firefox to run test on.')
        parser.add_argument('--ie', '-i',
                            help='Give the comma separated versions for IE to run test on.')
        parser.add_argument('--wait', '-w',
                            help='Set to true for wait until job to finish.')

        # parser.add_argument('--opera', '-O', help='Give the comma separated versions for Opera to run test on.')

        return parser

    def take_action(self, parsed_args):
        """take_action."""
        self.log.debug(parsed_args)
        try:
            browser_list = Utility.get_browser_dto(parsed_args)
            self.log.debug(browser_list)

            RunCrossBrowserTest.validate_inputs(parsed_args)

            body = test_sdk_client.CrossBrowserTestDto()
            body.app_name = parsed_args.app_name
            body.browser_list = browser_list
            body.sample_code_type = parsed_args.sample_code_type
            body.test_suite = parsed_args.test_suite
            body.deletevm = parsed_args.delete_virtual_machine
            body.run_sequential = parsed_args.run_sequential
            body.type = "functionaltest"  # type
            body.execution_strategy = "boost"
            body.is_presrve_if_failed = parsed_args.preserve_machine
            body.automation_code_type = parsed_args.automation_code_type

            # Add hardcoded values for sample code
            if parsed_args.sample_code_type:
                RunCrossBrowserTest.set_sample_parameters(parsed_args.sample_code_type, body)
            else:
                body.test_url = parsed_args.url

                if parsed_args.code_file_name != 'test':
                    self.log.debug("Uploading code file ...")
                    body.code_file_name = Utility.upload_code(parsed_args.code_file_name, parsed_args.app_name)
                    self.log.debug("Code object Name : %s ", body.code_file_name)
                    body.use_code_upload = True
                else:
                    body.git_url = parsed_args.git_repository_url
                    body.git_pass = parsed_args.git_password
                    body.git_user = parsed_args.git_username
                    body.branch_name = parsed_args.git_branch_name
                    body.use_code_upload = False

                body.command_to_run_test = parsed_args.command_to_run_test
                body.pre_script = parsed_args.pre_script
                body.post_script = parsed_args.post_script
                body.report_file = parsed_args.report_file_name
                body.output_dir = parsed_args.output_directory_path

            self.log.debug(body)
            self.log.debug("Execution stared for Automation Test")
            Utility.execute_test(body, parsed_args, self.log, test_sdk_client.RunJobsApi(Utility.set_headers()).submit_cross_browser_test_job)
        except Exception as exception:
            self.log.error(exception)
            Utility.print_exception(exception)

    @staticmethod
    def validate_inputs(params):
        """validate_automation_test_input."""
        # All the parameters validations goes in this function
        # log = logging.getLogger(__name__)
        # self.log.debug(params)

        message = ""
        if params.sample_code_type:
            if params.app_name is None:
                message = "Please enter app_name parameters."
            elif params.chrome is None and params.firefox is None and params.ie is None:
                message = "Please Provide at least one browser to Test."
        else:
            # Validation for Test URL
            if not validators.url(params.url):
                message = "Please enter valid Application URL."
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

            if params.code_file_name == 'test':  # Upload Code = false
                if params.git_repository_url is None:
                    message = "Please provide valid git credentials"
            else:
                if params.git_repository_url is not None:
                    message = "Upload file name and Git repository url parameters can not be used together"

            if message:
                raise RuntimeError(message)

    @staticmethod
    def set_sample_parameters(sample_code_type, body):
        """Set body parameters for sample code."""
        if sample_code_type == "Ruby":
            body.test_url = "https://34.199.118.11/"
            body.git_url = "https://github.com/reancloud/testnowrubyexample.git"
            body.branch_name = "master"
            body.command_to_run_test = "bundle install && cucumber features"
            body.output_dir = "reports"
            body.report_file = "magento_report.json"

        elif sample_code_type == "Java":
            body.test_url = "https://34.199.118.11/"
            body.git_url = "https://github.com/reancloud/testnowjavaexample.git"
            body.branch_name = "master"
            body.command_to_run_test = "java -jar magento-automation-1.0-tests.jar"
            body.output_dir = "reports"
            body.report_file = "index.json"

        elif sample_code_type == "UFT":
            body.test_url = "https://34.199.118.11/"
            body.git_url = "https://github.com/tahirstamboli/UFTMagentoTest"
            body.branch_name = "master"
            body.command_to_run_test = "Cscript 'C:/testnow/code/MagentoSuccessTest/RunUFT.vbs' 'C:/testnow/code/MagentoSuccessTest'"
            body.output_dir = "Report"
            body.report_file = "ResultDoc.dat"

        elif sample_code_type == "TestComplete":
            body.test_url = "http://34.199.118.11/"
            body.git_url = "https://github.com/rajashriDalavi/TestCompleteMagentoTest"
            body.branch_name = "master"
            body.command_to_run_test = """"C:\\Program Files (x86)\\SmartBear\\TestExecute 12\\Bin\\TestExecute.exe" "C:\\testnow\\code\\TestProject3\\TestProject3.pjs" /run /exit /SilentMode /exportLog:"C:\\testnow\\code\\Report\\Results.mht"
if %errorlevel% neq 0 (set level=%errorlevel%)
 cd /d "c:\\testnow\\code\\TestProject3\\Log"
 for /d %%a in (*) do copy "%%a\\RootLogData.dat" "c:\\testnow\\code\\Report\\ResultDoc.dat";
 exit /b %level%"""
            body.output_dir = "Report"
            body.report_file = "ResultDoc.dat"
