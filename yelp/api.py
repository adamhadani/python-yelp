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

"""
yelp.api

Yelp API client implementation.
Currently, the three different Yelp API's
are abstracted into three different classes,
each allowing the implementation of the various
different search formalisms yelp offers.

"""

from urllib import urlencode
import logging

try:
    import json
except ImportError:
    # Pre-2.6 python compatibility
    import simplejson as json

from httplib2 import Http

__all__ = [ 
    'ReviewSearchApi', 
    'PhoneApi', 
    'NeighborhoodApi' 
]

################################################################################

class HttpApiClient(object):
    """
    Base implementation for an HTTP
    API Client. Used by the different
    API implementation objects to manage
    Http connection.
    """

    LOG = logging.getLogger("HttpApiClient")

    def __init__(self, client_key, output):
        """Initialize base http client."""
        self._conn = Http()

        # Yelp client key
        self._client_key = client_key

        # Output format ('json', 'pickle', 'php')
        self._output = output

        
    def _http_request(self, base_url, **kwargs):
        """
        Perform an HTTP Request using base_url and parameters
        given by kwargs. 
        Results are expected to be given in JSON format
        and are parsed to python data structures.
        """

        # Build our URI
        request_params = urlencode(kwargs)
        uri = u'%s?%s&ywsid=%s&output=%s' % \
            (base_url, request_params, self._client_key, self._output)

        self.LOG.debug("_http_request() - URI: %s", uri)

        header, response = self._conn.request(uri, method='GET')

        return header, response

################################################################################

class ReviewSearchApi(HttpApiClient):
    """
    Yelp Review Search API client implementation.

    for latest documentation on using this API, see:	
    @link http://www.yelp.com/developers/documentation/search_api
    """

    BASE_URL = "http://api.yelp.com/business_review_search"

    def __init__(self, client_key, output="json"):
        """Initialize class instance data and parameters."""
        HttpApiClient.__init__(self, client_key, output=output)


    def by_bounding_box(self, tl_lat, tl_long, br_lat, br_long, term=None, num_biz_requested=None, category=None):
        """
        Perform a Yelp Review Search based on a map bounding box.

        Args:
          tl_lat   - bounding box top left latitude 
          tl_long  - bounding box top left longitude  
          br_lat   - bounding box bottom right latitude
          br_long  - bounding box bottom right longitude
          term     - Search term to filter by (Optional)
          num_biz_requested - Maximum number of matching results to return (Optional)
          category - '+'-seperated list of categories to filter by. See
        http://www.yelp.com/developers/documentation/category_list
        			  for list of valid categories. (Optional)

        """

        header, content = self._http_request(
            self.BASE_URL, 
            tl_lat  = tl_lat, 
            tl_long = tl_long,
            br_lat  = br_lat, 
            br_long = br_long,
            term    = term,
            category = category,
            num_biz_requested = num_biz_requested
        )		
        return json.loads(content)


    def by_geopoint(self, lat, long, radius, term=None, num_biz_requested=None, category=None):
        """
        Perform a Yelp Review Search based on a geopoint and radius tuple.

        Args:
          lat      - geopoint latitude 
          long     - geopoint longitude  
          radius   - search radius (in miles)
          term     - Search term to filter by (Optional)
          num_biz_requested - Maximum number of matching results to return (Optional)
          category - '+'-seperated list of categories to filter by. See
        http://www.yelp.com/developers/documentation/category_list
        			  for list of valid categories. (Optional)

        """
        
        header, content = self._http_request(
            self.BASE_URL,
            lat    = lat, 
            long   = long, 
            radius = radius, 
            term   = None, 
            num_biz_requested = None
        )		
        return json.loads(content)


    def by_location(self, location, cc=None, radius=None, term=None, num_biz_requested=None, category=None):
        """
        Perform a Yelp Review Search based on a location specifier.

        Args:
          location - textual location specifier of form: "address, neighborhood, city, state or zip, optional country"
          cc       - ISO 3166-1 alpha-2 country code. (Optional)
          radius   - search radius (in miles) (Optional)
          term     - Search term to filter by (Optional)
          num_biz_requested - Maximum number of matching results to return (Optional)
          category - '+'-seperated list of categories to filter by. See
        http://www.yelp.com/developers/documentation/category_list
        			  for list of valid categories. (Optional)
        """

        header, content = self._http_request(
            self.BASE_URL, 
            location = location, 
            cc = cc,
            radius = radius,
            term = term,
            num_biz_requested = num_biz_requested
        )		
        return json.loads(content)

################################################################################

class PhoneApi(HttpApiClient):
    """
    Yelp Phone API client implementation.

    for latest documentation on using this API, see:	
    http://www.yelp.com/developers/documentation/phone_api	
    """

    BASE_URL = "http://api.yelp.com/phone_search"

    def __init__(self, client_key, output="json"):
        """Initialize class instance data and parameters."""
        HttpApiClient.__init__(self, client_key, output=output)


    def by_phone(self, phone, cc=None):
        """
        Perform a Yelp Phone API Search based on phone number given.

        Args:
          phone    - Phone number to search by
          cc       - ISO 3166-1 alpha-2 country code. (Optional)

        """

        header, content = self._http_request(self.BASE_URL, phone=phone, cc=cc)
        return json.loads(content)

################################################################################

class NeighborhoodApi(HttpApiClient):
    """
    Yelp Neighborhood API client implementation.

    for latest documentation on using this API, see:	
    http://www.yelp.com/developers/documentation/neighborhood_api
    """

    BASE_URL = "http://api.yelp.com/neighborhood_search"

    def __init__(self, client_key, output="json"):
        """Initialize class instance data and parameters."""
        HttpApiClient.__init__(self, client_key, output=output)


    def by_geopoint(self, lat, long):
        """
        Perform a Yelp Neighborhood API Search based on a geopoint.

        Args:
          lat      - geopoint latitude 
          long     - geopoint longitude  
        """

        header, content = self._http_request(self.BASE_URL, lat=lat, long=long)		
        return json.loads(content)


    def by_location(self, location, cc=None):
        """
        Perform a Yelp Neighborhood API Search based on a location specifier.

        Args:
          location - textual location specifier of form: "address, city, state or zip, optional country"
          cc       - ISO 3166-1 alpha-2 country code. (Optional)
        """

        header, content = self._http_request(self.BASE_URL, location=location, cc=cc)		
        return json.loads(content)

################################################################################

