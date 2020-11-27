"""Run get report CLI."""

from pathlib import Path
import logging
from cliff.command import Command
import test_sdk_client
from reantest.utility import Utility


class GetJobReport(Command):
    """Get job reports."""

    log = logging.getLogger(__name__)
    _epilog = 'Example : \n\t rean-test get-job-report -j <job_id>'

    def get_parser(self, prog_name):
        """get_parser."""
        parser = super(GetJobReport, self).get_parser(prog_name)
        parser.add_argument('--job_id', '-j', help='Set Job Id to get Job status.', required=True)
        parser.add_argument('--output_directory', '-o', help='Set Output directory to store reports.')
        return parser

    def take_action(self, parsed_args):
        """take_action."""
        self.log.debug(parsed_args)

        try:
            api_instance = test_sdk_client.RunJobsApi(Utility.set_headers())
            api_response = api_instance.get_job_report(parsed_args.job_id, _preload_content=False)

            file_name = 'reports_' + parsed_args.job_id + '.zip'
            if parsed_args.output_directory is not None and Utility.validate_path(parsed_args):
                self.log.debug("File path Exists")
                if parsed_args.output_directory.endswith('/'):
                    open(parsed_args.output_directory + file_name, 'wb').write(api_response.data)
                    print("Reports downloaded successfully at " + parsed_args.output_directory + file_name)
                else:
                    open(parsed_args.output_directory + '/' + file_name, 'wb').write(api_response.data)
                    print("Reports downloaded successfully at " + parsed_args.output_directory + '/' + file_name)
            else:
                self.log.debug("File path not exists")
                open(str(Path.home()) + "/" + file_name, 'wb').write(api_response.data)
                print("Reports downloaded successfully at " + str(Path.home()) + "/" + file_name)

        except Exception as exception:
            Utility.print_exception(exception)
