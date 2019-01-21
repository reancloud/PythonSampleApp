"""Run Cross Browser Test."""
import logging
from cliff.command import Command
import test_sdk_client
from reantest.utility import Utility


class RunCrossBrowserTest(Command):
    """Run cross browser test."""

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        """get_parser."""
        parser = super(RunCrossBrowserTest, self).get_parser(prog_name)

        parser.add_argument('--app_name', '-a', help='Set the name for this Automation Job.', required=True)
        parser.add_argument('--url', '-u', help='Set url To be used in Automation test. Example:http://www.google.com.',
                            required=True)
        parser.add_argument('--use_code_upload', '-cu', help='Set upload code file as true to upload test file. Default=false', default="false")
        parser.add_argument('--code_file_name', '-cf', help='Set upload file name', default="test")
        parser.add_argument('--git_repository_url', '-gr', help='Set git clone url for Automation code.')
        parser.add_argument('--git_username', '-gu', help='Set user id in case of private git repository.')
        parser.add_argument('--git_password', '-gp', help='Set user password in case of private git repository')
        parser.add_argument('--git_branch_name', '-gb',
                            help='Set git repository branch name. '
                                 'If not specified, master branch will be considered by default.')
        parser.add_argument('--command_to_run_test', '-rc',
                            help='Set command to run Automation Testsuite. For e.g. mvn test ', required=True)
        parser.add_argument('--automation_code_type', '-at', help='Set automation code type as Ruby, Java, VBScript ',
                            required=True)
        parser.add_argument('--preserve_machine', '-p', help='Set true for preserve machine if test fails.')

        parser.add_argument('--pre_script', '-pr',
                            help='Set shell script to be executed before test suite runs. '
                                 'For e.g. mvn clean install to build your automation code.')
        parser.add_argument('--post_script', '-po', help='Set shell script to be executed after test suite runs.')
        parser.add_argument('--report_file_name', '-rf',
                            help='Set test execution report file, preferably in json or xml format.', required=True)
        parser.add_argument('--output_directory_path', '-od',
                            help='Set test execution reports directory.'
                                 'Example target/testng-report,'
                                 'Path should be relative to your automation code directory.',
                            required=True)
        parser.add_argument('--delete_virtual_machine', '-d', help='Set delete vm as true or false')
        parser.add_argument('--run_sequential', '-rs', help='Set run sequential as true or false')
        parser.add_argument('--sample_code_type', '-ct',
                            help='Set sample code type as Ruby, Java, HP-UFT, TestComplete ')
        parser.add_argument('--test_suite', '-ts', help='Set test suite as Selenium, UFT, TestComplete, NA',
                            required=True)

        parser.add_argument('--chrome', '-c',
                            help='Give the comma separated versions for Chrome to run test on.')
        parser.add_argument('--firefox', '-f',
                            help='Give the comma separated versions for Firefox to run test on.')
        parser.add_argument('--ie', '-i', help='Give the comma separated versions for IE to run test on.')
        parser.add_argument('--wait', '-w', help='Set to true for wait until job to finish.')

        # parser.add_argument('--opera', '-O', help='Give the comma separated versions for Opera to run test on.')

        return parser

    def take_action(self, parsed_args):
        """take_action."""
        self.log.debug(parsed_args)
        try:
            browser_list = Utility.get_browser_dto(parsed_args)
            self.log.debug(browser_list)

            error_message = Utility.validate_automation_test_inputs(parsed_args)
            if error_message:
                self.app.stdout.write(error_message)
                return

            body = test_sdk_client.CrossBrowserTestDto()
            body.app_name = parsed_args.app_name
            body.browser_list = browser_list
            body.test_url = parsed_args.url
            body.type = "functionaltest"  # type
            body.execution_strategy = "boost"
            body.automation_code_type = parsed_args.automation_code_type
            body.is_presrve_if_failed = parsed_args.preserve_machine

            if parsed_args.use_code_upload == 'true':
                self.log.debug("Uploading code file ...")
                body.code_file_name = Utility.upload_code(parsed_args.code_file_name, parsed_args.app_name)
                self.log.debug("Code object Name : %s ", body.code_file_name)
                body.use_code_upload = parsed_args.use_code_upload
            else:
                body.git_url = parsed_args.git_repository_url
                body.git_pass = parsed_args.git_password
                body.git_user = parsed_args.git_username
                body.branch_name = parsed_args.git_branch_name

            body.command_to_run_test = parsed_args.command_to_run_test
            body.pre_script = parsed_args.pre_script
            body.post_script = parsed_args.post_script
            body.report_file = parsed_args.report_file_name
            body.output_dir = parsed_args.output_directory_path

            body.deletevm = parsed_args.delete_virtual_machine
            body.run_sequential = parsed_args.run_sequential

            body.sample_code_type = parsed_args.sample_code_type
            body.test_suite = parsed_args.test_suite

            self.log.debug(body)
            self.log.debug("Execution stared for Automation Test")
            Utility.execute_test(body, parsed_args, self.log, test_sdk_client.RunJobsApi(Utility.set_headers()).submit_cross_browser_test_job)
        except Exception as exception:
            self.log.error(exception)
            Utility.print_exception(exception)
