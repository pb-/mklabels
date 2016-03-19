#!/usr/bin/env python
from setuptools import setup, find_packages

setup(
    name='mklabels',
    version='0.0.0',
    description='Generate a printable PDF sheet of labels with cutting guides',
    author='Paul Baecher',
    author_email='pbaecher@gmail.com',
    url='https://github.com/pb-/mklabels',
    packages=find_packages('.'),
    license='GPLv3',
    install_requires=[
    ],
    entry_points={
        'console_scripts': [
            'mklabels = mklabels.main:run',
        ],
    },
)
