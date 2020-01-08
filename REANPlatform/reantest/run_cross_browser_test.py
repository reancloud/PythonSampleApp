"""Run Cross Browser Test."""
import logging
import validators
from cliff.command import Command
import test_sdk_client
from reantest.utility import Utility


class RunCrossBrowserTest(Command):
    """Run cross browser test."""

    log = logging.getLogger(__name__)

    _description = 'Run Cross browser Test'
    _epilog = 'Example: rean-test run-automation-test --name <name> --test_suite Selenium --url <url> ' \
              '--git_repository_url <git_url> --git_branch <branch> --command_to_run_test <command to run test> ' \
              '--output_directory_path <report path> --report_file_name <report file name>  --chrome 64 ' \
              '--automation_code_language <Java/Ruby>'

    def get_parser(self, prog_name):
        """get_parser."""
        parser = super(RunCrossBrowserTest, self).get_parser(prog_name)

        # Basic configuration
        parser.add_argument('--name', '-n',
                            help='Set the name for this Automation Job.',
                            required=True)
        parser.add_argument('--test_suite', '-ts',
                            help='Set test suite. This parameter describe the test suite type')
        parser.add_argument('--url', '-u',
                            help='Set url To be used in Automation test. Example:http://www.google.com.')
        parser.add_argument('--preserve_machine', '-p',
                            choices=['true', 'False'],
                            help='Set true for preserve machine if test fails. default: False',
                            default=False)
        parser.add_argument('--automation_code_language', '-al',
                            choices=['Ruby', 'Java', 'VBScript', 'Python'],
                            help='Set automation code language', required=False)

        # CodeBase Parameters

        parser.add_argument('--upload_code_file_path', '-cf', help='Set upload file path', default="test")

        parser.add_argument('--git_repository_url', '-gr', help='Set git clone url for Automation code.')
        parser.add_argument('--git_username', '-gu', help='Set git username for Automation code.', default="")
        parser.add_argument('--git_password', '-gp', help='Set git password for Automation code.', default="")
        parser.add_argument('--git_branch', '-gb',
                            help='Set git repository branch name. '
                                 'If not specified, master branch will be considered by default.', default='master')

        # Execution Parameters
        parser.add_argument('--command_to_run_test', '-rc',
                            help='Set command to run Automation Testsuite. For e.g. mvn test')
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

        # Sample Code Parameters
        parser.add_argument('--sample_code_type', '-ct',
                            choices=['Ruby', 'Java', 'HP-UFT', 'TestComplete'],
                            help='Set sample code type')

        # Browsers

        parser.add_argument('--chrome', '-c',
                            help='Give the comma separated versions for Chrome to run test on.')
        parser.add_argument('--firefox', '-f',
                            help='Give the comma separated versions for Firefox to run test on.')
        parser.add_argument('--ie', '-i',
                            help='Give the comma separated versions for IE to run test on.')
        # Wait parameter
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

            functional_test_dto = test_sdk_client.FunctionalTestDto()
            functional_test_dto.name = parsed_args.name
            functional_test_dto.browsers = browser_list
            functional_test_dto.type = "functionaltest"  # type
            functional_test_dto.preserve_machine = parsed_args.preserve_machine

            # Add hardcoded values for sample code
            if parsed_args.sample_code_type:
                RunCrossBrowserTest.set_sample_parameters(parsed_args.sample_code_type, functional_test_dto)
            else:
                functional_test_dto.test_url = parsed_args.url

                if parsed_args.upload_code_file_path != 'test':
                    functional_test_dto.codebase_type = 'UPLOAD_CODE'
                    self.log.debug("Uploading code file ...")
                    functional_test_dto.upload_actual_input_file = parsed_args.upload_code_file_path
                    functional_test_dto.upload_code_file_name = Utility.upload_code(parsed_args.upload_code_file_path,
                                                                                    parsed_args.name)
                    self.log.debug("Code object Name : %s ", parsed_args.upload_code_file_path)
                else:
                    functional_test_dto.codebase_type = 'GIT'

                    git_config_dto = test_sdk_client.GitConfigDto()
                    git_config_dto.url = parsed_args.git_repository_url
                    git_config_dto.passsword = parsed_args.git_password
                    git_config_dto.user = parsed_args.git_username
                    git_config_dto.branch = parsed_args.git_branch
                    functional_test_dto.git_config = git_config_dto

                execution_details_dto = test_sdk_client.ExecutionDetailsDto()
                execution_details_dto.run_command = parsed_args.command_to_run_test
                execution_details_dto.pre_script = parsed_args.pre_script
                execution_details_dto.post_script = parsed_args.post_script
                execution_details_dto.report_file = parsed_args.report_file_name
                execution_details_dto.output_dir = parsed_args.output_directory_path
                functional_test_dto.execution_details = execution_details_dto

            self.log.debug(functional_test_dto)
            self.log.debug("Execution stared for Cross Browser Test")
            type(functional_test_dto)

            response_functional_test_dto = test_sdk_client.RunTestNewApi(Utility.set_headers()).run_functional_test(
                functional_test_dto)

            job_id = ""
            if response_functional_test_dto.id:
                job_id = response_functional_test_dto.id

            self.log.debug("Response is------------: %s ", job_id)
            print("The request Cross browser test submitted successfully. Job Id is : ", job_id)

            if job_id is not None and hasattr(parsed_args, 'wait') and parsed_args.wait == "true":
                api_instance = test_sdk_client.RunTestApi(Utility.set_headers())
                Utility.wait_while_job_running(api_instance, job_id)

        except Exception as exception:
            # self.log.error(exception)
            Utility.print_exception(exception)

    @staticmethod
    def validate_inputs(params):
        """validate_automation_test_input."""
        # All the parameters validations goes in this function
        # log = logging.getLogger(__name__)
        # self.log.debug(params)

        message = ""
        if params.sample_code_type:
            if params.name is None:
                message = "Please enter name parameters."
            elif params.chrome is None and params.firefox is None and params.ie is None:
                message = "Please Provide at least one browser to Test."
        else:
            # Validation for Test URL
            if not validators.url(params.url):
                message = "Please enter valid Application URL."
            elif params.name is None:
                message = "Please enter name parameters."
            elif params.command_to_run_test is None:
                message = "Please enter command_to_run_test parameters."
            elif params.report_file_name is None:
                message = "Please enter report_file parameters."
            elif params.output_directory_path is None:
                message = "Please enter output_dir parameters."
            elif params.test_suite is None:
                message = "Please enter test_suite parameters."

            # Validation for Browser list
            elif params.chrome is None and params.firefox is None and params.ie is None:
                message = "Please Provide at least one browser to Test."

            if params.upload_code_file_path == 'test':  # Upload Code = false
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

            body.automation_language = 'Ruby'
            body.test_suite = "Selenium"

            git_config_dto = test_sdk_client.GitConfigDto()
            git_config_dto.url = "https://github.com/reancloud/testnowrubyexample.git"
            git_config_dto.branch = "master"
            git_config_dto.user = ""
            git_config_dto.passsword = ""
            body.git_config = git_config_dto

            execution_details_dto = test_sdk_client.ExecutionDetailsDto()
            execution_details_dto.run_command = "bundle install && cucumber features"
            execution_details_dto.output_dir = "reports"
            execution_details_dto.report_file = "magento_report.json"
            body.execution_details = execution_details_dto

        elif sample_code_type == "Java":
            body.test_url = "https://34.199.118.11/"

            body.automation_language = 'Java'
            body.test_suite = "Selenium"

            git_config_dto = test_sdk_client.GitConfigDto()
            git_config_dto.url = "https://github.com/reancloud/testnowjavaexample.git"
            git_config_dto.branch = "master"
            git_config_dto.user = ""
            git_config_dto.passsword = ""
            body.git_config = git_config_dto

            execution_details_dto = test_sdk_client.ExecutionDetailsDto()
            execution_details_dto.run_command = "java -jar magento-automation-1.0-tests.jar"
            execution_details_dto.output_dir = "reports"
            execution_details_dto.report_file = "index.json"
            body.execution_details = execution_details_dto

        elif sample_code_type == "UFT":
            body.test_url = "https://34.199.118.11/"

            body.test_suite = "UFT"

            git_config_dto = test_sdk_client.GitConfigDto()
            git_config_dto.url = "https://github.com/tahirstamboli/UFTMagentoTest"
            git_config_dto.branch = "master"
            git_config_dto.user = ""
            git_config_dto.passsword = ""
            body.git_config = git_config_dto

            execution_details_dto = test_sdk_client.ExecutionDetailsDto()
            execution_details_dto.run_command = "Cscript 'C:/testnow/code/MagentoSuccessTest/RunUFT.vbs' 'C:/testnow/code/MagentoSuccessTest'"
            execution_details_dto.output_dir = "Report"
            execution_details_dto.report_file = "ResultDoc.dat"
            body.execution_details = execution_details_dto

        elif sample_code_type == "TestComplete":
            body.test_url = "http://34.199.118.11/"

            body.test_suite = "TestComplete"

            git_config_dto = test_sdk_client.GitConfigDto()
            git_config_dto.url = "https://github.com/rajashriDalavi/TestCompleteMagentoTest"
            git_config_dto.branch = "master"
            git_config_dto.user = ""
            git_config_dto.passsword = ""
            body.git_config = git_config_dto

            execution_details_dto = test_sdk_client.ExecutionDetailsDto()
            execution_details_dto.run_command = """"C:\\Program Files (x86)\\SmartBear\\TestExecute 12\\Bin\\TestExecute.exe" "C:\\testnow\\code\\TestProject3\\TestProject3.pjs" /run /exit /SilentMode /exportLog:"C:\\testnow\\code\\Report\\Results.mht"
if %errorlevel% neq 0 (set level=%errorlevel%)
 cd /d "c:\\testnow\\code\\TestProject3\\Log"
 for /d %%a in (*) do copy "%%a\\RootLogData.dat" "c:\\testnow\\code\\Report\\ResultDoc.dat";
 exit /b %level%"""
            execution_details_dto.output_dir = "Report"
            execution_details_dto.report_file = "ResultDoc.dat"
