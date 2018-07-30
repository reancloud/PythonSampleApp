"""Run get report CLI."""

from pathlib import Path
import logging
from cliff.command import Command
import test_sdk_client
from reantest.utility import Utility


class GetJobReport(Command):
    """Get job reports."""

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        """get_parser."""
        parser = super(GetJobReport, self).get_parser(prog_name)
        parser.add_argument('--job_id', '-j', help='Set Job Id to get Job status example:396f4cfc2c4d46c7921532741c7ab63e.', required=True)
        parser.add_argument('--output_dir', '-od', help='Set Output directory to store reports.')
        return parser

    def take_action(self, parsed_args):
        """take_action."""
        self.log.debug(parsed_args)

        try:
            api_instance = test_sdk_client.RunJobsApi()
            # api_instance.api_client.select_header_accept("application/zip")
            api_response = api_instance.get_job_report(parsed_args.job_id, _preload_content=False)

            file_name = 'reports_' + parsed_args.job_id + '.zip'
            if parsed_args.output_dir is not None and Utility.validate_path(parsed_args):
                self.log.debug("File path Exists")
                if parsed_args.output_dir.endswith('/'):
                    open(parsed_args.output_dir + file_name, 'wb').write(api_response.data)
                else:
                    open(parsed_args.output_dir + '/' + file_name, 'wb').write(api_response.data)
            else:
                print("File path not exists")
                open(str(Path.home()) + "/" + file_name, 'wb').write(api_response.data)

            print("Executed successfully.")
        except Exception as exception:
            self.log.error("Exception when calling GetJobReports->get_job_reports: %s\n", exception)
