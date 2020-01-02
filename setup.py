#!/usr/bin/env python3

from setuptools import setup, find_packages

setup(
    name='RESTo',
    version='0.1.0',
    description='REST API for restaurants',
    author='Julien Tagneres',
    author_email='julien.tagneres@gmail.com',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    scripts=[
        'src/scripts/resto-server',
    ],
    data_files=[
        ('/etc/peopledoc-test', ['config/resto.example.ini']),
    ],
    python_requires='>=3.8',
    install_requires=['aiohttp[speedups]', 'aiopg', 'pytest-aiohttp'],
)
