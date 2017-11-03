#!/usr/bin/env python

PROJECT = 'reantest'

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
            'reanplatform = reantest.main:main'
        ],
        'rean.platform': [
            'reantest_runurl = reantest.runurl:RunURL',
            'reantest_runupa = reantest.runupa:RunUPA',
            'reantest_getproperties = reantest.testnowutility:GetProperties',
            'hooked = reantest.hook:Hooked',
        ],
        'rean.test.hooked': [
            'sample-hook = reantest.hook:Hook',
        ],
    },

    zip_safe=False,
)
