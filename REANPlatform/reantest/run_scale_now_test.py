"""run scale now test."""
import logging
from cliff.command import Command
import test_sdk_client
from reantest.utility import Utility


class RunScaleNowTest(Command):
    """Run scale now test."""

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        """get_parser."""
        parser = super(RunScaleNowTest, self).get_parser(prog_name)

        parser.add_argument('--app_name', '-a', help='Set the name for this Automation Job.', required=True)
        parser.add_argument('--code_file_name', '-cf', help='Set upload file name', default="test")
        parser.add_argument('--git_repository_url', '-gr', help='Set git clone url for Automation code.')
        parser.add_argument('--git_password', '-gp', help='Set git password for Automation code.')
        parser.add_argument('--git_username', '-gu', help='Set git username for Automation code.')
        parser.add_argument('--git_branch_name', '-gb',
                            help='Set git repository branch name. '
                                 'If not specified, master branch will be considered by default.')
        parser.add_argument('--command_to_run_test', '-rc',
                            help='Set command to run Automation Test suite. For e.g. mvn test This option is mandatory.')
        parser.add_argument('--url', '-u',
                            help='Set url To be used in Automation test. example:http://www.google.com.', required=True)
        parser.add_argument('--page_load_time_out', '-to', help='Set page Load time.')
        parser.add_argument('--automation_code_type', '-t', help='Set automation code type as Ruby, Java, VBScript ')
        parser.add_argument('--pre_script', '-pr',
                            help='Set shell script to be executed before test suite runs. '
                                 'Example mvn clean install to build your automation code.')
        parser.add_argument('--post_script', '-po', help='Set shell script to be executed after test suite runs.')
        parser.add_argument('--report_file_name', '-rf',
                            help='Set test execution report file, preferably in json or xml format.', required=True)
        parser.add_argument('--output_directory_path', '-od',
                            help='Set test execution reports directory. '
                                 'Example target/testing-report. Path should be relative to your '
                                 'automation code directory')
        parser.add_argument('--delete_virtual_machine', '-d', help='Set delete vm as true or false')
        parser.add_argument('--run_sequential', '-rs', help='Set run sequential as true or false')
        parser.add_argument('--run_hours', '-rh',
                            help='Set duration in hours for the test suite to continuously run in repetition.')
        parser.add_argument('--parallel_users_count', '-pc',
                            help='Set users count to put load on your application in parallel.')
        parser.add_argument('--incremental_load', '-il', help='Set Incremental Load as true or false')
        parser.add_argument('--increment_with', '-iw',
                            help='Set users count to put load on your application after specified interval in parallel.')
        parser.add_argument('--increment_interval', '-ii', help='Set increment interval as integer value')
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
            body = test_sdk_client.ScaleNowTestDto()

            body.app_name = parsed_args.app_name
            body.browser_list = browser_list
            body.test_url = parsed_args.url
            body.text_to_search = "string"

            if parsed_args.code_file_name != 'test':
                self.log.debug("Uploading code file ...")
                body.code_file_name = Utility.upload_code(parsed_args.code_file_name, parsed_args.app_name)
                self.log.debug("Code object Name : %s ", body.code_file_name)
                body.use_code_upload = True
            else:
                body.git_url = parsed_args.git_repository_url
                body.git_pass = parsed_args.git_password
                body.git_encrypted_pwd = "String"
                body.git_user = parsed_args.git_username
                body.branch_name = parsed_args.git_branch_name
                body.use_code_upload = False

            body.page_load_time_out = parsed_args.page_load_time_out
            body.command_to_run_test = parsed_args.command_to_run_test

            body.type = "loadtest"  # type
            body.execution_strategy = "loadTest"
            body.automation_code_type = parsed_args.automation_code_type

            body.pre_script = parsed_args.pre_script
            body.post_script = parsed_args.post_script
            body.report_file = parsed_args.report_file_name
            body.output_dir = parsed_args.output_directory_path

            body.deletevm = parsed_args.delete_virtual_machine
            body.run_sequential = parsed_args.run_sequential
            body.run_hours = parsed_args.run_hours
            body.parrallel_browsers_count = parsed_args.parallel_users_count

            body.inc_load = parsed_args.incremental_load
            body.inc_with = parsed_args.increment_with
            body.inc_interval = parsed_args.increment_interval

            self.log.debug(body)
            self.log.debug("Execution stared for Automation Test")
            Utility.execute_test(body, parsed_args, self.log, test_sdk_client.RunJobsApi(Utility.set_headers()).submit_scale_now_test_job)

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

        if params.code_file_name == 'test':  # Upload Code = false
            if params.git_repository_url is None:
                message = "Please provide valid git credentials"
        else:
            if params.git_repository_url is not None:
                message = "Upload file name and Git repository url parameters can not be used together"

        if message:
            raise RuntimeError(message)
