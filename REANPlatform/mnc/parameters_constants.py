"""Contains constats required for commands."""
from pathlib import Path


class MncConstats():      # noqa: D203
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
    ENABLE_ACTION = 'enable_action'
    ENABLE_ACTION_INITIAL = '-e'

    # parameter forrule input
    DEPLOYING = '"DEPLOYING"'
    NOTIFIER_ROLE_NAME = 'release9_rean_mnc_notifier_lambda_role'
    PROCESSOR_ROLE_NAME = 'release9_rean_mnc_rule_processor_lambda_role'
    RULE_PROCESSOR_LAMBDA_NAME = 'release9_rean_mnc_rule_processor'
    MAXIMUM_EXECUTION_FREQUENCY = 'TwentyFour_Hours'       # One_Hour Three_Hours Six_Hours Twelve_Hours TwentyFour_Hours
    REGION = 'eu-west-1'
    FILE_BUCKET_NAME = str(Path.home()) + '/.mnc/config_bucket.yaml'
    CONFIGURATION_BUCKET_PATH = str(Path.home()) + '/.mnc/'
    LOCAL_ARTIFACTS_ZIP_PATH = '/tmp/mnc/'
    CUSTOMER_ACCOUNT_READ_ROLE_ARN = "arn:aws:iam::324224971769:role/mnc_read_role"
    CUSTOMER_ACCOUNT_WRITE_ROLE_ARN = "arn:aws:iam::324224971769:role/mnc_write_role"
    CUSTOMER_ACCOUNT_NUMBER = "324224971769"
