"""List Workflow Solution module deployments."""
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


class ListSolutionDeployment(Command):
    """Deploy Solution Package"""

    log = logging.getLogger(__name__)

    # EPILog will get print after commands
    _epilog = 'Example : rean-workflow list-solution-deployments'

    def get_parser(self, prog_name):
        """get_parser."""
        parser = super(ListSolutionDeployment, self).get_parser(prog_name)
        parser.add_argument('--format', '-f',
                            help='Allowed values are: [json, table]',
                            type=str, default='json',
                            nargs='?',
                            required=False)
        parser.add_argument('--output', '-o', help="Write output to <file> instead of stdout.", required=False)
        return parser

    def take_action(self, parsed_args):
        """take_action."""
        output_format = parsed_args.format
        ListSolutionDeployment.get_all_solution_package(parsed_args)

    @staticmethod
    def get_all_solution_package(parsed_args):
        """get all solution package."""
        api_client = set_header_parameter(WorkflowUtility.create_api_client(), Utility.get_url(WorkflowConstants.WORKFLOW_URL))
        workflow_api_instance = workflow_sdk_client.DeploymentcontrollerApi(api_client)
        try:
            api_response = workflow_api_instance.get_all_deployment_using_get()
            Utility.print_output_as_dict(api_response, parsed_args.output)
            Utility.print_output_as_str("Solution Package Deployment :{}".format(api_response), parsed_args.output)
        except ApiException as api_exception:
            Utility.print_exception(api_exception)
