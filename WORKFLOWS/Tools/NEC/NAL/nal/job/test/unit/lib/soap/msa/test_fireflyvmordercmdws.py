import inspect
import unittest

from job.auto.extension import routingpod
from job.lib.soap.msa import fireflyvmordercmdws
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

        job_input = {'type': 3, 'device_type': 1,
                     'operation_id': 'TestSoapUser'}

        job_instance = routingpod.RoutingPod()
        ret = job_instance.routing_pod(job_input)

        pod_id = ret['pod_id']
        dc_id = 'dc02'

        msa_instance = fireflyvmordercmdws.FireflyVmOrderCommandWs(
                            job_instance.job_config,
                            job_instance.nal_endpoint_config,
                            pod_id, dc_id)

        return msa_instance

    def test_create_firefly_vm_system_common(self):

        device_id = 'dev001'
        host_name = 'host001'
        firefly_vm_system_common_timezone = 'Asia/Tokyo'

        msa = self.get_msa_instance()
        res = msa.create_firefly_vm_system_common(device_id, host_name,
                                    firefly_vm_system_common_timezone)

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_delete_firefly_vm_system_common(self):

        device_id = 'dev001'
        host_name = 'host001'
        firefly_vm_system_common_timezone = 'Asia/Tokyo'

        msa = self.get_msa_instance()
        res = msa.delete_firefly_vm_system_common(device_id, host_name,
                                    firefly_vm_system_common_timezone)
        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_create_firefly_vm_wan_interface(self):

        device_id = 'dev001'
        interface_name = 'if001'
        firefly_vm_wan_interface_ip_address = '10.0.0.1'
        firefly_vm_wan_interface_netmask = '255.255.255.0'
        firefly_vm_wan_interface_mtu = 10

        msa = self.get_msa_instance()
        res = msa.create_firefly_vm_wan_interface(device_id, interface_name,
                                        firefly_vm_wan_interface_ip_address,
                                        firefly_vm_wan_interface_netmask,
                                        firefly_vm_wan_interface_mtu)
        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_delete_firefly_vm_wan_interface(self):

        device_id = 'dev001'
        interface_name = 'if001'

        msa = self.get_msa_instance()
        res = msa.delete_firefly_vm_wan_interface(device_id, interface_name)

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_create_firefly_vm_bgp_basic(self):

        device_id = 'dev001'
        host_name = 'host001'
        firefly_vm_bgp_interface_ip_address = '10.0.0.1'
        firefly_vm_bgp_local_preference = 'local'
        firefly_vm_bgp_authkey = 'key001'

        msa = self.get_msa_instance()
        res = msa.create_firefly_vm_bgp_basic(device_id, host_name,
                                    firefly_vm_bgp_interface_ip_address,
                                    firefly_vm_bgp_local_preference,
                                    firefly_vm_bgp_authkey)
        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_delete_firefly_vm_bgp_basic(self):

        device_id = 'dev001'
        node_name = 'host001'
        firefly_vm_bgp_interface_ip_address = '10.0.0.1'

        msa = self.get_msa_instance()
        res = msa.delete_firefly_vm_bgp_basic(device_id, node_name,
                                firefly_vm_bgp_interface_ip_address)
        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_create_firefly_vm_loopback_interface(self):

        device_id = 'dev001'
        interface_name = 'if001'
        firefly_vm_loopback_interface_ip_address = '10.0.0.1'
        firefly_vm_loopback_interface_netmask = '255.255.255.0'
        firefly_vm_loopback_interface_segment = 'segment1'

        msa = self.get_msa_instance()
        res = msa.create_firefly_vm_loopback_interface(device_id,
                                    interface_name,
                                    firefly_vm_loopback_interface_ip_address,
                                    firefly_vm_loopback_interface_netmask,
                                    firefly_vm_loopback_interface_segment)
        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_delete_firefly_vm_loopback_interface(self):

        device_id = 'dev001'
        interface_name = 'if001'
        firefly_vm_loopback_interface_netmask = '255.255.255.0'
        firefly_vm_loopback_interface_segment = 'segment1'

        msa = self.get_msa_instance()
        res = msa.delete_firefly_vm_loopback_interface(device_id,
                                    interface_name,
                                    firefly_vm_loopback_interface_netmask,
                                    firefly_vm_loopback_interface_segment)
        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_create_firefly_vm_lan_interface(self):

        device_id = 'dev001'
        interface_name = 'if001'
        firefly_vm_lan_interface_ip_address = '10.0.0.1'
        firefly_vm_lan_interface_netmask = '255.255.255.0'
        firefly_vm_lan_interface_vrrp_ip_address = '192.168.0.1'
        firefly_vm_lan_interface_segment = 'segment1'

        msa = self.get_msa_instance()
        res = msa.create_firefly_vm_lan_interface(device_id,
                                    interface_name,
                                    firefly_vm_lan_interface_ip_address,
                                    firefly_vm_lan_interface_netmask,
                                    firefly_vm_lan_interface_vrrp_ip_address,
                                    firefly_vm_lan_interface_segment)
        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_delete_firefly_vm_lan_interface(self):

        device_id = 'dev001'
        interface_name = 'if001'
        firefly_vm_lan_interface_netmask = '255.255.255.0'
        firefly_vm_lan_interface_segment = 'segment1'

        msa = self.get_msa_instance()
        res = msa.delete_firefly_vm_lan_interface(device_id,
                                        interface_name,
                                        firefly_vm_lan_interface_netmask,
                                        firefly_vm_lan_interface_segment)
        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_create_firefly_vm_vrrp(self):

        device_id = 'dev001'
        vrrp_interface_name = 'if001'
        firefly_vm_vrrp_vip = '255.255.255.0'
        firefly_vm_lan_interface_ip_address = '10.0.0.1'
        firefly_vm_lan_interface_netmask = '255.255.255.0'
        firefly_vm_vrrp_priority = '1'
        firefly_vm_vrrp_group_id = 'group001'
        firefly_vm_vrrp_authkey = 'ky001'

        msa = self.get_msa_instance()
        res = msa.create_firefly_vm_vrrp(device_id,
                                        vrrp_interface_name,
                                        firefly_vm_vrrp_vip,
                                        firefly_vm_lan_interface_ip_address,
                                        firefly_vm_lan_interface_netmask,
                                        firefly_vm_vrrp_priority,
                                        firefly_vm_vrrp_group_id,
                                        firefly_vm_vrrp_authkey)
        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_delete_firefly_vm_vrrp(self):

        device_id = 'dev001'
        vrrp_interface_name = 'if001'
        firefly_vm_vrrp_vip = '255.255.255.0'
        firefly_vm_lan_interface_ip_address = '10.0.0.1'
        firefly_vm_lan_interface_netmask = '255.255.255.0'
        firefly_vm_vrrp_priority = '1'
        firefly_vm_vrrp_group_id = 'group001'

        msa = self.get_msa_instance()
        res = msa.delete_firefly_vm_vrrp(device_id,
                                        vrrp_interface_name,
                                        firefly_vm_vrrp_vip,
                                        firefly_vm_lan_interface_ip_address,
                                        firefly_vm_lan_interface_netmask,
                                        firefly_vm_vrrp_priority,
                                        firefly_vm_vrrp_group_id)
        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_create_firefly_vm_bgp_peer(self):

        device_id = 'dev001'
        opp_host_name = 'host001'
        firefly_vm_bgp_peer_ip_address = '10.0.0.1'

        msa = self.get_msa_instance()
        res = msa.create_firefly_vm_bgp_peer(device_id,
                                        opp_host_name,
                                        firefly_vm_bgp_peer_ip_address)
        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_delete_firefly_vm_bgp_peer(self):

        device_id = 'dev001'
        opp_host_name = 'host001'
        firefly_vm_bgp_peer_ip_address = '10.0.0.1'

        msa = self.get_msa_instance()
        res = msa.delete_firefly_vm_bgp_peer(device_id,
                                        opp_host_name,
                                        firefly_vm_bgp_peer_ip_address)
        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_create_firefly_vm_vrrp_tracking(self):

        device_id = 'dev001'
        vrrp_tracking_name = 'tr001'
        firefly_vm_interface_name = 'if001'
        firefly_vm_lan_interface_ip_address = '10.0.0.1'
        firefly_vm_lan_interface_netmask = '255.255.255.0'
        firefly_vm_vrrp_group_id = 'gr001'
        firefly_vm_vrrp_track_segment = 'segment1'
        firefly_vm_vrrp_track_netmask = '255.255.255.1'
        firefly_vm_vrrp_track_prioritycost = '10'

        msa = self.get_msa_instance()
        res = msa.create_firefly_vm_vrrp_tracking(device_id,
                                        vrrp_tracking_name,
                                        firefly_vm_interface_name,
                                        firefly_vm_lan_interface_ip_address,
                                        firefly_vm_lan_interface_netmask,
                                        firefly_vm_vrrp_group_id,
                                        firefly_vm_vrrp_track_segment,
                                        firefly_vm_vrrp_track_netmask,
                                        firefly_vm_vrrp_track_prioritycost)
        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_delete_firefly_vm_vrrp_tracking(self):

        device_id = 'dev001'
        vrrp_tracking_name = 'tr001'
        firefly_vm_interface_name = 'if001'
        firefly_vm_lan_interface_ip_address = '10.0.0.1'
        firefly_vm_lan_interface_netmask = '255.255.255.0'
        firefly_vm_vrrp_group_id = 'gr001'
        firefly_vm_vrrp_track_segment = 'segment1'
        firefly_vm_vrrp_track_netmask = '255.255.255.1'

        msa = self.get_msa_instance()
        res = msa.delete_firefly_vm_vrrp_tracking(device_id,
                                        vrrp_tracking_name,
                                        firefly_vm_interface_name,
                                        firefly_vm_lan_interface_ip_address,
                                        firefly_vm_lan_interface_netmask,
                                        firefly_vm_vrrp_group_id,
                                        firefly_vm_vrrp_track_segment,
                                        firefly_vm_vrrp_track_netmask)
        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_create_firefly_vm_static_route(self):

        device_id = 'dev001'
        static_route_dst_name = 'dst001'
        firefly_vm_static_destination_ip_address = '10.0.0.1'
        firefly_vm_static_destination_netmask = '255.255.255.0'
        firefly_vm_static_nexthop_address = '192.168.0.1'

        msa = self.get_msa_instance()
        res = msa.create_firefly_vm_static_route(device_id,
                                    static_route_dst_name,
                                    firefly_vm_static_destination_ip_address,
                                    firefly_vm_static_destination_netmask,
                                    firefly_vm_static_nexthop_address)
        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_delete_firefly_vm_static_route(self):

        device_id = 'dev001'
        static_route_dst_name = 'dst001'
        firefly_vm_static_destination_ip_address = '10.0.0.1'
        firefly_vm_static_destination_netmask = '255.255.255.0'
        firefly_vm_static_nexthop_address = '192.168.0.1'

        msa = self.get_msa_instance()
        res = msa.delete_firefly_vm_static_route(device_id,
                                    static_route_dst_name,
                                    firefly_vm_static_destination_ip_address,
                                    firefly_vm_static_destination_netmask,
                                    firefly_vm_static_nexthop_address)
        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)
