"""Run UPA Test."""
import logging
import json
from cliff.command import Command
import hcaptest_sdk_client
from reantest.utility import Utility


class RunInfraTest(Command):
    """Run InfraTest."""

    log = logging.getLogger(__name__)
    _description = 'Run Infra test'
    _epilog = 'rean-test run-hcap-infra-test --name <name> --ip_address <ip> --spec_type Serverspec --user cliUser ' \
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
                            choices=['Serverspec', 'Awspec', 'Inspec', 'Azurespec'], required=True)
        parser.add_argument('--user', '-u', help='User of machine to be tested using serverspec or inspec')
        parser.add_argument('--password', '-p', help='Password of machine to be tested using serverspec or inspec')
        parser.add_argument('--key', '-k', help='Path to Key for machine to be tested using serverspec or inspec')

        # Codebase Parameters
        parser.add_argument('--upload_code_file_path', '-cf', help='Set upload file path', default="test")

        parser.add_argument('--git_repository_url', '-gr', help='Set git clone url for Automation code.')
        parser.add_argument('--git_username', '-gu', help='Set git username for Automation code.', default="")
        parser.add_argument('--git_password', '-gp', help='Set git password for Automation code.', default="")
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
        parser.add_argument('--provider_json', '-f', help='Provide file aws provider json file path')
        parser.add_argument('--assume_role', '-ar', help='set assume role true/false, default value is false',
                            default='false')
        parser.add_argument('--export_jobid_path', '-ej', help='Export job id to file absolute path.')
        parser.add_argument('--wait', '-w', action='store_true', help='Wait until job finish',
                            default=False)
        return parser

    @staticmethod
    def set_body(spec_dto, parsed_args):
        spec_dto = hcaptest_sdk_client.ServerSpecParamsDto()
        spec_dto.infra_test_ips = parsed_args.ip_address
        spec_dto.infra_test_user = parsed_args.user
        spec_dto.infra_test_password = parsed_args.password
        if parsed_args.key is not None:
            with Utility.open_file(parsed_args.key) as handle:
                key = handle.read()
                spec_dto.infra_test_key = key
        return spec_dto

    def take_action(self, parsed_args):
        """take_action."""
        self.log.debug(parsed_args)
        try:

            RunInfraTest.validate_parameter(parsed_args)
            infra_test_dto = hcaptest_sdk_client.InfraTestDto()
            job_param_dto = hcaptest_sdk_client.JobParamsDto()

            infra_test_dto.job_name = parsed_args.name
            infra_test_dto.infra_spec_type = parsed_args.spec_type

            if parsed_args.spec_type == "Serverspec":
                dto = hcaptest_sdk_client.ServerSpecParamsDto()
            elif parsed_args.spec_type == "Inspec":
                dto = hcaptest_sdk_client.InspecParamsDto()
            elif parsed_args.spec_type == "Awspec":
                dto = hcaptest_sdk_client.AwsInfraTestDto()
            elif parsed_args.spec_type == "Azurepec":
                dto = hcaptest_sdk_client.AzureInfraTestDto()

            if parsed_args.spec_type == "Serverspec" or parsed_args.spec_type == "Inspec":
                if parsed_args.spec_type == "Serverspec":
                    RunInfraTest.set_body(dto, parsed_args)
                elif parsed_args.spec_type == "Inspec":
                    RunInfraTest.set_body(dto, parsed_args)
            else:
                if parsed_args.spec_type == "Awspec":
                    self.log.debug("Creating aws provider json")

                    with Utility.open_file(parsed_args.provider_json) as handle:
                        filedata = handle.read()

                    provider_details_json = json.loads(filedata)
                    dto.region = provider_details_json['region']
                    if parsed_args.credentials_type == 'basic_credentials':
                        dto.access_key = provider_details_json['access_key']
                        dto.secret_key = provider_details_json['secret_key']
                        if "aws_session_token" in provider_details_json:
                            dto.aws_session_token = provider_details_json['aws_session_token']

                    # Removed instance profile.

                    if parsed_args.assume_role == 'true':
                        dto.assume_role_arn = provider_details_json['assume_role']['role_arn']
                        dto.session_name = provider_details_json['assume_role']['session_name']
                        dto.external_id = provider_details_json['assume_role']['external_id']

                else:
                    self.log.debug("Creating azure provider json")

                    with Utility.open_file(parsed_args.provider_json) as handle:
                        filedata = handle.read()

                    provider_details_json = json.loads(filedata)

                    dto.subscription_id = provider_details_json['subscription_id']
                    dto.client_id = provider_details_json['client_id']
                    dto.client_secret = provider_details_json['client_secret']
                    dto.tenant_id = provider_details_json['tenant_id']

                # Uploaded code as previous upload code API which used UploadServlet
                if parsed_args.upload_input_file_path != "":
                    dto.actual_input_file_name = parsed_args.upload_input_file_path
                    self.log.debug("Uploading input file ...")
                    dto.input_file_name = Utility.upload_code(parsed_args.upload_input_file_path,
                                                                                   parsed_args.name, True)
                    self.log.debug("input file object Name : %s ", parsed_args.upload_code_file_path)

            if parsed_args.upload_code_file_path != 'test':
                job_param_dto.use_upload_code = True
                job_param_dto.actualupload_code_file_name = parsed_args.upload_code_file_path
                self.log.debug("Uploading code file ...")
                job_param_dto.upload_code_file_name = Utility.upload_code(parsed_args.upload_code_file_path,
                                                                               parsed_args.name)
                self.log.debug("Code object Name : %s ", parsed_args.upload_code_file_path)
            else:
                job_param_dto.use_upload_code = False

                job_param_dto.git_url = parsed_args.git_repository_url
                job_param_dto.git_encrypted_pwd = parsed_args.git_password
                job_param_dto.git_user = parsed_args.git_username
                job_param_dto.branch_name = parsed_args.git_branch

            job_param_dto.run_command = parsed_args.command_to_run_test
            job_param_dto.pre_script = parsed_args.pre_script
            job_param_dto.post_script = parsed_args.post_script
            job_param_dto.report_file = parsed_args.report_file_name
            job_param_dto.output_dir = parsed_args.output_directory_path
            job_param_dto.re_run_from = ""

            infra_test_dto.job_params = job_param_dto

            self.log.debug(infra_test_dto)
            self.log.debug("Execution stared for Infra test")
            response_infra_test_dto_new = hcaptest_sdk_client.InfraTestControllerApi(Utility.set_headers())\
                .run_infra_test(job_param_dto)

            job_id = ""
            if response_infra_test_dto_new.id:
                job_id = response_infra_test_dto_new.id

            Utility.export_jobid(parsed_args.name, job_id, parsed_args.export_jobid_path)

            self.log.debug("Response is------------: %s ", job_id)
            print("Infra test job submitted successfully. Job Id is : ", job_id)

            # For wait need to refactor Utility.
            #if parsed_args.wait:
            #    Utility.wait_while_job_running(hcaptest_sdk_client.InfraTestControllerApi().get_job_status();
        except Exception as exception:
            # self.log.error(exception)
            Utility.print_exception(exception)

        @staticmethod
        def validate_parameter(parsed_args):
            """Validate parameters."""
            error_message = ""

            if parsed_args.spec_type != 'Awspec' and parsed_args.spec_type != 'Azurespec':
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
