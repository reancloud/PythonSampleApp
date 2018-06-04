import os
from pprint import pprint
import logging
from cliff.command import Command
import deploy_sdk_client
from deploy_sdk_client.rest import ApiException
from reanplatform.set_header import set_header_parameter
from reanplatform.utility import Utility


class GetDeploymentId(Command):
    """Get Deployment Status."""
    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        """get_parser."""
        # Define parser
        parser = super(GetDeploymentId, self).get_parser(prog_name)

        try:
            parser.add_argument('--deployment_name', '-n',
                                help='Deployment Name',
                                required=True)
            parser.add_argument('--env_id', '-id',
                                help='Environment Id',
                                required=True)
        except Exception as e:
            Utility.print_exception(e)

        return parser  

    def take_action(self, parsed_args):
        """take_action."""
        instance = deploy_sdk_client.EnvironmentApi()
        api_instance = set_header_parameter(instance)

        # Check the deployment status
        try:
            api_response = api_instance.get_all_deployments_for_environment_by_id_0(parsed_args.env_id, parsed_args.deployment_name)
            id = str(api_response.id)
            pprint("Deployment ID is " + id)
        except ApiException as e:
            pprint("Environment is not deployed yet")
            Utility.print_exception(e)
        try:
            api_response_map = api_instance.get_parent_deployment_mapping_data(parsed_args.env_id, parsed_args.deployment_name)
            pprint(api_response_map)
        except ApiException as e:
            Utility.print_exception(e)
