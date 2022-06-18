#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from distutils.core import setup

setup(name='jfuzz',
      version='0.1.0',
      description='CLI CAN fuzzing tool',
      author='winds0r',
      author_email='w.nds0r@protonmail.com',
      url='https://github.com/spiral-sec/jfuzz',
      packages=['python-can', 'cantools'],
     )
