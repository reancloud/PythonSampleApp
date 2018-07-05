"""Remove module."""
import logging
import time
import re
from cliff.command import Command
import deploy_sdk_client
from deploy_sdk_client.rest import ApiException
from mnc.parameters_constants import MncConstats
from reanplatform.set_header import set_header_parameter
from reanplatform.utility import Utility
from deploy.destroydeployment import DestroyDeployment


class RuleRemove(Command):      # noqa: D203
    """Remove deployed rule."""

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        """get_parser."""
        parser = super(RuleRemove, self).get_parser(prog_name)
        parser.add_argument(MncConstats.RULE_NAME, '-n', help='Rule name.',
                            required=False)
        parser.add_argument(MncConstats.RULE_TYPE, '-t', help='Rule type.',
                            required=False)
        parser.add_argument(MncConstats.CUSTOMER_ACC, '-acc',
                            help='Customer AWS account number.',
                            required=False)
        parser.add_argument(MncConstats.FORCE, '-f',
                            help='Forcefully remove rule.',
                            required=False)
        return parser

    # pylint: disable=R0201
    def __validate_parameters(rule_name, rule_type, customer_acc):
        """Validate cli parameter."""
        exception_msg = "Specify either " + MncConstats.CUSTOMER_ACC + " OR " + MncConstats.RULE_NAME + \
            " OR " + MncConstats.CUSTOMER_ACC + " and " + MncConstats.RULE_NAME
        if rule_name is None and customer_acc is None:
            raise RuntimeError(re.sub(' +', ' ', exception_msg))

    def take_action(self, parsed_args):
        """take_action."""
        try:
            rule_name = parsed_args.rule_name
            rule_type = parsed_args.rule_type
            customer_acc = parsed_args.customer_acc
            force = parsed_args.force

            RuleRemove.__validate_parameters(rule_name, rule_type, customer_acc)

            if force is None:
                force = input("Are you sure? [Yes/No] :")
            else:
                print("Exit")

            if force.lower() == 'yes' or force.lower() == 'y':
                instance = deploy_sdk_client.EnvironmentApi()
                api_instance = set_header_parameter(instance)
                all_env = api_instance.get_all_environments()
                deployment_id_to_remove = []

                for one_env in all_env:
                    deployment_id = None
                    if rule_name and customer_acc:
                        if one_env.name.startswith(rule_name):
                            deployment_id = RuleRemove.get_deployment_ids(one_env.config.env_id, customer_acc, None, api_instance, one_env.name)
                    elif customer_acc:
                        deployment_id = RuleRemove.get_deployment_ids(one_env.config.env_id, customer_acc, None, api_instance, one_env.name)
                    elif rule_name:
                        if one_env.name.startswith(rule_name):
                            deployment_id = RuleRemove.get_deployment_ids(one_env.config.env_id, customer_acc, rule_name, api_instance, one_env.name)

                    if deployment_id:
                        deployment_id_to_remove = deployment_id_to_remove + deployment_id

                if deployment_id_to_remove:
                    for deployment_id in deployment_id_to_remove:
                        DestroyDeployment.destroy_by_deploymentid(deployment_id)
                        time.sleep(20)
                else:
                    print("No deployment for account :", customer_acc)
        except ApiException as exception:
            Utility.print_exception(exception)

    @staticmethod
    def get_deployment_ids(env_id, customer_acc, rule_name, api_instance, env_name):
        """get_deployment_ids."""
        all_deployment = None
        deployment_id_to_remove = []
        all_deployment = api_instance.get_all_deployments_for_environment_by_id_0(env_id)
        if all_deployment:
            for single_deployment in all_deployment:
                if customer_acc and customer_acc in single_deployment.deployment_name or rule_name and single_deployment.deployment_name:
                    if env_name.endswith('assume_role'):
                        deployment_id_to_remove.insert(0, single_deployment.id)
                    else:
                        deployment_id_to_remove.append(single_deployment.id)
        return deployment_id_to_remove
