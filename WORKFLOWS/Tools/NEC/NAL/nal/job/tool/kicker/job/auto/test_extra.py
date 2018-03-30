import json
import os
import sys
import unittest
import urllib.error
import urllib.request
import urllib.parse

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../../../../')
from job.auto import base
from pprint import pprint


class TestSelectAPI(unittest.TestCase):
    # Do a test of Select.

    ID = 0

    def setUp(self):

        # Establish a clean test environment.
        super(TestSelectAPI, self).setUp()

        # Insert test data
        self.create_fixtures()

    def tearDown(self):
        """Clear the test environment"""
        super(TestSelectAPI, self).tearDown()
        self.destroy_fixtures()

    def create_fixtures(self):

        pass

    def destroy_fixtures(self):

        pass

    def test_get_config(self):

        res = base.JobAutoBase().get_config('nal_ep')
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_device_type_to_name(self):

        res = base.JobAutoBase().devicet_type_to_name('1', '1', '9')
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)
