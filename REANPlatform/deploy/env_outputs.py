"""Get Environment Deployment Outputs vars JSON."""
import logging
from cliff.command import Command
import deploy_sdk_client
from deploy_sdk_client.rest import ApiException
from reanplatform.set_header import set_header_parameter
from reanplatform.utility import Utility
from deploy.constants import DeployConstants
from deploy.utility import DeployUtility


class GetEnvOutputs(Command):
    """Get Output vars with values in JSON format for an environment."""

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        """get_parser."""
        # Define parser
        parser = super(GetEnvOutputs, self).get_parser(prog_name)
        parser.add_argument('--env_id', '-i', help='Environment id', required=True)
        parser.add_argument('--deployment_name', '-dn', default='default', help='Deployment name', required=False)
        parser.add_argument('--output', '-o',
                            help="Write output to <file> instead of stdout.",
                            required=False
                           )
        return parser

    @staticmethod
    def get_deployment_details(env_id, deployment_name):
        """Get Deployment Details."""
        try:
            # Initialise api_response
            api_response = None

            # Initialise api_instance to get deployment details
            api_client = set_header_parameter(DeployUtility.create_api_client(), Utility.get_url(DeployConstants.DEPLOY_URL))
            api_instance = deploy_sdk_client.EnvironmentApi(api_client)
            api_response = api_instance.get_deployment_details(env_id, deployment_name)
            return api_response
        except ApiException as api_exception:
            Utility.print_exception(api_exception)

    @staticmethod
    def get_resources(env_id):
        """Get All Resources for an environment."""
        try:
            # Initialise api_response
            api_response = None

            # Initialise api_instance to get deployment details
            api_client = set_header_parameter(DeployUtility.create_api_client(), Utility.get_url(DeployConstants.DEPLOY_URL))
            api_instance = deploy_sdk_client.EnvironmentApi(api_client)
            api_response = api_instance.get_all_resources(env_id)
            return api_response
        except ApiException as api_exception:
            Utility.print_exception(api_exception)

    @staticmethod
    def get_resource_status(env_deployment_id):
        """Get All deployed resources status for an environment."""
        try:
            # Initialise api_response
            api_response = None

            # Initialise api_instance to get deployment details
            api_client = set_header_parameter(DeployUtility.create_api_client(), Utility.get_url(DeployConstants.DEPLOY_URL))
            api_instance = deploy_sdk_client.EnvironmentApi(api_client)
            api_response = api_instance.get_deploy_resource_list(env_deployment_id)
            return api_response
        except ApiException as api_exception:
            Utility.print_exception(api_exception)

    def take_action(self, parsed_args):
        """take_action."""
        # Define parsed arguments
        env_id = parsed_args.env_id
        deployment_name = parsed_args.deployment_name

        env_deployment = GetEnvOutputs.get_deployment_details(env_id, deployment_name)
        if env_deployment:
            env_deployment_id = env_deployment.id

            if env_deployment.status != 'DEPLOYED':
                print("To get outputs for the environment with deployment name %s must be deployed successfully!!" % deployment_name)
                exit(1)

            # Get the existing resources for this environment.
            resources = GetEnvOutputs.get_resources(env_id)

            output_resource = next(filter(lambda x: x.resource_name == 'output', resources))

            # If the environment is deployed, then we can collect outputs.
            if output_resource:
                resource_status = GetEnvOutputs.get_resource_status(env_deployment_id)
                output_status = resource_status[str(output_resource.id)][0]
                other_attributes = output_status.other_attributes

                if parsed_args.output is not None:
                    Utility.print_output_as_dict(other_attributes, parsed_args.output)
                else:
                    print(Utility.get_parsed_json(other_attributes))

        else:
            print("Unable to find deployment for env %s  with deployment name %s" % (env_id, deployment_name))
            exit(1)
