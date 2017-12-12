#!/usr/bin/env python

PROJECT = 'test'

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

    description='CLI for REAN Platform with cliff',
    long_description=long_description,

    author='Rajashri Dalavi',
    author_email='rajashri.dalavi@reancloud.com',

    url='https://github.com/openstack/cliff',
    download_url='https://github.com/openstack/cliff/tarball/master',

    classifiers=['Development Status :: 3 - Alpha',
                 'License :: OSI Approved :: Apache Software License',
                 'Programming Language :: Python',
                 'Programming Language :: Python :: 2',
                 'Programming Language :: Python :: 2.7',
                 'Programming Language :: Python :: 3',
                 'Programming Language :: Python :: 3.2',
                 'Intended Audience :: Developers',
                 'Environment :: Console',
                 ],

    platforms=['Any'],

    scripts=[],

    provides=[],
    install_requires=['cliff','validators'],

    namespace_packages=[],
    packages=find_packages(),
    include_package_data=True,

    entry_points={
        'console_scripts': [
            'rp_test = test.main:main',
            'rp_deploy = test.main:main'
        ],
        'rean.platform': [
            'run-url-test = test.runurl:RunURLTest',
            'run-upa-test = test.runupa:RunUPA',
            'run-security-test = test.runsecuritytest:RunSecurityTest',
            'run-automation-test = test.runcrossbrowsertest:RunCrossBrowserTest',
            'run-scale-test =  test.runscalenowtest:RunScaleNowTest',
            'get-job-status = test.getjobstatus:GetJobStatus',
            'getproperties = test.testnowutility:GetProperties',
              'deploy_configure = deploy.configure:Configure',
            'getallvmconnections = deploy.getallvmconnections:GetALLVMConnections',
            'isconnectionexists = deploy.isconnectionexists:IsConnectionExists',
            'saveconnection = deploy.saveconnection:SaveConnection',
            'getproviderbyname = deploy.getproviderbyname:GetProviderByName',
            'checkifenvironmentexists = deploy.checkifenvironmentexists:CheckIfEnvironmentExists',
            'createnewenvresourceusingimport = deploy.createnewenvresourceusingimport:CreateNewEnvResourceUsingImport',
            'hooked = deploy.hook:Hooked',
        ],
        'rean.test.hooked': [
            'sample-hook = deploy.hook:Hook',
        ],
    },

    zip_safe=False,
)
