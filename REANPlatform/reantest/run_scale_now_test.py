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
        parser.add_argument('--git_repository_url', '-gr', help='Set git clone url for Automation code.')
        parser.add_argument('--git_password', '-gp', help='Set git password for Automation code.')
        parser.add_argument('--git_username', '-gu', help='Set git username for Automation code.')
        parser.add_argument('--git_branch_name', '-gb',
                            help='Set git repository branch name. If not specified, master branch will be considered by default.')
        parser.add_argument('--command_to_run_test', '-rc',
                            help='Set command to run Automation Test suite. For e.g. mvn test This option is mandatory.')
        parser.add_argument('--url', '-u',
                            help='Set url To be used in Automation test. example:http://www.google.com.', required=True)
        parser.add_argument('--page_load_time_out', '-to', help='Set page Load time.')
        parser.add_argument('--automation_code_type', '-t', help='Set automation code type as Ruby, Java, VBScript ')
        parser.add_argument('--use_code_upload', '-cu', help='Set upload code file as true or false')
        parser.add_argument('--code_file_name', '-cf', help='Set upload file name')
        parser.add_argument('--pre_script', '-pr',
                            help='Set shell script to be executed before test suite runs. For e.g. mvn clean install to build your automation code.')
        parser.add_argument('--post_script', '-po', help='Set shell script to be executed after test suite runs.')
        parser.add_argument('--report_file', '-rf',
                            help='Set test execution report file, preferably in json or xml format.', required=True)
        parser.add_argument('--output_directory', '-od',
                            help='Set test execution reports directory. For e.g. target/testng-report. Path should be relative to your automation code directory')
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

            error_message = Utility.validate_scale_test_inputs(parsed_args)
            if error_message:
                self.app.stdout.write(error_message)
                return

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
            body.git_url = parsed_args.git_repository_url
            body.git_pass = parsed_args.git_password
            body.git_encrypted_pwd = "String"
            body.git_user = parsed_args.git_username
            body.branch_name = parsed_args.git_branch_name
            body.command_to_run_test = parsed_args.command_to_run_test
            body.browser_list = browser_list
            body.test_url = parsed_args.url
            body.text_to_search = "string"
            body.page_load_time_out = parsed_args.page_load_time_out
            body.type = "loadtest"  # type
            body.execution_strategy = "loadTest"
            body.automation_code_type = parsed_args.automation_code_type
            body.use_code_upload = parsed_args.use_code_upload
            body.code_file_name = parsed_args.code_file_name
            body.pre_script = parsed_args.pre_script
            body.post_script = parsed_args.post_script
            body.report_file = parsed_args.report_file
            body.output_dir = parsed_args.output_directory
            body.deletevm = parsed_args.delete_virtual_machine
            body.run_sequential = parsed_args.run_sequential
            body.run_hours = parsed_args.run_hours
            body.parrallel_browsers_count = parsed_args.parallel_users_count
            body.inc_load = parsed_args.incremental_load
            body.inc_with = parsed_args.increment_with
            body.inc_interval = parsed_args.increment_interval

            self.log.debug(body)

            self.log.debug("Execution stared for Automation Test")
            Utility.execute_test(body, parsed_args, self.log, test_sdk_client.RunJobsApi().submit_scale_now_test_job)

        except Exception as exception:
            Utility.print_exception(exception)
