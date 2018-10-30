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
from deploy.constants import DeployConstants
from deploy.utility import DeployUtility

class RuleRemove(Command):      # noqa: D400
    """Destroy manage cloud deployed rule

    Example: rean-mnc remove-rule --rule_name mnc_check_ec2_unused_eip_value --customer_acc 693265998683
    """

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        """get_parser."""
        parser = super(RuleRemove, self).get_parser(prog_name)
        parser.add_argument('--' + MncConstats.RULE_NAME, MncConstats.RULE_NAME_INITIAL,
                            help='Managed cloud rule name',
                            required=False)
        parser.add_argument('--' + MncConstats.CUSTOMER_ACC, MncConstats.CUSTOMER_ACC_INITIAL,
                            help='Customer AWS account number',
                            required=False)
        parser.add_argument('--' + MncConstats.FORCE, MncConstats.FORCE_INITIAL,
                            help='Forcefully remove rule',
                            required=False)
        return parser

    # pylint: disable=R0201
    def __validate_parameters(self, rule_name, customer_acc):
        """Validate cli parameter."""
        exception_msg = "Specify either " + "--" + MncConstats.CUSTOMER_ACC + " OR " + "--" + MncConstats.RULE_NAME + \
            " OR " + "--" + MncConstats.CUSTOMER_ACC + " and " + "--" + MncConstats.RULE_NAME
        if rule_name is None and customer_acc is None:
            raise RuntimeError(re.sub(' +', ' ', exception_msg))

    def take_action(self, parsed_args):
        """take_action."""
        try:
            argparse_dict = vars(parsed_args)
            rule_name = argparse_dict[MncConstats.RULE_NAME]
            customer_acc = argparse_dict[MncConstats.CUSTOMER_ACC]
            force = argparse_dict[MncConstats.FORCE]

            self.__validate_parameters(rule_name, customer_acc)

            if force is None:
                force = input("Are you sure? [Yes/No]:")
            else:
                logging.info("Exit")

            if force.lower() == 'yes' or force.lower() == 'y':
                api_client = set_header_parameter(DeployUtility.create_api_client(), Utility.get_url(DeployConstants.DEPLOY_URL))
                api_instance = deploy_sdk_client.EnvironmentApi(api_client)
                all_env = api_instance.get_all_environments()
                deployment_id_to_remove = []
    
                for one_env in all_env:
                    deployment_id = None
                    time.sleep(1)
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
                        api_instance.destroy_deployment_by_id(deployment_id)
                        time.sleep(20)

                    if rule_name and customer_acc:
                        logging.info("Rule %s is destroyed for account: %s.", rule_name, customer_acc)
                    elif customer_acc:
                        logging.info("Destroyed all rules for account %s.", customer_acc)
                    elif rule_name:
                        logging.info("Destroyed rule %s in all account.", rule_name)
                else:
                    logging.info("No deployment found for account :%s", customer_acc)
        except ApiException as exception:
            logging.info("Failed to remove rule. Please try again.")
            # Utility.print_exception(exception)

    @staticmethod
    def get_deployment_ids(env_id, customer_acc, rule_name, api_instance, env_name):
        """get_deployment_ids."""
        all_deployment = None
        deployment_id_to_remove = []
        all_deployment = api_instance.get_all_deployments_for_environment_by_id(env_id)
        time.sleep(1)
        if all_deployment:
            for single_deployment in all_deployment:
                if customer_acc and customer_acc in single_deployment.deployment_name or rule_name and single_deployment.deployment_name:
                    if env_name.endswith('assume_role'):
                        deployment_id_to_remove.insert(0, single_deployment.id)
                    else:
                        deployment_id_to_remove.append(single_deployment.id)
        return deployment_id_to_remove
