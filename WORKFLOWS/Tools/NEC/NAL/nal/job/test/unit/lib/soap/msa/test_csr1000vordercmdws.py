import inspect
import unittest

from job.auto.extension import routingpod
from job.lib.soap.msa import csr1000vordercmdws
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

        job_input = {'type': 3, 'device_type': 2,
                     'operation_id': 'TestSoapUser'}

        job_instance = routingpod.RoutingPod()
        ret = job_instance.routing_pod(job_input)

        pod_id = ret['pod_id']
        dc_id = 'dc02'

        msa_instance = csr1000vordercmdws.Csr1000vOrderCommandWs(
                            job_instance.job_config,
                            job_instance.nal_endpoint_config,
                            pod_id, dc_id)

        return msa_instance

    def test_create_csr1000v_vm_system_common(self):

        device_id = 'dev001'
        object_id = 'host001'
        csr1000v_vm_system_common_timezone = 'Asia/Tokyo'

        msa = self.get_msa_instance()
        res = msa.create_csr1000v_vm_system_common(device_id, object_id,
                                    csr1000v_vm_system_common_timezone)

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_update_csr1000v_vm_system_common(self):

        device_id = 'dev001'
        object_id = 'host001'
        csr1000v_vm_system_common_timezone = 'Asia/Tokyo'

        msa = self.get_msa_instance()
        res = msa.update_csr1000v_vm_system_common(device_id, object_id,
                                    csr1000v_vm_system_common_timezone)

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_delete_csr1000v_vm_system_common(self):

        device_id = 'dev001'
        object_id = 'host001'

        msa = self.get_msa_instance()
        res = msa.delete_csr1000v_vm_system_common(device_id, object_id)

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_create_csr1000v_vm_wan_interface(self):

        device_id = 'dev001'
        object_id = 'host001'
        csr1000v_vm_wan_interface_ip_address = '10.0.0.1'
        csr1000v_vm_wan_interface_netmask = '255.255.255.0'
        csr1000v_vm_wan_interface_mtu = '100'
        csr1000v_vm_wan_interface_segment = '10.0.0.2'
        csr1000v_vm_wan_interface_netmask_cidr = '10.0.0.1/24'

        msa = self.get_msa_instance()
        res = msa.create_csr1000v_vm_wan_interface(device_id, object_id,
                                        csr1000v_vm_wan_interface_ip_address,
                                        csr1000v_vm_wan_interface_netmask,
                                        csr1000v_vm_wan_interface_mtu,
                                        csr1000v_vm_wan_interface_segment,
                                        csr1000v_vm_wan_interface_netmask_cidr
                                        )

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_update_csr1000v_vm_wan_interface(self):

        device_id = 'dev001'
        object_id = 'host001'
        csr1000v_vm_wan_interface_ip_address = '10.0.0.1'
        csr1000v_vm_wan_interface_netmask = '255.255.255.0'
        csr1000v_vm_wan_interface_mtu = '100'
        csr1000v_vm_wan_interface_segment = '10.0.0.2'
        csr1000v_vm_wan_interface_netmask_cidr = '10.0.0.1/24'

        msa = self.get_msa_instance()
        res = msa.update_csr1000v_vm_wan_interface(device_id, object_id,
                                        csr1000v_vm_wan_interface_ip_address,
                                        csr1000v_vm_wan_interface_netmask,
                                        csr1000v_vm_wan_interface_mtu,
                                        csr1000v_vm_wan_interface_segment,
                                        csr1000v_vm_wan_interface_netmask_cidr
                                        )

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_delete_csr1000v_vm_wan_interface(self):

        device_id = 'dev001'
        object_id = 'host001'
        csr1000v_vm_wan_interface_ip_address = '10.0.0.1'
        csr1000v_vm_wan_interface_mtu = '100'
        csr1000v_vm_wan_interface_segment = '10.0.0.2'
        csr1000v_vm_wan_interface_netmask_cidr = '10.0.0.1/24'

        msa = self.get_msa_instance()
        res = msa.delete_csr1000v_vm_wan_interface(device_id, object_id,
                                        csr1000v_vm_wan_interface_ip_address,
                                        csr1000v_vm_wan_interface_mtu,
                                        csr1000v_vm_wan_interface_segment,
                                        csr1000v_vm_wan_interface_netmask_cidr
                                        )

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_create_csr1000v_vm_lan_interface(self):

        device_id = 'dev001'
        object_id = 'host001'
        csr1000v_vm_lan_interface_ip_address = '10.0.0.1'
        csr1000v_vm_lan_interface_netmask = '255.255.255.0'
        csr1000v_vm_lan_interface_hsrp_ip_address = '10.0.0.2'
        csr1000v_vm_lan_interface_segment = 12
        csr1000v_vm_lan_interface_netmask_cidr = '10.0.0.1/24'

        msa = self.get_msa_instance()
        res = msa.create_csr1000v_vm_lan_interface(device_id, object_id,
                                    csr1000v_vm_lan_interface_ip_address,
                                    csr1000v_vm_lan_interface_netmask,
                                    csr1000v_vm_lan_interface_hsrp_ip_address,
                                    csr1000v_vm_lan_interface_segment,
                                    csr1000v_vm_lan_interface_netmask_cidr
                                        )

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_update_csr1000v_vm_lan_interface(self):

        device_id = 'dev001'
        object_id = 'host001'
        csr1000v_vm_lan_interface_ip_address = '10.0.0.1'
        csr1000v_vm_lan_interface_netmask = '255.255.255.0'
        csr1000v_vm_lan_interface_hsrp_ip_address = '10.0.0.2'
        csr1000v_vm_lan_interface_segment = 12
        csr1000v_vm_lan_interface_netmask_cidr = '10.0.0.1/24'

        msa = self.get_msa_instance()
        res = msa.update_csr1000v_vm_lan_interface(device_id, object_id,
                                    csr1000v_vm_lan_interface_ip_address,
                                    csr1000v_vm_lan_interface_netmask,
                                    csr1000v_vm_lan_interface_hsrp_ip_address,
                                    csr1000v_vm_lan_interface_segment,
                                    csr1000v_vm_lan_interface_netmask_cidr
                                        )

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_delete_csr1000v_vm_lan_interface(self):

        device_id = 'dev001'
        object_id = 'host001'
        csr1000v_vm_lan_interface_ip_address = '10.0.0.1'
        csr1000v_vm_lan_interface_hsrp_ip_address = '10.0.0.2'
        csr1000v_vm_lan_interface_segment = 12
        csr1000v_vm_lan_interface_netmask_cidr = '10.0.0.1/24'

        msa = self.get_msa_instance()
        res = msa.delete_csr1000v_vm_lan_interface(device_id, object_id,
                                    csr1000v_vm_lan_interface_ip_address,
                                    csr1000v_vm_lan_interface_hsrp_ip_address,
                                    csr1000v_vm_lan_interface_segment,
                                    csr1000v_vm_lan_interface_netmask_cidr
                                        )

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_create_csr1000v_vm_loopback_interface(self):

        device_id = 'dev001'
        object_id = 'host001'
        csr1000v_vm_loopback_interface_ip_address = '10.0.0.1'
        csr1000v_vm_loopback_interface_netmask = '10.0.0.2'
        csr1000v_vm_loopback_interface_segment = 12
        csr1000v_vm_loopback_interface_netmask_cidr = '10.0.0.1/24'

        msa = self.get_msa_instance()
        res = msa.create_csr1000v_vm_loopback_interface(device_id, object_id,
                                    csr1000v_vm_loopback_interface_ip_address,
                                    csr1000v_vm_loopback_interface_netmask,
                                    csr1000v_vm_loopback_interface_segment,
                                    csr1000v_vm_loopback_interface_netmask_cidr
                                        )

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_update_csr1000v_vm_loopback_interface(self):

        device_id = 'dev001'
        object_id = 'host001'
        csr1000v_vm_loopback_interface_ip_address = '10.0.0.1'
        csr1000v_vm_loopback_interface_netmask = '10.0.0.2'
        csr1000v_vm_loopback_interface_segment = 12
        csr1000v_vm_loopback_interface_netmask_cidr = '10.0.0.1/24'

        msa = self.get_msa_instance()
        res = msa.update_csr1000v_vm_loopback_interface(device_id, object_id,
                                    csr1000v_vm_loopback_interface_ip_address,
                                    csr1000v_vm_loopback_interface_netmask,
                                    csr1000v_vm_loopback_interface_segment,
                                    csr1000v_vm_loopback_interface_netmask_cidr
                                        )

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_delete_csr1000v_vm_loopback_interface(self):

        device_id = 'dev001'
        object_id = 'host001'
        csr1000v_vm_loopback_interface_ip_address = '10.0.0.1'
        csr1000v_vm_loopback_interface_segment = 12
        csr1000v_vm_loopback_interface_netmask_cidr = '10.0.0.1/24'

        msa = self.get_msa_instance()
        res = msa.delete_csr1000v_vm_loopback_interface(device_id, object_id,
                                    csr1000v_vm_loopback_interface_ip_address,
                                    csr1000v_vm_loopback_interface_segment,
                                    csr1000v_vm_loopback_interface_netmask_cidr
                                        )

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_create_csr1000v_vm_staticroute(self):

        device_id = 'dev001'
        object_id = 'host001'
        csr1000v_vm_static_destination_ip_address = '10.0.0.1'
        csr1000v_vm_static_destination_netmask = '255.255.255.0'
        csr1000v_vm_static_nexthop_address = '10.0.0.3'
        netmask_cidr = '16'

        msa = self.get_msa_instance()
        res = msa.create_csr1000v_vm_staticroute(device_id, object_id,
                                    csr1000v_vm_static_destination_ip_address,
                                    csr1000v_vm_static_destination_netmask,
                                    csr1000v_vm_static_nexthop_address,
                                    netmask_cidr
                                        )

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_update_csr1000v_vm_staticroute(self):

        device_id = 'dev001'
        object_id = 'host001'
        csr1000v_vm_static_destination_ip_address = '10.0.0.1'
        csr1000v_vm_static_destination_netmask = '255.255.255.0'
        csr1000v_vm_static_nexthop_address = '10.0.0.3'
        netmask_cidr = '16'

        msa = self.get_msa_instance()
        res = msa.update_csr1000v_vm_staticroute(device_id, object_id,
                                    csr1000v_vm_static_destination_ip_address,
                                    csr1000v_vm_static_destination_netmask,
                                    csr1000v_vm_static_nexthop_address,
                                    netmask_cidr
                                        )

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_delete_csr1000v_vm_staticroute(self):

        device_id = 'dev001'
        object_id = 'host001'
        csr1000v_vm_static_destination_ip_address = '10.0.0.1'
        csr1000v_vm_static_destination_netmask = '255.255.255.0'
        csr1000v_vm_static_nexthop_address = '10.0.0.3'
        netmask_cidr = '16'

        msa = self.get_msa_instance()
        res = msa.delete_csr1000v_vm_staticroute(device_id, object_id,
                                    csr1000v_vm_static_destination_ip_address,
                                    csr1000v_vm_static_destination_netmask,
                                    csr1000v_vm_static_nexthop_address,
                                    netmask_cidr
                                        )

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_create_csr1000v_vm_bgp_basic(self):

        device_id = 'dev001'
        object_id = 'host001'
        csr1000v_vm_bgp_interface_ip_address = '10.0.0.1'
        csr1000v_vm_bgp_local_preference = 'abc'

        msa = self.get_msa_instance()
        res = msa.create_csr1000v_vm_bgp_basic(device_id, object_id,
                                        csr1000v_vm_bgp_interface_ip_address,
                                        csr1000v_vm_bgp_local_preference
                                        )

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_update_csr1000v_vm_bgp_basic(self):

        device_id = 'dev001'
        object_id = 'host001'
        csr1000v_vm_bgp_interface_ip_address = '10.0.0.1'
        csr1000v_vm_bgp_local_preference = 'abc'

        msa = self.get_msa_instance()
        res = msa.update_csr1000v_vm_bgp_basic(device_id, object_id,
                                        csr1000v_vm_bgp_interface_ip_address,
                                        csr1000v_vm_bgp_local_preference
                                        )

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_delete_csr1000v_vm_bgp_basic(self):

        device_id = 'dev001'
        object_id = 'host001'

        msa = self.get_msa_instance()
        res = msa.delete_csr1000v_vm_bgp_basic(device_id, object_id
                                        )

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_create_csr1000v_vm_bgp_peer(self):

        device_id = 'dev001'
        object_id = 'host001'
        csr1000v_vm_bgp_peer_ip_address = '10.0.0.1'
        csr1000v_vm_bgp_authkey = 'abc'
        csr1000v_vm_bgp_wan_interface = 'xyz'

        msa = self.get_msa_instance()
        res = msa.create_csr1000v_vm_bgp_peer(device_id, object_id,
                                            csr1000v_vm_bgp_peer_ip_address,
                                            csr1000v_vm_bgp_authkey,
                                            csr1000v_vm_bgp_wan_interface
                                        )

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_update_csr1000v_vm_bgp_peer(self):

        device_id = 'dev001'
        object_id = 'host001'
        csr1000v_vm_bgp_peer_ip_address = '10.0.0.1'
        csr1000v_vm_bgp_authkey = 'abc'
        csr1000v_vm_bgp_wan_interface = 'xyz'

        msa = self.get_msa_instance()
        res = msa.update_csr1000v_vm_bgp_peer(device_id, object_id,
                                            csr1000v_vm_bgp_peer_ip_address,
                                            csr1000v_vm_bgp_authkey,
                                            csr1000v_vm_bgp_wan_interface
                                        )

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_delete_csr1000v_vm_bgp_peer(self):

        device_id = 'dev001'
        object_id = 'host001'
        csr1000v_vm_bgp_peer_ip_address = '10.0.0.1'

        msa = self.get_msa_instance()
        res = msa.delete_csr1000v_vm_bgp_peer(device_id, object_id,
                                            csr1000v_vm_bgp_peer_ip_address
                                        )

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_create_csr1000v_vm_hsrp_primary(self):

        device_id = 'dev001'
        object_id = 'host001'
        csr1000v_vm_hsrp_vip = '10.0.0.1'
        csr1000v_vm_hsrp_priority = 10
        csr1000v_vm_hsrp_group_id = 'xyz123'
        csr1000v_vm_hsrp_authkey = 'xyz999'

        msa = self.get_msa_instance()
        res = msa.create_csr1000v_vm_hsrp_primary(device_id, object_id,
                                        csr1000v_vm_hsrp_vip,
                                        csr1000v_vm_hsrp_priority,
                                        csr1000v_vm_hsrp_group_id,
                                        csr1000v_vm_hsrp_authkey
                                        )

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_update_csr1000v_vm_hsrp_primary(self):

        device_id = 'dev001'
        object_id = 'host001'
        csr1000v_vm_hsrp_vip = '10.0.0.1'
        csr1000v_vm_hsrp_priority = 10
        csr1000v_vm_hsrp_group_id = 'xyz123'
        csr1000v_vm_hsrp_authkey = 'xyz999'

        msa = self.get_msa_instance()
        res = msa.update_csr1000v_vm_hsrp_primary(device_id, object_id,
                                        csr1000v_vm_hsrp_vip,
                                        csr1000v_vm_hsrp_priority,
                                        csr1000v_vm_hsrp_group_id,
                                        csr1000v_vm_hsrp_authkey
                                        )

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_delete_csr1000v_vm_hsrp_primary(self):

        device_id = 'dev001'
        object_id = 'host001'
        csr1000v_vm_hsrp_group_id = 'xyz123'

        msa = self.get_msa_instance()
        res = msa.delete_csr1000v_vm_hsrp_primary(device_id, object_id,
                                        csr1000v_vm_hsrp_group_id
                                        )

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_create_csr1000v_vm_hsrp_secondary(self):

        device_id = 'dev001'
        object_id = 'host001'
        csr1000v_vm_hsrp_vip = '10.0.0.1'
        csr1000v_vm_hsrp_priority = 10
        csr1000v_vm_hsrp_group_id = 'xyz123'
        csr1000v_vm_hsrp_authkey = 'xyz999'

        msa = self.get_msa_instance()
        res = msa.create_csr1000v_vm_hsrp_secondary(device_id, object_id,
                                        csr1000v_vm_hsrp_vip,
                                        csr1000v_vm_hsrp_priority,
                                        csr1000v_vm_hsrp_group_id,
                                        csr1000v_vm_hsrp_authkey
                                        )

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_update_csr1000v_vm_hsrp_secondary(self):

        device_id = 'dev001'
        object_id = 'host001'
        csr1000v_vm_hsrp_vip = '10.0.0.1'
        csr1000v_vm_hsrp_priority = 10
        csr1000v_vm_hsrp_group_id = 'xyz123'
        csr1000v_vm_hsrp_authkey = 'xyz999'

        msa = self.get_msa_instance()
        res = msa.update_csr1000v_vm_hsrp_secondary(device_id, object_id,
                                        csr1000v_vm_hsrp_vip,
                                        csr1000v_vm_hsrp_priority,
                                        csr1000v_vm_hsrp_group_id,
                                        csr1000v_vm_hsrp_authkey
                                        )

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_delete_csr1000v_vm_hsrp_secondary(self):

        device_id = 'dev001'
        object_id = 'host001'
        csr1000v_vm_hsrp_group_id = 'xyz123'

        msa = self.get_msa_instance()
        res = msa.delete_csr1000v_vm_hsrp_secondary(device_id, object_id,
                                        csr1000v_vm_hsrp_group_id
                                        )

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_create_csr1000v_vm_hsrp_tracking(self):

        device_id = 'dev001'
        object_id = 'host001'
        csr1000v_vm_interface_name = 'if001'
        csr1000v_vm_hsrp_group_id = 'abc123'
        csr1000v_vm_hsrp_track_segment = '10.1.0.1'
        csr1000v_vm_hsrp_track_netmask = '255.255.255.0'
        csr1000v_vm_hsrp_track_prioritycost = 1000
        csr1000v_vm_hsrp_track_group_id = 'xyz999'

        msa = self.get_msa_instance()
        res = msa.create_csr1000v_vm_hsrp_tracking(device_id, object_id,
                                        csr1000v_vm_interface_name,
                                        csr1000v_vm_hsrp_group_id,
                                        csr1000v_vm_hsrp_track_segment,
                                        csr1000v_vm_hsrp_track_netmask,
                                        csr1000v_vm_hsrp_track_prioritycost,
                                        csr1000v_vm_hsrp_track_group_id
                                        )

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_update_csr1000v_vm_hsrp_tracking(self):

        device_id = 'dev001'
        object_id = 'host001'
        csr1000v_vm_interface_name = 'if001'
        csr1000v_vm_hsrp_group_id = 'abc123'
        csr1000v_vm_hsrp_track_segment = '10.1.0.1'
        csr1000v_vm_hsrp_track_netmask = '255.255.255.0'
        csr1000v_vm_hsrp_track_prioritycost = 1000
        csr1000v_vm_hsrp_track_group_id = 'xyz999'

        msa = self.get_msa_instance()
        res = msa.update_csr1000v_vm_hsrp_tracking(device_id, object_id,
                                        csr1000v_vm_interface_name,
                                        csr1000v_vm_hsrp_group_id,
                                        csr1000v_vm_hsrp_track_segment,
                                        csr1000v_vm_hsrp_track_netmask,
                                        csr1000v_vm_hsrp_track_prioritycost,
                                        csr1000v_vm_hsrp_track_group_id
                                        )

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_delete_csr1000v_vm_hsrp_tracking(self):

        device_id = 'dev001'
        object_id = 'host001'
        csr1000v_vm_interface_name = 'if001'
        csr1000v_vm_hsrp_group_id = 'abc123'
        csr1000v_vm_hsrp_track_group_id = 'xyz999'

        msa = self.get_msa_instance()
        res = msa.delete_csr1000v_vm_hsrp_tracking(device_id, object_id,
                                        csr1000v_vm_interface_name,
                                        csr1000v_vm_hsrp_group_id,
                                        csr1000v_vm_hsrp_track_group_id
                                        )

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_create_csr1000v_vm_hsrp_interface_tracking(self):

        device_id = 'dev001'
        object_id = 'host001'
        csr1000v_vm_interface_name = 'if001'
        csr1000v_vm_hsrp_group_id = 'abc123'
        csr1000v_vm_hsrp_track_interface_name = 'xyz999'
        csr1000v_vm_hsrp_track_prioritycost = 100
        csr1000v_vm_hsrp_track_group_id = 'aaa001'

        msa = self.get_msa_instance()
        res = msa.create_csr1000v_vm_hsrp_interface_tracking(
                                        device_id, object_id,
                                        csr1000v_vm_interface_name,
                                        csr1000v_vm_hsrp_group_id,
                                        csr1000v_vm_hsrp_track_interface_name,
                                        csr1000v_vm_hsrp_track_prioritycost,
                                        csr1000v_vm_hsrp_track_group_id
                                        )

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_update_csr1000v_vm_hsrp_interface_tracking(self):

        device_id = 'dev001'
        object_id = 'host001'
        csr1000v_vm_interface_name = 'if001'
        csr1000v_vm_hsrp_group_id = 'abc123'
        csr1000v_vm_hsrp_track_interface_name = 'xyz999'
        csr1000v_vm_hsrp_track_prioritycost = 100
        csr1000v_vm_hsrp_track_group_id = 'aaa001'

        msa = self.get_msa_instance()
        res = msa.update_csr1000v_vm_hsrp_interface_tracking(
                                        device_id, object_id,
                                        csr1000v_vm_interface_name,
                                        csr1000v_vm_hsrp_group_id,
                                        csr1000v_vm_hsrp_track_interface_name,
                                        csr1000v_vm_hsrp_track_prioritycost,
                                        csr1000v_vm_hsrp_track_group_id
                                        )

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_delete_csr1000v_vm_hsrp_interface_tracking(self):

        device_id = 'dev001'
        object_id = 'host001'
        csr1000v_vm_interface_name = 'if001'
        csr1000v_vm_hsrp_group_id = 'abc123'
        csr1000v_vm_hsrp_track_group_id = 'xyz999'

        msa = self.get_msa_instance()
        res = msa.delete_csr1000v_vm_hsrp_interface_tracking(
                                        device_id, object_id,
                                        csr1000v_vm_interface_name,
                                        csr1000v_vm_hsrp_group_id,
                                        csr1000v_vm_hsrp_track_group_id
                                        )

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_create_csr1000v_vm_snmp(self):

        device_id = 'dev001'
        object_id = 'host001'
        csr1000v_vm_snmp_community = 'if001'
        csr1000v_vm_snmp_trap_source_interface = 'abc123'
        csr1000v_vm_snmp_trap_destination_ip_address = '10.0.0.1'
        csr1000v_vm_snmp_trap_version = '2c'

        msa = self.get_msa_instance()
        res = msa.create_csr1000v_vm_snmp(device_id, object_id,
                                csr1000v_vm_snmp_community,
                                csr1000v_vm_snmp_trap_source_interface,
                                csr1000v_vm_snmp_trap_destination_ip_address,
                                csr1000v_vm_snmp_trap_version
                                        )

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_update_csr1000v_vm_snmp(self):

        device_id = 'dev001'
        object_id = 'host001'
        csr1000v_vm_snmp_community = 'if001'
        csr1000v_vm_snmp_trap_source_interface = 'abc123'
        csr1000v_vm_snmp_trap_destination_ip_address = '10.0.0.1'
        csr1000v_vm_snmp_trap_version = '2c'

        msa = self.get_msa_instance()
        res = msa.update_csr1000v_vm_snmp(device_id, object_id,
                                csr1000v_vm_snmp_community,
                                csr1000v_vm_snmp_trap_source_interface,
                                csr1000v_vm_snmp_trap_destination_ip_address,
                                csr1000v_vm_snmp_trap_version
                                        )

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_delete_csr1000v_vm_snmp(self):

        device_id = 'dev001'
        object_id = 'host001'

        msa = self.get_msa_instance()
        res = msa.delete_csr1000v_vm_snmp(device_id, object_id)

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_create_csr1000v_vm_syslog(self):

        device_id = 'dev001'
        object_id = 'host001'
        csr1000v_vm_syslog_server_ip_address = '10.0.0.1'
        csr1000v_vm_syslog_source_interface = 'abc123'
        csr1000v_vm_syslog_facility = 'local0'
        csr1000v_vm_syslog_severity = 'warning'

        msa = self.get_msa_instance()
        res = msa.create_csr1000v_vm_syslog(device_id, object_id,
                                    csr1000v_vm_syslog_server_ip_address,
                                    csr1000v_vm_syslog_source_interface,
                                    csr1000v_vm_syslog_facility,
                                    csr1000v_vm_syslog_severity
                                        )

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_update_csr1000v_vm_syslog(self):

        device_id = 'dev001'
        object_id = 'host001'
        csr1000v_vm_syslog_server_ip_address = '10.0.0.1'
        csr1000v_vm_syslog_source_interface = 'abc123'
        csr1000v_vm_syslog_facility = 'local0'
        csr1000v_vm_syslog_severity = 'warning'

        msa = self.get_msa_instance()
        res = msa.update_csr1000v_vm_syslog(device_id, object_id,
                                    csr1000v_vm_syslog_server_ip_address,
                                    csr1000v_vm_syslog_source_interface,
                                    csr1000v_vm_syslog_facility,
                                    csr1000v_vm_syslog_severity
                                        )

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_delete_csr1000v_vm_syslog(self):

        device_id = 'dev001'
        object_id = 'host001'
        csr1000v_vm_syslog_server_ip_address = '10.0.0.1'
        csr1000v_vm_syslog_source_interface = 'abc123'

        msa = self.get_msa_instance()
        res = msa.delete_csr1000v_vm_syslog(device_id, object_id,
                                    csr1000v_vm_syslog_server_ip_address,
                                    csr1000v_vm_syslog_source_interface
                                        )

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_create_csr1000v_vm_ntp(self):

        device_id = 'dev001'
        object_id = 'host001'
        csr1000v_vm_ntp_server_ip_address = '10.0.0.1'
        csr1000v_vm_ntp_source_interface = 'abc123'

        msa = self.get_msa_instance()
        res = msa.create_csr1000v_vm_ntp(device_id, object_id,
                                    csr1000v_vm_ntp_server_ip_address,
                                    csr1000v_vm_ntp_source_interface
                                        )

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_update_csr1000v_vm_ntp(self):

        device_id = 'dev001'
        object_id = 'host001'
        csr1000v_vm_ntp_server_ip_address = '10.0.0.1'
        csr1000v_vm_ntp_source_interface = 'abc123'

        msa = self.get_msa_instance()
        res = msa.update_csr1000v_vm_ntp(device_id, object_id,
                                    csr1000v_vm_ntp_server_ip_address,
                                    csr1000v_vm_ntp_source_interface
                                        )

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_delete_csr1000v_vm_ntp(self):

        device_id = 'dev001'
        object_id = 'host001'
        csr1000v_vm_ntp_server_ip_address = '10.0.0.1'
        csr1000v_vm_ntp_source_interface = 'abc123'

        msa = self.get_msa_instance()
        res = msa.delete_csr1000v_vm_ntp(device_id, object_id,
                                    csr1000v_vm_ntp_server_ip_address,
                                    csr1000v_vm_ntp_source_interface
                                        )

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_create_csr1000v_vm_defaultroute(self):

        device_id = 'dev001'
        object_id = 'host001'
        ip_address = '10.0.0.1'
        netmask = 'abc123'
        nexthop_address = '10.0.0.2'

        msa = self.get_msa_instance()
        res = msa.create_csr1000v_vm_defaultroute(device_id, object_id,
                                    ip_address,
                                    netmask,
                                    nexthop_address
                                    )

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_update_csr1000v_vm_defaultroute(self):

        device_id = 'dev001'
        object_id = 'host001'
        ip_address = '10.0.0.1'
        netmask = 'abc123'
        nexthop_address = '10.0.0.2'

        msa = self.get_msa_instance()
        res = msa.update_csr1000v_vm_defaultroute(device_id, object_id,
                                    ip_address,
                                    netmask,
                                    nexthop_address
                                    )

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_delete_csr1000v_vm_defaultroute(self):

        device_id = 'dev001'
        object_id = 'host001'
        ip_address = '10.0.0.1'
        netmask = 'abc123'
        nexthop_address = '10.0.0.2'

        msa = self.get_msa_instance()
        res = msa.delete_csr1000v_vm_defaultroute(device_id, object_id,
                                    ip_address,
                                    netmask,
                                    nexthop_address
                                    )

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_create_csr1000v_vm_dns(self):

        device_id = 'dev001'
        object_id = 'host001'
        ip_address = '10.0.0.1'

        msa = self.get_msa_instance()
        res = msa.create_csr1000v_vm_dns(device_id, object_id,
                                    ip_address)

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_update_csr1000v_vm_dns(self):

        device_id = 'dev001'
        object_id = 'host001'
        ip_address = '10.0.0.1'

        msa = self.get_msa_instance()
        res = msa.update_csr1000v_vm_dns(device_id, object_id,
                                    ip_address)

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_delete_csr1000v_vm_dns(self):

        device_id = 'dev001'
        object_id = 'host001'
        ip_address = '10.0.0.1'

        msa = self.get_msa_instance()
        res = msa.delete_csr1000v_vm_dns(device_id, object_id,
                                    ip_address)

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_create_csr1000v_vm_license(self):

        device_id = 'dev001'
        object_id = 'host001'
        idtoken = 'abc123'

        msa = self.get_msa_instance()
        res = msa.create_csr1000v_vm_license(device_id, object_id,
                                    idtoken
                                    )

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_update_csr1000v_vm_license(self):

        device_id = 'dev001'
        object_id = 'host001'
        idtoken = 'abc123'

        msa = self.get_msa_instance()
        res = msa.update_csr1000v_vm_license(device_id, object_id,
                                    idtoken
                                    )

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_delete_csr1000v_vm_license(self):

        device_id = 'dev001'
        object_id = 'host001'

        msa = self.get_msa_instance()
        res = msa.delete_csr1000v_vm_license(device_id, object_id)

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_create_csr1000v_vm_throughput(self):

        device_id = 'dev001'
        object_id = 'host001'
        throughput = 10

        msa = self.get_msa_instance()
        res = msa.create_csr1000v_vm_throughput(device_id, object_id,
                                    throughput
                                    )

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_update_csr1000v_vm_throughput(self):

        device_id = 'dev001'
        object_id = 'host001'
        throughput = 10

        msa = self.get_msa_instance()
        res = msa.update_csr1000v_vm_throughput(device_id, object_id,
                                    throughput
                                    )

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_delete_csr1000v_vm_throughput(self):

        device_id = 'dev001'
        object_id = 'host001'

        msa = self.get_msa_instance()
        res = msa.delete_csr1000v_vm_throughput(device_id, object_id)

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_create_csr1000v_vm_tunnel_interface(self):

        device_id = 'dev001'
        object_id = 'host001'
        ip_address = '10.0.01'
        netmask = '255.255.255.0'
        segment = '10.0.0.2'
        netmask_cidr = 24
        destination_ip_address = '192.168.0.1'
        interface = 'GigabitEthernet1'
        profile_name = 'VTI'

        msa = self.get_msa_instance()
        res = msa.create_csr1000v_vm_tunnel_interface(device_id, object_id,
                                            ip_address,
                                            netmask,
                                            segment,
                                            netmask_cidr,
                                            destination_ip_address,
                                            interface,
                                            profile_name
                                    )

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_update_csr1000v_vm_tunnel_interface(self):

        device_id = 'dev001'
        object_id = 'host001'
        ip_address = '10.0.01'
        netmask = '255.255.255.0'
        segment = '10.0.0.2'
        netmask_cidr = 24
        destination_ip_address = '192.168.0.1'
        interface = 'GigabitEthernet1'
        profile_name = 'VTI'

        msa = self.get_msa_instance()
        res = msa.update_csr1000v_vm_tunnel_interface(device_id, object_id,
                                            ip_address,
                                            netmask,
                                            segment,
                                            netmask_cidr,
                                            destination_ip_address,
                                            interface,
                                            profile_name
                                    )

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_delete_csr1000v_vm_tunnel_interface(self):

        device_id = 'dev001'
        object_id = 'host001'
        ip_address = '10.0.01'
        netmask = '255.255.255.0'
        segment = '10.0.0.2'
        netmask_cidr = 24
        destination_ip_address = '192.168.0.1'
        interface = 'GigabitEthernet1'
        profile_name = 'VTI'

        msa = self.get_msa_instance()
        res = msa.delete_csr1000v_vm_tunnel_interface(device_id, object_id,
                                            ip_address,
                                            netmask,
                                            segment,
                                            netmask_cidr,
                                            destination_ip_address,
                                            interface,
                                            profile_name
                                    )

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_create_csr1000v_vm_ipsec_basic_esp(self):

        device_id = 'dev001'
        object_id = 'host001'
        params = {
            'priority': 1,
            'encryption_algorithm': '3des',
            'hash_algorithm': 'md5',
            'diffie_hellman_group': 2,
            'isakmp_sa_lifetime': '86400',
            'transform_set': 'IPSEC',
            'encryption_transform': 'esp-3des',
            'authentication_transform': 'esp-md5-hmac',
            'ipsec_sa_lifetime': '3600',
            'profile_name': 'VTI',
        }

        msa = self.get_msa_instance()
        res = msa.create_csr1000v_vm_ipsec_basic_esp(device_id, object_id,
                                                     params)

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_update_csr1000v_vm_ipsec_basic_esp(self):

        device_id = 'dev001'
        object_id = 'host001'
        params = {
            'priority': 1,
            'encryption_algorithm': '3des',
            'hash_algorithm': 'md5',
            'diffie_hellman_group': 2,
            'isakmp_sa_lifetime': '86400',
            'transform_set': 'IPSEC',
            'encryption_transform': 'esp-3des',
            'authentication_transform': 'esp-md5-hmac',
            'ipsec_sa_lifetime': '3600',
            'profile_name': 'VTI',
        }

        msa = self.get_msa_instance()
        res = msa.update_csr1000v_vm_ipsec_basic_esp(device_id, object_id,
                                                     params)

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_delete_csr1000v_vm_ipsec_basic_esp(self):

        device_id = 'dev001'
        object_id = 'host001'
        params = {
            'priority': 1,
            'transform_set': 'IPSEC',
            'profile_name': 'VTI',
        }

        msa = self.get_msa_instance()
        res = msa.delete_csr1000v_vm_ipsec_basic_esp(device_id, object_id,
                                                     params)

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_create_csr1000v_vm_ipsec_basic_ah(self):

        device_id = 'dev001'
        object_id = 'host001'
        params = {
            'priority': 1,
            'encryption_algorithm': '3des',
            'hash_algorithm': 'md5',
            'diffie_hellman_group': 2,
            'isakmp_sa_lifetime': '86400',
            'transform_set': 'IPSEC',
            'authentication_transform': 'ah-md5-hmac',
            'ipsec_sa_lifetime': '3600',
            'profile_name': 'VTI',
        }

        msa = self.get_msa_instance()
        res = msa.create_csr1000v_vm_ipsec_basic_ah(device_id, object_id,
                                                    params)

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_update_csr1000v_vm_ipsec_basic_ah(self):

        device_id = 'dev001'
        object_id = 'host001'
        params = {
            'priority': 1,
            'encryption_algorithm': '3des',
            'hash_algorithm': 'md5',
            'diffie_hellman_group': 2,
            'isakmp_sa_lifetime': '86400',
            'transform_set': 'IPSEC',
            'authentication_transform': 'ah-md5-hmac',
            'ipsec_sa_lifetime': '3600',
            'profile_name': 'VTI',
        }

        msa = self.get_msa_instance()
        res = msa.update_csr1000v_vm_ipsec_basic_ah(device_id, object_id,
                                                    params)

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_delete_csr1000v_vm_ipsec_basic_ah(self):

        device_id = 'dev001'
        object_id = 'host001'
        params = {
            'priority': 1,
            'transform_set': 'IPSEC',
            'profile_name': 'VTI',
        }

        msa = self.get_msa_instance()
        res = msa.delete_csr1000v_vm_ipsec_basic_ah(device_id, object_id,
                                                    params)

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_create_csr1000v_vm_ipsec_peer(self):

        device_id = 'dev001'
        object_id = 'host001'
        ip_address = '10.0.0.1'
        pre_shared_key = 'key'

        msa = self.get_msa_instance()
        res = msa.create_csr1000v_vm_ipsec_peer(device_id, object_id,
                                        ip_address,
                                        pre_shared_key
                                    )

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_update_csr1000v_vm_ipsec_peer(self):

        device_id = 'dev001'
        object_id = 'host001'
        ip_address = '10.0.0.1'
        pre_shared_key = 'key'

        msa = self.get_msa_instance()
        res = msa.update_csr1000v_vm_ipsec_peer(device_id, object_id,
                                        ip_address,
                                        pre_shared_key
                                    )

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_delete_csr1000v_vm_ipsec_peer(self):

        device_id = 'dev001'
        object_id = 'host001'
        ip_address = '10.0.0.1'
        pre_shared_key = 'key'

        msa = self.get_msa_instance()
        res = msa.delete_csr1000v_vm_ipsec_peer(device_id, object_id,
                                        ip_address,
                                        pre_shared_key
                                    )

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_create_csr1000v_vm_staticroute_for_dc(self):

        device_id = 'dev001'
        object_id = 'static001'
        ip_address = '10.0.0.1'
        netmask = '255.255.255.0'
        nexthop_address = '10.0.0.2'
        interface = 'GigabitEthernet2'
        netmask_cidr = 24

        msa = self.get_msa_instance()
        res = msa.create_csr1000v_vm_staticroute_for_dc(device_id, object_id,
                                            ip_address,
                                            netmask,
                                            nexthop_address,
                                            interface,
                                            netmask_cidr
                                    )

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_update_csr1000v_vm_staticroute_for_dc(self):

        device_id = 'dev001'
        object_id = 'static001'
        ip_address = '10.0.0.1'
        netmask = '255.255.255.0'
        nexthop_address = '10.0.0.2'
        interface = 'GigabitEthernet2'
        netmask_cidr = 24

        msa = self.get_msa_instance()
        res = msa.update_csr1000v_vm_staticroute_for_dc(device_id, object_id,
                                            ip_address,
                                            netmask,
                                            nexthop_address,
                                            interface,
                                            netmask_cidr
                                    )

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_delete_csr1000v_vm_staticroute_for_dc(self):

        device_id = 'dev001'
        object_id = 'static001'
        ip_address = '10.0.0.1'
        netmask = '255.255.255.0'
        nexthop_address = '10.0.0.2'
        interface = 'GigabitEthernet2'
        netmask_cidr = 24

        msa = self.get_msa_instance()
        res = msa.delete_csr1000v_vm_staticroute_for_dc(device_id, object_id,
                                            ip_address,
                                            netmask,
                                            nexthop_address,
                                            interface,
                                            netmask_cidr
                                    )

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)
