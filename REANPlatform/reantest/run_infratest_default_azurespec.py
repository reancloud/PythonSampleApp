"""Run Infratest Default AzureSpec."""
import logging
import json
from cliff.command import Command
import test_sdk_client
import deploy_sdk_client
from reantest.utility import Utility as TestUtility
from reanplatform.set_header import set_header_parameter
from reanplatform.utility import Utility as PlatformUtility
from deploy.utility import DeployUtility
from deploy.constants import DeployConstants


class RunInfraDefaultAzureSpec(Command):
    """Run Infratest Default AzureSpec."""

    log = logging.getLogger(__name__)
    _description = 'Run Infra Default AzureSpec test'
    _epilog = 'Example : \n\t rean-test run-infra-default-azurespec --name <name> -i <Absolute path to input.json> ' \
              '--env_name <environment name> -pf <Absolute path to provider.json>'

    def get_parser(self, prog_name):
        """get_parser."""
        parser = super(RunInfraDefaultAzureSpec, self).get_parser(prog_name)

        parser.add_argument('--name', '-n', help='Set the name for this Infra test Job', required=True)
        parser.add_argument('--env_name', '-en', help='Environment name', required=False)
        parser.add_argument('--env_version', '-ev', help='Environment version.', required=False)
        parser.add_argument('--env_id', '-id', help='Environment id', required=False)
        parser.add_argument('--provider_file_path', '-pf', help='Provide file azure provider json file path',
                            required=True)
        parser.add_argument('--input', '-i', help='Input json file', required=True)
        parser.add_argument('--deployment_name', '-dn', default='default',
                            help='Deployment name. Please provide this attribute if deployment name is not default.',
                            required=False)
        return parser

    def take_action(self, parsed_args):
        """take_action."""
        try:

            self.log.debug(parsed_args)
            body = test_sdk_client.AzurespecParam()
            body.name = parsed_args.name
            azure_provider = test_sdk_client.AzureProvider()
            RunInfraDefaultAzureSpec.validate_env_inputs(parsed_args.env_id, parsed_args.env_name)
            with TestUtility.open_file(parsed_args.provider_file_path) as handle:
                filedata = handle.read()

            provider_json = json.loads(filedata)
            if provider_json.get('subscription_id') is not None:
                azure_provider.subscription_id = provider_json['subscription_id']

            if provider_json.get('client_id') is not None:
                azure_provider.client_id = provider_json['client_id']

            if provider_json.get('client_secret') is not None:
                azure_provider.client_secret = provider_json['client_secret']

            if provider_json.get('tenant_id') is not None:
                azure_provider.tenant_id = provider_json['tenant_id']

            body.azure_provider = azure_provider

            with TestUtility.open_file(parsed_args.input) as handle:
                input_data = handle.read()

            body.input = json.loads(input_data)

            api_client = set_header_parameter(DeployUtility.create_api_client(),
                                              PlatformUtility.get_url(DeployConstants.DEPLOY_URL))
            api_instance = deploy_sdk_client.EnvironmentApi(api_client)

            if parsed_args.env_name is not None:
                if parsed_args.env_version is not None:
                    env_res = api_instance.get_environment_by_version_and_name(parsed_args.env_name,
                                                                               parsed_args.env_version)
                else:
                    env_res = api_instance.get_environment_by_name_with_latest_version(parsed_args.env_name)

            if parsed_args.env_id is not None:
                api_status = api_instance.get_deploy_status_by_env_id_and_deployment_name(parsed_args.env_id,
                                                                                          parsed_args.deployment_name)
            else:
                api_status = api_instance.get_deploy_status_by_env_id_and_deployment_name(env_res.id,
                                                                                          parsed_args.deployment_name)

            if api_status.status != 'DEPLOYED':
                message = "Environment status is not Deployed."
                if message:
                    raise RuntimeError(message)

            if parsed_args.env_id is not None:
                api_response = api_instance.get_deployed_resource_ids_by_env_id_and_dep_name(parsed_args.env_id,
                                                                                             parsed_args.deployment_name)
            else:
                api_response = api_instance.get_deployed_resource_ids_by_env_id_and_dep_name(env_res.id,
                                                                                             parsed_args.deployment_name)

            body.output = api_response

            self.log.debug(body)
            self.log.debug("Execution started for RunInfraTestDefaultAzureSpec")

            job_id = test_sdk_client.RunTestNewApi(TestUtility.set_headers()).execute_infra_azurespec(body)
            self.log.debug("Response is------------: %s ", job_id)
            print("The request Infra  default azurespec test submitted successfully. Job Id is : ", job_id)

        except Exception as exception:
            TestUtility.print_exception(exception)

    @staticmethod
    def validate_env_inputs(env_id, env_name):
        """Validate EnvId or EnvName."""
        message = ""

        if env_id is not None and env_name is not None:
            message = "Please Provide either env_id or env_name."

        elif env_id is None and env_name is None:
            message = "Please Provide either env_id or env_name."

        if message:
            raise RuntimeError(message)
