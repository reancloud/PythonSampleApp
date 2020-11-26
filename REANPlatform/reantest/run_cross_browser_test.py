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
              '--automation_code_language <Java/Ruby> --wait'

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
        parser.add_argument('--automation_code_language', '-al',
                            choices=['Ruby', 'Java', 'VBScript', 'Python'],
                            help='Set automation code language', required=False)

        parser.add_argument('--preserve_machine', '-p',
                            choices=['true', 'False'],
                            help='Set true for preserve machine if test fails. default: False',
                            default=False)

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

        # Browsers

        parser.add_argument('--chrome', '-c',
                            help='Give the comma separated versions for Chrome to run test on.')
        parser.add_argument('--firefox', '-f',
                            help='Give the comma separated versions for Firefox to run test on.')
        parser.add_argument('--ie', '-i',
                            help='Give the comma separated versions for IE to run test on.')
        parser.add_argument('--export_jobid_path', '-ej', help='Export job id to file absolute path.')
        # Wait parameter
        parser.add_argument('--wait', '-w', action='store_true', help='Wait until job finish', default=False)
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

            Utility.export_jobid(parsed_args.name, job_id, parsed_args.export_jobid_path)

            self.log.debug("Response is------------: %s ", job_id)
            print("The request Cross browser test submitted successfully. Job Id is : ", job_id)

            if parsed_args.wait:
                Utility.wait_while_job_running(test_sdk_client.RunTestApi(Utility.set_headers()), job_id)

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
