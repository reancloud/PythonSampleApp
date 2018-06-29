""" Setup of REAN Platform CLI."""
#   !/usr/bin/env python
from setuptools import setup, find_packages

PROJECT = 'REANPlatform'

#   Change docs/sphinx/conf.py too!
VERSION = '0.1'

try:
    LONG_DESCRIPTION = open('README.rst', 'rt').read()
except IOError:
    LONG_DESCRIPTION = ''

setup(
    name=PROJECT,
    version=VERSION,
    description='CLI for REAN Platform',
    long_description=LONG_DESCRIPTION,
    url='https://github.com/reancloud/',
    download_url='https://github.com/reancloud/deploy_sdk_client',
    classifiers=['Development Status :: 3 - Alpha', \
                'License :: OSI Approved :: Apache Software License', \
                'Programming Language :: Python', \
                'Programming Language :: Python :: 3', \
                'Programming Language :: Python :: 3.2', \
                'Programming Language :: Python :: 3.5.1', \
                'Programming Language :: Python :: 3.5.5', \
                'Programming Language :: Python :: 3.6', \
                'Intended Audience :: Developers', \
                'Environment :: Console'], \

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
            'rean-deploy = deploy.main:main'
        ],
        'rean.platform': [
            'configure = reanplatform.configure:Configure',
            'rean-deploy = reanplatform.reanhelp:Helpdeploy',
            'rean-test = reanplatform.reanhelp:Helptest',
            'rean-mnc = reanplatform.reanhelp:Helpmnc'
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
    },

    zip_safe=False,
)
