"""Install Rule."""
import logging
import json
import ast
import time
import os
from os.path import basename
from cliff.command import Command
import deploy_sdk_client
from deploy_sdk_client.rest import ApiException
from reanplatform.set_header import set_header_parameter
from reanplatform.utility import Utility
from mnc.parameters_constants import MncConstats
from mnc.utility import MncUtility
from deploy.deployenv import DepolyEnv
from deploy.getdeploymentstatus import Status
from deploy.constants import DeployConstants
from deploy.utility import DeployUtility


class RuleInstall(Command):     # noqa: D203, D204
    """Install manage cloud rule. Example: rean-mnc install-rule --rule_name mnc_ec2_termination_protection --customer_acc 693265998683 --deploy_provider mnc_client --customer_email_to mayuri.patil@reancloud.com --customer_mail_cc akshay.deshpande@reancloud.com --customer_email_domain reancloud --action False."""
    # noqa: C0303
    def get_parser(self, prog_name):
        """get_parser."""
        parser = super(RuleInstall, self).get_parser(prog_name)
        parser.add_argument('--' + MncConstats.RULE_NAME, MncConstats.RULE_NAME_INITIAL,
                            help='Managed cloud rule name',
                            required=False)
        parser.add_argument('--' + MncConstats.CUSTOMER_ACC, MncConstats.CUSTOMER_ACC_INITIAL,
                            help='Customer AWS account number',
                            required=False)
        parser.add_argument('--' + MncConstats.DEPLOY_PROVIDER, MncConstats.DEPLOY_PROVIDER_INITIAL,
                            help='Provider name of client account for REAN-Deploy',
                            required=False)
        parser.add_argument('--' + MncConstats.CUSTOMER_EMAIL_TO, MncConstats.CUSTOMER_EMAIL_TO_INITIAL,
                            help='Customer email address To send email',
                            required=False)
        parser.add_argument('--' + MncConstats.CUSTOMER_MAIL_CC, MncConstats.CUSTOMER_MAIL_CC_INITIAL,
                            help='Customer CC email address',
                            required=False)
        parser.add_argument('--' + MncConstats.CUSTOMER_EMAIL_DOMAIN, MncConstats.CUSTOMER_EMAIL_DOMAIN_INITIAL,
                            help='Customer email domain',
                            required=False)
        parser.add_argument('--' + MncConstats.ENABLE_ACTION, MncConstats.ENABLE_ACTION_INITIAL,
                            help='Enable action allowed values are: [True, False]',
                            required=False)
        return parser

    def __validate_parameters(self, rule_name, customer_acc, provider_name, email_to, email_cc, domain, action):
        """Validate cli parameters."""
        logging.info("Validating parameters")
        if rule_name is None or customer_acc is None or provider_name is None or email_to is None or domain is None or action is None:
            raise RuntimeError("Specify all require parametes, for more help check 'rean-mnc install-rule --help'")    # noqa: E501

    def re_deploy_environment(self, environment_id, deployment_name, deployment_description, provider_name, region, child_input_json, depends_on_json):
        """Redeploy An Environment."""
        try:
            # Initialise instance and api_instance and response
            api_client = set_header_parameter(DeployUtility.create_api_client(), Utility.get_url(DeployConstants.DEPLOY_URL))
            instance = deploy_sdk_client.EnvironmentApi(api_client)
            response = None
            body = deploy_sdk_client.DeploymentConfigurationDto(
                environment_id=environment_id,
                deployment_name=deployment_name,
                deployment_description=deployment_description,
                region=region,
                provider_name=provider_name,
                input_json=child_input_json,
                parent_deployments=depends_on_json
            )
            response = instance.deploy_by_config(
                body=body
            )

            # Get deployment status
            status = Status.deployment_status(environment_id, deployment_name)
            while status is not None:
                status = Status.deployment_status(environment_id, deployment_name)  # noqa: E501
                status_dict = str(status)
                if MncConstats.DEPLOYING in status_dict:
                    time.sleep(1)
                else:
                    break

            return response
        except ApiException as api_exception:
            Utility.print_exception(api_exception)

    def take_action(self, parsed_args):
        """List Environment."""
        argparse_dict = vars(parsed_args)
        rule_name = argparse_dict[MncConstats.RULE_NAME]
        customer_acc = argparse_dict[MncConstats.CUSTOMER_ACC]
        provider_name = argparse_dict[MncConstats.DEPLOY_PROVIDER]
        email_to = argparse_dict[MncConstats.CUSTOMER_EMAIL_TO]
        email_cc = argparse_dict[MncConstats.CUSTOMER_MAIL_CC]
        domain = argparse_dict[MncConstats.CUSTOMER_EMAIL_DOMAIN]
        action = argparse_dict[MncConstats.ENABLE_ACTION]
        region = MncConstats.REGION
        self.__validate_parameters(rule_name, customer_acc, provider_name, email_to, email_cc, domain, action)

        prepare_data = {}
        dependent_resource_file = os.getcwd() + '/' + 'depends_on_resource.json'
        input_json_file_path = os.getcwd() + '/' + 'input_json.json'
        depends_on_json = None
        deployment_name = 'default_client_' + customer_acc
        child_input_json = None
        deployment_description = 'test'

        try:
            api_client = set_header_parameter(DeployUtility.create_api_client(), Utility.get_url(DeployConstants.DEPLOY_URL))
            instance = deploy_sdk_client.EnvironmentApi(api_client)
            # Get all environments for user
            all_env = instance.get_all_environments()
            env_ids = {}

            for one_env in all_env:
                if (one_env.name.startswith(rule_name) and one_env.name.endswith('rules_setup')):
                    env_ids['parent'] = one_env.config.env_id
                    input_from_env = instance.get_input_json(one_env.config.env_id)
                    RuleInstall.updated_input_file(input_json_file_path, input_from_env, email_to, email_cc, action)
                    parent_input_json = DepolyEnv.read_file_as_json_object(input_json_file_path)
                    RuleInstall.create_att_file(dependent_resource_file, prepare_data)
                    result = RuleInstall.re_deploy_environment(self, env_ids['parent'], deployment_name, deployment_description, provider_name, region, parent_input_json, depends_on_json)
            # Create File of Depends_On resource
            config_status = RuleInstall.get_status(env_ids['parent'], deployment_name)
            logging.info("Rule %s is deployed for account: %s", rule_name, customer_acc)

        except ApiException as exception:
            # Utility.print_exception(exception)
            logging.info("Failed to install rule. Please try again.")

    @staticmethod
    def get_status(env_id, deployment_name):
        """get_status of deployment."""
        status = None
        while True:
            status = Status.deployment_status(env_id, deployment_name)  # noqa: E501
            status_dict = str(status)
            if MncConstats.DEPLOYING in status_dict:
                time.sleep(1)
            else:
                break
        return status

    @staticmethod
    def create_att_file(file_name, prepare_data):
        """create_att_file."""
        try:
            os.chdir(os.path.dirname(file_name))
            with open(basename(file_name), 'w') as outfile:
                json.dump(prepare_data, outfile, indent=4, sort_keys=True)
        except Exception as exception:
            logging.info("Failed to create attribute file. Please try again.")
            # Utility.print_exception(exception)

    @staticmethod
    def updated_input_file(input_json_file_path, input_from_env, email_to, email_cc, action):
        """Create updated_input_file."""
        data = ast.literal_eval(input_from_env)
        input_data = data['input_variables']['input_variables']
        input_data['toEmail'] = email_to
        input_data['ccEmail'] = email_cc
        input_data['performAction'] = action
        input_data['notifierLambdaRoleArn'] = MncUtility.read_role_arn(MncConstats.NOTIFIER_ROLE_NAME)
        input_data['lambdaRoleArn'] = MncUtility.read_role_arn(MncConstats.PROCESSOR_ROLE_NAME)
        input_data['lambdaArn'] = MncUtility.read_lambda_arn(MncConstats.RULE_PROCESSOR_LAMBDA_NAME)
        input_data['maximum_execution_frequency'] = MncConstats.MAXIMUM_EXECUTION_FREQUENCY
        RuleInstall.create_att_file(input_json_file_path, input_data)
