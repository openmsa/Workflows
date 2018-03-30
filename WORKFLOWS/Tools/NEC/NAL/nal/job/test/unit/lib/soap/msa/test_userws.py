import inspect
import unittest

from job.auto.extension import routingpod
from job.lib.soap.msa import userws
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

    def get_msa_instance(self):

        job_input = {'type': 1, 'device_type': 1,
                     'operation_id': 'TestSoapUser'}

        job_instance = routingpod.RoutingPod()
        ret = job_instance.routing_pod(job_input)

        pod_id = ret['pod_id']

        msa_instance = userws.UserWs(
                            job_instance.job_config,
                            job_instance.nal_endpoint_config,
                            pod_id)

        return msa_instance

    def test_create_customer(self):

        customer_name = 'ksp'
        operator_prefix = 'AAA'

        res = self.get_msa_instance()\
                .create_customer(customer_name, operator_prefix)
        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_delete_customer_by_id(self):

        customer_id = '99'

        res = self.get_msa_instance()\
                .delete_customer_by_id(customer_id)
        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)
