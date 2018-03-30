import inspect
import unittest

from job.conf import config
from job.lib.script import licenseauth
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

    def test_a10_vthunder_authentication(self):

        job_config = config.JobConfig()

        params = []
        params.append('aaa')
        params.append('bbb')

        passwords = []
        passwords.append('password1')
        passwords.append('password2')

        res = licenseauth.LicenseAuthClient(job_config)\
                .a10_vthunder_authentication(params, passwords)
        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertEqual(type(res), list)
        self.assertGreaterEqual(len(res), 1)

    def test_paloalto_authentication(self):

        job_config = config.JobConfig()

        params = []
        params.append('aaa')
        params.append('bbb')

        passwords = []
        passwords.append('password1')
        passwords.append('password2')

        res = licenseauth.LicenseAuthClient(job_config)\
                    .paloalto_authentication(params, passwords)
        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertEqual(type(res), list)
        self.assertGreaterEqual(len(res), 1)
