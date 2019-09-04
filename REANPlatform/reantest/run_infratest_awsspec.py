"""Run Infratest AWSSpec."""
import logging
import json
from cliff.command import Command
from reantest.utility import Utility
import test_sdk_client


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
        parser.add_argument('--input', '-i', help='Input json file', required=True)
        parser.add_argument('--output', '-o', help='Output json file', required=True)
        return parser

    def take_action(self, parsed_args):
        """take_action."""
        try:

            self.log.debug(parsed_args)
            body = test_sdk_client.AwspecParam()
            body.name = parsed_args.name
            aws_provider = test_sdk_client.AwsProvider()
            with Utility.open_file(parsed_args.provider_file_path) as handle:
                filedata = handle.read()

            provider_json = json.loads(filedata)
            aws_provider.region = provider_json['region']
            if provider_json.get('access_key') is not None:
                aws_provider.access_key = provider_json['access_key']
                aws_provider.secret_key = provider_json['secret_key']

            if provider_json.get('iam_instance_profile') is not None:
                instance_profile = test_sdk_client.InstanceProfile
                instance_profile.name = provider_json['iam_instance_profile']['name']
                instance_profile.arn = provider_json['iam_instance_profile']['arn']
                aws_provider.iam_instance_profile = instance_profile

            if provider_json.get('assume_role') is not None:
                assume_role = test_sdk_client.AssumeRole
                assume_role.role_arn = provider_json['assume_role']['role_arn']
                assume_role.session_name = provider_json['assume_role']['session_name']
                assume_role.external_id = provider_json['assume_role']['external_id']
                aws_provider.assume_role = assume_role

            body.provider = aws_provider

            with Utility.open_file(parsed_args.input) as handle:
                input_data = handle.read()

            body.input = json.loads(input_data)

            with Utility.open_file(parsed_args.output) as handle:
                output_data = handle.read()

            body.output = json.loads(output_data)

            self.log.debug(body)
            self.log.debug("Execution stared for RunInfraTestAwsSpec")

            job_id = test_sdk_client.RunTestNewApi(Utility.set_headers()).execute_infra_awspec(body)
            self.log.debug("Response is------------: %s ", job_id)
            print("The request Infra awsspec test submitted successfully. Job Id is : ", job_id)

        except Exception as exception:
            Utility.print_exception(exception)
