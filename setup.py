#!/usr/bin/env python
#
# Copyright 2009 Adam Ever-Hadani
#
#  Licensed under the Apache License, Version 2.0 (the "License"); 
#  you may not use this file except in compliance with the License. 
#  You may obtain a copy of the License at 
#  
#      http://www.apache.org/licenses/LICENSE-2.0 
#     
#  Unless required by applicable law or agreed to in writing, software 
#  distributed under the License is distributed on an "AS IS" BASIS, 
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. 
#  See the License for the specific language governing permissions and 
#  limitations under the License. 

"""Yelp API Python client installation script."""

# Basic package metadata
METADATA = dict(
    name = 'yelp-python-client',
    version  = '0.1.1',
    author   = 'Adam Ever-Hadani',
    author_email = 'adamhadani@gmail.com',
    description  = 'A python client for the Yelp API',
    license = 'Apache License 2.0',
    url = 'http://code.google.com/p/yelp-python-client/',
    keywords = 'yelp api',
    packages = ['yelp']
)

# Meta-data used specifically by setuptools if available
SETUPTOOLS_METADATA = dict(
    install_requires = ['httplib2'],

    test_suite = "test_yelp.suite"
)

# Try using setuptools if available, otherwise distutils.
try:
    import setuptools
    METADATA.update(SETUPTOOLS_METADATA)
    setuptools.setup(**METADATA)
except ImportError:
    import distutils.core
    distutils.core.setup(**METADATA)

