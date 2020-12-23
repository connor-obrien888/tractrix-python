# -*- coding: utf-8 -*-
"""
Created on Tue Dec 22 10:08:46 2020

@author: connor o'brien
"""

from setuptools import find_packages, setup

setup(
    name = 'tractrix',
    packages = find_packages(where="tractrix", include=['tractrix']),
    version = '0.1.3',
    description = 'A convenient implementation of the tractrix magnetopause',
    author = 'Connor OBrien',
    author_email = 'obrienco@bu.edu',
    license = 'MIT',
    url="https://github.com/connor-obrien888/tractrix",
    install_requires = ['numpy'],
        classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)