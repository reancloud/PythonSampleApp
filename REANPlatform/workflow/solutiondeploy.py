"""Save provider module."""
import os
import json
import logging
from cliff.command import Command
import workflow_sdk_client
from workflow_sdk_client.rest import ApiException
from reanplatform.set_header import set_header_parameter
from reanplatform.utility import Utility
from workflow.constants import WorkflowConstants
from workflow.utility import WorkflowUtility


class SolutionDeploy(Command):
    """Deploy Solution Package"""

    log = logging.getLogger(__name__)

    # EPILog will get print after commands
    _epilog = 'Example : rean-workflow solution-deploy --package_details /Users/reandeploy/package.json'

    def get_parser(self, prog_name):
        """get_parser."""
        parser = super(SolutionDeploy, self).get_parser(prog_name)
        parser.add_argument('--package_details', '-f',
                            help='Json file with applicable key-value pair \
                            for solution package deployment. File absolute path',
                            required=True
                           )
        parser.add_argument('--output', '-o',
                            help="Write output to <file> instead of stdout.",
                            required=False
                           )
        return parser

    def take_action(self, parsed_args):
        """take_action."""
        package_details = parsed_args.package_details
        SolutionDeploy.deploy_solution_packag(package_details, parsed_args)

    @staticmethod
    def deploy_solution_packag(package_details, parsed_args):
        """create_provider."""
        api_client = set_header_parameter(WorkflowUtility.create_api_client(), Utility.get_url(WorkflowConstants.WORKFLOW_URL))
        workflow_api_instance = workflow_sdk_client.DeploymentcontrollerApi(api_client)
        try:
            file_path = package_details

            if not os.path.isfile(file_path):
                raise RuntimeError('Provider details file %s does not exists' % file_path)

            # Parse parameters
            with open(file_path, "r") as handle:
                filedata = handle.read()

            jsondata = json.loads(filedata)
            api_response = workflow_api_instance.deploy_using_post(jsondata)
            Utility.print_output_as_str("Solution Package Deployment Succesfully: {}".format(api_response), parsed_args.output)
        except ApiException as api_exception:
            Utility.print_exception(api_exception)
