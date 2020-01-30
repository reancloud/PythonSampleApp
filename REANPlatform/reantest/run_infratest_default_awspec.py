"""Run Infratest Default AwsSpec."""

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


class RunInfraTestDefaultAwsSpec(Command):
    """Run Infratest Default AwsSpec."""

    log = logging.getLogger(__name__)
    _description = 'Run Infra test Default AwsSpec'
    _epilog = 'Example : \n\t rean-test run-infratest-default-awsspec --name <name> -i <Absolute path to input.json> ' \
              '--env_name <environment name> -pf <Absolute path to provider.json>'

    def get_parser(self, prog_name):
        """get_parser."""
        parser = super(RunInfraTestDefaultAwsSpec, self).get_parser(prog_name)

        parser.add_argument('--name', '-n', help='Set the name for this Infra test Job', required=True)
        parser.add_argument('--env_name', '-en', help='Environment name', required=True)
        parser.add_argument('--env_version', '-ev', help='Environment version.', required=False)
        parser.add_argument('--provider_file_path', '-pf', help='Provide file aws provider json file path',
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
            body = test_sdk_client.AwspecParam()
            body.name = parsed_args.name
            aws_provider = test_sdk_client.AwsProvider()
            with TestUtility.open_file(parsed_args.provider_file_path) as handle:
                filedata = handle.read()

            provider_json = json.loads(filedata)
            RunInfraTestDefaultAwsSpec.validate_instance_profile_inputs(provider_json)
            aws_provider.region = provider_json['region']
            if provider_json.get('access_key') is not None:
                aws_provider.access_key = provider_json['access_key']
                aws_provider.secret_key = provider_json['secret_key']

            if provider_json.get('iam_instance_profile') is not None:
                instance_profile = test_sdk_client.InstanceProfile
                if 'name' in provider_json['iam_instance_profile']:
                    instance_profile.name = provider_json['iam_instance_profile']['name']
                    instance_profile.arn = None
                if 'arn' in provider_json['iam_instance_profile']:
                    instance_profile.name = None
                    instance_profile.arn = provider_json['iam_instance_profile']['arn']
                aws_provider.iam_instance_profile = instance_profile

            if provider_json.get('assume_role') is not None:
                assume_role = test_sdk_client.AssumeRole
                assume_role.role_arn = provider_json['assume_role']['role_arn']
                assume_role.session_name = provider_json['assume_role']['session_name']
                assume_role.external_id = provider_json['assume_role']['external_id']
                aws_provider.assume_role = assume_role

            body.provider = aws_provider

            with TestUtility.open_file(parsed_args.input) as handle:
                input_data = handle.read()

            body.input = json.loads(input_data)

            api_client = set_header_parameter(DeployUtility.create_api_client(),
                                              PlatformUtility.get_url(DeployConstants.DEPLOY_URL))
            api_instance = deploy_sdk_client.EnvironmentApi(api_client)

            if parsed_args.env_version is not None:
                env_res = api_instance.get_environment_by_version_and_name(parsed_args.env_name, parsed_args.env_version)
            else:
                env_res = api_instance.get_environment_by_name_with_latest_version(parsed_args.env_name)

            api_status = api_instance.get_deploy_status_by_env_id_and_deployment_name(env_res.id, parsed_args.deployment_name)

            if api_status.status != 'DEPLOYED':
                message = "Environment status is not Deployed."
                if message:
                    raise RuntimeError(message)

            api_response = api_instance.get_deployed_resource_ids_by_env_id_and_dep_name(env_res.id, parsed_args.deployment_name)

            body.output = api_response

            self.log.debug(body)
            self.log.debug("Execution started for RunInfraTestDefaultAwsSpec")

            job_id = test_sdk_client.RunTestNewApi(TestUtility.set_headers()).execute_infra_awspec(body)
            self.log.debug("Response is------------: %s ", job_id)
            print("The request Infra test Default AwsSpec submitted successfully. Job Id is : ", job_id)

        except Exception as exception:
            TestUtility.print_exception(exception)

    @staticmethod
    def validate_instance_profile_inputs(params):
        """Validate Role and name."""
        message = ""
        # # Validation name and arn
        if 'iam_instance_profile' in params:
            if 'arn' in params['iam_instance_profile'] and 'name' in params['iam_instance_profile']:
                message = "Please Provide either name or role arn."

        if message:
            raise RuntimeError(message)
