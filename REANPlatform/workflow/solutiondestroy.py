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
from workflow.workflow_utility import WorkflowUtility


class SolutionDestroy(Command):
    """Destroy Solution Package By Id"""

    log = logging.getLogger(__name__)

    # EPILog will get print after commands
    _epilog = 'Example : rean-workflow solution-destroy --id AXX0hYc_VcpUxUfs1-CA'

    def get_parser(self, prog_name):
        """get_parser."""
        parser = super(SolutionDestroy, self).get_parser(prog_name)
        parser.add_argument('--id', help='Solution Package Deployment id',
                            required=True
                           )
        parser.add_argument('--output', '-o',
                            help="Write output to <file> instead of stdout.",
                            required=False
                           )
        return parser

    def take_action(self, parsed_args):
        """take_action."""
        solution_package_id = parsed_args.id
        SolutionDestroy.validate_parameters(solution_package_id)
        SolutionDestroy.destroy_solution_package(solution_package_id, parsed_args)

    @staticmethod
    def validate_parameters(solution_package_id):
        """Validate cli parameters."""
        if solution_package_id is None:
            raise RuntimeError("Please provide HCAP Workflow Solution Deployment Id")

    @staticmethod
    def destroy_solution_package(solution_package_id, parsed_args):
        """destroy solution package using id."""
        api_client = set_header_parameter(WorkflowUtility.create_api_client(), Utility.get_url(WorkflowConstants.WORKFLOW_URL))
        workflow_api_instance = workflow_sdk_client.DeploymentcontrollerApi(api_client)
        try:
            api_response = workflow_api_instance.destroy_using_delete(solution_package_id)
            Utility.print_output_as_str("Solution Package Destroy Succesfully: {}".format(api_response), parsed_args.output)
        except ApiException as api_exception:
            Utility.print_exception(api_exception)
