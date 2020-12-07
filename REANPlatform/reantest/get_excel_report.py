"""Run get excel report CLI."""

import os
import logging
from cliff.command import Command
from reantest.utility import Utility

from reanplatform.constants import Constants
from reanplatform.utility import Utility as PlatformUtility


class GetExcelReport(Command):
    """Get excel reports."""

    log = logging.getLogger(__name__)
    _epilog = 'Example : \n\t rean-test get-excel-report -j <job_id>'

    def get_parser(self, prog_name):
        """get_parser."""
        parser = super(GetExcelReport, self).get_parser(prog_name)
        parser.add_argument('--job_id', '-j', help='Set Job Id to get Job status.', required=True)
        parser.add_argument('--output_directory', '-o', help='Set Output directory to store reports.')
        return parser

    def take_action(self, parsed_args):
        """take_action."""
        self.log.debug(parsed_args)
        job_id = parsed_args.job_id
        output_directory = parsed_args.output_directory

        try:
            path = '/export/excel/' + job_id
            curl_url = Constants.PLATFORM_BASE_URL + Constants.TEST_URL + path
            api_response = PlatformUtility.get_zip_stream(curl_url)
            if api_response.status_code == 200:
                file_name = 'TestData-' + job_id + '.xlsx'
                if output_directory is not None:
                    if os.path.isdir(output_directory):
                        if parsed_args.output_directory.endswith('/'):
                            output_directory = output_directory + file_name
                        else:
                            output_directory = output_directory + '/' + file_name
                    else:
                        raise RuntimeError("Invalid path! Please provide a valid path")
                else:
                    output_directory = os.path.abspath(file_name)
                open(output_directory, 'wb').write(api_response.content)
                print("Reports downloaded successfully at " + output_directory)
            else:
                print(api_response.text)
        except Exception as exception:
            Utility.print_exception(exception)
