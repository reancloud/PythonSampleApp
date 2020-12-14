"""Run Infratest AzureSpec."""
import logging
import json
from cliff.command import Command
from reantest.utility import Utility
import test_sdk_client


class RunInfraAzureSpec(Command):
    """Run Infratest AzureSpec."""

    log = logging.getLogger(__name__)
    _description = 'Run Infra AzureSpec test'
    _epilog = 'Example : \n\t rean-test run-infra-azurespec --name <name> -i <Absolute path to input.json> ' \
              '-o <Absolute path to output.json> -pf <Absolute path to provider.json>'

    def get_parser(self, prog_name):
        """get_parser."""
        parser = super(RunInfraAzureSpec, self).get_parser(prog_name)

        parser.add_argument('--name', '-n', help='Set the name for this Infra test Job', required=True)
        parser.add_argument('--provider_file_path', '-pf', help='Provide file azure provider json file path',
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
            azure_param_old = test_sdk_client.AzurespecParamOld()
            azure_param_old.name = parsed_args.name
            azure_provider = test_sdk_client.AzureProviderOld()
            RunInfraAzureSpec.validate(parsed_args)
            with Utility.open_file(parsed_args.provider_file_path) as handle:
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

            azure_param_old.azure_provider = azure_provider

            if parsed_args.upload_input_file is not None:
                self.log.debug("Uploading input file ...")
                azure_param_old.actual_input_file_name = parsed_args.upload_input_file
                azure_param_old.input_file_name = Utility.upload_code(
                    parsed_args.upload_input_file, parsed_args.name, False)
                self.log.debug("Input code object Name : %s ", azure_param_old.input_file_name)
            else:

                with Utility.open_file(parsed_args.input) as handle:
                    input_data = handle.read()

                azure_param_old.input = json.loads(input_data)

                with Utility.open_file(parsed_args.output) as handle:
                    output_data = handle.read()

                azure_param_old.output = json.loads(output_data)

            self.log.debug(azure_param_old)
            self.log.debug("Execution stared for RunInfraTestAzureSpec")

            job_id = test_sdk_client.TestbackwardscompatibilitycontrollerApi(
                Utility.set_headers()).run_default_azurespec_using_post(azure_param_old)
            self.log.debug("Response is------------: %s ", job_id)
            Utility.export_jobid(parsed_args.name, job_id, parsed_args.export_jobid_path)
            print("The request Infra azurespec test submitted successfully. Job Id is : ", job_id)

            if parsed_args.wait:
                Utility.wait_while_job_running(job_id)

        except Exception as exception:
            Utility.print_exception(exception)

    @staticmethod
    def validate(parsed_args):
        """Validate arguments"""
        if parsed_args.upload_input_file is None and parsed_args.input is None and parsed_args.output is None:
            raise RuntimeError("Provide input, output or upload input file path.")

        if parsed_args.upload_input_file is None:
            if parsed_args.input is None or parsed_args.output is None:
                raise RuntimeError("Provide input and output.")
