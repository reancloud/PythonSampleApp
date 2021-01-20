"""REANPlatform setup.py."""
# !/usr/bin/env python

from setuptools import setup, find_packages

PROJECT = 'reanplatform-cli'

# Change docs/sphinx/conf.py too!

VERSION = '3.0.4'

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
                 'Programming Language :: Python :: 3.6.7',
                 'Intended Audience :: Developers',
                 'Environment :: Console',
                ],

    platforms=['Any'],

    scripts=[],

    provides=[],
    install_requires=['cliff==2.15.0', 'validators==0.14.0', 'boto3==1.9.225', 'urllib3==1.25.11', 'wheel==0.33.6', 'pycryptodome==3.9.0', 'certifi==2019.6.16', 'python-jenkins==1.5.0', 'cmd2==0.9.1', 'setuptools>=40.4.1', 'authnz_sdk_client==3.1.0', 'deploy_sdk_client==3.1.0', 'test_sdk_client==3.2.0', 'solution_sdk_client==0.16.0', 'workflow_sdk_client==0.16.0'],
    namespace_packages=[],
    packages=find_packages(),
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'rean-platform = reanplatform.main:main',
            'rean-deploy = deploy.main:main',
            'rean-auth = auth.main:main',
            'rean-mnc = mnc.main:main',
            'rean-test = reantest.main:main',
            'rean-workflow = workflow.main:main'
        ],
        'rean.workflow': [
            'create-solution=workflow.createsolution:CreateSolution',
            'delete-solution=workflow.deletesolution:DeleteSolution',
            'get-solution=workflow.getsolution:GetSolution',
            'list-solution=workflow.listsolution:ListSolutions',
            'solution-deploy=workflow.solutiondeploy:SolutionDeploy',
            'solution-destroy=workflow.solutiondestroy:SolutionDestroy',
            'get-solution-deployment=workflow.getsolutiondeployment:GetSolutionDeployment',
            'list-solution-deployments=workflow.listsolutiondeployment:ListSolutionDeployment',
        ],
        'rean.platform': [
            'rean-platform = reanplatform.reanhelp:HelpPlatform',
            'configure = reanplatform.configure:Configure',
            'rean-deploy = reanplatform.reanhelp:HelpDeploy',
            'rean-test = reanplatform.reanhelp:HelpTest',
            'rean-mnc = reanplatform.reanhelp:HelpMnc',
            'rean-auth = reanplatform.reanhelp:HelpAuth',
            'rean-workflow = reanplatform.reanhelp:HelpWorkflow'
        ],
        'rean.deploy': [
            'list-provider = deploy.listproviders:ListProvider',
            'create-provider = deploy.createprovider:SaveProvider',
            'update-provider = deploy.updateprovider:UpdateProvider',
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
            'get-env-outputs = deploy.env_outputs:GetEnvOutputs',
            'get-deployment-input = deploy.get_deployment_input:GetDeploymentInput',
            'get-deployment-logs = deploy.get_deployment_logs:GetDeploymentLogs',
            'get-deployment-output = deploy.get_deployment_output:GetDeploymentOutput',
            'get-validation-param = deploy.getvalidationparam:GetValidationParam',
            'get-status = deploy.getdeploymentstatus:Status',
            'get-environment = deploy.getenvironment:GetEnvironment',
            'get-terraform-code = deploy.getterraformcode:GetTerraformCode',
            'deploy-env = deploy.deployenv:DepolyEnv',
            'create-multiple-providers = deploy.create_multiple_providers:CreateMultipleProviders',
            'share-entity = deploy.share_entity:ShareEntity',
            'get-entity-actions = deploy.get_entity_actions:GetEntityActions',
            'get-provider = deploy.get_provider:GetProvider',
            'get-connection = deploy.get_connection:GetConnection',
            'get-deployment-resource-ids = deploy.get_deployment_resource_ids:GetDeploymentResourceIds',
            'get-accelerator-version = deploy.get_accelerator_version:GetAcceleratorVersion',
            'plan-environment = deploy.plan_environment:PlanEnvironment'
        ],
        'rean.auth': [
            'get-all-users = auth.get_users:GetUsers',
            'get-user = auth.get_user_by_name_or_id:GetUserByNameOrId',
            'change-password = auth.change_password:ChangePassword',
            'create-user = auth.create_user:CreateUser',
            'create-group= auth.create_group:CreateGroup',
            'verify-user=auth.verify_user:VerifyUser',
            'get-group=auth.get_group:GetGroup',
            'get-group-users=auth.get_group_users:GetGroupUsers',
            'add-user-to-group=auth.add_user_to_group:AddUserToGroup',
            'list-groups = auth.list_groups:ListGroups',
        ],
        'rean.test': [
            'run-url-test = reantest.run_url:RunURLTest',
            'run-security-test = reantest.run_security_test:RunSecurityTest',
            'run-automation-test = reantest.run_cross_browser_test:RunCrossBrowserTest',
            'run-scale-test =  reantest.run_scale_now_test:RunScaleNowTest',
            'get-job-status = reantest.get_job_status:GetJobStatus',
            'get-job-report = reantest.get_job_report:GetJobReport',
            'get-excel-report = reantest.get_excel_report:GetExcelReport',
            'get-infra-job-status = reantest.get_infra_job_status:GetInfraJobStatus',
            'run-infra-test = reantest.run_infra_test:RunInfraTest',
            'run-infra-awsspec = reantest.run_infratest_awsspec:RunInfraTestAwsSpec',
            'run-infra-azurespec = reantest.run_infratest_azurespec:RunInfraAzureSpec',
            'run-infratest-default-awsspec = reantest.run_infratest_default_awspec:RunInfraTestDefaultAwsSpec',
            'run-infratest-default-azurespec = reantest.run_infratest_default_azurespec:RunInfraDefaultAzureSpec',
            'run-api-test = reantest.run_api_test:RunApiTest',
            'get-accelerator-version = reantest.get_accelerator_version:GetAcceleratorVersion',
            'get-job-logs = reantest.get_logs:GetLogs',
            'run-infra-gcpspec = reantest.run_infratest_gcpspec:RunInfraTestGcpSpec'
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
