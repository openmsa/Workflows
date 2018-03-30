import json
import os
import sys
import unittest
import urllib.error
import urllib.request
import urllib.parse

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../../../../')
from job.auto import method
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
#         url = 'http://localhost:8081/index.py/global-ip-addresses'
#         params = {'delete_flg': 0,
#                   'create_id': 'test_create_id'}
#
#         query = ''
#         for key in params:
#             if len(query) > 0:
#                 query += '&'
#             else:
#                 query = '?'
#             query += key + '=' + str(params[key])
#
#         url += query
#
#         res = urllib.request.urlopen(url)
#
#         res_data = res.read().decode('utf-8')
#         res_data = json.loads(res_data)
#
#         # Check Status Code
#         self.assertEqual(res.status, 200)

    def destroy_fixtures(self):

        pass

    def test_routing_pod(self):

        job_input = {
            'IaaS_region_id': 'IaaS_region_id_001',
            'IaaS_tenant_id': 'IaaS_tenant_id_001',
            'type': 1,
            'device_type': 3,
        }

        res = method.JobAutoMethod().routing_pod(job_input)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_routing_vxlangw_pod(self):

        job_input = {
            'IaaS_region_id': 'f5892461-fdb1-4f3f-bfdc-aaaaaaaaaaaa',
            'IaaS_tenant_id': 'IaaS_tenant_id_001',
            'type': 1,
            'device_type': 3,
        }

        res = method.JobAutoMethod().routing_vxlangw_pod(job_input)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)
