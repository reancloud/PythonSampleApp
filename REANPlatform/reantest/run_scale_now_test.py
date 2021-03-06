"""run scale now test."""
import logging
from cliff.command import Command
import test_sdk_client
from reantest.utility import Utility


class RunScaleNowTest(Command):
    """Run scale now test."""

    log = logging.getLogger(__name__)
    _description = 'Run Scale test'
    _epilog = 'Example : rean-test run-scale-test --name <name> --url <URL> --parallel_users_count <int value>' \
              ' --hours_to_run <int value> --incremental_load False --upload_code_file_name <code absolute path> ' \
              '--command_to_run_test <command to run test> --pre_script <Pre script>' \
              '--post_script <Post script>' \
              ' --report_file_name features_report.json --output_directory_path report --chrome 64'

    def get_parser(self, prog_name):
        """get_parser."""
        parser = super(RunScaleNowTest, self).get_parser(prog_name)

        # Basic Parameters
        parser.add_argument('--name', '-n', help='Set the name for this Automation Job.', required=True)
        parser.add_argument('--url', '-u',
                            help='Set url To be used in Automation test. example:http://www.google.com.', required=True)
        parser.add_argument('--parallel_users_count', '-pc',
                            help='Set users count to put load on your application in parallel.', required=True)
        parser.add_argument('--browser_per_instance', '-bi', help='Set browsers count per instance. default: 3',
                            type=int, default=3)
        parser.add_argument('--hours_to_run', '-hr', help='Set maximum hours to run test', type=int, required=True)
        parser.add_argument('--incremental_load', '-l', help='Set Incremental load. Default: False', choices=['True', 'False'],
                            default=False)

        # CodeBase Parameters
        parser.add_argument('--upload_code_file_name', '-cf', help='Set upload file name', default="test")

        parser.add_argument('--git_repository_url', '-gr', help='Set git clone url for Automation code.')
        parser.add_argument('--git_username', '-gu', help='Set git username for Automation code.')
        parser.add_argument('--git_password', '-gp', help='Set git password for Automation code.')
        parser.add_argument('--git_branch', '-gb',
                            help='Set git repository branch name. '
                                 'If not specified, master branch will be considered by default.', default='master')

        # Execution Parameters
        parser.add_argument('--command_to_run_test', '-rc',
                            help='Set command to run Automation Test suite. For e.g. mvn test This option is mandatory.',
                            required=True)
        parser.add_argument('--pre_script', '-pr',
                            help='Set shell script to be executed before test suite runs. '
                                 'Example mvn clean install to build your automation code.')
        parser.add_argument('--post_script', '-po', help='Set shell script to be executed after test suite runs.')
        parser.add_argument('--report_file_name', '-rf',
                            help='Set test execution report file, preferably in json or xml format.', required=True)
        parser.add_argument('--output_directory_path', '-od',
                            help='Set test execution reports directory. '
                                 'Example target/testing-report. Path should be relative to your '
                                 'automation code directory', required=True)

        # Browsers
        parser.add_argument('--chrome', '-c',
                            help='Give the comma separated versions for Chrome to run test on.')
        parser.add_argument('--firefox', '-f',
                            help='Give the comma separated versions for Firefox to run test on.')

        parser.add_argument('--wait', '-w', help='Set to true for wait until job to finish.')

        return parser

    def take_action(self, parsed_args):
        """take_action."""
        self.log.debug(parsed_args)
        try:
            browser_list = Utility.get_browser_dto(parsed_args)
            RunScaleNowTest.validate_scale_test_inputs(parsed_args)

            if parsed_args.firefox is not None:
                firefox = Utility.get_unique_seq(parsed_args.firefox.split(","))
                self.log.debug(firefox)
                browser_list.firefox = firefox
            if parsed_args.chrome is not None:
                chrome = Utility.get_unique_seq(parsed_args.chrome.split(","))
                self.log.debug(chrome)
                browser_list.chrome = chrome

            self.log.debug(browser_list)

            scale_test_dto = test_sdk_client.ScaleTestDto()

            scale_test_dto.name = parsed_args.name
            scale_test_dto.browsers = browser_list
            scale_test_dto.test_url = parsed_args.url
            scale_test_dto.parallel_user_count = parsed_args.parallel_users_count
            scale_test_dto.browser_per_instance = parsed_args.browser_per_instance
            scale_test_dto.hours_to_run = parsed_args.hours_to_run
            scale_test_dto.type = "loadtest"  # type

            if parsed_args.upload_code_file_name != 'test':
                scale_test_dto.codebase_type = 'UPLOAD_CODE'
                self.log.debug("Uploading code file ...")
                scale_test_dto.upload_code_file_name = Utility.upload_code(parsed_args.upload_code_file_name,
                                                                           parsed_args.name)
                self.log.debug("Code object Name : %s ", parsed_args.upload_code_file_name)
            else:
                scale_test_dto.codebase_type = 'GIT'
                git_config_dto = test_sdk_client.GitConfigDto()

                git_config_dto.url = parsed_args.git_repository_url
                git_config_dto.passsword = parsed_args.git_password
                git_config_dto.user = parsed_args.git_username
                git_config_dto.branch = parsed_args.git_branch
                scale_test_dto.git_config = git_config_dto

            execution_details_dto = test_sdk_client.ExecutionDetailsDto()
            execution_details_dto.run_command = parsed_args.command_to_run_test
            execution_details_dto.pre_script = parsed_args.pre_script
            execution_details_dto.post_script = parsed_args.post_script
            execution_details_dto.report_file = parsed_args.report_file_name
            execution_details_dto.output_dir = parsed_args.output_directory_path
            scale_test_dto.execution_details = execution_details_dto

            self.log.debug(scale_test_dto)
            self.log.debug("Execution stared for Scale Test")

            response_scale_test_dto = test_sdk_client.RunTestNewApi(Utility.set_headers()).run_scale_test(scale_test_dto)

            job_id = ""
            if response_scale_test_dto.id:
                job_id = response_scale_test_dto.id

            self.log.debug("Response is------------: %s ", job_id)
            print("The request scale test submitted successfully. Job Id is : ", job_id)

            if job_id is not None and hasattr(parsed_args, 'wait') and parsed_args.wait == "true":
                api_instance = test_sdk_client.RunTestApi(Utility.set_headers())
                Utility.wait_while_job_running(api_instance, job_id)

        except Exception as exception:
            self.log.error(exception)
            Utility.print_exception(exception)

    @staticmethod
    def validate_scale_test_inputs(params):
        """Validate url and browsers input."""
        # All the parameters validations goes in this function

        message = ""
        # # Validation for Test URL
        # if not validators.url(params.url):
        #     message = "Please enter valid Test URL."

        # Validation for Browser list
        if params.chrome is None and params.firefox is None:
            message = "Please Provide at least one browser to Test."

        if params.upload_code_file_name == 'test':  # Upload Code = false
            if params.git_repository_url is None:
                message = "Please provide valid git credentials"
        else:
            if params.git_repository_url is not None:
                message = "Upload file name and Git repository url parameters can not be used together"

        if message:
            raise RuntimeError(message)
