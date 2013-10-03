#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name='Eve-docs',
    version='0.1.0',
    url='https://github.com/charlesflynn/eve-docs',
    author='Charles Flynn',
    description='Generates documentation for Eve APIs',
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=[
        'Eve>=0.1',
        'Flask>=0.10',
        'Flask-Bootstrap>=3.0',
    ]
)
