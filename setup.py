# -*- coding: utf-8 -*-
# Copyright (c) 2008 Ross Patterson

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program; see the file COPYING. If not, write to the
# Free Software Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.
"""
This module contains the tool of rpatterson.mailsync
"""
import os
from setuptools import setup, find_packages

version = '0.1'

README = os.path.join(
    os.path.dirname(__file__), 'rpatterson', 'mailsync', 'README.txt')

long_description = open(README).read() + '\n\n'

tests_require = [
        'zope.testing',
    ]

setup(name='rpatterson.mailsync',
      version=version,
      description="",
      long_description=long_description,
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='',
      author='Ross Patterson',
      author_email='me@rpatterson.net',
      url='http://pypi.python.org/pypi/rpatterson.mailsync',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['rpatterson'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          # -*- Extra requirements: -*-
      ],
      test_suite = "rpatterson.mailsync.tests.test_suite",
      tests_require=tests_require,
      extras_require=dict(test=tests_require),
      entry_points="""
      # -*- Entry points: -*-
      [console_scripts]
      mailsync_watch = rpatterson.mailsync.watch:main
      """,
      )

