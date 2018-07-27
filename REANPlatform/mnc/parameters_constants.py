"""Contains constats required for commands."""
from pathlib import Path


class MncConstats(object):      # noqa: D203
    """Contains constats required for MNCCLI."""

    RULE_NAME = 'rule_name'
    RULE_NAME_INITIAL = '-n'
    RULE_TYPE = 'rule_type'
    RULE_TYPE_INITIAL = '-t'
    CUSTOMER_ACC = 'customer_acc'
    CUSTOMER_ACC_INITIAL = '-a'
    FORCE = 'force'
    FORCE_INITIAL = '-f'
    DEPLOY_PROVIDER = 'deploy_provider'
    DEPLOY_PROVIDER_INITIAL = '-p'
    CUSTOMER_EMAIL_TO = 'customer_to_email'
    CUSTOMER_EMAIL_TO_INITIAL = '-to'
    CUSTOMER_MAIL_CC = 'customer_cc_email'
    CUSTOMER_MAIL_CC_INITIAL = '-cc'
    CUSTOMER_EMAIL_DOMAIN = 'customer_email_domain'
    CUSTOMER_EMAIL_DOMAIN_INITIAL = '-d'
    ACTION = 'action'
    ACTION_INITIAL = '-a'
    CONFIGURATION_BUCKET = 'configuration_bucket'
    CONFIGURATION_BUCKET_INITIAL = '-cb'
    DEPLOY_GROUP = 'deploy_group'
    DEPLOY_GROUP_INITIAL = '-g'
    MASTER_PROVIDER = 'master_provider'
    MASTER_PROVIDER_INITIAL = '-p'
    ARTIFACTORY_BUCKET = 'artifactory_bucket'
    ARTIFACTORY_BUCKET_INITIAL = '-b'
    MASTER_ACC = 'master_acc_no'
    MASTER_ACC_INITIAL = '-n'
    MASTER_CONNECTION = 'master_connection'
    MASTER_CONNECTION_INITIAL = '-c'

    # parameter forrule input
    DEPLOYING = '"DEPLOYING"'
    NOTIFIER_ROLE_NAME = 'rean_mnc_notifier_lambda_role'
    PROCESSOR_ROLE_NAME = 'rean_mnc_rule_processor_lambda_role'
    RULE_PROCESSOR_LAMBDA_NAME = 'rean_mnc_rule_processor'
    MAXIMUM_EXECUTION_FREQUENCY = 'TwentyFour_Hours'       # One_Hour Three_Hours Six_Hours Twelve_Hours TwentyFour_Hours
    REGION = 'us-east-1'
    FILE_BUCKET_NAME = str(Path.home()) + '/.mnc/bucket.yml'
    CONFIGURATION_BUCKET_PATH = str(Path.home()) + '/.mnc/'
    LOCAL_ARTIFACTS_ZIP_PATH = '/tmp/mnc/'
