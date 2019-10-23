"""Run UPA Test."""
import logging
import json
from cliff.command import Command
import test_sdk_client
from reantest.utility import Utility


class RunInfraTest(Command):
    """Run InfraTest."""

    log = logging.getLogger(__name__)
    _description = 'Run Infra test'
    _epilog = 'rean-test run-infra-test --name <name> --ip_address <ip> --spec_type Serverspec --user cliUser ' \
              '--password <password> --git_repository_url <git_url> --git_username <git_username> ' \
              '--git_branch <git_branch> --command_to_run_test <command to run> ' \
              '--output_directory_path <output_dir> --report_file_name <report file name>'

    def get_parser(self, prog_name):
        """get_parser."""
        parser = super(RunInfraTest, self).get_parser(prog_name)

        # Basic Parameters
        parser.add_argument('--name', '-n', help='Set the name for this Infra test Job', required=True)
        parser.add_argument('--ip_address', '-i', help='IP of machine to be tested using serverspec or inspec')
        parser.add_argument('--spec_type', '-s', help='Set spec type',
                            choices=['Serverspec', 'Awspec', 'Inspec'], required=True)
        parser.add_argument('--user', '-u', help='User of machine to be tested using serverspec or inspec')
        parser.add_argument('--password', '-p', help='Password of machine to be tested using serverspec or inspec')
        parser.add_argument('--key', '-k', help='Path to Key for machine to be tested using serverspec or inspec')

        # Codebase Parameters
        parser.add_argument('--upload_code_file_path', '-cf', help='Set upload file path', default="test")

        parser.add_argument('--git_repository_url', '-gr', help='Set git clone url for Automation code.')
        parser.add_argument('--git_username', '-gu', help='Set git username for Automation code.')
        parser.add_argument('--git_password', '-gp', help='Set git password for Automation code.')
        parser.add_argument('--git_branch', '-gb',
                            help='Set git repository branch name. '
                                 'If not specified, master branch will be considered by default.', default='master')

        # Execution Parameters
        parser.add_argument('--command_to_run_test', '-rc',
                            help='Set command to run Automation Test suite. For e.g. mvn test This option is mandatory.',
                            required=True)
        parser.add_argument('--pre_script', '-pr',
                            help='Set shell script to be executed before test suite runs. '
                                 'Example mvn clean install to build your automation code.')
        parser.add_argument('--post_script', '-po', help='Set shell script to be executed after test suite runs.')
        parser.add_argument('--report_file_name', '-rf',
                            help='Set test execution report file, preferably in json or xml format.', required=True)
        parser.add_argument('--output_directory_path', '-od',
                            help='Set test execution reports directory. '
                                 'Example target/testing-report. Path should be relative to your '
                                 'automation code directory', required=True)
        parser.add_argument('--upload_input_file_path', '-if', help='Set input file path', default="")

        parser.add_argument('--credentials_type', '-t', help='Set credentials credential type',
                            choices=['basic_credentials', 'instance_profile'], default='basic_credentials')
        parser.add_argument('--provider_json', '-f', help='Provide file aws provider json file path')
        parser.add_argument('--assume_role', '-ar', help='set assume role true/false, default value is false',
                            default='false')

        return parser

    def take_action(self, parsed_args):
        """take_action."""
        self.log.debug(parsed_args)
        try:
            RunInfraTest.validate_parameter(parsed_args)

            infra_test_dto_new = test_sdk_client.InfraTestDtoNew()

            infra_test_dto_new.name = parsed_args.name

            infra_test_dto_new.re_run_from = ""
            infra_test_dto_new.spec_type = parsed_args.spec_type

            if parsed_args.spec_type == "Serverspec" or parsed_args.spec_type == "Inspec":

                machine_credentials = test_sdk_client.MachineCredentials()

                machine_credentials.ip = parsed_args.ip_address
                machine_credentials.user = parsed_args.user
                machine_credentials.password = parsed_args.password
                if parsed_args.key is not None:
                    with Utility.open_file(parsed_args.key) as handle:
                        key = handle.read()
                    machine_credentials.key = key
                infra_test_dto_new.machine_creds = machine_credentials
            else:
                aws_provider = test_sdk_client.AwsProvider()

                with Utility.open_file(parsed_args.provider_json) as handle:
                    filedata = handle.read()

                provider_details_json = json.loads(filedata)
                aws_provider.region = provider_details_json['region']
                if parsed_args.credentials_type == 'basic_credentials':
                    aws_provider.access_key = provider_details_json['access_key']
                    aws_provider.secret_key = provider_details_json['secret_key']

                if parsed_args.credentials_type == 'instance_profile':
                    instance_profile = test_sdk_client.InstanceProfile
                    instance_profile.name = provider_details_json['iam_instance_profile']['name']
                    instance_profile.arn = provider_details_json['iam_instance_profile']['arn']
                    aws_provider.iam_instance_profile = instance_profile
                if parsed_args.assume_role == 'true':
                    assume_role = test_sdk_client.AssumeRole
                    assume_role.role_arn = provider_details_json['assume_role']['role_arn']
                    assume_role.session_name = provider_details_json['assume_role']['session_name']
                    assume_role.external_id = provider_details_json['assume_role']['external_id']
                    aws_provider.assume_role = assume_role

                infra_test_dto_new.provider = aws_provider

                if parsed_args.upload_input_file_path != "":
                    infra_test_dto_new.awspec_actual_input_file = parsed_args.upload_input_file_path
                    self.log.debug("Uploading input file ...")
                    infra_test_dto_new.infra_param_file_name = Utility.upload_code(parsed_args.upload_input_file_path,
                                                                                   parsed_args.name)
                    self.log.debug("input file object Name : %s ", parsed_args.upload_code_file_path)

            if parsed_args.upload_code_file_path != 'test':
                infra_test_dto_new.codebase_type = 'UPLOAD_CODE'
                self.log.debug("Uploading code file ...")
                infra_test_dto_new.upload_code_file_name = Utility.upload_code(parsed_args.upload_code_file_path,
                                                                               parsed_args.name)
                self.log.debug("Code object Name : %s ", parsed_args.upload_code_file_name)
            else:
                infra_test_dto_new.codebase_type = 'GIT'

                git_config_dto = test_sdk_client.GitConfigDto()
                git_config_dto.url = parsed_args.git_repository_url
                git_config_dto.passsword = parsed_args.git_password
                git_config_dto.user = parsed_args.git_username
                git_config_dto.branch = parsed_args.git_branch
                infra_test_dto_new.git_config = git_config_dto

            execution_details_dto = test_sdk_client.ExecutionDetailsDto()
            execution_details_dto.run_command = parsed_args.command_to_run_test
            execution_details_dto.pre_script = parsed_args.pre_script
            execution_details_dto.post_script = parsed_args.post_script
            execution_details_dto.report_file = parsed_args.report_file_name
            execution_details_dto.output_dir = parsed_args.output_directory_path
            infra_test_dto_new.execution_details = execution_details_dto
            infra_test_dto_new.re_run_from = ""

            self.log.debug(infra_test_dto_new)
            self.log.debug("Execution stared for Infra test")
            response_infra_test_dto_new = test_sdk_client.RunTestNewApi(Utility.set_headers()).run_infra_test(
                infra_test_dto_new)

            job_id = ""
            if response_infra_test_dto_new.id:
                job_id = response_infra_test_dto_new.id

            self.log.debug("Response is------------: %s ", job_id)
            print("Infra test job submitted successfully. Job Id is : ", job_id)

        except Exception as exception:
            # self.log.error(exception)
            Utility.print_exception(exception)

    @staticmethod
    def validate_parameter(parsed_args):
        """Validate parameters."""
        error_message = ""

        if parsed_args.spec_type != 'Awspec':
            if parsed_args.password is None and parsed_args.key is None:
                error_message = "Password or key required"

        if parsed_args.upload_code_file_path == 'test':  # Upload Code = false
            if parsed_args.git_repository_url is None:
                error_message = "Please provide valid git credentials"
        else:
            if parsed_args.git_repository_url is not None:
                error_message = "Upload file name and Git repository url parameters can not be used together"

        if error_message:
            raise RuntimeError(error_message)
