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

        parser.add_argument('--url', '-u', help='Set url To test example:http://www.google.com.', required=True)
        parser.add_argument('--text_to_search', '-t', help='Set the text to search.', required=True)
        parser.add_argument('--page_load_time_out', '-p', help='Set the Page load timeout time in secs.')
        parser.add_argument('--upa', '-a', help='Set true if needs UPA test to run with the Test.')
        parser.add_argument('--crawl', '-cr', help='Set true if needs Crawl test to run with the Test.')

        parser.add_argument('--chrome', '-c', help='Give the comma separated versions for Chrome to run test on.')
        parser.add_argument('--firefox', '-f', help='Give the comma separated versions for Firefox to run test on.')

        parser.add_argument('--ie', '-i', help='Give the comma separated versions for IE to run test on.')
        parser.add_argument('--wait', '-w', help='Set to true for wait until job to finish.')

        return parser

    def take_action(self, parsed_args):
        """take_action."""
        self.log.debug(parsed_args)
        try:
            browser_list = Utility.get_browser_dto(parsed_args)
            self.log.debug(browser_list)

            error_message = Utility.validate_url_test_inputs(parsed_args)
            if error_message:
                self.app.stdout.write(error_message)
                return

            body = test_sdk_client.UrlTestDto()

            body.browser_list = browser_list
            body.test_url = parsed_args.url
            body.text_to_search = parsed_args.text_to_search
            body.page_load_time_out = parsed_args.page_load_time_out
            body.type = "urltest"
            body.execution_strategy = "boost"
            body.run_upa = parsed_args.upa
            body.run_crawl = parsed_args.crawl

            self.log.debug("Execution stared for URL test")
            Utility.execute_test(body, parsed_args, self.log, test_sdk_client.RunJobsApi(Utility.set_headers()).submit_url_test_job)
        except Exception as exception:
            Utility.print_exception(exception)
