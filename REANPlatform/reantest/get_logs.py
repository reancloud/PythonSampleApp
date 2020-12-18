"""Get Job logs."""
import os
import logging
from cliff.command import Command
from reantest.utility import Utility
import test_sdk_client

class GetLogs(Command):
    """Get user job status."""

    log = logging.getLogger(__name__)
    _epilog = 'Example : \n\t rean-test get-job-logs -j <job_id> -f <firefox_version> -o <path_to_output_directory>'

    def get_parser(self, prog_name):
        """get_parser."""
        parser = super(GetLogs, self).get_parser(prog_name)

        parser.add_argument('--job_id', '-j', help='Set Job Id to get Job logs.', required=True)
        parser.add_argument('--chrome', '-c', help='Set Chrome version to get Job logs.')
        parser.add_argument('--firefox', '-f', help='Set Firefox version to get Job logs.')
        parser.add_argument('--output_directory', '-o', help='Set Output directory to store reports.')

        return parser

    def take_action(self, parsed_args):
        """take_action."""
        self.log.debug(parsed_args)

        try:
            browser_type = None
            browser_version = None
            job_id = parsed_args.job_id
            if parsed_args.chrome:
                browser_type = 'Chrome'
                browser_version = parsed_args.chrome

            if parsed_args.firefox:
                browser_type = 'Firefox'
                browser_version = parsed_args.firefox

            api_instance = test_sdk_client.TeststoragecontrollerApi(Utility.set_headers())
            api_response = api_instance.download_logs_by_browser_using_get(
                browser_type, job_id, browser_version, _preload_content=False)

            file_name = job_id + '-' + browser_type + '-' + browser_version + '.log'
            if parsed_args.output_directory is not None and Utility.validate_path(parsed_args):
                self.log.debug("File path Exists")
                if parsed_args.output_directory.endswith('/'):
                    open(parsed_args.output_directory + file_name, 'wb').write(api_response.data)
                    print("Logs downloaded successfully at " + parsed_args.output_directory + file_name)
                else:
                    open(parsed_args.output_directory + '/' + file_name, 'wb').write(api_response.data)
                    print("Logs downloaded successfully at " + parsed_args.output_directory + '/' + file_name)
            else:
                self.log.debug("File path not exists")
                open(os.path.abspath(file_name), 'wb').write(api_response.data)
                print("Logs downloaded successfully at " + os.path.abspath(file_name))

        except Exception as exception:
            Utility.print_exception(exception)
