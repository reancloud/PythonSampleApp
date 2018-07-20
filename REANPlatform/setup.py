"""REANPlatform setup.py."""
# !/usr/bin/env python

from setuptools import setup, find_packages

PROJECT = 'REANPlatform'

# Change docs/sphinx/conf.py too!
VERSION = '0.1'

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
    download_url='https://github.com/reancloud/deploy_sdk_client',
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

    install_requires=['cliff', 'validators', 'boto3', 'Crypto', 'wheel', 'pycrypto'],

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
            'list-environment = deploy.listenvironments:ListEnvironments',
            'delete-environment = deploy.deleteenvironment:DeleteEnvironment',
            'prepare-blueprint = deploy.blueprint_prepare:PrepareBlueprint',
            'import-blueprint = deploy.blueprint_import:ImportBlueprint',
            'get-deployment-id = deploy.getdeploymentid:GetDeployments',
            'get-status = deploy.getdeploymentstatus:Status',
            'deploy-env = deploy.deployenv:DepolyEnv'
        ],
        'rean.auth': [
            'get-all-users = auth.get_users:GetUsers',
            'get-user = auth.get_user_by_name_or_id:GetUserByNameOrId'
        ],
        'rean.test': [
            'run-url-test = reantest.run_url:RunURLTest',
            'run-upa-test = reantest.run_upa:RunUPA',
            'run-security-test = reantest.run_security_test:RunSecurityTest',
            'run-automation-test = reantest.run_cross_browser_test:RunCrossBrowserTest',
            'run-scale-test =  reantest.run_scale_now_test:RunScaleNowTest',
            'get-job-status = reantest.get_job_status:GetJobStatus'
        ],
        'rean.mnc': [
            # 'configure = mnc.configure:Configure',
            # 'rule = mnc.rule:Rule',
            'rule-install = mnc.rule_install:RuleInstall',
            'rule-list = mnc.rule_list:RuleList',
            'rule-remove = mnc.rule_remove:RuleRemove'
        ],
        #    'rean.deploy': [
        #        'deploy-configure = deploy.configure:Configure',
        #        'create-provider = deploy.createprovider:SaveProvider',
        #        'delete-provider = deploy.deleteprovider:DeleteProvider',
        #        'list-provider = deploy.listproviders:ListProvider',
        #        'create-environment = deploy.createenvironment:CreateEnv',
        #        'deploy-environment = deploy.deployenvironment:DepolyEnv',
        #        'list-connections = deploy.listconnections:ListConnections',
        #        'isconnectionexists = deploy.isconnectionexists:IsConnectionExists',
        #        'create-connection = deploy.createconnection:SaveConnection',
        #        'delete-connection = deploy.deleteconnection:DeleteConnection',
        #        'get-connection = deploy.getconnection:GetConnection',
        #        'get-provider = deploy.getproviderbyname:GetProviderByName',
        #        'update-connection = deploy.updateconnection:UpdateConnection',
        #        'get-aws-regions = deploy.getawsregions:GetAwsRegions',
        #        'delete-environment = deploy.deleteenvironment:DeleteEnv',
        #        'checkifenvironmentexists = deploy.checkifenvironmentexists:CheckIfEnvironmentExists',
        #        'download-terraform-files =deploy.downloadterraformfiles:DownloadTerraformFiles',
        #        'update-provider = deploy.updateprovider:UpdateProvider',
        #        'import-blueprint = deploy.importblueprint:ImportBlueprint',
        #        'import-environment = deploy.importenvironment:ImportEnvironment',
        #        'createnewenvresourceusingimport = deploy.createnewenvresourceusingimport:CreateNewEnvResourceUsingImport',
        #        'hooked = deploy.hook:Hooked',
        #    ],
        #    'rean.test.hooked': [
        #        'sample-hook = deploy.hook:Hook',
        #   ],
    },

    zip_safe=False,
)
