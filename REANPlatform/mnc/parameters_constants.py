"""Contains constats required for commands."""
from pathlib import Path


class MncConstats(object):      # noqa: D203
    """Contains constats required for MNCCLI."""

    RULE_NAME = 'rule_name'
    RULE_NAME_INITIAL = '-n'
    RULE_TYPE = 'rule_type'
    RULE_TYPE_INITIAL = '-t'
    CUSTOMER_ACC = 'customer_acc'
    CUSTOMER_ACC_INITIAL = '-acc'
    FORCE = 'force'
    FORCE_INITIAL = '-f'
    DEPLOY_PROVIDER = 'deploy_provider'
    DEPLOY_PROVIDER_INITIAL = '-provider'
    CUSTOMER_EMAIL_TO = 'customer_email_to'
    CUSTOMER_EMAIL_TO_INITIAL = '-email_to'
    CUSTOMER_MAIL_CC = 'customer_mail_cc'
    CUSTOMER_MAIL_CC_INITIAL = '-email_cc'
    CUSTOMER_EMAIL_DOMAIN = 'customer_email_domain'
    CUSTOMER_EMAIL_DOMAIN_INITIAL = '-domain'
    ACTION = 'action'
    ACTION_INITIAL = '-a'

    # parameter forrule input
    DEPLOYING = '"DEPLOYING"'
    NOTIFIER_ROLE_NAME = 'rean_mnc_notifier_lambda_role'
    PROCESSOR_ROLE_NAME = 'rean_mnc_rule_processor_lambda_role'
    RULE_PROCESSOR_LAMBDA_NAME = 'rean_mnc_rule_processor'
    MAXIMUM_EXECUTION_FREQUENCY = 'TwentyFour_Hours'       # One_Hour Three_Hours Six_Hours Twelve_Hours TwentyFour_Hours
    REGION = 'us-east-1'
    FILE_BUCKET_NAME = str(Path.home()) + '/.mnc/bucket.yml'
