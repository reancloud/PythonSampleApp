"""Run Infratest AWSSpec."""
import logging
import json
from cliff.command import Command
import test_sdk_client
from reantest.utility import Utility


class RunInfraTestAwsSpec(Command):
    """Run Infratest AWSSpec."""

    log = logging.getLogger(__name__)
    _description = 'Run Infra AWSSpec test'
    _epilog = 'Example : \n\t rean-test run-infra-awsspec --name <name> -i <Absolute path to input.json> ' \
              '-o <Absolute path to output.json> -pf <Absolute path to provider.json>'

    def get_parser(self, prog_name):
        """get_parser."""
        parser = super(RunInfraTestAwsSpec, self).get_parser(prog_name)

        parser.add_argument('--name', '-n', help='Set the name for this Infra test Job', required=True)
        parser.add_argument('--provider_file_path', '-pf', help='Provide file aws provider json file path',
                            required=True)
        parser.add_argument('--input', '-i', help='Input json file', required=False)
        parser.add_argument('--output', '-o', help='Output json file', required=False)
        parser.add_argument('--upload_input_file', '-u', help='Infrastructure detail file as zip', required=False)
        parser.add_argument('--export_jobid_path', '-ej', help='Export job id to file absolute path.')
        parser.add_argument('--wait', '-w', action='store_true', help='Wait until job finish', default=False)
        return parser

    def take_action(self, parsed_args):
        """take_action."""
        try:

            self.log.debug(parsed_args)
            awspec_param_old = test_sdk_client.AwspecParamOld()
            awspec_param_old.name = parsed_args.name
            aws_provider = test_sdk_client.AwsProviderOld()
            RunInfraTestAwsSpec.validate(parsed_args)

            with Utility.open_file(parsed_args.provider_file_path) as handle:
                filedata = handle.read()

            provider_json = json.loads(filedata)
            aws_provider.region = provider_json['region']
            if provider_json.get('access_key') is not None:
                aws_provider.access_key = provider_json['access_key']
                aws_provider.secret_key = provider_json['secret_key']
                if "aws_session_token" in provider_json:
                    aws_provider.aws_session_token = provider_json['aws_session_token']

            if provider_json.get('iam_instance_profile') is not None:
                RunInfraTestAwsSpec.validate_instance_profile_inputs(provider_json)
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

            awspec_param_old.provider = aws_provider

            if parsed_args.upload_input_file is not None:
                self.log.debug("Uploading input file ...")
                awspec_param_old.actual_input_file_name = parsed_args.upload_input_file
                awspec_param_old.input_file_name = Utility.upload_code(
                    parsed_args.upload_input_file, parsed_args.name, False)
                self.log.debug("Input code object Name : %s ", awspec_param_old.input_file_name)
            else:
                with Utility.open_file(parsed_args.input) as handle:
                    input_data = handle.read()

                awspec_param_old.input = json.loads(input_data)

                with Utility.open_file(parsed_args.output) as handle:
                    output_data = handle.read()

                awspec_param_old.output = json.loads(output_data)

            self.log.debug(awspec_param_old)
            self.log.debug("Execution stared for RunInfraTestAwsSpec")

            job_id = test_sdk_client.TestbackwardscompatibilitycontrollerApi(
                Utility.set_headers()).run_default_awspec_using_post(awspec_param_old)
            self.log.debug("Response is------------: %s ", job_id)
            Utility.export_jobid(parsed_args.name, job_id, parsed_args.export_jobid_path)
            print("The request Infra awsspec test submitted successfully. Job Id is : ", job_id)

            if parsed_args.wait:
                Utility.wait_while_job_running(job_id)

        except Exception as exception:
            Utility.print_exception(exception)

    @staticmethod
    def validate(parsed_args):
        """Validate argument."""
        if parsed_args.upload_input_file is None and parsed_args.input is None and parsed_args.output is None:
            raise RuntimeError("Provide input, output or upload input file path.")

        if parsed_args.upload_input_file is None:
            if parsed_args.input is None or parsed_args.output is None:
                raise RuntimeError("Provide input and output.")

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
