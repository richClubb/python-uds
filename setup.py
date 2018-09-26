#!/usr/bin/env python

__author__ = "Richard Clubb"
__copyrights__ = "Copyright 2018, the python-uds project"
__credits__ = ["Richard Clubb"]

__license__ = "MIT"
__maintainer__ = "Richard Clubb"
__email__ = "richard.clubb@embeduk.com"
__status__ = "Development"


from setuptools import setup


with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    # Needed to silence warnings (and to be a worthwhile package)
    name='python-uds',
    url='https://github.com/richClubb/python-uds',
    author='Richard Clubb',
    author_email='richard.clubb@embeduk.com',
    # Needed to actually package something
    packages=['uds'],
    # Needed for dependencies
    install_requires=['python-can'],
    # *strongly* suggested for sharing
    version='0.1.2',
    # The license can be anything you like
    license='MIT',
    description='A library for interfacing with UDS using python',
    # We will also need a readme eventually (there will be a warning)
    # long_description=open('README.txt').read(),
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "Operating System :: OS Independent"
    ],
    include_package_data=True
)
