import inspect
import unittest

from job.conf import config
from job.lib.script import zerotouch
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

    def test_a10_vthunder_provisioning(self):

        job_config = config.JobConfig()

        params = []
        params.append('aaa')
        params.append('password1')
        params.append('password2')
        params.append('bbb')

        passwords = []
        passwords.append('password1')
        passwords.append('password2')

        res = zerotouch.ZeroTouchClient(job_config)\
                .a10_vthunder_provisioning(params, passwords)
        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertEqual(type(res), list)
        self.assertGreaterEqual(len(res), 1)

    def test_bigip_provisioning(self):

        job_config = config.JobConfig()

        params = []
        params.append('aaa')
        params.append('password1')
        params.append('password2')
        params.append('bbb')

        passwords = []
        passwords.append('password1')
        passwords.append('password2')

        res = zerotouch.ZeroTouchClient(job_config)\
                    .bigip_provisioning(params, passwords)
        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertEqual(type(res), list)
        self.assertGreaterEqual(len(res), 1)

    def test_fortivm_provisioning(self):

        job_config = config.JobConfig()

        params = []
        params.append('aaa')
        params.append('password1')
        params.append('password2')
        params.append('bbb')

        passwords = []
        passwords.append('password1')
        passwords.append('password2')

        res = zerotouch.ZeroTouchClient(job_config)\
                    .fortivm_provisioning(params, passwords)
        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertEqual(type(res), list)
        self.assertGreaterEqual(len(res), 1)

    def test_paloalto_provisioning(self):

        job_config = config.JobConfig()

        params = []
        params.append('aaa')
        params.append('password1')
        params.append('password2')
        params.append('bbb')

        passwords = []
        passwords.append('password1')
        passwords.append('password2')

        res = zerotouch.ZeroTouchClient(job_config)\
                    .paloalto_provisioning(params, passwords)
        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertEqual(type(res), list)
        self.assertGreaterEqual(len(res), 1)

    def test_vsrx_ff_provisioning(self):

        job_config = config.JobConfig()

        params = []
        params.append('aaa')
        params.append('password1')
        params.append('password2')
        params.append('bbb')

        passwords = []
        passwords.append('password1')
        passwords.append('password2')

        res = zerotouch.ZeroTouchClient(job_config)\
                    .vsrx_ff_provisioning(params, passwords)
        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertEqual(type(res), list)
        self.assertGreaterEqual(len(res), 1)
