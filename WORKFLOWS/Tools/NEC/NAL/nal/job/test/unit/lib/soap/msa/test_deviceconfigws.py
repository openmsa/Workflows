import inspect
import unittest

from job.auto.extension import routingpod
from job.lib.soap.msa import deviceconfigws
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

        msa_instance = deviceconfigws.DeviceConfigurationWs(
                            job_instance.job_config,
                            job_instance.nal_endpoint_config,
                            pod_id)

        return msa_instance

    def test_create_managed_device(self):

        device_id = '10'
        object_file = \
        '/CommandDefinition/FORTINET/Generic/FortiVdomProvPNF.xml'

        msa = self.get_msa_instance()
        res = msa.attach_files_to_device(device_id, object_file)

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_detach_files_from_device(self):

        device_id = '10'
        object_file = \
        '/CommandDefinition/FORTINET/Generic/FortiVdomProvPNF.xml'

        msa = self.get_msa_instance()
        res = msa.detach_files_from_device(device_id, object_file)

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)
