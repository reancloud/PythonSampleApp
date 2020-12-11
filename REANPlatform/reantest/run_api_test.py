"""Run Cross Browser Test."""
import logging
import time
import validators
from cliff.command import Command
import test_sdk_client
from reantest.utility import Utility


class RunApiTest(Command):
    """Run cross browser test."""

    log = logging.getLogger(__name__)

    _description = 'Run Api Test'
    _epilog = 'Example: rean-test run-automation-test --name <name> --test_suite Selenium --url <url> ' \
              '--git_repository_url <git_url> --git_branch <branch> --command_to_run_test <command to run test> ' \
              '--output_directory_path <report path> --report_file_name <report file name>  --chrome 64 ' \
              '--automation_code_language <Java/Ruby> --wait'

    def get_parser(self, prog_name):
        """get_parser."""
        parser = super(RunApiTest, self).get_parser(prog_name)

        # Basic configuration
        parser.add_argument('--name', '-n',
                            help='Set the name for this Api Test Job.',
                            required=True)
        parser.add_argument('--url', '-u',
                            help='Set url To be used in Api Test test.', required=True)

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

        parser.add_argument('--export_jobid_path', '-ej', help='Export job id to file absolute path.')
        # Wait parameter
        parser.add_argument('--wait', '-w', action='store_true', help='Wait until job finish', default=False)

        return parser

    def take_action(self, parsed_args):
        """take_action."""
        self.log.debug(parsed_args)
        try:

            api_test_dto = test_sdk_client.AppTestDto()
            api_test_dto.job_name = parsed_args.name + "-" + str(int(time.time()))  # added epoch time
            api_test_dto.application_url = parsed_args.url

            api_test_dto.test_url = parsed_args.url

            job_param_dto = test_sdk_client.JobParamsDto()

            if parsed_args.upload_code_file_path != 'test':
                job_param_dto.useUploadCode = True
                self.log.debug("Uploading code file ...")
                job_param_dto.actualupload_code_file_name = parsed_args.upload_code_file_path
                job_param_dto.upload_code_file_name = Utility.upload_code(
                    parsed_args.upload_code_file_path, parsed_args.name)
                self.log.debug("Code object Name : %s ", parsed_args.upload_code_file_path)
            else:
                job_param_dto.useUploadCode = False

                job_param_dto.git_url = parsed_args.git_repository_url
                job_param_dto.git_password = parsed_args.git_password
                job_param_dto.git_user = parsed_args.git_username
                job_param_dto.branch_name = parsed_args.git_branch

            job_param_dto.command_to_run_test = parsed_args.command_to_run_test
            job_param_dto.pre_script = parsed_args.pre_script
            job_param_dto.post_script = parsed_args.post_script
            job_param_dto.report_file = parsed_args.report_file_name
            job_param_dto.output_dir = parsed_args.output_directory_path

            api_test_dto.job_params = job_param_dto

            self.log.debug(api_test_dto)
            self.log.debug("Execution stared for Api Test")

            response_api_test_dto = test_sdk_client.ApitestcontrollerApi(
                Utility.set_headers()).run_api_test_using_post(api_test_dto)

            job_id = ""
            if response_api_test_dto.id:
                job_id = response_api_test_dto.id

            Utility.export_jobid(parsed_args.name, job_id, parsed_args.export_jobid_path)

            self.log.debug("Response is------------: %s ", job_id)
            print("The request Api test submitted successfully. Job Id is : ", job_id)

            if parsed_args.wait:
                Utility.wait_while_job_running(job_id)

        except Exception as exception:
            self.log.error(exception)
            Utility.print_exception(exception)

    @staticmethod
    def validate_inputs(params):
        """validate_automation_test_input."""
        message = ""
        if not validators.url(params.url):
            message = "Please enter valid Application URL."
        elif params.command_to_run_test is None:
            message = "Please enter command_to_run_test parameters."
        elif params.report_file_name is None:
            message = "Please enter report_file parameters."
        elif params.output_directory_path is None:
            message = "Please enter output_dir parameters."

        if params.upload_code_file_path == 'test':  # Upload Code = false
            if params.git_repository_url is None:
                message = "Please provide valid git credentials"
        else:
            if params.git_repository_url is not None:
                message = "Upload file name and Git repository url parameters can not be used together"

        if message:
            raise RuntimeError(message)
