"""List Rules."""
import logging
from pprint import pprint
from cliff.command import Command
import deploy_sdk_client
import json
from deploy_sdk_client.rest import ApiException
from reanplatform.set_header import set_header_parameter
from prettytable import PrettyTable
from reanplatform.utility import Utility
import re
from collections import OrderedDict


class RuleList(Command):
    """List Manage Cloud Rules."""

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        """get_parser."""
        parser = super(RuleList, self).get_parser(prog_name)
        parser.add_argument('--rule_name', '-rule_name',
                            help='Rule name',
                            required=False)
        parser.add_argument('--rule_type', '-rule_type',
                            help='Rule type',
                            required=False)
        parser.add_argument('--customer_acc', '-customer_acc',
                            help='Customer account number',
                            required=False)
        return parser

    def validate_parameters(self, rule_name, rule_type, customer_acc):
        """Validate cli parameters."""
        if rule_name is None and rule_type is None and customer_acc is None:
            raise RuntimeError("Specify either --rule_name OR --customer_acc OR --rule_name and --customer_acc")    # noqa: E501

    def take_action(self, parsed_args):
        """List Environment."""
        rule_name = parsed_args.rule_name
        rule_type = parsed_args.rule_type
        customer_acc = parsed_args.customer_acc
        rule_name_key = None
        self.validate_parameters(rule_name, rule_type, customer_acc)
        try:
            instance = deploy_sdk_client.EnvironmentApi()
            api_instance = set_header_parameter(instance)
            all_env = api_instance.get_all_environments()

            display_data = OrderedDict()
            #   input_json = ''

            for one_env in all_env:
                    prepare_data = {}
                    deployment_id = None
                    input_json = None
                    if rule_name and customer_acc:
                        if (one_env.name.startswith(rule_name)):       # noqa: E501
                            input_json = self.get_input_json(one_env.config.env_id, customer_acc, api_instance, rule_name=None)     # noqa: E501
                            if input_json:
                                display_data = {
                                        'Customer-Account': customer_acc,
                                        'Rule-name': rule_name,
                                        'Rule-type': None,
                                        'Input-Parameters': input_json
                                     }
                    elif customer_acc:
                        input_json = self.get_input_json(one_env.config.env_id, customer_acc, api_instance, rule_name)     # noqa: E501
                        rule_name = ''
                        if input_json:
                            display_data['Customer-Account'] = customer_acc
                            display_data['Rule-type'] = rule_type
                            rule_name_key = one_env.name.replace('_config_rule_setup', '')      # noqa: E501
                            display_data[rule_name_key] = {
                                                "Input-Parameters": input_json
                                        }
                    elif rule_name:
                        if (one_env.name.startswith(rule_name)):
                            input_all_deployment = self.get_input_json(one_env.config.env_id, customer_acc, api_instance, rule_name)     # noqa: E501

                            if input_all_deployment:
                                display_data['Rule-Name'] = rule_name
                                display_data['Rule-type'] = rule_type
                                for input_json in input_all_deployment:
                                    if input_json['input_data'] and ''.join(input_json['acc_no']):        # noqa: E501
                                        display_data[''.join(input_json['acc_no'])] = {                 # noqa: E501
                                                          "Input-Parameters": input_json['input_data']      # noqa: E501
                                                        }
            if display_data:
                print(json.dumps(display_data, indent=4))
            else:
                print("Rule deployment not found")
        except ApiException as e:
            Utility.print_exception(e)

    def get_input_json(self, env_id, customer_acc, api_instance, rule_name):
        """get_input_json."""
        all_deployment = None
        input_data = None
        input_all_deployment = []
        all_deployment = api_instance.get_all_deployments_for_environment_by_id_0(env_id)     # noqa: E501

        if all_deployment:
            for single_deployment in all_deployment:
                if customer_acc and customer_acc in single_deployment.deployment_name or rule_name:   # noqa: E501
                    input_data = api_instance.get_deployment_input_json(env_id=env_id, deployment_name=single_deployment.deployment_name)      # noqa: E501         # noqa: E501
                    if rule_name and 'client' in single_deployment.deployment_name:     # noqa: E501
                        data = {}
                        data = {
                            'deployment_name': single_deployment.deployment_name,       # noqa: E501
                            'input_data': input_data,
                            'acc_no':  re.findall(r'-?\d+\.?\d*', single_deployment.deployment_name)         # noqa: E501
                        }
                        input_all_deployment.append(data)
                    else:   # for acc num
                        if input_data and 'client' in single_deployment.deployment_name:         # noqa: E501
                            input_all_deployment = input_data
        return input_all_deployment
