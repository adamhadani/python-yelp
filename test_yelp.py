#!/usr/bin/env python
"""
Yelp API Python client unit test suite.
"""

import os
import sys
import logging
from pprint import pprint
import unittest

from yelp import *

################################################################################

logging.basicConfig(level=logging.WARN)

# By default expect the client key to be provided by environment.
try:
    YWSID = os.environ['YWSID']
except:
    raise SystemExit("'YWSID' was not set in environment. Yelp API requires a valid client key.")

################################################################################

class ReviewSearchApiTest(unittest.TestCase):
    """
    Unit test for the Yelp Review Search API.
    """

    def setUp(self):
        self._client = ReviewSearchApi(client_key=YWSID)

        self._test_location = "Noe Valley, San Francisco CA"
        self._test_geopoints = [
            (37.788022, -122.399797, 20)
        ]
        self._test_bbox = [
            (37.9, -122.5, 37.788022, -122.399797)
        ]


    def testByGeopoint(self):
        """Testing the Yelp Review Search API Search by geopoint"""
        for lat, long, radius in self._test_geopoints:
            ret = self._client.by_geopoint(lat=lat, long=long, radius=radius)	
            self.assert_(ret is not None, "Could not parse Review Search API results")


    def testByLocation(self):
        """Testing the Yelp Review Search API Search by location string"""
        ret = self._client.by_location(location=self._test_location)			
        self.assert_(ret is not None, "Could not parse Review Search API results")


    def testByBoundingBox(self):
        """Testing the Yelp Review Search API Search by bounding box"""
        for tl_lat, tl_long, br_lat, br_long in self._test_bbox:
            ret = self._client.by_bounding_box(tl_lat=tl_lat, tl_long=tl_long, br_lat=br_lat, br_long=br_long)			
            self.assert_(ret is not None, "Could not parse Review Search API results")


################################################################################

class PhoneApiTest(unittest.TestCase):
    """
    Unit test for the Yelp Phone API.
    """

    def setUp(self):
        self._client = PhoneApi(client_key=YWSID)


    def testByPhone(self):
        """Testing the Yelp Phone API By Phone search"""

        ret = self._client.by_phone(phone='6505833244')

        self.assert_(ret is not None, "Could not parse Phone API results")

################################################################################

class NeighborhoodApiTest(unittest.TestCase):
    """
    Unit test for the Yelp Neighborhood API.
    """

    def setUp(self):
        self._client = NeighborhoodApi(client_key=YWSID)

        self._test_location = "Noe Valley, San Francisco CA"
        self._test_geopoints = [
            (37.788022, -122.399797)
        ]

    def testByLocation(self):
        """Testing the Yelp Neighborhood API By Location string"""

        ret = self._client.by_location(location=self._test_location)			
        self.assert_(ret is not None, "Could not parse Neighborhood API results")


    def testByGeopoint(self):
        """Testing the Yelp Neighborhood API By Geocode search"""

        for lat, long in self._test_geopoints:
            ret = self._client.by_geopoint(lat=lat, long=long)	
            self.assert_(ret is not None, "Could not parse Neighborhood API results")

################################################################################

def suite():
    suite = unittest.TestSuite()
    suite.addTests(unittest.makeSuite(ReviewSearchApiTest))
    suite.addTests(unittest.makeSuite(PhoneApiTest))
    suite.addTests(unittest.makeSuite(NeighborhoodApiTest))

    return suite    

################################################################################

if __name__ == "__main__":	
    unittest.main()
