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
    python_requires='>=3.8',
    install_requires=[
        'aiohttp[speedups]==3.6.2',
        'aiopg==1.0.0',
        'pytest-aiohttp==0.3.0'
    ],
)
