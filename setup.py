# Copyright (c) 2019 Gleb Orlov
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
from __future__ import absolute_import, division, print_function, unicode_literals

from setuptools import find_packages, setup

import efc

classifiers = [
    'Development Status :: 2 - Pre-Alpha',
    'Programming Language :: Python :: 2',
    'Programming Language :: Python :: 3',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
]

with open('README.md', 'r') as fp:
    long_description = fp.read()

setup(name='excel-formulas-calculator',
      version=efc.__version__,
      author='Gleb Orlov',
      author_email='orlovgb@mail.ru',
      url='https://github.com/ulalka/excel-formulas-calculator',
      packages=find_packages(),
      include_package_data=True,
      install_requires=['six'],
      extras_require={
          'openpyxl': ['openpyxl'],
      },
      tests_require=['pytest'],
      test_suite='tests',
      license='MIT',
      description='Library to calculate excel formulas',
      long_description=long_description,
      long_description_content_type='text/markdown',
      classifiers=classifiers,
      python_requires='>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*, !=3.5.*, <4',
      )
