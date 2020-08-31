"""Get accelerator version."""

import logging
from cliff.command import Command
import test_sdk_client
from test_sdk_client.rest import ApiException
from reantest.utility import Utility
from reanplatform.utility import Utility as PlatformUtility


class GetAcceleratorVersion(Command):
    """Get accelerator version."""

    log = logging.getLogger(__name__)
    _epilog = 'Example : \n\t rean-test get-accelerator-version'

    def get_parser(self, prog_name):
        """get_parser."""
        parser = super(GetAcceleratorVersion, self).get_parser(prog_name)
        return parser

    def take_action(self, parsed_args):
        """take_action."""
        self.log.debug(parsed_args)

        try:
            api_instance = test_sdk_client.VersionResourceApi(Utility.set_headers())
            version = api_instance.get_accelerator_version()

            if version:
                PlatformUtility.print_output_as_str("{} {} ".format(version["acceleratorName"],
                                                                    version["acceleratorVersion"]))
        except ApiException as exception:
            PlatformUtility.print_exception(exception)
