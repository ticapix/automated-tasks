#!/usr/bin/env python3

from distutils.core import setup
import py2exe

setup(name='erdf_comptage',
    version='1.0',
    description='parse extract.zip and generate xls files',
    author='Pierre Gronlier',
    author_email='ticapix@gmail.com',
    url='https://www.python.org/sigs/distutils-sig/',
#    packages=['xlwt'],
    console=['erdf_extract/main.py']
    )
