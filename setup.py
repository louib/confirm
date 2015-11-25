#!/usr/bin/env python
from setuptools import setup
import os
import os.path

version = 'dev'

if os.path.exists('version'):
  version = file('version').readline()[:-1]

setup(
      name="confirm",
      version=version,
      description="Simple Python configuration file management.",
      author="Louis-Bertrand Varin",
      author_email="louisbvarin@gmail.com",
      packages=['confirm',]
     )
