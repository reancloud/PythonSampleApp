"""Remove module."""
import logging
from cliff.command import Command
import deploy_sdk_client
import json
import re
from deploy_sdk_client.rest import ApiException
from reanplatform.set_header import set_header_parameter
from prettytable import PrettyTable
from reanplatform.utility import Utility
from deploy.destroydeployment import DestroyDeployment


class RuleRemove(Command):
    """Remove deployed rule."""

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        """get_parser."""
        parser = super(RuleRemove, self).get_parser(prog_name)
        parser.add_argument('--rule_name', '-n', help='Rule name.',
                            required=False)
        parser.add_argument('--rule_type', '-t', help='Rule type.',
                            required=False)
        parser.add_argument('--customer_acc', '-acc',
                            help='Customer AWS account number.', required=True)
        parser.add_argument('--force', '-f',
                            help='Forcefully remove rule.',
                            required=False)
        return parser

    def validate_parameters(self, rule_name, rule_type, customer_acc):
        """Validate cli parameter."""
        exception_msg = "Specify either ---customer_acc OR --rule_name\
                and --customer_acc"
        if rule_name is None and customer_acc is None:
            raise RuntimeError(re.sub(' +', ' ', exception_msg))
        elif rule_name and customer_acc is None:
            raise RuntimeError(re.sub(' +', ' ', exception_msg))

    def take_action(self, parsed_args):
        """take_action."""
        try:
            rule_name = parsed_args.rule_name
            rule_type = parsed_args.rule_type
            customer_acc = parsed_args.customer_acc
            force = parsed_args.force

            self.validate_parameters(rule_name, rule_type, customer_acc)

            if force is None:
                force = input("Are you sure? [Yes/No] :")
            else:
                exit

            if force == 'yes' or force == 'Yes' or force == 'y' or force == 'Y':    # noqa: E501
                instance = deploy_sdk_client.EnvironmentApi()
                api_instance = set_header_parameter(instance)
                all_env = api_instance.get_all_environments()
                deployment_id_to_remove = []

                for one_env in all_env:
                    deployment_id = None
                    if rule_name and customer_acc:
                        if one_env.name == rule_name:
                            deployment_id = self.get_deployment_ids(one_env.config.env_id, customer_acc, api_instance)     # noqa: E501
                    elif customer_acc:
                        deployment_id = self.get_deployment_ids(one_env.config.env_id, customer_acc, api_instance)     # noqa: E501

                    if deployment_id:
                        deployment_id_to_remove.append(deployment_id)

                if deployment_id_to_remove:
                    for deployment_id in deployment_id_to_remove:
                        DestroyDeployment.destroy_by_deploymentid(deployment_id)    # noqa: E501
                else:
                    print("No deployment for account :", customer_acc)

        except ApiException as e:
            Utility.print_exception(e)

    def get_deployment_ids(self, env_id, customer_acc, api_instance):
        all_deployment = None
        all_deployment = api_instance.get_all_deployments_for_environment_by_id(env_id)     # noqa: E501
        if all_deployment:
            for single_deployment in all_deployment:
                if single_deployment.input_json and customer_acc in single_deployment.input_json:   # noqa: E501
                    return single_deployment.id
