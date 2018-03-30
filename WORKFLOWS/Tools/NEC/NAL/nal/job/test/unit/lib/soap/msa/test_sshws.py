import inspect
import json
import unittest

from job.auto.extension import routingpod
from job.lib.soap.msa import sshws


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

        msa_instance = sshws.SshWs(
                            job_instance.job_config,
                            job_instance.nal_endpoint_config,
                            pod_id)

        return msa_instance

    def test_create_customer(self):

        ip_address = '100.106.1.1'
        port = '22'

        res = self.get_msa_instance()\
                .confirm_ssh_status(ip_address, port)
        print(inspect.currentframe().f_code.co_name)
        print(json.dumps(res))

        # Assertion
        self.assertGreaterEqual(len(res), 1)
