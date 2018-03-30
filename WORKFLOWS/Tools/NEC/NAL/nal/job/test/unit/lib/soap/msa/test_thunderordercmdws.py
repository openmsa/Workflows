import inspect
import json
import unittest

from job.auto.extension import routingpod
from job.lib.soap.msa import thunderordercmdws
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

        job_input = {'type': 1, 'device_type': 3,
                     'operation_id': 'TestSoapUser'}

        job_instance = routingpod.RoutingPod()
        ret = job_instance.routing_pod(job_input)

        pod_id = ret['pod_id']

        msa_instance = thunderordercmdws.ThunderOrderCommandWs(
                            job_instance.job_config,
                            job_instance.nal_endpoint_config,
                            pod_id)

        return msa_instance

    def test_create_thunder_login(self):

        device_id = 'dev001'
        object_id = 'obj001'

        res = self.get_msa_instance()\
                .create_thunder_login(device_id, object_id)
        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        message = json.loads(res['out']['message'])
        print('session_id=' + message['response']['message']['session_id'])
        print('session_id=' + json.loads(
                res['out']['message'])['response']['message']['session_id'])

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_delete_thunder_login(self):

        device_id = 'dev001'
        object_id = 'obj001'
        session_id = '644b9901bbf588f919fb5f33f66dfb'

        res = self.get_msa_instance()\
                .delete_thunder_login(device_id, object_id, session_id)
        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_create_thunder_partition(self):

        device_id = 'dev001'
        object_id = 'partition123'
        session_id = '644b9901bbf588f919fb5f33f66dfb'
        partition_id = '1'

        res = self.get_msa_instance()\
                .create_thunder_partition(
                    device_id, object_id, session_id, partition_id)
        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_delete_thunder_partition(self):

        device_id = 'dev001'
        object_id = 'partition123'
        session_id = '644b9901bbf588f919fb5f33f66dfb'

        res = self.get_msa_instance()\
                .delete_thunder_partition(device_id,
                                          object_id,
                                          session_id)
        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_create_thunder_move_partition(self):

        device_id = 'dev001'
        object_id = 'partition123'
        session_id = '644b9901bbf588f919fb5f33f66dfb'

        res = self.get_msa_instance()\
                .create_thunder_move_partition(device_id,
                                          object_id,
                                          session_id)
        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_delete_thunder_move_partition(self):

        device_id = 'dev001'
        object_id = '1'
        session_id = '644b9901bbf588f919fb5f33f66dfb'

        res = self.get_msa_instance()\
                .delete_thunder_move_partition(device_id, object_id,
                                               session_id)
        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_create_thunder_vlan(self):

        device_id = 'dev001'
        object_id = '1000'
        session_id = '644b9901bbf588f919fb5f33f66dfb'
        port_number = '80'

        res = self.get_msa_instance()\
                .create_thunder_vlan(device_id,
                                            object_id,
                                            session_id,
                                            port_number)
        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_delete_thunder_vlan(self):

        device_id = 'dev001'
        object_id = '1000'
        session_id = '644b9901bbf588f919fb5f33f66dfb'

        res = self.get_msa_instance()\
                .delete_thunder_vlan(device_id,
                                            object_id,
                                            session_id)
        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_create_thunder_set_ip(self):

        device_id = 'dev001'
        object_id = '192.168.0.1'
        session_id = '644b9901bbf588f919fb5f33f66dfb'
        subnet_mask = '255.255.255.0'
        vlan_id = '1000'

        res = self.get_msa_instance()\
                .create_thunder_set_ip(device_id,
                                            object_id,
                                            session_id,
                                            subnet_mask,
                                            vlan_id)
        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_delete_thunder_set_ip(self):

        device_id = 'dev001'
        object_id = '192.168.0.1'
        session_id = '644b9901bbf588f919fb5f33f66dfb'
        vlan_id = '1000'

        res = self.get_msa_instance()\
                .delete_thunder_set_ip(device_id,
                                            object_id,
                                            session_id,
                                            vlan_id)
        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_create_thunder_save(self):

        device_id = 'dev001'
        object_id = '644b9901bbf588f919fb5f33f66dfb'

        res = self.get_msa_instance()\
                .create_thunder_save(device_id, object_id)
        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_delete_thunder_save(self):

        device_id = 'dev001'
        object_id = '644b9901bbf588f919fb5f33f66dfb'

        res = self.get_msa_instance()\
                .delete_thunder_save(device_id, object_id)
        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_create_thunder_vrrp(self):

        device_id = 'dev001'
        object_id = '10.0.0.1'
        session_id = '644b9901bbf588f919fb5f33f66dfb'
        enable_password = 'pass123'
        preempt_mode = 'enable'
        vrid = '31'
        vrrp_priority = '1'

        res = self.get_msa_instance()\
                .create_thunder_vrrp(device_id,
                                            object_id,
                                            session_id,
                                            enable_password,
                                            preempt_mode,
                                            vrid,
                                            vrrp_priority)
        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_delete_thunder_vrrp(self):

        device_id = 'dev001'
        object_id = '10.0.0.1'
        session_id = '644b9901bbf588f919fb5f33f66dfb'

        res = self.get_msa_instance()\
                .delete_thunder_vrrp(device_id, object_id, session_id)
        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_create_thunder_manage(self):

        device_id = 'dev001'
        object_id = '1000'
        enable_password = 'pass123'
        session_id = '644b9901bbf588f919fb5f33f66dfb'

        res = self.get_msa_instance()\
                .create_thunder_manage(device_id,
                                            object_id,
                                            enable_password,
                                            session_id)
        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_create_thunder_static_route(self):

        device_id = 'dev001'
        object_id = '10.0.0.1'
        session_id = '644b9901bbf588f919fb5f33f66dfb'
        gateway = '192.168.0.1'
        subnet_mask = '255.255.255.0'
        port_number = '2016'

        res = self.get_msa_instance()\
                .create_thunder_static_route(device_id, object_id,
                                                gateway,
                                                session_id,
                                                subnet_mask,
                                                port_number)
        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_delete_thunder_static_route(self):

        device_id = 'dev001'
        object_id = '10.0.0.1'
        session_id = '644b9901bbf588f919fb5f33f66dfb'
        gateway = '192.168.0.1'
        subnet_mask = '255.255.255.0'
        port_number = '2016'

        res = self.get_msa_instance()\
                .delete_thunder_static_route(device_id, object_id,
                                                gateway,
                                                session_id,
                                                subnet_mask,
                                                port_number)
        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_create_thunder_user(self):

        device_id = 'dev001'
        object_id = 'admin123'
        session_id = '644b9901bbf588f919fb5f33f66dfb'
        partition_name = 'partition123'
        password = 'password123'
        role_name = 'partition-write'

        res = self.get_msa_instance()\
                .create_thunder_user(device_id,
                                            object_id,
                                            session_id,
                                            partition_name,
                                            password,
                                            role_name)

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_delete_thunder_user(self):

        device_id = 'dev001'
        object_id = 'admin123'
        session_id = '644b9901bbf588f919fb5f33f66dfb'

        res = self.get_msa_instance()\
                .delete_thunder_user(device_id, object_id, session_id)

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_create_thunder_api_set_ipv6(self):

        device_id = 'dev001'
        object_id = 'admin123'
        session_id = '644b9901bbf588f919fb5f33f66dfb'
        ipv6_address = '2001:db5::1'
        ipv6_prefix_length = '48'

        res = self.get_msa_instance()\
                .create_thunder_api_set_ipv6(device_id, object_id,
                                                ipv6_address,
                                                ipv6_prefix_length,
                                                session_id)

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_delete_thunder_api_set_ipv6(self):

        device_id = 'dev001'
        object_id = 'admin123'
        session_id = '644b9901bbf588f919fb5f33f66dfb'

        res = self.get_msa_instance()\
                .delete_thunder_api_set_ipv6(device_id, object_id, session_id)

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_create_thunder_api_vrrpv6(self):

        device_id = 'dev001'
        object_id = 'admin123'
        enable_password = '2001:db5::1'
        session_id = '644b9901bbf588f919fb5f33f66dfb'
        preempt_mode = 'disable'
        vrid = '1'
        vrrp_priority = '1'

        res = self.get_msa_instance()\
                .create_thunder_api_vrrpv6(device_id, object_id,
                                                   enable_password,
                                                   session_id,
                                                   preempt_mode,
                                                   vrid,
                                                   vrrp_priority)

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_delete_thunder_api_vrrpv6(self):

        device_id = 'dev001'
        object_id = 'admin123'
        session_id = '644b9901bbf588f919fb5f33f66dfb'

        res = self.get_msa_instance()\
                .delete_thunder_api_vrrpv6(device_id, object_id, session_id)

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_create_thunder_api_static_routev6(self):

        device_id = 'dev001'
        object_id = '::'
        gateway = '2001:db5::1'
        session_id = '644b9901bbf588f919fb5f33f66dfb'
        vlan_id = '2016'
        prefix = '0'

        res = self.get_msa_instance()\
                .create_thunder_api_static_routev6(device_id, object_id,
                                                        gateway,
                                                        session_id,
                                                        vlan_id,
                                                        prefix)

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_delete_thunder_api_static_routev6(self):

        device_id = 'dev001'
        object_id = '::'
        gateway = '2001:db5::1'
        session_id = '644b9901bbf588f919fb5f33f66dfb'
        prefix = '0'

        res = self.get_msa_instance()\
                .delete_thunder_api_static_routev6(device_id, object_id,
                                                        gateway,
                                                        session_id,
                                                        prefix)

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)
