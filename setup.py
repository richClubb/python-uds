from setuptools import setup

setup(
    # Needed to silence warnings (and to be a worthwhile package)
    name='python-uds',
    url='https://github.com/richClubb/python-uds',
    author='Richard Clubb',
    author_email='richard.clubb@embeduk.com',
    # Needed to actually package something
    packages=['python-uds'],
    # Needed for dependencies
    install_requires=['python-can'],
    # *strongly* suggested for sharing
    version='0.1',
    # The license can be anything you like
    license='MIT',
    description='A library for interfacing with UDS using python',
    # We will also need a readme eventually (there will be a warning)
    # long_description=open('README.txt').read(),
)