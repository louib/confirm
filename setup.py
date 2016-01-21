#!/usr/bin/env python
import os
from setuptools import setup

LONG_DESC = open(os.path.join(os.path.dirname(__file__), 'README.rst')).read()

setup(
      name="confirm",
      version="0.1.2",
      description="Simple Python configuration file management.",
      long_description=LONG_DESC,
      license='MIT',
      author="Louis-Bertrand Varin",
      author_email="louisbvarin@gmail.com",
      url='https://github.com/louib/confirm',
      packages=['confirm',],
      install_requires=[
          'PyYAML>=3.0',
          'colorama>=0.3',
          'click>=5.0'
      ],
      classifiers=[
          'Programming Language :: Python',
          'Development Status :: 3 - Alpha',
          'Intended Audience :: Developers',
          'Intended Audience :: System Administrators',
          'Topic :: Utilities',
          'License :: OSI Approved :: MIT License',
      ],
      entry_points = {
        'console_scripts': ['confirm = confirm.main:cli'],
      }
     )
