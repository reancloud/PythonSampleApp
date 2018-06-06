"""Get Parent Deployment Mapping Data Module."""
import logging
from cliff.command import Command
import deploy_sdk_client
import json
from deploy_sdk_client.rest import ApiException
from reanplatform.set_header import set_header_parameter
from prettytable import PrettyTable
from reanplatform.utility import Utility

class ParentMapping(Command):
    """Parent Deployment Mapping Data."""

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        """get_parser."""
        parser = super(ParentMapping, self).get_parser(prog_name)
        parser.add_argument('--environment_id', '-env_id',
                            help='Environment ID',
                            required=True)
        parser.add_argument('--deployment_id', '-dep_id',
                            help='Deployment ID',
                            required=True)
        return parser

    def take_action(self, parsed_args):
        """take action to list parent deployment mapping data"""
        # create an instance of the API class 
        instance = deploy_sdk_client.EnvironmentApi()
        api_instance = set_header_parameter(instance)
        try:
            api_response = api_instance.get_parent_deployment_mapping_data(
                parsed_args.environment_id,
                parsed_args.deployment_id
            )
        except ApiException as e:
            Utility.print_exception(e)