"""List Rules."""
import logging
import json
import re
from collections import OrderedDict
from cliff.command import Command
from mnc.parameters_constants import MncConstats
import deploy_sdk_client
from deploy_sdk_client.rest import ApiException
from reanplatform.utility import Utility
from reanplatform.set_header import set_header_parameter
from deploy.constants import DeployConstants


class RuleList(Command):        # noqa: D203.
    """List Manage Cloud Rules."""

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        """get_parser."""
        parser = super(RuleList, self).get_parser(prog_name)
        parser.add_argument('--' + MncConstats.RULE_NAME, MncConstats.RULE_NAME_INITIAL,
                            help='Rule name',
                            required=False)
        parser.add_argument('--' + MncConstats.RULE_TYPE, MncConstats.RULE_TYPE_INITIAL,
                            help='Rule type',
                            required=False)
        parser.add_argument('--' + MncConstats.CUSTOMER_ACC, MncConstats.CUSTOMER_ACC_INITIAL,
                            help='Customer account number',
                            required=False)
        return parser

    # pylint: disable=R0201
    def __validate_parameters(self, rule_name, rule_type, customer_acc):
        """Validate cli parameters."""
        if rule_name is None and rule_type is None and customer_acc is None:
            raise RuntimeError("Specify either " + '--' + MncConstats.RULE_NAME + " OR " + '--' + MncConstats.CUSTOMER_ACC + " OR " + '--' + MncConstats.RULE_NAME + " and " + '--' + MncConstats.CUSTOMER_ACC)

    def take_action(self, parsed_args):
        """List Environment."""
        argparse_dict = vars(parsed_args)

        rule_name = argparse_dict[MncConstats.RULE_NAME]
        rule_type = argparse_dict[MncConstats.RULE_TYPE]
        customer_acc = argparse_dict[MncConstats.CUSTOMER_ACC]
        rule_name_key = None
        self.__validate_parameters(rule_name, rule_type, customer_acc)
        try:
            instance = deploy_sdk_client.EnvironmentApi()
            api_instance = set_header_parameter(instance, Utility.get_url(DeployConstants.DEPLOY_URL))
            all_env = api_instance.get_all_environments()

            display_data = OrderedDict()
            for one_env in all_env:
                input_json = None
                if rule_name and customer_acc:
                    if one_env.name.startswith(rule_name):
                        input_json = RuleList.get_input_json(one_env.config.env_id, customer_acc, api_instance, rule_name=None)
                        if input_json:
                            display_data['Customer-Account'] = customer_acc
                            display_data['Rule-name'] = rule_name
                            display_data['Rule-type'] = None
                            display_data['Input-Parameters'] = input_json
                elif customer_acc:
                    input_json = RuleList.get_input_json(one_env.config.env_id, customer_acc, api_instance, rule_name)
                    rule_name = ''
                    if input_json:
                        display_data['Customer-Account'] = customer_acc
                        display_data['Rule-type'] = rule_type
                        rule_name_key = one_env.name.replace('_config_rule_setup', '')
                        display_data[rule_name_key] = {
                            "Input-Parameters": input_json}
                elif rule_name:
                    if one_env.name.startswith(rule_name):
                        input_all_deployment = RuleList.get_input_json(one_env.config.env_id, customer_acc, api_instance, rule_name)

                        if input_all_deployment:
                            display_data['Rule-Name'] = rule_name
                            display_data['Rule-type'] = rule_type
                            for input_json in input_all_deployment:
                                if input_json['input_data'] and ''.join(input_json['acc_no']):
                                    display_data[''.join(input_json['acc_no'])] = {
                                        "Input-Parameters": input_json['input_data']}
            if display_data:
                logging.info(json.dumps(display_data, indent=4))
            else:
                logging.info("Rule deployment not found")
        except ApiException as exception:
            Utility.print_exception(exception)

    @staticmethod
    def get_input_json(env_id, customer_acc, api_instance, rule_name):
        """get_input_json."""
        all_deployment = None
        input_data = None
        input_all_deployment = []
        all_deployment = api_instance.get_all_deployments_for_environment_by_id(env_id)

        if all_deployment:
            for single_deployment in all_deployment:
                if customer_acc and customer_acc in single_deployment.deployment_name or rule_name:
                    input_data = api_instance.get_deployment_input_json(env_id=env_id, deployment_name=single_deployment.deployment_name)
                    if rule_name and 'client' in single_deployment.deployment_name:
                        data = {}
                        data = {
                            'deployment_name': single_deployment.deployment_name,
                            'input_data': input_data,
                            'acc_no': re.findall(r'-?\d+\.?\d*', single_deployment.deployment_name)
                        }
                        input_all_deployment.append(data)
                    else:   # for acc num
                        if input_data and 'client' in single_deployment.deployment_name:
                            input_all_deployment = input_data
        return input_all_deployment
