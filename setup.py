#!/usr/bin/env python

from distutils.core import setup

setup(name='Spencer-Bot',
      version='2.0',
      description='Discord Bot',
      author='Anson Mansfield',
      author_email='anson.mansfield@gmail.com',
      url='https://github.com/AJMansfield/Spencer-Bot',
      packages=['spencer'],
      requires=['discord.py', 'django'],
     )