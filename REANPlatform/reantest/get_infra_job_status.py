"""Get User Job Status."""
import logging
from cliff.command import Command
from reantest.utility import Utility

import test_sdk_client


class GetInfraJobStatus(Command):
    """Get infra job status."""

    log = logging.getLogger(__name__)
    _epilog = 'Example : \n\t rean-test get-infra-job-status -j <job_id>'

    def get_parser(self, prog_name):
        """get_parser."""
        parser = super(GetInfraJobStatus, self).get_parser(prog_name)

        parser.add_argument('--job_id', '-j',
                            help='Set Job Id to get Job status.',
                            required=True)
        return parser

    def take_action(self, parsed_args):
        """take_action."""
        self.log.debug(parsed_args)

        try:
            api_instance = test_sdk_client.InfraTestApi(Utility.set_headers())
            api_response = api_instance.get_infra_test_job_status(parsed_args.job_id)
            self.log.debug(api_response)
            print(api_response)
        except Exception as exception:
            Utility.print_exception(exception)
