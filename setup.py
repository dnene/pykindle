#!/usr/bin/env python

from setuptools import setup

requires = [
    "beautifulsoup4==4.2.1",
    "requests==1.2.3",
    "mechanize==0.2.5",
]

setup(name='pykindle',
      version='1.0',
      description='Python Kindle scraper',
      author='Dhananjay Nene',
      author_email='dhananjay.nene@gmail.com',
      url='http://github.com/dnene/pykindle',
      py_modules=['pykindle'],
      install_requires = requires,
     )
