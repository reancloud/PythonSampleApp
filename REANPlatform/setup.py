"""REANPlatform setup.py."""
# !/usr/bin/env python

from setuptools import setup, find_packages

PROJECT = 'REANPlatform'

# Change docs/sphinx/conf.py too!
VERSION = '0.0.5'

try:
    long_description = open('README.rst', 'rt').read()
except IOError:
    long_description = ''

setup(
    name=PROJECT,
    version=VERSION,
    description='CLI for REAN Platform',
    long_description=long_description,
    url='https://github.com/reancloud/',
    download_url='',
    classifiers=['Development Status :: 3 - Alpha',
                 'License :: OSI Approved :: Apache Software License',
                 'Programming Language :: Python',
                 'Programming Language :: Python :: 3',
                 'Programming Language :: Python :: 3.2',
                 'Programming Language :: Python :: 3.5.1',
                 'Programming Language :: Python :: 3.5.5',
                 'Programming Language :: Python :: 3.6',
                 'Intended Audience :: Developers',
                 'Environment :: Console',
                ],

    platforms=['Any'],

    scripts=[],

    provides=[],

    install_requires=['cliff', 'validators', 'boto3', 'wheel', 'pycrypto', 'certifi', 'python-jenkins'],
    namespace_packages=[],
    packages=find_packages(),
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'rean-platform = reanplatform.main:main',
            'rean-deploy = deploy.main:main',
            'rean-auth = auth.main:main',
            'rean-mnc = mnc.main:main',
            'rean-test = reantest.main:main'
        ],
        'rean.platform': [
            'rean-platform = reanplatform.reanhelp:HelpPlatform',
            'configure = reanplatform.configure:Configure',
            'rean-deploy = reanplatform.reanhelp:HelpDeploy',
            'rean-test = reanplatform.reanhelp:HelpTest',
            'rean-mnc = reanplatform.reanhelp:HelpMnc',
            'rean-auth = reanplatform.reanhelp:HelpAuth'
        ],
        'rean.deploy': [
            'list-provider = deploy.listproviders:ListProvider',
            'create-provider = deploy.createprovider:SaveProvider',
            'delete-provider = deploy.deleteprovider:DeleteProvider',
            'list-connection = deploy.listconnections:ListConnections',
            'create-connection = deploy.createconnection:SaveConnection',
            'delete-connection = deploy.deleteconnection:DeleteConnection',
            'destroy-deployment = deploy.destroydeployment:DestroyDeployment',
            'plan-deployment = deploy.plandeployment:PlanDeployment',
            'stop-deployment = deploy.stop_deployment:StopDeployment',
            'export-environment = deploy.exportenvironment:ExportEnvironment',
            'export-blueprint-environment = deploy.exportblueprintenvironment:ExportBlueprintEnvironment',
            'list-environment = deploy.listenvironments:ListEnvironments',
            'delete-environment = deploy.deleteenvironment:DeleteEnvironment',
            'prepare-blueprint = deploy.blueprint_prepare:PrepareBlueprint',
            'import-blueprint = deploy.blueprint_import:ImportBlueprint',
            'get-deployment-id = deploy.getdeploymentid:GetDeploymentId',
            'get-deployment-input = deploy.get_deployment_input:GetDeploymentInput',
            'get-deployment-output = deploy.get_deployment_output:GetDeploymentOutput',
            'get-validation-param = deploy.getvalidationparam:GetValidationParam',
            'get-status = deploy.getdeploymentstatus:Status',
            'deploy-env = deploy.deployenv:DepolyEnv',
            'create-multiple-providers = deploy.create_multiple_providers:CreateMultipleProviders'
        ],
        'rean.auth': [
            'get-all-users = auth.get_users:GetUsers',
            'get-user = auth.get_user_by_name_or_id:GetUserByNameOrId',
            'change-password = auth.change_password:ChangePassword'
        ],
        'rean.test': [
            'run-url-test = reantest.run_url:RunURLTest',
            'run-upa-test = reantest.run_upa:RunUPA',
            'run-security-test = reantest.run_security_test:RunSecurityTest',
            'run-automation-test = reantest.run_cross_browser_test:RunCrossBrowserTest',
            'run-scale-test =  reantest.run_scale_now_test:RunScaleNowTest',
            'get-job-status = reantest.get_job_status:GetJobStatus',
            'get-job-report = reantest.get_job_report:GetJobReport',
            'create-provider = reantest.create_provider:CreateProvider',
            'list-providers = reantest.list_providers:ListProvider',
            'get-infra-job-status = reantest.get_infra_job_status:GetInfraJobStatus',
            'run-infra-test = reantest.run_infra_test:RunInfraTest',
            'run-infra-awsspec = reantest.run_infratest_awsspec:RunInfraTestAwsSpec',
            'update-tags = reantest.config_update_tags:ConfigUpdateTags',
            'update-property = reantest.config_update_property:ConfigUpdateProperty',
            'list-config-properties = reantest.get_all_config_properties:ConfigListProperties'
        ],
        'rean.mnc': [
            'configure = mnc.configure:Configure',
            'available-rules = mnc.rules_available:RuleAvailable',
            'install-rule = mnc.rule_install:RuleInstall',
            'list-rule = mnc.rule_list:RuleList',
            'remove-rule = mnc.rule_remove:RuleRemove'
        ]
    },

    zip_safe=True,
)
