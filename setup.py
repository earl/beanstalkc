#!/usr/bin/env python
import os
from setuptools import setup
from beanstalkc import __version__ as version

pkg_version = version
git_version = os.popen('git describe --tags --abbrev=6').read().strip()[7:]
if git_version:
    pkg_version += '.dev' + git_version

setup(
    name='beanstalkc',
    version=pkg_version,
    py_modules=['beanstalkc'],

    author='Andreas Bolka',
    author_email='a@bolka.at',
    description='A simple beanstalkd client library',
    long_description='''
beanstalkc is a simple beanstalkd client library for Python. `beanstalkd
<http://kr.github.com/beanstalkd/>`_ is a fast, distributed, in-memory
workqueue service.
''',
    url='http://github.com/earl/beanstalkc',
    license='Apache License, Version 2.0',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
