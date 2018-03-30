import inspect
import unittest

from job.auto.extension import routingpod
from job.lib.soap.msa import devicews
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

        msa_instance = devicews.DeviceWs(
                            job_instance.job_config,
                            job_instance.nal_endpoint_config,
                            pod_id)

        return msa_instance

    def test_create_managed_device(self):

        customer_id = '10'
        device_name = 'dev001'
        login_user = 'usr123'
        password = 'pass123'
        admin_password = 'admin123'
        manufacture_id = 'manu100'
        model_id = 'model001'
        ip_address = '10.0.0.1'

        msa = self.get_msa_instance()
        res = msa.create_managed_device(customer_id,
                                device_name,
                                login_user,
                                password,
                                admin_password,
                                manufacture_id,
                                model_id,
                                ip_address)
        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_delete_device_by_id(self):

        device_id = '10'

        msa = self.get_msa_instance()
        res = msa.delete_device_by_id(device_id)

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_do_provisioning_by_device_id(self):

        device_id = '10'

        msa = self.get_msa_instance()
        res = msa.do_provisioning_by_device_id(device_id)

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_get_provisioning_status_by_id(self):

        device_id = '10'

        msa = self.get_msa_instance()
        res = msa.get_provisioning_status_by_id(device_id)

        print(inspect.currentframe().f_code.co_name)
        print(res)
        print(type(res['out']))
        print(type(res['out']['rawJSONResult']))

        # Assertion
        self.assertGreaterEqual(len(res), 1)
