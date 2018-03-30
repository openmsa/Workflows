import inspect
import unittest

from job.auto.extension import routingpod
from job.lib.soap.msa import ciscocsrstdiosxeordercmdws
from pprint import pprint


class TestCsrStdIosXeOrderCommandWs(unittest.TestCase):
    # Do a test of Select.

    ID = 0

    def setUp(self):

        # Establish a clean test environment.
        super(TestCsrStdIosXeOrderCommandWs, self).setUp()

        # Insert test data
        self.create_csr1000v_fixtures()

    def tearDown(self):
        """Clear the test environment"""
        super(TestCsrStdIosXeOrderCommandWs, self).tearDown()
        self.destroy_fixtures()

    def create_csr1000v_fixtures(self):

        pass

    def destroy_fixtures(self):

        pass

    def get_msa_instance(self):

        job_input = {'type': 3, 'device_type': 2,
                     'operation_id': 'TestSoapUser'}

        job_instance = routingpod.RoutingPod()
        ret = job_instance.routing_pod(job_input)

        pod_id = ret['pod_id']
        dc_id = 'dc02'

        msa_instance = ciscocsrstdiosxeordercmdws.\
                        CsrStdIosXeOrderCommandWs(
                            job_instance.job_config,
                            job_instance.nal_endpoint_config,
                            pod_id, dc_id)

        return msa_instance

    def test_create_csr1000v_system_common_ipv6(self):

        device_id = 'dev001'
        object_id = 'host001'
        option_params = {'timezone': 'JST 9 0'}

        msa = self.get_msa_instance()
        print(msa.OBJECT_FILE_NAME['create_csr1000v_system_common_ipv6'])
        res = msa.create_csr1000v_system_common_ipv6(device_id, object_id,
                                            option_params)

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_update_csr1000v_system_common_ipv6(self):

        device_id = 'dev001'
        object_id = 'host001'
        option_params = {'timezone': 'JST 9 0'}

        msa = self.get_msa_instance()
        res = msa.update_csr1000v_system_common_ipv6(device_id, object_id,
                                            option_params)

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_delete_csr1000v_system_common_ipv6(self):

        device_id = 'dev001'
        object_id = 'host001'

        msa = self.get_msa_instance()
        res = msa.delete_csr1000v_system_common_ipv6(device_id, object_id)

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_create_csr1000v_bgp_basic_ipv4(self):

        device_id = 'dev001'
        object_id = 'host001'
        option_params = {
            'ip_address': '10.0.0.1',
            'local_preference': 200,
        }

        msa = self.get_msa_instance()
        res = msa.create_csr1000v_bgp_basic_ipv4(device_id, object_id,
                                            option_params)

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_update_csr1000v_bgp_basic_ipv4(self):

        device_id = 'dev001'
        object_id = 'host001'
        option_params = {
            'ip_address': '10.0.0.1',
            'local_preference': 200,
        }

        msa = self.get_msa_instance()
        res = msa.update_csr1000v_bgp_basic_ipv4(device_id, object_id,
                                            option_params)

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_delete_csr1000v_bgp_basic_ipv4(self):

        device_id = 'dev001'
        object_id = 'host001'

        msa = self.get_msa_instance()
        res = msa.delete_csr1000v_bgp_basic_ipv4(device_id, object_id)

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_create_csr1000v_bgp_basic_ipv6(self):

        device_id = 'dev001'
        object_id = 'host001'
        option_params = {
            'local_preference': 200,
        }

        msa = self.get_msa_instance()
        res = msa.create_csr1000v_bgp_basic_ipv6(device_id, object_id,
                                            option_params)

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_update_csr1000v_bgp_basic_ipv6(self):

        device_id = 'dev001'
        object_id = 'host001'
        option_params = {
            'local_preference': 200,
        }

        msa = self.get_msa_instance()
        res = msa.update_csr1000v_bgp_basic_ipv6(device_id, object_id,
                                            option_params)

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_delete_csr1000v_bgp_basic_ipv6(self):

        device_id = 'dev001'
        object_id = 'host001'

        msa = self.get_msa_instance()
        res = msa.delete_csr1000v_bgp_basic_ipv6(device_id, object_id)

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_create_csr1000v_loopback_interface(self):

        device_id = 'dev001'
        object_id = 'GigabitEthernet3'

        option_params = {
            'ip_address': '10.0.0.1',
            'netmask': '255.255.255.0',
            'segment': '192.168.0.1',
            'netmask_cidr': 24,
        }

        msa = self.get_msa_instance()
        res = msa.create_csr1000v_loopback_interface(device_id, object_id,
                                            option_params)

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_update_csr1000v_loopback_interface(self):

        device_id = 'dev001'
        object_id = 'GigabitEthernet3'

        option_params = {
            'ip_address': '10.0.0.1',
            'netmask': '255.255.255.0',
            'segment': '192.168.0.1',
            'netmask_cidr': 24,
        }

        msa = self.get_msa_instance()
        res = msa.update_csr1000v_loopback_interface(device_id, object_id,
                                            option_params)

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_delete_csr1000v_loopback_interface(self):

        device_id = 'dev001'
        object_id = 'GigabitEthernet3'

        option_params = {
            'ip_address': '10.0.0.1',
            'segment': '192.168.0.1',
            'netmask_cidr': 24,
        }

        msa = self.get_msa_instance()
        res = msa.delete_csr1000v_loopback_interface(device_id, object_id,
                                            option_params)

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_create_csr1000v_lan_interface_ipv4(self):

        device_id = 'dev001'
        object_id = 'GigabitEthernet3'

        option_params = {
            'ip_address': '10.0.0.1',
            'netmask': '255.255.255.0',
            'hsrp_ip_address': '10.0.0.2',
            'segment': '192.168.0.1',
            'netmask_cidr': 24,
        }

        msa = self.get_msa_instance()
        res = msa.create_csr1000v_lan_interface_ipv4(device_id, object_id,
                                            option_params)

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_update_csr1000v_lan_interface_ipv4(self):

        device_id = 'dev001'
        object_id = 'GigabitEthernet3'

        option_params = {
            'ip_address': '10.0.0.1',
            'netmask': '255.255.255.0',
            'hsrp_ip_address': '10.0.0.2',
            'segment': '192.168.0.1',
            'netmask_cidr': 24,
        }

        msa = self.get_msa_instance()
        res = msa.update_csr1000v_lan_interface_ipv4(device_id, object_id,
                                            option_params)

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_delete_csr1000v_lan_interface_ipv4(self):

        device_id = 'dev001'
        object_id = 'GigabitEthernet3'

        option_params = {
            'ip_address': '10.0.0.1',
            'hsrp_ip_address': '10.0.0.2',
            'segment': '192.168.0.1',
            'netmask_cidr': 24,
        }

        msa = self.get_msa_instance()
        res = msa.delete_csr1000v_lan_interface_ipv4(device_id, object_id,
                                            option_params)

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_create_csr1000v_lan_interface_ipv6(self):

        device_id = 'dev001'
        object_id = 'GigabitEthernet3'

        option_params = {
            'ipv6_address': 'dea:beaf::1',
            'prefix': 48,
            'hsrp_ipv6_address': 'dea:beaf::2',
            'segment': 'dead:beef::',
        }

        msa = self.get_msa_instance()
        res = msa.create_csr1000v_lan_interface_ipv6(device_id, object_id,
                                            option_params)

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_update_csr1000v_lan_interface_ipv6(self):

        device_id = 'dev001'
        object_id = 'GigabitEthernet3'

        option_params = {
            'ipv6_address': 'dea:beaf::1',
            'prefix': 48,
            'hsrp_ipv6_address': 'dea:beaf::2',
            'segment': 'dead:beef::',
        }

        msa = self.get_msa_instance()
        res = msa.update_csr1000v_lan_interface_ipv6(device_id, object_id,
                                            option_params)

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_delete_csr1000v_lan_interface_ipv6(self):

        device_id = 'dev001'
        object_id = 'GigabitEthernet3'

        option_params = {
            'ipv6_address': 'dea:beaf::1',
            'prefix': 48,
            'hsrp_ipv6_address': 'dea:beaf::2',
            'segment': 'dead:beef::',
        }

        msa = self.get_msa_instance()
        res = msa.delete_csr1000v_lan_interface_ipv6(device_id, object_id,
                                            option_params)

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_create_csr1000v_hsrp_primary_ipv4(self):

        device_id = 'dev001'
        object_id = 'GigabitEthernet3'

        option_params = {
            'ip_address': '10.0.0.1',
            'priority': '120',
            'group_id': 4095,
            'authkey': 'tenant001',
        }

        msa = self.get_msa_instance()
        res = msa.create_csr1000v_hsrp_primary_ipv4(device_id, object_id,
                                            option_params)

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_update_csr1000v_hsrp_primary_ipv4(self):

        device_id = 'dev001'
        object_id = 'GigabitEthernet3'

        option_params = {
            'ip_address': '10.0.0.1',
            'priority': '120',
            'group_id': 4095,
            'authkey': 'tenant001',
        }

        msa = self.get_msa_instance()
        res = msa.update_csr1000v_hsrp_primary_ipv4(device_id, object_id,
                                            option_params)

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_delete_csr1000v_hsrp_primary_ipv4(self):

        device_id = 'dev001'
        object_id = 'GigabitEthernet3'

        option_params = {
            'ip_address': '10.0.0.1',
            'group_id': 4095,
        }

        msa = self.get_msa_instance()
        res = msa.delete_csr1000v_hsrp_primary_ipv4(device_id, object_id,
                                            option_params)

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_create_csr1000v_hsrp_primary_ipv6(self):

        device_id = 'dev001'
        object_id = 'GigabitEthernet3'

        option_params = {
            'ipv6_address': 'dea:beaf::1',
            'priority': '120',
            'group_id': 4095,
            'authkey': 'tenant001',
        }

        msa = self.get_msa_instance()
        res = msa.create_csr1000v_hsrp_primary_ipv6(device_id, object_id,
                                            option_params)

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_update_csr1000v_hsrp_primary_ipv6(self):

        device_id = 'dev001'
        object_id = 'GigabitEthernet3'

        option_params = {
            'ipv6_address': 'dea:beaf::1',
            'priority': '120',
            'group_id': 4095,
            'authkey': 'tenant001',
        }

        msa = self.get_msa_instance()
        res = msa.update_csr1000v_hsrp_primary_ipv6(device_id, object_id,
                                            option_params)

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_delete_csr1000v_hsrp_primary_ipv6(self):

        device_id = 'dev001'
        object_id = 'GigabitEthernet3'

        option_params = {
            'ipv6_address': 'dea:beaf::1',
            'group_id': 4095,
        }

        msa = self.get_msa_instance()
        res = msa.delete_csr1000v_hsrp_primary_ipv6(device_id, object_id,
                                            option_params)

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_create_csr1000v_hsrp_secondary_ipv4(self):

        device_id = 'dev001'
        object_id = 'GigabitEthernet3'

        option_params = {
            'ip_address': '10.0.0.1',
            'priority': '115',
            'group_id': 4095,
            'authkey': 'tenant001',
        }

        msa = self.get_msa_instance()
        res = msa.create_csr1000v_hsrp_secondary_ipv4(device_id, object_id,
                                            option_params)

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_update_csr1000v_hsrp_secondary_ipv4(self):

        device_id = 'dev001'
        object_id = 'GigabitEthernet3'

        option_params = {
            'ip_address': '10.0.0.1',
            'priority': '115',
            'group_id': 4095,
            'authkey': 'tenant001',
        }

        msa = self.get_msa_instance()
        res = msa.update_csr1000v_hsrp_secondary_ipv4(device_id, object_id,
                                            option_params)

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_delete_csr1000v_hsrp_secondary_ipv4(self):

        device_id = 'dev001'
        object_id = 'GigabitEthernet3'

        option_params = {
            'ip_address': '10.0.0.1',
            'group_id': 4095,
        }

        msa = self.get_msa_instance()
        res = msa.delete_csr1000v_hsrp_secondary_ipv4(device_id, object_id,
                                            option_params)

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_create_csr1000v_hsrp_secondary_ipv6(self):

        device_id = 'dev001'
        object_id = 'GigabitEthernet3'

        option_params = {
            'ipv6_address': 'dea:beaf::1',
            'priority': '115',
            'group_id': 4095,
            'authkey': 'tenant001',
        }

        msa = self.get_msa_instance()
        res = msa.create_csr1000v_hsrp_secondary_ipv6(device_id, object_id,
                                            option_params)

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_update_csr1000v_hsrp_secondary_ipv6(self):

        device_id = 'dev001'
        object_id = 'GigabitEthernet3'

        option_params = {
            'ipv6_address': 'dea:beaf::1',
            'priority': '115',
            'group_id': 4095,
            'authkey': 'tenant001',
        }

        msa = self.get_msa_instance()
        res = msa.update_csr1000v_hsrp_secondary_ipv6(device_id, object_id,
                                            option_params)

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_delete_csr1000v_hsrp_secondary_ipv6(self):

        device_id = 'dev001'
        object_id = 'GigabitEthernet3'

        option_params = {
            'ipv6_address': 'dea:beaf::1',
            'group_id': 4095,
        }

        msa = self.get_msa_instance()
        res = msa.delete_csr1000v_hsrp_secondary_ipv6(device_id, object_id,
                                            option_params)

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

    def test_create_csr1000v_hsrp_interface_tracking(self):

        device_id = 'dev001'
        object_id = 'GigabitEthernet3_track_GigabitEthernet4'

        option_params = {
            'interface': 'GigabitEthernet3',
            'group_id': '1',
            'track_interface': 'GigabitEthernet3',
            'prioritycost': 10,
            'track_id': 1000,
        }

        msa = self.get_msa_instance()
        res = msa.create_csr1000v_hsrp_interface_tracking(device_id, object_id,
                                            option_params)

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_update_csr1000v_hsrp_interface_tracking(self):

        device_id = 'dev001'
        object_id = 'GigabitEthernet3_track_GigabitEthernet4'

        option_params = {
            'interface': 'GigabitEthernet3',
            'group_id': '1',
            'track_interface': 'GigabitEthernet3',
            'prioritycost': 10,
            'track_id': 1000,
        }

        msa = self.get_msa_instance()
        res = msa.update_csr1000v_hsrp_interface_tracking(device_id, object_id,
                                            option_params)

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_delete_csr1000v_hsrp_interface_tracking(self):

        device_id = 'dev001'
        object_id = 'GigabitEthernet3_track_GigabitEthernet4'

        option_params = {
            'interface': 'GigabitEthernet3',
            'group_id': '1',
            'track_id': 1000,
        }

        msa = self.get_msa_instance()
        res = msa.delete_csr1000v_hsrp_interface_tracking(device_id, object_id,
                                            option_params)

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_create_csr1000v_default_route_ipv4(self):

        device_id = 'dev001'
        object_id = 'default'

        option_params = {
            'ip_address': '0.0.0.0',
            'netmask': '0.0.0.1',
            'nexthop_address': '192.168.0.1',
        }

        msa = self.get_msa_instance()
        res = msa.create_csr1000v_default_route_ipv4(device_id, object_id,
                                            option_params)

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_update_csr1000v_default_route_ipv4(self):

        device_id = 'dev001'
        object_id = 'default'

        option_params = {
            'ip_address': '0.0.0.0',
            'netmask': '0.0.0.1',
            'nexthop_address': '192.168.0.1',
        }

        msa = self.get_msa_instance()
        res = msa.update_csr1000v_default_route_ipv4(device_id, object_id,
                                            option_params)

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_delete_csr1000v_default_route_ipv4(self):

        device_id = 'dev001'
        object_id = 'default'

        option_params = {
            'ip_address': '0.0.0.0',
            'netmask': '0.0.0.1',
            'nexthop_address': '192.168.0.1',
        }

        msa = self.get_msa_instance()
        res = msa.delete_csr1000v_default_route_ipv4(device_id, object_id,
                                            option_params)

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_create_csr1000v_default_route_ipv6(self):

        device_id = 'dev001'
        object_id = 'default'

        option_params = {
            'nexthop_address': '192.168.0.1',
        }

        msa = self.get_msa_instance()
        res = msa.create_csr1000v_default_route_ipv6(device_id, object_id,
                                            option_params)

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_update_csr1000v_default_route_ipv6(self):

        device_id = 'dev001'
        object_id = 'default'

        option_params = {
            'nexthop_address': '192.168.0.1',
        }

        msa = self.get_msa_instance()
        res = msa.update_csr1000v_default_route_ipv6(device_id, object_id,
                                            option_params)

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_delete_csr1000v_default_route_ipv6(self):

        device_id = 'dev001'
        object_id = 'default'

        option_params = {
            'nexthop_address': '192.168.0.1',
        }

        msa = self.get_msa_instance()
        res = msa.delete_csr1000v_default_route_ipv6(device_id, object_id,
                                            option_params)

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_create_csr1000v_static_route(self):

        device_id = 'dev001'
        object_id = 'static001'

        option_params = {
            'ip_address': '10.0.0.1',
            'netmask': '255.255.225.0',
            'nexthop_address': '192.168.0.1',
            'netmask_cidr': 24,
        }

        msa = self.get_msa_instance()
        res = msa.create_csr1000v_static_route(device_id, object_id,
                                            option_params)

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_update_csr1000v_static_route(self):

        device_id = 'dev001'
        object_id = 'static001'

        option_params = {
            'ip_address': '10.0.0.1',
            'netmask': '255.255.225.0',
            'nexthop_address': '192.168.0.1',
            'netmask_cidr': 24,
        }

        msa = self.get_msa_instance()
        res = msa.update_csr1000v_static_route(device_id, object_id,
                                            option_params)

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_delete_csr1000v_static_route(self):

        device_id = 'dev001'
        object_id = 'static001'

        option_params = {
            'ip_address': '10.0.0.1',
            'netmask': '255.255.225.0',
            'nexthop_address': '192.168.0.1',
            'netmask_cidr': 24,
        }

        msa = self.get_msa_instance()
        res = msa.delete_csr1000v_static_route(device_id, object_id,
                                            option_params)

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_create_csr1000v_static_route_ipv6(self):

        device_id = 'dev001'
        object_id = 'static001'

        option_params = {
            'nexthop_address': 'dea:beaf::2',
            'prefix': 48,
            'segment': 'dead:beef::',
        }

        msa = self.get_msa_instance()
        res = msa.create_csr1000v_static_route_ipv6(device_id, object_id,
                                            option_params)

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_update_csr1000v_static_route_ipv6(self):

        device_id = 'dev001'
        object_id = 'static001'

        option_params = {
            'nexthop_address': 'dea:beaf::2',
            'prefix': 48,
            'segment': 'dead:beef::',
        }

        msa = self.get_msa_instance()
        res = msa.update_csr1000v_static_route_ipv6(device_id, object_id,
                                            option_params)

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_delete_csr1000v_static_route_ipv6(self):

        device_id = 'dev001'
        object_id = 'static001'

        option_params = {
            'nexthop_address': 'dea:beaf::2',
            'prefix': 48,
            'segment': 'dead:beef::',
        }

        msa = self.get_msa_instance()
        res = msa.delete_csr1000v_static_route_ipv6(device_id, object_id,
                                            option_params)

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_create_csr1000v_bgp_peer_ipv4(self):

        device_id = 'dev001'
        object_id = 'host001'

        option_params = {
            'ip_address': '10.0.0.1',
            'authkey': 'auth001',
            'interface': 'GigabitEthernet2',
        }

        msa = self.get_msa_instance()
        res = msa.create_csr1000v_bgp_peer_ipv4(device_id, object_id,
                                            option_params)

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_update_csr1000v_bgp_peer_ipv4(self):

        device_id = 'dev001'
        object_id = 'host001'

        option_params = {
            'ip_address': '10.0.0.1',
            'authkey': 'auth001',
            'interface': 'GigabitEthernet2',
        }

        msa = self.get_msa_instance()
        res = msa.update_csr1000v_bgp_peer_ipv4(device_id, object_id,
                                            option_params)

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_delete_csr1000v_bgp_peer_ipv4(self):

        device_id = 'dev001'
        object_id = 'host001'

        option_params = {
            'ip_address': '10.0.0.1',
        }

        msa = self.get_msa_instance()
        res = msa.delete_csr1000v_bgp_peer_ipv4(device_id, object_id,
                                            option_params)

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_create_csr1000v_bgp_peer_ipv6(self):

        device_id = 'dev001'
        object_id = 'host001'

        option_params = {
            'ipv6_address': 'dea:beaf::1',
            'authkey': 'auth001',
            'interface': 'GigabitEthernet2',
        }

        msa = self.get_msa_instance()
        res = msa.create_csr1000v_bgp_peer_ipv6(device_id, object_id,
                                            option_params)

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_update_csr1000v_bgp_peer_ipv6(self):

        device_id = 'dev001'
        object_id = 'host001'

        option_params = {
            'ipv6_address': 'dea:beaf::1',
            'authkey': 'auth001',
            'interface': 'GigabitEthernet2',
        }

        msa = self.get_msa_instance()
        res = msa.update_csr1000v_bgp_peer_ipv6(device_id, object_id,
                                            option_params)

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_delete_csr1000v_bgp_peer_ipv6(self):

        device_id = 'dev001'
        object_id = 'host001'

        option_params = {
            'ipv6_address': 'dea:beaf::1',
        }

        msa = self.get_msa_instance()
        res = msa.delete_csr1000v_bgp_peer_ipv6(device_id, object_id,
                                            option_params)

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_create_csr1000v_hsrp_tracking(self):

        device_id = 'dev001'
        object_id = 'GigabitEthernet3-DC03'

        option_params = {
            'interface': 'GigabitEthernet3',
            'group_id': 1,
            'segment': '192.168.0.0',
            'netmask': '255.255.255.0',
            'prioritycost': 10,
            'track_id': 1000,
        }

        msa = self.get_msa_instance()
        res = msa.create_csr1000v_hsrp_tracking(device_id, object_id,
                                            option_params)

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_update_csr1000v_hsrp_tracking(self):

        device_id = 'dev001'
        object_id = 'GigabitEthernet3-DC03'

        option_params = {
            'interface': 'GigabitEthernet3',
            'group_id': 1,
            'segment': '192.168.0.0',
            'netmask': '255.255.255.0',
            'prioritycost': 10,
            'track_id': 1000,
        }

        msa = self.get_msa_instance()
        res = msa.update_csr1000v_hsrp_tracking(device_id, object_id,
                                            option_params)

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_delete_csr1000v_hsrp_tracking(self):

        device_id = 'dev001'
        object_id = 'GigabitEthernet3-DC03'

        option_params = {
            'interface': 'GigabitEthernet3',
            'group_id': 1,
            'track_id': 1000,
        }

        msa = self.get_msa_instance()
        res = msa.delete_csr1000v_hsrp_tracking(device_id, object_id,
                                            option_params)

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_create_csr1000v_dns_ipv4(self):

        device_id = 'dev001'
        object_id = 'host001'

        option_params = {
            'ip_address': '192.168.0.1',
        }

        msa = self.get_msa_instance()
        res = msa.create_csr1000v_dns_ipv4(device_id, object_id,
                                            option_params)

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_update_csr1000v_dns_ipv4(self):

        device_id = 'dev001'
        object_id = 'host001'

        option_params = {
            'ip_address': '192.168.0.1',
        }

        msa = self.get_msa_instance()
        res = msa.update_csr1000v_dns_ipv4(device_id, object_id,
                                            option_params)

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_delete_csr1000v_dns_ipv4(self):

        device_id = 'dev001'
        object_id = 'host001'

        option_params = {
            'ip_address': '192.168.0.1',
        }

        msa = self.get_msa_instance()
        res = msa.delete_csr1000v_dns_ipv4(device_id, object_id,
                                            option_params)

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_create_csr1000v_dns_ipv6(self):

        device_id = 'dev001'
        object_id = 'host001'

        option_params = {
            'ipv6_address': 'dead::beaf::1',
        }

        msa = self.get_msa_instance()
        res = msa.create_csr1000v_dns_ipv6(device_id, object_id,
                                            option_params)

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_update_csr1000v_dns_ipv6(self):

        device_id = 'dev001'
        object_id = 'host001'

        option_params = {
            'ipv6_address': 'dead::beaf::1',
        }

        msa = self.get_msa_instance()
        res = msa.update_csr1000v_dns_ipv6(device_id, object_id,
                                            option_params)

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_delete_csr1000v_dns_ipv6(self):

        device_id = 'dev001'
        object_id = 'host001'

        option_params = {
            'ipv6_address': 'dead::beaf::1',
        }

        msa = self.get_msa_instance()
        res = msa.delete_csr1000v_dns_ipv6(device_id, object_id,
                                            option_params)

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_create_csr1000v_snmp_ipv4(self):

        device_id = 'dev001'
        object_id = 'host001'

        option_params = {
            'community_name': 'nw',
            'interface': 'GigabitEthernet3',
            'ip_address': '192.168.0.1',
            'version': '2c',
        }

        msa = self.get_msa_instance()
        res = msa.create_csr1000v_snmp_ipv4(device_id, object_id,
                                            option_params)

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_update_csr1000v_snmp_ipv4(self):

        device_id = 'dev001'
        object_id = 'host001'

        option_params = {
            'community_name': 'nw',
            'interface': 'GigabitEthernet3',
            'ip_address': '192.168.0.1',
            'version': '2c',
        }

        msa = self.get_msa_instance()
        res = msa.update_csr1000v_snmp_ipv4(device_id, object_id,
                                            option_params)

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_delete_csr1000v_snmp_ipv4(self):

        device_id = 'dev001'
        object_id = 'host001'

        option_params = {
            'community_name': 'nw',
            'ip_address': '192.168.0.1',
            'version': '2c',
        }

        msa = self.get_msa_instance()
        res = msa.delete_csr1000v_snmp_ipv4(device_id, object_id,
                                            option_params)

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_create_csr1000v_snmp_ipv6(self):

        device_id = 'dev001'
        object_id = 'host001'

        option_params = {
            'community_name': 'nw',
            'interface': 'GigabitEthernet3',
            'ipv6_address': 'dead::beaf::1',
            'version': '2c',
        }

        msa = self.get_msa_instance()
        res = msa.create_csr1000v_snmp_ipv6(device_id, object_id,
                                            option_params)

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_update_csr1000v_snmp_ipv6(self):

        device_id = 'dev001'
        object_id = 'host001'

        option_params = {
            'community_name': 'nw',
            'interface': 'GigabitEthernet3',
            'ipv6_address': 'dead::beaf::1',
            'version': '2c',
        }

        msa = self.get_msa_instance()
        res = msa.update_csr1000v_snmp_ipv6(device_id, object_id,
                                            option_params)

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_delete_csr1000v_snmp_ipv6(self):

        device_id = 'dev001'
        object_id = 'host001'

        option_params = {
            'community_name': 'nw',
            'ipv6_address': 'dead::beaf::1',
            'version': '2c',
        }

        msa = self.get_msa_instance()
        res = msa.delete_csr1000v_snmp_ipv6(device_id, object_id,
                                            option_params)

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_create_csr1000v_syslog_ipv4(self):

        device_id = 'dev001'
        object_id = 'host001'

        option_params = {
            'ip_address': '192.168.0.1',
            'interface': 'GigabitEthernet3',
            'facility': 'local0',
            'severity': 'warnings',
        }

        msa = self.get_msa_instance()
        res = msa.create_csr1000v_syslog_ipv4(device_id, object_id,
                                            option_params)

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_update_csr1000v_syslog_ipv4(self):

        device_id = 'dev001'
        object_id = 'host001'

        option_params = {
            'ip_address': '192.168.0.1',
            'interface': 'GigabitEthernet3',
            'facility': 'local0',
            'severity': 'warnings',
        }

        msa = self.get_msa_instance()
        res = msa.update_csr1000v_syslog_ipv4(device_id, object_id,
                                            option_params)

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_delete_csr1000v_syslog_ipv4(self):

        device_id = 'dev001'
        object_id = 'host001'

        option_params = {
            'ip_address': '192.168.0.1',
        }

        msa = self.get_msa_instance()
        res = msa.delete_csr1000v_syslog_ipv4(device_id, object_id,
                                            option_params)

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_create_csr1000v_syslog_ipv6(self):

        device_id = 'dev001'
        object_id = 'host001'

        option_params = {
            'ipv6_address': 'dead::beaf::1',
            'interface': 'GigabitEthernet3',
            'facility': 'local0',
            'severity': 'warnings',
        }

        msa = self.get_msa_instance()
        res = msa.create_csr1000v_syslog_ipv6(device_id, object_id,
                                            option_params)

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_update_csr1000v_syslog_ipv6(self):

        device_id = 'dev001'
        object_id = 'host001'

        option_params = {
            'ipv6_address': 'dead::beaf::1',
            'interface': 'GigabitEthernet3',
            'facility': 'local0',
            'severity': 'warnings',
        }

        msa = self.get_msa_instance()
        res = msa.update_csr1000v_syslog_ipv6(device_id, object_id,
                                            option_params)

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_delete_csr1000v_syslog_ipv6(self):

        device_id = 'dev001'
        object_id = 'host001'

        option_params = {
            'ipv6_address': 'dead::beaf::1',
        }

        msa = self.get_msa_instance()
        res = msa.delete_csr1000v_syslog_ipv6(device_id, object_id,
                                            option_params)

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_create_csr1000v_ntp_ipv4(self):

        device_id = 'dev001'
        object_id = 'host001'

        option_params = {
            'ip_address': '192.168.0.1',
            'interface': 'GigabitEthernet3',
        }

        msa = self.get_msa_instance()
        res = msa.create_csr1000v_ntp_ipv4(device_id, object_id,
                                            option_params)

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_update_csr1000v_ntp_ipv4(self):

        device_id = 'dev001'
        object_id = 'host001'

        option_params = {
            'ip_address': '192.168.0.1',
            'interface': 'GigabitEthernet3',
        }

        msa = self.get_msa_instance()
        res = msa.update_csr1000v_ntp_ipv4(device_id, object_id,
                                            option_params)

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_delete_csr1000v_ntp_ipv4(self):

        device_id = 'dev001'
        object_id = 'host001'

        option_params = {
            'ip_address': '192.168.0.1',
            'interface': 'GigabitEthernet3',
        }

        msa = self.get_msa_instance()
        res = msa.delete_csr1000v_ntp_ipv4(device_id, object_id,
                                            option_params)

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_create_csr1000v_ntp_ipv6(self):

        device_id = 'dev001'
        object_id = 'host001'

        option_params = {
            'ipv6_address': 'dead::beaf::1',
            'interface': 'GigabitEthernet3',
        }

        msa = self.get_msa_instance()
        res = msa.create_csr1000v_ntp_ipv6(device_id, object_id,
                                            option_params)

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_update_csr1000v_ntp_ipv6(self):

        device_id = 'dev001'
        object_id = 'host001'

        option_params = {
            'ipv6_address': 'dead::beaf::1',
            'interface': 'GigabitEthernet3',
        }

        msa = self.get_msa_instance()
        res = msa.update_csr1000v_ntp_ipv6(device_id, object_id,
                                            option_params)

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_delete_csr1000v_ntp_ipv6(self):

        device_id = 'dev001'
        object_id = 'host001'

        option_params = {
            'ipv6_address': 'dead::beaf::1',
            'interface': 'GigabitEthernet3',
        }

        msa = self.get_msa_instance()
        res = msa.delete_csr1000v_ntp_ipv6(device_id, object_id,
                                            option_params)

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_create_csr1000v_license(self):

        device_id = 'dev001'
        object_id = 'host001'

        option_params = {
            'idtoken': 'token001',
        }

        msa = self.get_msa_instance()
        res = msa.create_csr1000v_license(device_id, object_id,
                                            option_params)

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_update_csr1000v_license(self):

        device_id = 'dev001'
        object_id = 'host001'

        option_params = {
            'idtoken': 'token001',
        }

        msa = self.get_msa_instance()
        res = msa.update_csr1000v_license(device_id, object_id,
                                            option_params)

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_delete_csr1000v_license(self):

        device_id = 'dev001'
        object_id = 'host001'

        msa = self.get_msa_instance()
        res = msa.delete_csr1000v_license(device_id, object_id)

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_create_csr1000v_throughput(self):

        device_id = 'dev001'
        object_id = 'host001'

        option_params = {
            'throughput': 100,
        }

        msa = self.get_msa_instance()
        res = msa.create_csr1000v_throughput(device_id, object_id,
                                            option_params)

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_update_csr1000v_throughput(self):

        device_id = 'dev001'
        object_id = 'host001'

        option_params = {
            'throughput': 100,
        }

        msa = self.get_msa_instance()
        res = msa.update_csr1000v_throughput(device_id, object_id,
                                            option_params)

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_delete_csr1000v_throughput(self):

        device_id = 'dev001'
        object_id = 'host001'

        msa = self.get_msa_instance()
        res = msa.delete_csr1000v_throughput(device_id, object_id)

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_create_csr1000v_wan_interface_ipv4(self):

        device_id = 'dev001'
        object_id = 'GigabitEthernet2'

        option_params = {
            'ip_address': '10.0.0.1',
            'netmask': '255.255.255.0',
            'mtu': 1400,
            'segment': '192.168.0.1',
            'netmask_cidr': 24,
            'tcp_mss': 1360,
        }

        msa = self.get_msa_instance()
        res = msa.create_csr1000v_wan_interface_ipv4(device_id, object_id,
                                            option_params)

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_update_csr1000v_wan_interface_ipv4(self):

        device_id = 'dev001'
        object_id = 'GigabitEthernet2'

        option_params = {
            'ip_address': '10.0.0.1',
            'netmask': '255.255.255.0',
            'mtu': 1400,
            'segment': '192.168.0.1',
            'netmask_cidr': 24,
            'tcp_mss': 1360,
        }

        msa = self.get_msa_instance()
        res = msa.update_csr1000v_wan_interface_ipv4(device_id, object_id,
                                            option_params)

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_delete_csr1000v_wan_interface_ipv4(self):

        device_id = 'dev001'
        object_id = 'GigabitEthernet2'

        option_params = {
            'ip_address': '10.0.0.1',
            'mtu': 1400,
            'segment': '192.168.0.1',
            'netmask_cidr': 24,
            'tcp_mss': 1360,
        }

        msa = self.get_msa_instance()
        res = msa.delete_csr1000v_wan_interface_ipv4(device_id, object_id,
                                            option_params)

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_create_csr1000v_wan_interface_ipv6(self):

        device_id = 'dev001'
        object_id = 'GigabitEthernet2'

        option_params = {
            'ipv6_address': 'dead:beaf::1',
            'prefix': 48,
            'segment': 'dead:beaf::',
        }

        msa = self.get_msa_instance()
        res = msa.create_csr1000v_wan_interface_ipv6(device_id, object_id,
                                            option_params)

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_update_csr1000v_wan_interface_ipv6(self):

        device_id = 'dev001'
        object_id = 'GigabitEthernet2'

        option_params = {
            'ipv6_address': 'dead:beaf::1',
            'prefix': 48,
            'segment': 'dead:beaf::',
        }

        msa = self.get_msa_instance()
        res = msa.update_csr1000v_wan_interface_ipv6(device_id, object_id,
                                            option_params)

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_delete_csr1000v_wan_interface_ipv6(self):

        device_id = 'dev001'
        object_id = 'GigabitEthernet2'

        option_params = {
            'ipv6_address': 'dead:beaf::1',
            'prefix': 48,
            'segment': 'dead:beaf::',
        }

        msa = self.get_msa_instance()
        res = msa.delete_csr1000v_wan_interface_ipv6(device_id, object_id,
                                            option_params)

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_create_csr1000v_wan_interface_gre_ipv4(self):

        device_id = 'dev001'
        object_id = 'GigabitEthernet2'

        option_params = {
            'ip_address': '10.0.0.1',
            'netmask': '255.255.255.0',
            'mtu': 1400,
            'segment': '192.168.0.1',
            'netmask_cidr': 24,
            'tcp_mss': 1360,
        }

        msa = self.get_msa_instance()
        res = msa.create_csr1000v_wan_interface_gre_ipv4(device_id, object_id,
                                            option_params)

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_update_csr1000v_wan_interface_gre_ipv4(self):

        device_id = 'dev001'
        object_id = 'GigabitEthernet2'

        option_params = {
            'ip_address': '10.0.0.1',
            'netmask': '255.255.255.0',
            'mtu': 1400,
            'segment': '192.168.0.1',
            'netmask_cidr': 24,
            'tcp_mss': 1360,
        }

        msa = self.get_msa_instance()
        res = msa.update_csr1000v_wan_interface_gre_ipv4(device_id, object_id,
                                            option_params)

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_delete_csr1000v_wan_interface_gre_ipv4(self):

        device_id = 'dev001'
        object_id = 'GigabitEthernet2'

        option_params = {
            'ip_address': '10.0.0.1',
            'segment': '192.168.0.1',
            'netmask_cidr': 24,
            'mtu': 1400,
            'tcp_mss': 1360,
        }

        msa = self.get_msa_instance()
        res = msa.delete_csr1000v_wan_interface_gre_ipv4(device_id, object_id,
                                            option_params)

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_create_csr1000v_tunnel_interface_gre_ipv4(self):

        device_id = 'dev001'
        object_id = 'Tunnel0'

        option_params = {
            'destination_ip_address': '10.0.0.2',
            'interface': 'GigabitEthernet2',
            'segment': '192.168.0.0',
            'ip_address': '10.0.0.1',
            'netmask': '255.255.255.0',
            'netmask_cidr': 24,
        }

        msa = self.get_msa_instance()
        res = msa.create_csr1000v_tunnel_interface_gre_ipv4(
                                            device_id, object_id,
                                            option_params)

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_update_csr1000v_tunnel_interface_gre_ipv4(self):

        device_id = 'dev001'
        object_id = 'Tunnel0'

        option_params = {
            'destination_ip_address': '10.0.0.2',
            'interface': 'GigabitEthernet2',
            'segment': '192.168.0.0',
            'ip_address': '10.0.0.1',
            'netmask': '255.255.255.0',
            'netmask_cidr': 24,
        }

        msa = self.get_msa_instance()
        res = msa.update_csr1000v_tunnel_interface_gre_ipv4(
                                            device_id, object_id,
                                            option_params)

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_delete_csr1000v_tunnel_interface_gre_ipv4(self):

        device_id = 'dev001'
        object_id = 'Tunnel0'

        option_params = {
            'segment': '192.168.0.0',
            'ip_address': '10.0.0.1',
            'netmask_cidr': 24,
        }

        msa = self.get_msa_instance()
        res = msa.delete_csr1000v_tunnel_interface_gre_ipv4(
                                            device_id, object_id,
                                            option_params)

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_create_csr1000v_tunnel_interface_gre_ipv6(self):

        device_id = 'dev001'
        object_id = 'Tunnel0'

        option_params = {
            'ipv6_address': 'dead:beaf::1',
            'prefix': 48,
            'ipv6_segment': 'dead:beaf::',
        }

        msa = self.get_msa_instance()
        res = msa.create_csr1000v_tunnel_interface_gre_ipv6(
                                            device_id, object_id,
                                            option_params)

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_update_csr1000v_tunnel_interface_gre_ipv6(self):

        device_id = 'dev001'
        object_id = 'Tunnel0'

        option_params = {
            'ipv6_address': 'dead:beaf::1',
            'prefix': 48,
            'ipv6_segment': 'dead:beaf::',
        }

        msa = self.get_msa_instance()
        res = msa.update_csr1000v_tunnel_interface_gre_ipv6(
                                            device_id, object_id,
                                            option_params)

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_delete_csr1000v_tunnel_interface_gre_ipv6(self):

        device_id = 'dev001'
        object_id = 'Tunnel0'

        option_params = {
            'ipv6_address': 'dead:beaf::1',
            'prefix': 48,
            'ipv6_segment': 'dead:beaf::',
        }

        msa = self.get_msa_instance()
        res = msa.delete_csr1000v_tunnel_interface_gre_ipv6(
                                            device_id, object_id,
                                            option_params)

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_create_csr1000v_ipsec_basic_esp_gre_ipv4(self):

        device_id = 'dev001'
        object_id = 'host001'

        option_params = {
            'priority': 1,
            'encryption_algorithm': '3des',
            'hash_algorithm': 'md5',
            'diffie_hellman_group': 2,
            'isakmp_sa_lifetime': 86400,
            'transform_set': 'IPSEC',
            'encryption_transform': 'esp-3des',
            'authentication_transform': 'esp-md5-hmac',
            'ipsec_sa_lifetime': 3600,
        }
        msa = self.get_msa_instance()
        res = msa.create_csr1000v_ipsec_basic_esp_gre_ipv4(
                                            device_id, object_id,
                                            option_params)

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_update_csr1000v_ipsec_basic_esp_gre_ipv4(self):

        device_id = 'dev001'
        object_id = 'host001'

        option_params = {
            'priority': 1,
            'encryption_algorithm': '3des',
            'hash_algorithm': 'md5',
            'diffie_hellman_group': 2,
            'isakmp_sa_lifetime': 86400,
            'transform_set': 'IPSEC',
            'encryption_transform': 'esp-3des',
            'authentication_transform': 'esp-md5-hmac',
            'ipsec_sa_lifetime': 3600,
        }

        msa = self.get_msa_instance()
        res = msa.update_csr1000v_ipsec_basic_esp_gre_ipv4(
                                            device_id, object_id,
                                            option_params)

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_delete_csr1000v_ipsec_basic_esp_gre_ipv4(self):

        device_id = 'dev001'
        object_id = 'host001'

        option_params = {
            'priority': 1,
            'transform_set': 'IPSEC',
        }

        msa = self.get_msa_instance()
        res = msa.delete_csr1000v_ipsec_basic_esp_gre_ipv4(
                                            device_id, object_id,
                                            option_params)

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_create_csr1000v_ipsec_basic_ah_gre_ipv4(self):

        device_id = 'dev001'
        object_id = 'host001'

        option_params = {
            'priority': 1,
            'encryption_algorithm': '3des',
            'hash_algorithm': 'md5',
            'diffie_hellman_group': 2,
            'isakmp_sa_lifetime': 86400,
            'transform_set': 'IPSEC',
            'authentication_transform': 'ah-md5-hmac',
            'ipsec_sa_lifetime': 3600,
        }

        msa = self.get_msa_instance()
        res = msa.create_csr1000v_ipsec_basic_ah_gre_ipv4(
                                            device_id, object_id,
                                            option_params)

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_update_csr1000v_ipsec_basic_ah_gre_ipv4(self):

        device_id = 'dev001'
        object_id = 'host001'

        option_params = {
            'priority': 1,
            'encryption_algorithm': '3des',
            'hash_algorithm': 'md5',
            'diffie_hellman_group': 2,
            'isakmp_sa_lifetime': 86400,
            'transform_set': 'IPSEC',
            'authentication_transform': 'ah-md5-hmac',
            'ipsec_sa_lifetime': 3600,
        }

        msa = self.get_msa_instance()
        res = msa.update_csr1000v_ipsec_basic_ah_gre_ipv4(device_id, object_id,
                                            option_params)

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_delete_csr1000v_ipsec_basic_ah_gre_ipv4(self):

        device_id = 'dev001'
        object_id = 'host001'

        option_params = {
            'priority': 1,
            'transform_set': 'IPSEC',
        }

        msa = self.get_msa_instance()
        res = msa.delete_csr1000v_ipsec_basic_ah_gre_ipv4(device_id, object_id,
                                            option_params)

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_create_csr1000v_ipsec_peer_gre_ipv4(self):

        device_id = 'dev001'
        object_id = 'host001'

        option_params = {
            'ip_address': '10.0.0.1',
            'peer_ip_address': '192.168.0.1',
            'pre_shared_key': 'pre_shared_key001',
            'acl_number': 'host002',
            'sequence_number': 1000,
            'transform_set': 'IPSEC',
            'interface': 'GigabitEthernet2',
        }

        msa = self.get_msa_instance()
        res = msa.create_csr1000v_ipsec_peer_gre_ipv4(device_id, object_id,
                                            option_params)

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_update_csr1000v_ipsec_peer_gre_ipv4(self):

        device_id = 'dev001'
        object_id = 'host001'

        option_params = {
            'ip_address': '10.0.0.1',
            'peer_ip_address': '192.168.0.1',
            'pre_shared_key': 'pre_shared_key001',
            'acl_number': 'host002',
            'sequence_number': 1000,
            'transform_set': 'IPSEC',
            'interface': 'GigabitEthernet2',
        }

        msa = self.get_msa_instance()
        res = msa.update_csr1000v_ipsec_peer_gre_ipv4(device_id, object_id,
                                            option_params)

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_delete_csr1000v_ipsec_peer_gre_ipv4(self):

        device_id = 'dev001'
        object_id = 'host001'

        option_params = {
            'ip_address': '10.0.0.1',
            'peer_ip_address': '192.168.0.1',
            'pre_shared_key': 'pre_shared_key001',
            'acl_number': 'host002',
            'sequence_number': 1000,
            'interface': 'GigabitEthernet2',
        }

        msa = self.get_msa_instance()
        res = msa.delete_csr1000v_ipsec_peer_gre_ipv4(device_id, object_id,
                                            option_params)

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_create_csr1000v_static_route_for_dc(self):

        device_id = 'dev001'
        object_id = 'static001'

        option_params = {
            'ip_address': '10.0.0.1',
            'netmask': '255.255.255.0',
            'nexthop_address': '192.168.0.1',
            'netmask_cidr': 24,
        }

        msa = self.get_msa_instance()
        res = msa.create_csr1000v_static_route_for_dc(device_id, object_id,
                                            option_params)

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_update_csr1000v_static_route_for_dc(self):

        device_id = 'dev001'
        object_id = 'static001'

        option_params = {
            'ip_address': '10.0.0.1',
            'netmask': '255.255.255.0',
            'nexthop_address': '192.168.0.1',
            'netmask_cidr': 24,
        }

        msa = self.get_msa_instance()
        res = msa.update_csr1000v_static_route_for_dc(device_id, object_id,
                                            option_params)

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_delete_csr1000v_static_route_for_dc(self):

        device_id = 'dev001'
        object_id = 'static001'

        option_params = {
            'ip_address': '10.0.0.1',
            'netmask': '255.255.255.0',
            'nexthop_address': '192.168.0.1',
            'netmask_cidr': 24,
        }

        msa = self.get_msa_instance()
        res = msa.delete_csr1000v_static_route_for_dc(device_id, object_id,
                                            option_params)

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)
