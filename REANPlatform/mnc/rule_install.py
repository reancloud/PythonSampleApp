"""Install Rule."""
import logging
import json
import ast
import time
import os
from os.path import basename
import boto3
from cliff.command import Command
import deploy_sdk_client
from deploy_sdk_client.rest import ApiException
from reanplatform.set_header import set_header_parameter
from reanplatform.utility import Utility
from mnc.parameters_constants import MncConstats
from deploy.deployenv import DepolyEnv
from deploy.getdeploymentstatus import Status


class RuleInstall(Command):     # noqa: D203
    """Install Manage Cloud Rules."""

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        """get_parser."""
        parser = super(RuleInstall, self).get_parser(prog_name)
        parser.add_argument('--' + MncConstats.RULE_NAME, MncConstats.RULE_NAME_INITIAL,
                            help='Rule name',
                            required=False)
        parser.add_argument('--' + MncConstats.RULE_TYPE, MncConstats.RULE_TYPE_INITIAL,
                            help='Rule type',
                            required=False)
        parser.add_argument('--' + MncConstats.CUSTOMER_ACC, MncConstats.CUSTOMER_ACC_INITIAL,
                            help='Customer account number',
                            required=False)
        parser.add_argument('--' + MncConstats.DEPLOY_PROVIDER, MncConstats.DEPLOY_PROVIDER_INITIAL,
                            help='Rean deploy provider',
                            required=False)
        parser.add_argument('--' + MncConstats.CUSTOMER_EMAIL_TO, MncConstats.CUSTOMER_EMAIL_TO_INITIAL,
                            help='Customer To email',
                            required=False)
        parser.add_argument('--' + MncConstats.CUSTOMER_MAIL_CC, MncConstats.CUSTOMER_MAIL_CC_INITIAL,
                            help='Customer CC email',
                            required=False)
        parser.add_argument('--' + MncConstats.CUSTOMER_EMAIL_DOMAIN, MncConstats.CUSTOMER_EMAIL_DOMAIN_INITIAL,
                            help='Customer email domain',
                            required=False)
        parser.add_argument('--' + MncConstats.ACTION, MncConstats.ACTION_INITIAL,
                            help='Customer account number',
                            required=False)
        return parser

    def __validate_parameters(rule_name, rule_type, customer_acc, provider_name, email_to, email_cc, domain, action):
        """Validate cli parameters."""
        if rule_name is None and rule_type is None and customer_acc is None:
            raise RuntimeError("Specify either --rule_name OR --customer_acc OR --rule_name and --customer_acc")    # noqa: E501

    def take_action(self, parsed_args):
        """List Environment."""
        argparse_dict = vars(parsed_args)
        rule_name = argparse_dict[MncConstats.RULE_NAME]
        rule_type = argparse_dict[MncConstats.RULE_TYPE]
        customer_acc = argparse_dict[MncConstats.CUSTOMER_ACC]
        provider_name = argparse_dict[MncConstats.DEPLOY_PROVIDER]
        email_to = argparse_dict[MncConstats.CUSTOMER_EMAIL_TO]
        email_cc = argparse_dict[MncConstats.CUSTOMER_MAIL_CC]
        domain = argparse_dict[MncConstats.CUSTOMER_EMAIL_DOMAIN]
        action = argparse_dict[MncConstats.ACTION]
        region = MncConstats.REGION
        RuleInstall.__validate_parameters(rule_name, rule_type, customer_acc, provider_name, email_to, email_cc, domain, action)


        prepare_data = {}
        dependent_resource_file = os.getcwd() + '/' + 'depends_on_resource.json'
        input_json_file_path = os.getcwd() + '/' + 'input_json.json'
        depends_on_json = None
        deployment_name = 'default_client_' + customer_acc
        child_input_json = None
        deployment_description = 'test'

        try:
            instance = deploy_sdk_client.EnvironmentApi()
            api_instance = set_header_parameter(instance)
            all_env = api_instance.get_all_environments()
            env_ids = {}

            for one_env in all_env:
                if (one_env.name.startswith(rule_name) and one_env.name.endswith('config_rule_setup')):
                    env_ids['parent'] = one_env.config.env_id
                    input_from_env = api_instance.get_input_json(one_env.config.env_id)
                    RuleInstall.updated_input_file(input_json_file_path, input_from_env, email_to, email_cc, action)
                    parent_input_json = DepolyEnv.read_file_as_json_object(input_json_file_path)

                elif (one_env.name.startswith(rule_name) and one_env.name.endswith('assume_role')):
                    env_ids['child'] = one_env.config.env_id
                    depend_resources = ast.literal_eval(api_instance.get_input_json(one_env.config.env_id))
                    for depend_name in depend_resources:
                        if 'Depends_On' in depend_resources[depend_name]:
                            if str(depend_name) == 'mnc_rule_dependency':
                                prepare_data[depend_name] = deployment_name
                            else:
                                prepare_data[depend_name] = 'default'

            # Create File of Depends_On resource
            if prepare_data:
                RuleInstall.create_att_file(dependent_resource_file, prepare_data)

            result = DepolyEnv.re_deploy_environment(env_ids['parent'], deployment_name, deployment_description, provider_name, region, parent_input_json, depends_on_json)

            status = RuleInstall.get_status(env_ids['parent'], deployment_name)
            logging.info("Config rule status::%s", status)

            # Deploy child
            if status.status == 'DEPLOYED':
                child_input_json = None
                time.sleep(10)
                provider_name = RuleInstall.provider_name_from_s3(str(RuleInstall.read_bucket_name()))
                deployment_name = 'default_master_' + customer_acc
                depends_json = DepolyEnv.read_file_as_json_object(dependent_resource_file)
                result = DepolyEnv.re_deploy_environment(env_ids['child'], deployment_name, deployment_description, provider_name, region, child_input_json, depends_json)
                if result:
                    status = self.get_status(env_ids['child'], deployment_name)
                    logging.info("Assume rule Status ::%s", status.status)
        except ApiException as exception:
            Utility.print_exception(exception)

    @staticmethod
    def get_status(env_id, deployment_name):
        """get_status of deployment."""
        status = None
        while 1:
            status = Status.deployment_status(env_id, deployment_name)  # noqa: E501
            status_dict = str(status)
            if "DEPLOYING" in status_dict:
                time.sleep(1)
            else:
                break
        return status

    @staticmethod
    def read_bucket_name():
        """read_bucket_name of mnc config."""
        with open(MncConstats.FILE_BUCKET_NAME, "r") as file_data:
            bucket_name = file_data.read().replace('\n', '')
            bucket_name = bucket_name.split(':')[-1]
            bucket_name = bucket_name.strip()
        return bucket_name

    @staticmethod
    def create_att_file(file_name, prepare_data):
        """create_att_file."""
        os.chdir(os.path.dirname(file_name))
        with open(basename(file_name), 'w') as outfile:
            json.dump(prepare_data, outfile, indent=4, sort_keys=True)

    @staticmethod
    def provider_name_from_s3(bucket_name):
        """Read deploy provider_name_from_s3 of master account."""
        s3_client = boto3.client('s3')
        response = s3_client.list_objects(Bucket=bucket_name)
        for file in response['Contents']:
            obj = s3_client.get_object(Bucket=bucket_name, Key=file['Key'])
            file_s3_content = obj['Body'].read()

            for file_line in file_s3_content.decode('utf-8').split("\n"):
                if "rean_deploy_mnc_master_provider" in file_line:
                    provider_name = file_line.split(':')[-1]
                    provider_name = provider_name.strip()
        return provider_name

    @staticmethod
    def updated_input_file(input_json_file_path, input_from_env, email_to, email_cc, action):
        """Create updated_input_file."""
        data = ast.literal_eval(input_from_env)
        input_data = data['Input Variables']['input_variables']
        input_data['toEmail'] = email_to
        input_data['ccEmail'] = email_cc
        input_data['performAction'] = action
        input_data['notifierLambdaRoleArn'] = RuleInstall.read_role_arn(MncConstats.NOTIFIER_ROLE_NAME)
        input_data['lambdaRoleArn'] = RuleInstall.read_role_arn(MncConstats.PROCESSOR_ROLE_NAME)
        input_data['lambdaArn'] = RuleInstall.read_lambda_arn(MncConstats.RULE_PROCESSOR_LAMBDA_NAME)
        input_data['maximum_execution_frequency'] = MncConstats.MAXIMUM_EXECUTION_FREQUENCY
        RuleInstall.create_att_file(input_json_file_path, input_data)

    @staticmethod
    def read_role_arn(role_name):
        """read_role_arn."""
        client = boto3.client('iam')
        notifier_lambda_role = client.get_role(RoleName=role_name)
        return notifier_lambda_role['Role']['Arn']

    @staticmethod
    def read_lambda_arn(lambda_name):
        """read_lambda_arn."""
        client = boto3.client('lambda')
        response = client.get_function(FunctionName=lambda_name)
        return response['Configuration']['FunctionArn']
