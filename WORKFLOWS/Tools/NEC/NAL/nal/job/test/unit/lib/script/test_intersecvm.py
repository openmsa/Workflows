import inspect
import unittest

from job.conf import config
from job.lib.script import intersecvm
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

    def test_intersec_vm_get_rsa(self):

        job_config = config.JobConfig()

        params = []
        params.append('root')
        params.append('password123')
        params.append('10.0.0.1')
        params.append('/home/user123')

        passwords = []
        passwords.append('password123')

        res = intersecvm.IntersecVmClient(job_config)\
                .intersec_vm_get_rsa(params, passwords)
        print(inspect.currentframe().f_code.co_name)
        print(res)

        # Assertion
        self.assertEqual(type(res), list)
        self.assertEqual(len(res), 2)

    def test_intersec_vm_put_rsa(self):

        job_config = config.JobConfig()

        params = []
        params.append('root')
        params.append('password123')
        params.append('10.0.0.1')
        params.append('host123')
        params.append('/home/admin/20160620035201981_id_rsa')

        passwords = []
        passwords.append('password123')

        res = intersecvm.IntersecVmClient(job_config)\
                    .intersec_vm_put_rsa(params, passwords)
        print(inspect.currentframe().f_code.co_name)
        print(res)

        # Assertion
        self.assertEqual(type(res), list)
        self.assertEqual(len(res), 0)
