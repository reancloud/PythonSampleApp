"""CLI to get all possible actions on the specified entity type."""
import logging
from cliff.command import Command
import deploy_sdk_client
from reanplatform.set_header import set_header_parameter
from reanplatform.utility import Utility
from deploy.constants import DeployConstants
from deploy.utility import DeployUtility


class GetEntityActions(Command):
    """CLI to get all possible actions on the specified entity type."""

    log = logging.getLogger(__name__)

    # EPILog will get print after commands
    _epilog = 'Example : rean-deploy get-entity-actions --entity_type ENVIRONMENT'

    def get_parser(self, prog_name):
        """get_parser."""
        # Define parser
        parser = super(GetEntityActions, self).get_parser(prog_name)
        parser.add_argument('--entity_type', '-t', help='Entity type. Allowed values are: [ENVIRONMENT, PACKAGE, PROVIDER, CONNECTION, DEPLOYMENT]', required=True)
        return parser

    @staticmethod
    def get_entity_actions(entity_type):
        """Get Entity Actions."""
        # Initialise api_client and api_instance
        api_client = set_header_parameter(DeployUtility.create_api_client(), Utility.get_url(DeployConstants.DEPLOY_URL))
        api_instance = deploy_sdk_client.ShareApi(api_client)
        api_response = api_instance.get_resource_actions(entity_type)
        return api_response

    @staticmethod
    def validate_resource_type(entity_type):
        """validate_resource_type."""
        resource_type = ['ENVIRONMENT', 'PACKAGE', 'PROVIDER', 'CONNECTION', 'DEPLOYMENT']
        if entity_type not in resource_type:
            raise RuntimeError("Invalid entity type. Allowed values are: [ENVIRONMENT, PACKAGE, PROVIDER, CONNECTION, DEPLOYMENT]")

    def take_action(self, parsed_args):
        """take_action."""
        # Define parsed_args
        entity_type = parsed_args.entity_type
        GetEntityActions.validate_resource_type(entity_type)
        actions = GetEntityActions.get_entity_actions(entity_type)
        if actions:
            Utility.print_output_as_dict(actions, None)
