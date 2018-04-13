#!/usr/bin/env python

PROJECT = 'REANPlatform'

# Change docs/sphinx/conf.py too!
VERSION = '0.1'

from setuptools import setup, find_packages

try:
    long_description = open('README.rst', 'rt').read()
except IOError:
    long_description = ''

setup(
    name=PROJECT,
    version=VERSION,

    description='CLI for REAN Platform',
    long_description=long_description,

    author='Rajashri Dalavi',
    author_email='rajashri.dalavi@reancloud.com',

    url='https://www.reancloud.com/',
    download_url='https://www.reancloud.com/',

    classifiers=['Development Status :: 3 - Alpha',
                 'License :: OSI Approved :: Apache Software License',
                 'Programming Language :: Python',
                 'Programming Language :: Python :: 3',
                 'Programming Language :: Python :: 3.2',
                 'Programming Language :: Python :: 3.6',
                 'Intended Audience :: Developers',
                 'Environment :: Console',
                 ],

    platforms=['Any'],

    scripts=[],

    provides=[],
    install_requires=['cliff','validators','boto3'],

    namespace_packages=[],
    packages=find_packages(),
    include_package_data=True,

    entry_points={
        'console_scripts': [
            'rean-test = test.main:main',
            'rean-deploy = deploy.main:main',
            'rean-mnc = mnc.main:main'
        ],
        'rean.mnc': [
            'configure = mnc.configure:Configure',
            'rule = mnc.rule:Rule',
            'rule install = mnc.rule_install:RuleInstall',
            'rule list = mnc.rule_list:RuleList',
            'rule remove = mnc.rule_remove:RuleRemove'
        ],
        'rean.test': [
            'run-url-test = test.runurl:RunURLTest',
            'run-upa-test = test.runupa:RunUPA',
            'run-security-test = test.runsecuritytest:RunSecurityTest',
            'run-automation-test = test.runcrossbrowsertest:RunCrossBrowserTest',
            'run-scale-test =  test.runscalenowtest:RunScaleNowTest',
            'get-job-status = test.getjobstatus:GetJobStatus',
            'getproperties = test.testnowutility:GetProperties',
        ],
        'rean.deploy': [
            'deploy-configure = deploy.configure:Configure',
            'create-environment = deploy.createenvironment:CreateEnv',
            'deploy-environment = deploy.deployenvironment:DepolyEnv',
            'list-connections = deploy.listconnections:ListConnections',
            'isconnectionexists = deploy.isconnectionexists:IsConnectionExists',
            'create-connection = deploy.createconnection:SaveConnection',
            'create-provider = deploy.createprovider:SaveProvider',
            'delete-connection = deploy.deleteconnection:DeleteConnection',
            'get-connection = deploy.getconnection:GetConnection',
            'get-provider = deploy.getproviderbyname:GetProviderByName',
            'update-connection = deploy.updateconnection:UpdateConnection',
            'delete-provider = deploy.deleteprovider:DeleteProvider',
            'list-provider = deploy.listproviders:ListProviders',
            'get-aws-regions = deploy.getawsregions:GetAwsRegions',
            'delete-environment = deploy.deleteenvironment:DeleteEnv',
            'checkifenvironmentexists = deploy.checkifenvironmentexists:CheckIfEnvironmentExists',
            'download-terraform-files =deploy.downloadterraformfiles:DownloadTerraformFiles',
            'update-provider = deploy.updateprovider:UpdateProvider',
            'import-blueprint = deploy.importblueprint:ImportBlueprint',
            'import-environment = deploy.importenvironment:ImportEnvironment',
            'createnewenvresourceusingimport = deploy.createnewenvresourceusingimport:CreateNewEnvResourceUsingImport',
            'hooked = deploy.hook:Hooked',
        ],
        'rean.test.hooked': [
            'sample-hook = deploy.hook:Hook',
        ],
    },

    zip_safe=False,
)
