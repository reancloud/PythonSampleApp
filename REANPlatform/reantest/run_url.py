"""run url test module."""
import logging
# from argparse import ArgumentDefaultsHelpFormatter
from cliff.command import Command
import validators
import test_sdk_client
from reantest.utility import Utility


class RunURLTest(Command):
    """Run URL test."""

    log = logging.getLogger(__name__)

    _description = 'Run URL test'
    _epilog = 'Example : \n\t rean-test run-url-test -u http://www.google.com -t GMail -c 64 -w true'
    # EPILog will get print after commands

    def get_parser(self, prog_name):
        """get_parser."""
        parser = super(RunURLTest, self).get_parser(prog_name)

        # parser.formatter_class = ArgumentDefaultsHelpFormatter
        parser.add_argument('--app_name', '-a', help='Set the name for this Automation Job.', required=True)
        parser.add_argument('--url', '-u', help='Set url To test example:http://www.google.com', required=True)
        parser.add_argument('--text_to_search', '-t', type=str, help='Set the text to search', required=True)

        parser.add_argument('--page_load_time_out', '-p', type=int, help='Set the Page load timeout time in secs', required=True)
        parser.add_argument('--crawl', '-cr', help='Set true if needs Crawl test to run with the Test')
        parser.add_argument('--chrome', '-c', help='Give the comma separated versions for Chrome to run test on')
        parser.add_argument('--firefox', '-f', help='Give the comma separated versions for Firefox to run test on')
        parser.add_argument('--ie', '-i', help='Give the comma separated versions for IE to run test on')
        parser.add_argument('--export_jobid_path', '-ej', help='Export job id to file absolute path.')
        parser.add_argument('--wait', '-w', action='store_true', help='Wait until job finish', default=False)

        return parser

    def take_action(self, parsed_args):
        """take_action."""
        self.log.debug(parsed_args)
        try:
            browser_list = Utility.get_browser_dto(parsed_args)
            self.log.debug(browser_list)

            RunURLTest.validate_url_test_inputs(parsed_args)

            url_test_dto_new = test_sdk_client.UrlTestOldDto()
            url_test_dto_new.name = parsed_args.app_name
            url_test_dto_new.browsers = browser_list
            url_test_dto_new.test_url = parsed_args.url
            url_test_dto_new.text_to_search = parsed_args.text_to_search
            url_test_dto_new.page_load_time_out = parsed_args.page_load_time_out
            url_test_dto_new.type = "urltest"
            url_test_dto_new.run_upa = False
            url_test_dto_new.run_crawl = parsed_args.crawl

            self.log.debug("Execution stared for URL test")

            response_url_test_dto_new = test_sdk_client.TestbackwardscompatibilitycontrollerApi(
                Utility.set_headers()).run_url_test_using_post1(url_test_dto_new)
            job_id = response_url_test_dto_new.id

            self.log.debug("Response is------------: %s ", job_id)
            Utility.export_jobid(parsed_args.app_name, job_id, parsed_args.export_jobid_path)
            print("The request URL test submitted successfully. Job Id is : ", job_id)

            if parsed_args.wait:
                Utility.wait_while_job_running(job_id)

        except Exception as exception:
            self.log.debug(exception)
            Utility.print_exception(exception)
            return 1

    @staticmethod
    def validate_url_test_inputs(params):
        """Validate url and browsers input."""

        # Validation for Test URL
        if not validators.url(params.url):
            raise RuntimeError("Please enter valid Test URL.")

        # Validation for Browser list
        if params.chrome is None and params.firefox is None and params.ie is None:
            raise RuntimeError("Please Provide at least one browser to Test.")
