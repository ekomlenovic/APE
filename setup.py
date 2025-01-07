"""
This file is used to install the package.
"""
from setuptools import setup, find_packages

setup(
    name='ape',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'nicegui',
        ''

    ],
    entry_points={
        'console_scripts': [
            'main=ape.__main__:main'
        ],
    },
)
