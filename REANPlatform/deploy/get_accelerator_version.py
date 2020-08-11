"""Get Accelerator Version."""
import logging
from cliff.command import Command
import deploy_sdk_client
from deploy_sdk_client.rest import ApiException
from reanplatform.set_header import set_header_parameter
from reanplatform.utility import Utility
from deploy.constants import DeployConstants
from deploy.utility import DeployUtility


class GetAcceleratorVersion(Command):
    """Get Accelerator Version."""

    log = logging.getLogger(__name__)

    # EPILog will get print after commands
    _epilog = 'Example : rean-deploy get-accelerator-version'

    def get_parser(self, prog_name):
        """get_parser."""
        # Define parser
        parser = super(GetAcceleratorVersion, self).get_parser(prog_name)
        return parser

    def take_action(self, parsed_args):
        """take_action."""
        try:
            # Initialise version
            version = None
            # Initialise api_client and api_instance to get accelerator version
            api_client = set_header_parameter(DeployUtility.create_api_client(), Utility.get_url(DeployConstants.DEPLOY_URL))
            api_instance = deploy_sdk_client.VersionControllerApi(api_client)
            version = api_instance.get_accelerator_version()
            if version:
                Utility.print_output_as_str("{} {} ".format(version.accelerator_name, version.accelerator_version))
        except ApiException as api_exception:
            Utility.print_exception(api_exception)
