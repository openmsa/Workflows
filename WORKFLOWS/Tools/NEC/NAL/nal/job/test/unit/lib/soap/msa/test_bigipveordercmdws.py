import inspect
import unittest

from job.auto.extension import routingpod
from job.lib.soap.msa import bigipveordercmdws
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

        job_input = {'type': 2, 'device_type': 1,
                     'operation_id': 'TestSoapUser'}

        job_instance = routingpod.RoutingPod()
        ret = job_instance.routing_pod(job_input)

        pod_id = ret['pod_id']

        msa_instance = bigipveordercmdws.BigIpVeOrderCommandWs(
                            job_instance.job_config,
                            job_instance.nal_endpoint_config,
                            pod_id)

        return msa_instance

    def test_create_big_ip_ve_system_common(self):

        device_id = 'dev001'
        host_name = 'host001'
        bigip_ve_system_common_domain = 'dm001'

        msa = self.get_msa_instance()
        res = msa.create_big_ip_ve_system_common(device_id,
                                    host_name,
                                    bigip_ve_system_common_domain)
        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_delete_big_ip_ve_system_common(self):

        device_id = 'dev001'
        host_name = 'host001'

        msa = self.get_msa_instance()
        res = msa.delete_big_ip_ve_system_common(device_id,
                                    host_name)
        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_create_big_ip_ve_network_vlan(self):

        device_id = 'dev001'
        vlan_name = 'vlan001'
        bigip_ve_network_interface_name = 'if001'

        msa = self.get_msa_instance()
        res = msa.create_big_ip_ve_network_vlan(device_id,
                                vlan_name,
                                bigip_ve_network_interface_name)
        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_delete_big_ip_ve_network_vlan(self):

        device_id = 'dev001'
        vlan_name = 'vlan001'

        msa = self.get_msa_instance()
        res = msa.delete_big_ip_ve_network_vlan(device_id,
                                    vlan_name)
        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_create_big_ip_network_self_ip(self):

        device_id = 'dev001'
        bigip_ve_network_self_ip_name = 'ip001'
        bigip_ve_network_self_ip_address = '10.0.0.1'
        bigip_ve_network_self_ip_netmask = '255.255.255.0'
        bigip_ve_network_vlan_name = 'vlan001'

        msa = self.get_msa_instance()
        res = msa.create_big_ip_network_self_ip(device_id,
                                bigip_ve_network_self_ip_name,
                                bigip_ve_network_self_ip_address,
                                bigip_ve_network_self_ip_netmask,
                                bigip_ve_network_vlan_name)
        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_delete_big_ip_network_self_ip(self):

        device_id = 'dev001'
        bigip_ve_network_self_ip_name = 'ip001'

        msa = self.get_msa_instance()
        res = msa.delete_big_ip_network_self_ip(device_id,
                                    bigip_ve_network_self_ip_name)
        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_create_big_ip_system_dns(self):

        device_id = 'dev001'
        host_name = 'host001'
        ip_address1 = '10.0.0.1'
        ip_address2 = '192.168.0.1'

        msa = self.get_msa_instance()
        res = msa.create_big_ip_system_dns(device_id,
                                        host_name,
                                        ip_address1,
                                        ip_address2)
        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_delete_big_ip_system_dns(self):

        device_id = 'dev001'
        host_name = 'host001'

        msa = self.get_msa_instance()
        res = msa.delete_big_ip_system_dns(device_id,
                                    host_name)
        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_create_big_ip_system_snmp_trap(self):

        device_id = 'dev001'
        server_name = 'sv001'
        bigip_ve_system_snmp_trap_community = '?'
        bigip_ve_system_snmp_trap_server_address = '192.168.0.1'

        msa = self.get_msa_instance()
        res = msa.create_big_ip_system_snmp_trap(device_id,
                            server_name,
                            bigip_ve_system_snmp_trap_community,
                            bigip_ve_system_snmp_trap_server_address)
        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_delete_big_ip_system_snmp_trap(self):

        device_id = 'dev001'
        server_name = 'sv001'

        msa = self.get_msa_instance()
        res = msa.delete_big_ip_system_snmp_trap(device_id,
                                    server_name)
        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_create_big_ip_system_snmp(self):

        device_id = 'dev001'
        community_name = 'sv001'
        ip_address = '192.168.0.1'

        msa = self.get_msa_instance()
        res = msa.create_big_ip_system_snmp(device_id,
                                            community_name,
                                            ip_address)
        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_delete_big_ip_system_snmp(self):

        device_id = 'dev001'
        community_name = 'sv001'
        bigip_ve_snmp_server_end_number = '10'

        msa = self.get_msa_instance()
        res = msa.delete_big_ip_system_snmp(device_id,
                                            community_name,
                            bigip_ve_snmp_server_end_number)
        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_create_big_ip_system_ntp(self):

        device_id = 'dev001'
        host_name = 'host001'
        ip_address1 = '10.0.0.1'
        ip_address2 = '192.168.0.1'
        bigip_ve_system_ntp_timezone = 'Asia/Tokyo'

        msa = self.get_msa_instance()
        res = msa.create_big_ip_system_ntp(device_id,
                                    host_name,
                                    ip_address1,
                                    ip_address2,
                                    bigip_ve_system_ntp_timezone)
        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_delete_big_ip_system_ntp(self):

        device_id = 'dev001'
        host_name = 'host001'

        msa = self.get_msa_instance()
        res = msa.delete_big_ip_system_ntp(device_id,
                                    host_name)
        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_create_big_ip_network_routes(self):

        device_id = 'dev001'
        route_name = 'rt001'
        bigip_ve_network_routes_default_gateway_action = 'action'
        bigip_ve_network_routes_gateway_address = '192.168.0.0'
        bigip_ve_network_routes_network_address = '192.168.0.1'
        bigip_ve_network_routes_netmask = '255.255.255.0'

        msa = self.get_msa_instance()
        res = msa.create_big_ip_network_routes(device_id,
                        route_name,
                        bigip_ve_network_routes_default_gateway_action,
                        bigip_ve_network_routes_gateway_address,
                        bigip_ve_network_routes_network_address,
                        bigip_ve_network_routes_netmask)
        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_delete_big_ip_network_routes(self):

        device_id = 'dev001'
        route_no = '2001'

        msa = self.get_msa_instance()
        res = msa.delete_big_ip_network_routes(device_id,
                                    route_no)
        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_create_big_ip_system_admin_account(self):

        device_id = 'dev001'
        user_name = 'admin'
        bigip_ve_system_user_password = 'passw0rd'

        msa = self.get_msa_instance()
        res = msa.create_big_ip_system_admin_account(device_id,
                                user_name,
                                bigip_ve_system_user_password)
        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_delete_big_ip_system_admin_account(self):

        device_id = 'dev001'
        user_name = 'admin'

        msa = self.get_msa_instance()
        res = msa.delete_big_ip_system_admin_account(device_id,
                                    user_name)
        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_create_f5_bigipve_ipv6_selfip(self):

        device_id = 'dev001'
        object_id = 'selfipv6'
        self_ipv6_address = 'dead:beef::3'
        self_ipv6_netmask = 48
        vlan_name = 'vlan001'

        msa = self.get_msa_instance()
        res = msa.create_f5_bigipve_ipv6_selfip(device_id, object_id,
                                        self_ipv6_address,
                                        self_ipv6_netmask,
                                        vlan_name)

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_delete_f5_bigipve_ipv6_selfip(self):

        device_id = 'dev001'
        object_id = 'selfipv6'

        msa = self.get_msa_instance()
        res = msa.delete_f5_bigipve_ipv6_selfip(device_id, object_id)

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_create_f5_bigipve_ipv6_dns(self):

        device_id = 'dev001'
        object_id = 'selfipv6'
        ipv6_address = 'dead:beef::3'

        msa = self.get_msa_instance()
        res = msa.create_f5_bigipve_ipv6_dns(device_id, object_id,
                                        ipv6_address)
        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_delete_f5_bigipve_ipv6_dns(self):

        device_id = 'dev001'
        object_id = 'selfipv6'

        msa = self.get_msa_instance()
        res = msa.delete_f5_bigipve_ipv6_dns(device_id, object_id)

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_create_f5_bigipve_ipv6_ntp(self):

        device_id = 'dev001'
        object_id = 'selfipv6'
        ipv6_address = 'dead:beef::3'
        ntp_timezone = 'America/Denver'

        msa = self.get_msa_instance()
        res = msa.create_f5_bigipve_ipv6_ntp(device_id, object_id,
                                        ipv6_address,
                                        ntp_timezone)

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_delete_f5_bigipve_ipv6_ntp(self):

        device_id = 'dev001'
        object_id = 'selfipv6'

        msa = self.get_msa_instance()
        res = msa.delete_f5_bigipve_ipv6_ntp(device_id, object_id)

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_create_f5_bigipve_ipv6_staticroute(self):

        device_id = 'dev001'
        object_id = 'selfipv6'
        is_default_gateway = 'no'
        gateway_ipv6_address = 'dead:beef::1'
        destination_ipv6_address = 'dead:beef::2'
        destination_netmask = 48

        msa = self.get_msa_instance()
        res = msa.create_f5_bigipve_ipv6_staticroute(device_id, object_id,
                                        is_default_gateway,
                                        gateway_ipv6_address,
                                        destination_ipv6_address,
                                        destination_netmask)

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_delete_f5_bigipve_ipv6_staticroute(self):

        device_id = 'dev001'
        object_id = 'selfipv6'

        msa = self.get_msa_instance()
        res = msa.delete_f5_bigipve_ipv6_staticroute(device_id, object_id)

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)
