#!/usr/bin/env python
from setuptools import setup
setup(
    name='beanstalkc',
    version='0.1.0',
    py_modules=['beanstalkc'],

    author='Andreas Bolka',
    author_email='a@bolka.at',
    description='A simple beanstalkd client library',
    long_description='''
beanstalkc is a simple beanstalkd client library for Python. `beanstalkd
<http://xph.us/software/beanstalkd/>`_ is a fast, distributed, in-memory
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
