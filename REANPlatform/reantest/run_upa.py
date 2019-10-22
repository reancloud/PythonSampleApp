"""Run UPA Test."""
import logging
from cliff.command import Command
import test_sdk_client
from reantest.utility import Utility


class RunUPA(Command):
    """Run UI Performance test."""

    log = logging.getLogger(__name__)
    _epilog = 'Example : \n\t rean-test run-upa-test --app_name <app_test> --url <application_url> ' \
              '--text_to_search <search_text> --page_load_time_out <time_out_in_seconds>'

    def get_parser(self, prog_name):
        """get_parser."""
        parser = super(RunUPA, self).get_parser(prog_name)

        parser.add_argument('--app_name', '-a', help='Set the name for this Automation Job.', required=True)
        parser.add_argument('--url', '-u', help='Set upa To test example:http://www.google.com.', required=True)
        parser.add_argument('--text_to_search', '-s', help='Set the text to search.', required=True)
        parser.add_argument('--page_load_time_out', '-p', help='Set the Page load timeout time in secs.', required=True)
        parser.add_argument('--crawl', '-c', help='Set true if needs Crawl test to run with the Test.')
        parser.add_argument('--wait', '-w', help='Set to true for wait until job to finish.')

        return parser

    def take_action(self, parsed_args):
        """take_action."""
        self.log.debug(parsed_args)
        try:
            error_message = Utility.validate_url(parsed_args)
            if error_message:
                self.app.stdout.write(error_message)
                return

            body = test_sdk_client.UpaTestDto()

            body.app_name = parsed_args.app_name
            body.test_url = parsed_args.url
            body.text_to_search = parsed_args.text_to_search
            body.page_load_time_out = parsed_args.page_load_time_out
            body.type = "upatest"  # type
            body.execution_strategy = "boost"  # execution_strategy
            body.run_upa = True
            body.run_crawl = parsed_args.crawl

            self.log.debug(body)

            self.log.debug("Execution stared for UPA Test")
            Utility.execute_test(body, parsed_args, self.log, test_sdk_client.RunJobsApi(Utility.set_headers()).submit_upa_test_job)

        except Exception as exception:
            Utility.print_exception(exception)
