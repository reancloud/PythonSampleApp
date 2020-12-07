"""Run Infratest Default AwsSpec."""

import logging
import json
from cliff.command import Command
import test_sdk_client
from deploy.getdeploymentstatus import Status
from deploy.get_deployment_resource_ids import GetDeploymentResourceIds
from deploy.getenvironment import GetEnvironment
from reantest.utility import Utility as TestUtility


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
        parser.add_argument('--env_name', '-en', help='Environment name', required=False)
        parser.add_argument('--env_id', '-id', help='Environment id', required=False)
        parser.add_argument('--env_version', '-ev', help='Environment version.', required=False)
        parser.add_argument('--provider_file_path', '-pf', help='Provide file aws provider json file path',
                            required=True)
        parser.add_argument('--input', '-i', help='Input json file', required=True)
        parser.add_argument('--deployment_name', '-dn', default='default',
                            help='Deployment name. Please provide this attribute if deployment name is not default.',
                            required=False)
        parser.add_argument('--export_jobid_path', '-ej', help='Export job id to file absolute path.')
        parser.add_argument('--wait', '-w', action='store_true', help='Wait until job finish', default=False)

        return parser

    def take_action(self, parsed_args):
        """take_action."""
        try:

            self.log.debug(parsed_args)
            body = test_sdk_client.AwspecParamOld()
            body.name = parsed_args.name
            aws_provider = test_sdk_client.AwsProviderOld()
            with TestUtility.open_file(parsed_args.provider_file_path) as handle:
                filedata = handle.read()

            provider_json = json.loads(filedata)
            RunInfraTestDefaultAwsSpec.validate_env_inputs(parsed_args.env_id, parsed_args.env_name)
            aws_provider.region = provider_json['region']
            if provider_json.get('access_key') is not None:
                aws_provider.access_key = provider_json['access_key']
                aws_provider.secret_key = provider_json['secret_key']
                if "aws_session_token" in provider_json:
                    aws_provider.aws_session_token = provider_json['aws_session_token']

            if provider_json.get('iam_instance_profile') is not None:
                RunInfraTestDefaultAwsSpec.validate_instance_profile_inputs(provider_json)
                instance_profile = test_sdk_client.InstanceProfileOld
                if 'name' in provider_json['iam_instance_profile']:
                    instance_profile.name = provider_json['iam_instance_profile']['name']
                    instance_profile.arn = None
                if 'arn' in provider_json['iam_instance_profile']:
                    instance_profile.name = None
                    instance_profile.arn = provider_json['iam_instance_profile']['arn']
                aws_provider.iam_instance_profile = instance_profile

            if provider_json.get('assume_role') is not None:
                assume_role = test_sdk_client.AssumeRoleOld
                assume_role.role_arn = provider_json['assume_role']['role_arn']
                assume_role.session_name = provider_json['assume_role']['session_name']
                assume_role.external_id = provider_json['assume_role']['external_id']
                aws_provider.assume_role = assume_role

            body.provider = aws_provider

            with TestUtility.open_file(parsed_args.input) as handle:
                input_data = handle.read()

            body.input = json.loads(input_data)

            if parsed_args.env_name is not None:
                if parsed_args.env_version is not None:

                    env_res = GetEnvironment.get_environment_by_name_and_version(parsed_args.env_name, parsed_args.env_version)
                else:
                    env_res = GetEnvironment.get_environment_by_env_name(parsed_args.env_name)

            if parsed_args.env_id is not None:
                api_status = Status.deployment_status(parsed_args.env_id, parsed_args.deployment_name)
            else:
                api_status = Status.deployment_status(env_res.id, parsed_args.deployment_name)

            status_dict = str(api_status)
            if "DEPLOYED" not in status_dict:
                message = "Environment status is not Deployed."
                if message:
                    raise RuntimeError(message)

            if parsed_args.env_id is not None:
                api_response = GetDeploymentResourceIds.get_deployment_resource_ids(parsed_args.env_id, parsed_args.deployment_name)

            else:
                api_response = GetDeploymentResourceIds.get_deployment_resource_ids(env_res.id, parsed_args.deployment_name)

            body.output = api_response

            self.log.debug(body)
            self.log.debug("Execution started for RunInfraTestDefaultAwsSpec")

            job_id = test_sdk_client.TestbackwardscompatibilitycontrollerApi(
                TestUtility.set_headers()).run_default_awspec_using_post(body)
            self.log.debug("Response is------------: %s ", job_id)
            print("The request Infra test Default AwsSpec submitted successfully. Job Id is : ", job_id)

            if parsed_args.wait:
                TestUtility.wait_while_job_running(test_sdk_client.TestbackwardscompatibilitycontrollerApi(
                    TestUtility.set_headers()), job_id, False)

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
