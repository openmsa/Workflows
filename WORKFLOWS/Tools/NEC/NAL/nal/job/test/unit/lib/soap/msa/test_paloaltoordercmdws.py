import inspect
import unittest

from job.auto.extension import routingpod
from job.lib.soap.msa import paloaltoordercmdws
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

        msa_instance = paloaltoordercmdws.PaloaltoOrderCommandWs(
                            job_instance.job_config,
                            job_instance.nal_endpoint_config,
                            pod_id)

        return msa_instance

    def test_create_paloalto_vsys(self):

        device_id = 'dev001'
        vsys_id = 2
        paloalto_vsys_display_name = 'vsys001'

        res = self.get_msa_instance()\
                .create_paloalto_vsys(
                    device_id, vsys_id, paloalto_vsys_display_name)
        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_delete_paloalto_vsys(self):

        device_id = 'dev001'
        vsys_id = 2

        res = self.get_msa_instance()\
                .delete_paloalto_vsys(device_id, vsys_id)
        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_create_paloalto_system_vsys_users(self):

        device_id = 'dev001'
        virtual_system_user_name = 'system'
        paloalto_system_user_password = 'abcdefg'
        paloalto_system_vsys_name = 'vsys001'

        res = self.get_msa_instance()\
                .create_paloalto_system_vsys_users(
                                        device_id,
                                        virtual_system_user_name,
                                        paloalto_system_user_password,
                                        paloalto_system_vsys_name)
        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_delete_paloalto_system_vsys_users(self):

        device_id = 'dev001'
        virtual_system_user_name = 'system'

        res = self.get_msa_instance()\
                .delete_paloalto_system_vsys_users(
                                    device_id, virtual_system_user_name)
        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_create_paloalto_network_interface_mngprofile(self):

        device_id = 'dev001'
        interface_management_profile_name = 'mng123'
        paloalto_network_interface_snmp_action = 'yes'
        paloalto_network_interface_ssh_action = 'no'
        paloalto_network_interface_https_action = 'yes'
        paloalto_network_interface_ping_action = 'no'

        res = self.get_msa_instance()\
                .create_paloalto_network_interface_mngprofile(
                                device_id,
                                interface_management_profile_name,
                                paloalto_network_interface_snmp_action,
                                paloalto_network_interface_ssh_action,
                                paloalto_network_interface_https_action,
                                paloalto_network_interface_ping_action)
        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_delete_paloalto_network_interface_mngprofile(self):

        device_id = 'dev001'
        interface_management_profile_name = 'mng123'

        res = self.get_msa_instance()\
                .delete_paloalto_network_interface_mngprofile(
                        device_id, interface_management_profile_name)
        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_create_paloalto_network_subinterface(self):

        device_id = 'dev001'
        sub_interface_name = 'sub123'
        paloalto_network_interface_name = 'if001'
        paloalto_network_subinterface_ip_address = '192.168.0.1'
        paloalto_network_subinterface_netmask = '255.255.255.0'
        paloalto_network_subinterface_vlan = 'v123'
        paloalto_network_profile_name = 'nw001'

        res = self.get_msa_instance()\
                .create_paloalto_network_subinterface(
                                device_id,
                                sub_interface_name,
                                paloalto_network_interface_name,
                                paloalto_network_subinterface_ip_address,
                                paloalto_network_subinterface_netmask,
                                paloalto_network_subinterface_vlan,
                                paloalto_network_profile_name)
        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_delete_paloalto_network_subinterface(self):

        device_id = 'dev001'
        sub_interface_name = 'sub123'
        paloalto_network_interface_name = 'if001'

        res = self.get_msa_instance()\
                .delete_paloalto_network_subinterface(
                                    device_id,
                                    sub_interface_name,
                                    paloalto_network_interface_name)
        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_create_paloalto_vsys_zone(self):

        device_id = 'dev001'
        zone_name = 'zone123'
        paloalto_vsys_name = 'vsys001'

        res = self.get_msa_instance()\
                .create_paloalto_vsys_zone(
                                    device_id,
                                    zone_name, paloalto_vsys_name)
        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_delete_paloalto_vsys_zone(self):

        device_id = 'dev001'
        zone_name = 'zone123'
        paloalto_vsys_name = 'vsys001'

        res = self.get_msa_instance()\
                .delete_paloalto_vsys_zone(
                                    device_id,
                                    zone_name, paloalto_vsys_name)
        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_create_paloalto_network_virtualrouter(self):

        device_id = 'dev001'
        virtual_router_name = 'rt123'

        res = self.get_msa_instance()\
                .create_paloalto_network_virtualrouter(
                                    device_id,
                                    virtual_router_name)
        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_delete_paloalto_network_virtualrouter(self):

        device_id = 'dev001'
        virtual_router_name = 'rt123'

        res = self.get_msa_instance()\
                .delete_paloalto_network_virtualrouter(
                                    device_id,
                                    virtual_router_name)
        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_create_paloalto_network_vrouter_mapping(self):

        device_id = 'dev001'
        vrouter_name = 'rt123'
        interface_name = 'if123'

        res = self.get_msa_instance()\
                .create_paloalto_network_vrouter_mapping(device_id,
                                    vrouter_name, interface_name)
        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_delete_paloalto_network_vrouter_mapping(self):

        device_id = 'dev001'
        vrouter_name = 'rt123'

        res = self.get_msa_instance()\
                .delete_paloalto_network_vrouter_mapping(device_id,
                                    vrouter_name)
        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_create_paloalto_network_staticroute(self):

        device_id = 'dev001'
        static_route_name = 'st123'
        paloalto_network_staticroute_vrouter = 'vs123'
        paloalto_network_staticroute_destination_address = '192.168.0.1'
        paloalto_network_staticroute_destination_netmask = '255.255.255.0'
        paloalto_network_staticroute_nexthop_address = '10.0.0.1'
        paloalto_network_staticroute_source_interface = 'http'

        res = self.get_msa_instance()\
                .create_paloalto_network_staticroute(device_id,
                    static_route_name,
                    paloalto_network_staticroute_vrouter,
                    paloalto_network_staticroute_destination_address,
                    paloalto_network_staticroute_destination_netmask,
                    paloalto_network_staticroute_nexthop_address,
                    paloalto_network_staticroute_source_interface)
        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_delete_paloalto_network_staticroute(self):

        device_id = 'dev001'
        static_route_name = 'st123'
        paloalto_network_staticroute_vrouter = 'vr123'

        res = self.get_msa_instance()\
                .delete_paloalto_network_staticroute(device_id,
                                static_route_name,
                                paloalto_network_staticroute_vrouter)
        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_create_paloalto_vsys_interface_importing(self):

        device_id = 'dev001'
        vsys_name = 'vsys123'
        interface_name = 'if123'

        res = self.get_msa_instance()\
                .create_paloalto_vsys_interface_importing(device_id,
                                            vsys_name, interface_name)
        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_delete_paloalto_vsys_interface_importing(self):

        device_id = 'dev001'
        vsys_name = 'vsys123'

        res = self.get_msa_instance()\
                .delete_paloalto_vsys_interface_importing(device_id,
                                                          vsys_name)
        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_create_paloalto_vsys_vrouter_importing(self):

        device_id = 'dev001'
        vsys_name = 'vsys123'
        vrouter_name = 'vr123'

        res = self.get_msa_instance()\
                .create_paloalto_vsys_vrouter_importing(device_id,
                                            vsys_name, vrouter_name)
        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_delete_paloalto_vsys_vrouter_importing(self):

        device_id = 'dev001'
        vsys_name = 'vsys123'

        res = self.get_msa_instance()\
                .delete_paloalto_vsys_vrouter_importing(device_id, vsys_name)

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_create_paloalto_vsys_zone_mapping(self):

        device_id = 'dev001'
        zone_name = 'zone123'
        paloalto_vsys_name = 'vsys123'
        interface_name = 'if123'

        res = self.get_msa_instance()\
                .create_paloalto_vsys_zone_mapping(device_id,
                                        zone_name,
                                        paloalto_vsys_name,
                                        interface_name)
        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_delete_paloalto_vsys_zone_mapping(self):

        device_id = 'dev001'
        zone_name = 'zone123'
        paloalto_vsys_name = 'vsys123'

        res = self.get_msa_instance()\
                .delete_paloalto_vsys_zone_mapping(device_id,
                                    zone_name, paloalto_vsys_name)
        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_create_paloalto_paloalto_ipv6_interface(self):

        device_id = 'dev001'
        object_id = 'ethernet1/3.1'
        interface = 'ethernet1/3'
        ipv6_address = '2003::'
        netmask = '64'

        res = self.get_msa_instance()\
                .create_paloalto_paloalto_ipv6_interface(device_id,
                                                             object_id,
                                                             interface,
                                                             ipv6_address,
                                                             netmask)
        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_delete_paloalto_paloalto_ipv6_interface(self):

        device_id = 'dev001'
        object_id = 'ethernet1/3.1'

        res = self.get_msa_instance()\
                .delete_paloalto_paloalto_ipv6_interface(device_id,
                                                            object_id)
        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_create_paloalto_paloalto_ipv6_interface_enable(self):

        device_id = 'dev001'
        object_id = 'ethernet1/3.1'
        interface = 'ethernet1/3'

        res = self.get_msa_instance()\
                .create_paloalto_paloalto_ipv6_interface_enable(device_id,
                                                            object_id,
                                                            interface)
        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_delete_paloalto_paloalto_ipv6_interface_enable(self):

        device_id = 'dev001'
        object_id = 'ethernet1/3.1'
        interface = 'ethernet1/3'

        res = self.get_msa_instance()\
                .delete_paloalto_paloalto_ipv6_interface_enable(device_id,
                                                            object_id,
                                                            interface)
        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_create_paloalto_paloalto_ipv6_static_route(self):

        device_id = 'dev001'
        object_id = 'ipv6defaultroute'
        destination_ipv6_address = '::'
        destination_netmask = '0'
        ipv6_address = '2001:260:88:0040::FF11'
        source_interface = 'ethernet1/3.1'

        res = self.get_msa_instance()\
                .create_paloalto_paloalto_ipv6_static_route(device_id,
                                          object_id,
                                          destination_ipv6_address,
                                          destination_netmask,
                                          ipv6_address,
                                          source_interface)
        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_delete_paloalto_paloalto_ipv6_static_route(self):

        device_id = 'dev001'
        object_id = 'ipv6defaultroute'

        res = self.get_msa_instance()\
                .delete_paloalto_paloalto_ipv6_static_route(device_id,
                                                        object_id)
        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_create_paloalto_paloalto_permitted_ip(self):

        device_id = 'dev001'
        object_id = 'ipv6defaultroute'
        profile_name = 'TenantA-Ext'
        ip_address = '2001:260:88:0040::'
        netmask = '64'

        res = self.get_msa_instance()\
                .create_paloalto_paloalto_permitted_ip(device_id,
                                          object_id,
                                          profile_name,
                                          ip_address,
                                          netmask)
        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_delete_paloalto_paloalto_permitted_ip(self):

        device_id = 'dev001'
        object_id = '1'
        profile_name = 'TenantA-Ext'
        ip_address = '2001:260:88:0040::'
        netmask = '64'

        res = self.get_msa_instance()\
                .delete_paloalto_paloalto_permitted_ip(device_id,
                                          object_id,
                                          profile_name,
                                          ip_address,
                                          netmask)
        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)
