"""run url test module."""
import logging
from cliff.command import Command
import test_sdk_client
from reantest.utility import Utility


class RunURLTest(Command):
    """Run URL test."""

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        """get_parser."""
        parser = super(RunURLTest, self).get_parser(prog_name)

        # 'browser_list': 'BrowsersDto',
        # 'test_url': 'str',
        # 'text_to_search': 'str',
        # 'page_load_time_out': 'int',
        # 'type': 'str',
        # 'execution_strategy': 'str',
        # 'run_upa': 'str',
        # 'run_crawl': 'str'

        parser.add_argument('--url', '-u', help='Set url To test example:http://www.google.com.', required=True)
        parser.add_argument('--text_to_search', '-t', help='Set the text to search.', required=True)
        parser.add_argument('--page_load_time_out', '-p', help='Set the Page load timeout time in secs.')
        parser.add_argument('--upa', '-r', help='Set true if needs UPA test to run with the Test.')
        parser.add_argument('--crawl', '-c', help='Set true if needs Crawl test to run with the Test.')

        parser.add_argument('--chrome', '-C', help='Give the comma separated versions for Chrome to run test on.')
        parser.add_argument('--firefox', '-F', help='Give the comma separated versions for Firefox to run test on.')

        parser.add_argument('--ie', '-I', help='Give the comma separated versions for IE to run test on.')
        parser.add_argument('--wait', '-w', help='Set to true for wait until job to finish.')
        # parser.add_argument('--safari', '-S', help='message')
        # parser.add_argument('--ios', '-A', help='message')
        # parser.add_argument('--ui_perf_analysis', '-U', help='message')
        # parser.add_argument('--device', '-D', help='message')

        return parser

    def take_action(self, parsed_args):
        """take_action."""
        self.log.debug(parsed_args)

        browser_list = Utility.get_browser_dto(parsed_args)
        self.log.debug(browser_list)

        error_message = Utility.validate_url_test_inputs(parsed_args)
        if error_message:
            self.app.stdout.write(error_message)
            return

        # order should be maintained as the constructor takes values as parameter in the same order.
        body = test_sdk_client.UrlTestDto(
            browser_list,
            parsed_args.url,
            parsed_args.text_to_search,
            parsed_args.page_load_time_out,
            "urltest",  # type
            "boost",  # execution_strategy
            parsed_args.upa,
            parsed_args.crawl)

        try:
            self.log.debug("Execution stared for URL Test")
            Utility.execute_test(body, parsed_args, self.log, test_sdk_client.RunJobsApi().submit_url_test_job)
        except Exception as exception:
            self.log.error("Exception when calling RunUrlTest->submit_url_test_job: %s\n", exception)
