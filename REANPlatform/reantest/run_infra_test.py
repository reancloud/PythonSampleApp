"""Run UPA Test."""
import logging
import json
from cliff.command import Command
import test_sdk_client
from reantest.utility import Utility


class RunInfraTest(Command):
    """Run InfraTest."""

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        """get_parser."""
        parser = super(RunInfraTest, self).get_parser(prog_name)

        parser.add_argument('--application_name', '-a', help='Set the name for this Infra test Job', required=True)
        parser.add_argument('--ip_adders', '-i', help='IP of machine to be tested using serverspec or inspec')
        parser.add_argument('--spec_type', '-s', help='Set spec type serverspec/awspec/inspec', required=True)
        parser.add_argument('--user', '-u', help='User of machine to be tested using serverspec or inspec')
        parser.add_argument('--password', '-p', help='Password of machine to be tested using serverspec or inspec')
        parser.add_argument('--key', '-k', help='Key for machine to be tested using serverspec or inspec')

        parser.add_argument('--use_code_upload', '-cu',
                            help='Set upload code file as true to upload test file. Default=false', default="false")
        parser.add_argument('--code_file_name', '-cf', help='Set upload file name', default="test")
        parser.add_argument('--git_repository_url', '-gr', help='Set Git URL')
        parser.add_argument('--git_password', '-gp', help='Set git password')
        parser.add_argument('--git_user', '-gu', help='Set git username')
        parser.add_argument('--git_branch', '-gb', help='Set git branch name')
        parser.add_argument('--pre_script', '-pr', help='Set shell script to be executed before test suite runs.\
                            For e.g. mvn clean install to build your automation code.')
        parser.add_argument('--command_to_run_test', '-rc',
                            help='Set command to run Automation Test suite. For e.g. mvn test ', required=True)
        parser.add_argument('--post_script', '-po', help='Set shell script to be executed after test suite runs.')
        parser.add_argument('--report_file_name', '-rf',
                            help='Set test execution report file, preferably in json or xml format.', required=True)
        parser.add_argument('--output_directory_path', '-od',
                            help='Set test execution reports directory. For e.g. target/testng-report. Path should be \
                            relative to your automation code directory.', required=True)

        parser.add_argument('--credentials_type', '-t', help='Set credentials credential type. \
                            For e.g. basic_credentials, instance_profile, default value is \
                            basic_credentials', default='basic_credentials')
        parser.add_argument('--provider_json', '-f', help='Provide file aws provider json file path')
        parser.add_argument('--assume_role', '-ar', help='set assume role true/false, default value is false', default='false')

        return parser

    def take_action(self, parsed_args):
        """take_action."""
        self.log.debug(parsed_args)
        try:
            if parsed_args.use_code_upload == 'true':
                if parsed_args.code_file_name == "test":
                    raise RuntimeError("Please provide valid file path to upload code.")
            else:
                if parsed_args.git_repository_url is None:
                    raise RuntimeError("Please provide valid git credentials")
            body = test_sdk_client.InfraTestDto(
                app_name=parsed_args.application_name,
                re_run_from=""
            )
            body.infra_spec_type = parsed_args.spec_type
            if parsed_args.spec_type == "serverspec" or parsed_args.spec_type == "inspec":
                body.infra_test_ips = parsed_args.ip_adders
                body.infra_test_user = parsed_args.user
                body.infra_test_password = parsed_args.password
                if parsed_args.key is not None:
                    with Utility.open_file(parsed_args.key) as handle:
                        key = handle.read()
                    body.infra_test_key = key
            else:
                aws_provider = test_sdk_client.AwsProvider()

                with Utility.open_file(parsed_args.provider_json) as handle:
                    filedata = handle.read()

                provider_details_json = json.loads(filedata)
                aws_provider.access_key = provider_details_json['access_key']
                aws_provider.secret_key = provider_details_json['secret_key']
                aws_provider.region = provider_details_json['region']

                if parsed_args.credentials_type == 'instance_profile':
                    instance_profile = test_sdk_client.InstanceProfile
                    instance_profile.name = provider_details_json.iam_instance_profile['name']
                    instance_profile.arn = provider_details_json.iam_instance_profile['arn']
                    aws_provider.iam_instance_profile = instance_profile

                if parsed_args.assume_role == 'true':
                    assume_role = test_sdk_client.AssumeRole
                    assume_role.role_arn = provider_details_json.assume_role['role_arn']
                    assume_role.session_name = provider_details_json.assume_role['session_name']
                    assume_role.external_id = provider_details_json.assume_role['external_id']
                    aws_provider.assume_role = assume_role

                body.provider = aws_provider

            if parsed_args.use_code_upload == 'true':
                self.log.debug("Uploading code file ...")
                body.code_file_name = Utility.upload_code(parsed_args.code_file_name, parsed_args.application_name)
                self.log.debug("Code object Name : %s ", body.code_file_name)
            else:
                body.git_url = parsed_args.git_repository_url
                body.git_user = parsed_args.git_user
                body.git_pass = parsed_args.git_password
                body.branch_name = parsed_args.git_branch

            body.pre_script = parsed_args.pre_script
            body.command_to_run_test = parsed_args.command_to_run_test
            body.post_script = parsed_args.post_script
            body.report_file = parsed_args.report_file_name
            body.output_dir = parsed_args.output_directory_path
            body.re_run_from = ""

            self.log.debug(body)
            self.log.debug("Execution stared for Infra test")
            Utility.execute_test(body, parsed_args, self.log, test_sdk_client.InfraTestApi(Utility.set_headers()).run)

        except Exception as exception:
            self.log.error(exception)
            Utility.print_exception(exception)
