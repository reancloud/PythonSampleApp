"""List Rules."""
import logging
import json
import re
import time
import ast
from collections import OrderedDict
from prettytable import PrettyTable
from cliff.command import Command
from mnc.parameters_constants import MncConstats
import deploy_sdk_client
from deploy_sdk_client.rest import ApiException
from reanplatform.utility import Utility
from reanplatform.set_header import set_header_parameter
from deploy.constants import DeployConstants
from deploy.getdeploymentstatus import Status
from deploy.utility import DeployUtility
from deploy.get_deployment_input import GetDeploymentInput


class RuleList(Command):    # noqa: D203, D204
    """List manage cloud deployed rules. Example: rean-mnc rule-list --rule_name mnc_check_s3_exposed_buckets --customer_acc 120987654321."""
    # noqa: C0303
    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        """get_parser."""
        parser = super(RuleList, self).get_parser(prog_name)
        parser.add_argument('--' + MncConstats.RULE_NAME, MncConstats.RULE_NAME_INITIAL,
                            help='Managed cloud rule name',
                            required=False)
        parser.add_argument('--' + MncConstats.CUSTOMER_ACC, MncConstats.CUSTOMER_ACC_INITIAL,
                            help='Customer AWS account number',
                            required=False)
        return parser

    # pylint: disable=R0201
    def __validate_parameters(self, rule_name, customer_acc):
        """Validate cli parameters."""
        logging.info("Validating parameters")
        if rule_name is None and customer_acc is None:
            raise RuntimeError("Specify either " + '--' + MncConstats.RULE_NAME + " OR " + '--' + MncConstats.CUSTOMER_ACC + " OR " + '--' + MncConstats.RULE_NAME + " and " + '--' + MncConstats.CUSTOMER_ACC)

    def take_action(self, parsed_args):
        """List Environment."""
        argparse_dict = vars(parsed_args)

        rule_name = argparse_dict[MncConstats.RULE_NAME]
        customer_acc = argparse_dict[MncConstats.CUSTOMER_ACC]
        rule_name_key = None
        self.__validate_parameters(rule_name, customer_acc)
        try:
            api_client = set_header_parameter(DeployUtility.create_api_client(), Utility.get_url(DeployConstants.DEPLOY_URL))
            instance = deploy_sdk_client.EnvironmentApi(api_client)
            # Get all environments for user
            api_response = instance.get_all_environments()
            logging.info("Please wait!")
            display_data = OrderedDict()
            table = None
            table_only_acc = PrettyTable(['Customer Account Number', 'Rule Name', 'Status'])
            table_only_name = PrettyTable(['Rule Name', 'Customer Account Number', 'Status'])
            add_acc = True
            for one_env in api_response:
                input_json = None
                if rule_name and customer_acc:
                    if one_env.name.startswith(rule_name):
                        input_json = RuleList.get_input_json(one_env.config.env_id, customer_acc, instance, rule_name=None)
                        if input_json:
                            del input_json['status']
                            display_data['Customer-Account'] = customer_acc
                            display_data['Rule-name'] = rule_name
                            display_data['Rule-type'] = None
                            display_data['Input-Parameters'] = input_json
                elif customer_acc:
                    input_json = RuleList.get_input_json(one_env.config.env_id, customer_acc, instance, rule_name)
                    if input_json:
                        rule_name_add = one_env.name.replace('_config_rule_setup', '')
                        customer_acc = customer_acc if add_acc else ''
                        table_only_acc.add_row([customer_acc, rule_name_add, input_json['status']])
                        add_acc = False
                        table = table_only_acc
                elif rule_name:
                    if one_env.name.startswith(rule_name):
                        input_all_deployment = RuleList.get_input_json(one_env.config.env_id, customer_acc, instance, rule_name)
                        if input_all_deployment:
                            add_acc = True
                            for input_json in input_all_deployment:
                                if input_json['input_data'] and ''.join(input_json['acc_no']):
                                    rule_name = rule_name if add_acc else ''
                                    table_only_name.add_row([
                                        rule_name,
                                        ''.join(input_json['acc_no']),
                                        input_json['status']
                                    ])
                                    add_acc = False
                    table = table_only_name
            if table:
                logging.info(table)
            elif display_data:
                logging.info(json.dumps(display_data, default=lambda o: o.__dict__, sort_keys=False, indent=4).replace("\"_", '"'))
            else:
                logging.info("No rule deployment found.")
        except ApiException as exception:
            logging.info("Please try again.")
            Utility.print_exception(exception)

    @staticmethod
    def get_input_json(env_id, customer_acc, instance, rule_name):
        """get_input_json."""
        all_deployment = None
        input_data = None
        input_all_deployment = []
        all_deployment = instance.get_all_deployments_for_environment_by_id(env_id)
        time.sleep(2)
        if all_deployment:
            for single_deployment in all_deployment:
                if customer_acc and customer_acc in single_deployment.deployment_name or rule_name:
                    input_data = GetDeploymentInput.get_deployment_input_json(env_id=env_id, deployment_name=single_deployment.deployment_name)
                    input_data = ast.literal_eval(str(input_data))
                    status = Status.deployment_status(env_id, single_deployment.deployment_name)
                    time.sleep(2)
                    if rule_name and 'client' in single_deployment.deployment_name:
                        data = {}
                        data = {
                            'deployment_name': single_deployment.deployment_name,
                            'input_data': input_data,
                            'acc_no': re.findall(r'-?\d+\.?\d*', single_deployment.deployment_name),
                            'status': status
                        }
                        input_all_deployment.append(data)
                    else:   # for acc num
                        if input_data and 'client' in single_deployment.deployment_name:
                            input_all_deployment = input_data
                            input_data['status'] = status
        return input_all_deployment
