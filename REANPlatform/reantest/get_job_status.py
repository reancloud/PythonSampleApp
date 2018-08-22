"""Get User Job Status."""
import logging
from cliff.command import Command
from reantest.utility import Utility

import test_sdk_client


class GetJobStatus(Command):
    """Get user job status."""

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        """get_parser."""
        parser = super(GetJobStatus, self).get_parser(prog_name)

        parser.add_argument('--job_id', '-j',
                            help='Set Job Id to get Job status example:396f4cfc2c4d46c7921532741c7ab63e.',
                            required=True)
        return parser

    def take_action(self, parsed_args):
        """take_action."""
        self.log.debug(parsed_args)

        try:
            api_instance = test_sdk_client.RunTestApi(Utility.set_headers())
            api_response = api_instance.get_job_status(parsed_args.job_id)
            self.log.debug(api_response)
            print(api_response)
        except Exception as exception:
            Utility.print_exception(exception)
