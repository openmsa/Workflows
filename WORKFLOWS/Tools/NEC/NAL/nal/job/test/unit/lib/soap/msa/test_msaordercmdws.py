import inspect
import unittest

from job.auto.extension import routingpod
from job.lib.soap.msa import msaordercmdws
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

        msa_instance = msaordercmdws.MsaOrderCommandWs(
                            job_instance.job_config,
                            job_instance.nal_endpoint_config,
                            pod_id)

        return msa_instance

    def test_create_msa_network_vlan(self):

        device_id = '10'
#         vlan_name = 'vlan123'
        vlan_id = 1020
        ip_address = '10.0.0.1'
        netmask = '255.255.255.0'

        msa = self.get_msa_instance()
        res = msa.create_msa_network_vlan(
                                        device_id,
#                                         vlan_name,
                                        vlan_id,
                                        ip_address,
                                        netmask
                                        )
        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_delete_msa_network_vlan(self):

        device_id = '10'
        vlan_name = 'vlan123'

        msa = self.get_msa_instance()
        res = msa.delete_msa_network_vlan(
                                        device_id,
                                        vlan_name
                                        )
        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)
