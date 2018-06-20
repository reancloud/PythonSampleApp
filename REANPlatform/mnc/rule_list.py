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
        if rule_name is None and  rule_type is None and customer_acc is None  :
            raise RuntimeError("Specify either --rule_name OR --customer_acc OR --rule_name and --customer_acc")    

    def take_action(self, parsed_args):
        """List Environment."""
        rule_name = parsed_args.rule_name
        rule_type = parsed_args.rule_type
        customer_acc = parsed_args.customer_acc
        self.validate_parameters(rule_name, rule_type, customer_acc)
        try:
            instance = deploy_sdk_client.EnvironmentApi()
            api_instance = set_header_parameter(instance)
            api_response = api_instance.get_all_environments()
            all_env = api_instance.get_all_environments()
            display_data = []
            input_json = ''

            for one_env in all_env:
                    prepare_data = {}
                    deployment_id = None
                    input_json = None
                    if rule_name and customer_acc:
                        if (one_env.name.startswith(rule_name)):       # noqa: E501
                            input_json = self.get_input_json(one_env.config.env_id, customer_acc, api_instance, rule_name=None)     # noqa: E501
                            if input_json:
                                prepare_data = {
                                        'Customer-Acc': customer_acc,
                                        'Blueprint Input Parameters': input_json,
                                        'Rule-type': None,
                                        'Rule-name': rule_name
                                    }

                    elif customer_acc:
                        input_json = self.get_input_json(one_env.config.env_id, customer_acc, api_instance, rule_name)     # noqa: E501
                        if input_json:
                            prepare_data = {
                                    'Blueprint Input Parameters': input_json,
                                    'Rule-type': None,
                                    'Rule-name': one_env.name
                            }
                    elif rule_name:
                        if (one_env.name.startswith(rule_name)):
                            input_json = self.get_input_json(one_env.config.env_id, customer_acc, api_instance, rule_name)     # noqa: E501
                            if input_json:
                                prepare_data = {
                                        'Blueprint Input Parameters': input_json['input_data'],
                                        'Rule-type': None,
                                        'Customer-Account': input_json['acc_no'],
                                        'Rule-name': one_env.name
                                    }

                    if prepare_data:
                        display_data.append(prepare_data)
            print(
                    json.dumps(
                            display_data,
                            default=lambda o: o.__dict__,
                            sort_keys=True, indent=4
                            ).replace("\"_", '"')
                    )
        except ApiException as e:
            Utility.print_exception(e)

    def get_input_json(self, env_id, customer_acc, api_instance, rule_name):
        """get_input_json."""
        all_deployment = None
        input_data = None
        all_deployment = api_instance.get_all_deployments_for_environment_by_id_0(env_id)     # noqa: E501
        if all_deployment:
            for single_deployment in all_deployment:
                if customer_acc and customer_acc in single_deployment.deployment_name or rule_name:   # noqa: E501
                    input_data = single_deployment.input_json
                    if rule_name:
                        data = {
                            'input_data': input_data,
                            'acc_no':  re.findall(r'-?\d+\.?\d*', single_deployment.deployment_name)
                        }
                        input_data = data
                return input_data
