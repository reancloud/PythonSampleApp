"""Run Infratest AWSSpec."""
import logging
import json
from cliff.command import Command
import test_sdk_client
from reantest.utility import Utility
import time


class RunInfraTestGcpSpec(Command):
    """Run Infratest AWSSpec."""

    log = logging.getLogger(__name__)
    _description = 'Run Infra AWSSpec test'
    _epilog = 'Example : \n\t rean-test run-infra-gcppec --name <name> -i <Absolute path to input.json> ' \
              '-o <Absolute path to output.json> -pf <Absolute path to provider.json>'

    def get_parser(self, prog_name):
        """get_parser."""
        parser = super(RunInfraTestGcpSpec, self).get_parser(prog_name)

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

            RunInfraTestGcpSpec.validate(parsed_args)

            test_sdk_client.InfraTestDto()

            gcpspec_dto = test_sdk_client.GcpInfraTestDto()
            gcpspec_dto.job_name = parsed_args.name + "-" + str(int(time.time()))  # added epoch time

            with Utility.open_file(parsed_args.provider_file_path) as handle:
                filedata = handle.read()

            provider_json = json.loads(filedata)
            self.log.debug('Reading provider file')

            gcpspec_dto.project = provider_json['project']
            gcpspec_dto.credentials = provider_json['credentials']

            if parsed_args.upload_input_file is not None:
                self.log.debug("Uploading input file ...")
                gcpspec_dto.actual_input_file_name = parsed_args.upload_input_file
                gcpspec_dto.input_file_name = Utility.upload_code(
                    parsed_args.upload_input_file, parsed_args.name, False)
                self.log.debug("Input code object Name : %s ", gcpspec_dto.input_file_name)
            else:
                with Utility.open_file(parsed_args.input) as handle:
                    input_data = handle.read()

                gcpspec_dto.input = json.loads(input_data)

                with Utility.open_file(parsed_args.output) as handle:
                    output_data = handle.read()

                gcpspec_dto.output = json.loads(output_data)

            self.log.debug(gcpspec_dto)
            self.log.debug("Execution stared for RunInfraTestGcpSpec")

            gcpspec_dto.infra_spec_type = 'gcpspec'

            job_id = test_sdk_client.InfratestcontrollerApi(
                Utility.set_headers()).run_default_infra_test_using_post(gcpspec_dto).id
            self.log.debug("Response is------------: %s ", job_id)
            Utility.export_jobid(parsed_args.name, job_id, parsed_args.export_jobid_path)
            print("The request Infra gcpspec test submitted successfully. Job Id is : ", job_id)

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
