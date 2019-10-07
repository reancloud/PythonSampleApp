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
        parser.add_argument('--input', '-i', help='Input json file', required=True)
        parser.add_argument('--output', '-o', help='Output json file', required=True)
        return parser

    def take_action(self, parsed_args):
        """take_action."""
        try:

            self.log.debug(parsed_args)
            body = test_sdk_client.AzurespecParam()
            body.name = parsed_args.name
            azure_provider = test_sdk_client.AzureProvider()
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

            body.azure_provider = azure_provider

            with Utility.open_file(parsed_args.input) as handle:
                input_data = handle.read()

            body.input = json.loads(input_data)

            with Utility.open_file(parsed_args.output) as handle:
                output_data = handle.read()

            body.output = json.loads(output_data)

            self.log.debug(body)
            self.log.debug("Execution stared for RunInfraTestAzureSpec")

            job_id = test_sdk_client.RunTestNewApi(Utility.set_headers()).execute_infra_azurespec(body)
            self.log.debug("Response is------------: %s ", job_id)
            print("The request Infra azurespec test submitted successfully. Job Id is : ", job_id)

        except Exception as exception:
            Utility.print_exception(exception)
