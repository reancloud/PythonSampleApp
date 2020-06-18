"""Destroy deployment module."""
import logging
import time
import json
from cliff.command import Command
import deploy_sdk_client
from deploy_sdk_client.rest import ApiException
from reanplatform.set_header import set_header_parameter
from reanplatform.utility import Utility
from deploy.constants import DeployConstants
from deploy.utility import DeployUtility


class DestroyDeployment(Command):
    """Destroy deployment."""

    log = logging.getLogger(__name__)

    # EPILog will get print after commands
    _epilog = 'Example : rean-deploy destroy-deployment --env_id 1 --deployment_name dummyDeployment'

    def get_parser(self, prog_name):
        """get_parser."""
        parser = super(DestroyDeployment, self).get_parser(prog_name)
        parser.add_argument('--env_id', '-i', help='Environment id.', required=True)
        parser.add_argument('--deployment_name', '-dn', default='default', help='Deployment name.', required=False)
        parser.add_argument('--output', '-o',
                            help="Write output to <file> instead of stdout.",
                            required=False
                           )
        return parser

    def take_action(self, parsed_args):
        """take_action."""
        env_id = parsed_args.env_id
        deployment_name = parsed_args.deployment_name

        DestroyDeployment.destroy_by_envid_deploymentname(env_id, deployment_name, parsed_args)

    @staticmethod
    def destroy_by_envid_deploymentname(env_id, deployment_name, parsed_args):
        """destroy_by_envid_deploymentname."""
        try:
            api_client = set_header_parameter(DeployUtility.create_api_client(), Utility.get_url(DeployConstants.DEPLOY_URL))
            env_api_instance = deploy_sdk_client.EnvironmentApi(api_client)
            deploy_status = None

            deployment_response = env_api_instance.destroy_deployment(env_id, deployment_name)
        except ApiException as api_exception:
            Utility.print_exception(api_exception)

        try:
            while 1:
                deploy_status = env_api_instance.get_deployment_details(env_id, deployment_name)
                status_dict = str(deploy_status.status)
                if "DESTROYING" in status_dict:
                    time.sleep(1)
                else:
                    break
        except ApiException as api_exception:
            err = json.loads(api_exception.body)
            error_message = "Deployment with Environment ID: {} and Deployment name {} does not exist.".format(env_id, deployment_name)
            if error_message in err['message']:
                Utility.print_output_as_str("Environment Status : DESTROYED")
