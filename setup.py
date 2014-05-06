#!/usr/bin/env python

from setuptools import setup, find_packages
LONG_DESCRIPTION = open('README.rst').read()

setup(
    name='Eve-docs',
    version='0.1.4',
    url='https://github.com/charlesflynn/eve-docs',
    author='Charles Flynn',
    author_email='git@irab.org',
    description='Generates documentation for Eve APIs',
    long_description=LONG_DESCRIPTION,
    license=open('LICENSE').read(),
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=[
        'Eve>=0.1',
        'Flask>=0.10',
        'Flask-Bootstrap>=3.0',
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)
