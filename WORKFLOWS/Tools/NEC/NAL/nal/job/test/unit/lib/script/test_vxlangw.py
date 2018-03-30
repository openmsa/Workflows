import inspect
import re
import unittest

from job.conf import config
from job.lib.script import vxlangw
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

    def test_create_vxlan_gw(self):

        job_config = config.JobConfig()

        params = []
        params.append('aaa')
        params.append('password1')
        params.append('password2')
        params.append('bbb')

        passwords = []
        passwords.append('password1')
        passwords.append('password2')

        res = vxlangw.VxlanGwClient(job_config)\
                .create_vxlan_gw(params, passwords)
        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertEqual(type(res), list)
        self.assertGreaterEqual(len(res), 1)

        rule_id = ''
        pattern = re.compile('\|\s+id\s+\|\s+(.*)\s+\|')
        for vxlan_gw in res:
            matchOB = pattern.match(vxlan_gw)
            if matchOB:
                print(vxlan_gw)
                rule_id = matchOB.group(1)
                break

        print(rule_id)

        # Assertion
        self.assertGreaterEqual(len(rule_id), 1)

    def test_delete_vxlan_gw(self):

        job_config = config.JobConfig()

        params = []
        params.append('aaa')
        params.append('password1')
        params.append('password2')
        params.append('bbb')

        passwords = []
        passwords.append('password1')
        passwords.append('password2')

        res = vxlangw.VxlanGwClient(job_config)\
                    .delete_vxlan_gw(params, passwords)
        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertEqual(type(res), list)
        self.assertGreaterEqual(len(res), 1)
