import inspect
import unittest

from job.auto.extension import routingpod
from job.lib.soap.msa import vthunder411ordercmdws
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

        msa_instance = vthunder411ordercmdws.Vthunder411OrderCommandWs(
                            job_instance.job_config,
                            job_instance.nal_endpoint_config,
                            pod_id)

        return msa_instance

    def test_create_vthunder_system_common(self):

        device_id = 'dev001'
        object_id = 'obj001'
        vthunder_system_common_timezone = 'Asia/Tokyo'

        res = self.get_msa_instance()\
                .create_vthunder_system_common(device_id,
                                    object_id,
                                    vthunder_system_common_timezone)

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_update_vthunder_system_common(self):

        device_id = 'dev001'
        object_id = 'obj001'
        vthunder_system_common_timezone = 'Asia/Tokyo'

        res = self.get_msa_instance()\
                .update_vthunder_system_common(device_id,
                                    object_id,
                                    vthunder_system_common_timezone)

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_delete_vthunder_system_common(self):

        device_id = 'dev001'
        object_id = 'obj001'
        vthunder_system_common_timezone = 'Asia/Tokyo'

        res = self.get_msa_instance()\
                .delete_vthunder_system_common(device_id,
                                    object_id,
                                    vthunder_system_common_timezone)

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

#     def test_create_vthunder_network_vlan_interface(self):
#
#         device_id = 'dev001'
#         object_id = 'obj001'
#         vthunder_network_vlan_untagged_interface_number = 'Asia/Tokyo'
#         vthunder_network_virtual_interface_ip_address = '10.0.0.1'
#         vthunder_network_virtual_interface_netmask = '255.255.255.0'
#         vthunder_network_vlan_description = 'abcd'
#
#         res = self.get_msa_instance()\
#                 .create_vthunder_network_vlan_interface(device_id, object_id,
#                             vthunder_network_vlan_untagged_interface_number,
#                             vthunder_network_virtual_interface_ip_address,
#                             vthunder_network_virtual_interface_netmask,
#                             vthunder_network_vlan_description)
#
#         print(inspect.currentframe().f_code.co_name)
#         pprint(res)
#
#         # Assertion
#         self.assertGreaterEqual(len(res), 1)
#
#     def test_update_vthunder_network_vlan_interface(self):
#
#         device_id = 'dev001'
#         object_id = 'obj001'
#         vthunder_network_vlan_untagged_interface_number = 'Asia/Tokyo'
#         vthunder_network_virtual_interface_ip_address = '10.0.0.1'
#         vthunder_network_virtual_interface_netmask = '255.255.255.0'
#         vthunder_network_vlan_description = 'abcd'
#
#         res = self.get_msa_instance()\
#                 .update_vthunder_network_vlan_interface(device_id, object_id,
#                             vthunder_network_vlan_untagged_interface_number,
#                             vthunder_network_virtual_interface_ip_address,
#                             vthunder_network_virtual_interface_netmask,
#                             vthunder_network_vlan_description)
#
#         print(inspect.currentframe().f_code.co_name)
#         pprint(res)
#
#         # Assertion
#         self.assertGreaterEqual(len(res), 1)
#
#     def test_delete_vthunder_network_vlan_interface(self):
#
#         device_id = 'dev001'
#         object_id = 'obj001'
#
#         res = self.get_msa_instance()\
#                 .delete_vthunder_network_vlan_interface(device_id, object_id)
#
#         print(inspect.currentframe().f_code.co_name)
#         pprint(res)
#
#         # Assertion
#         self.assertGreaterEqual(len(res), 1)

    def test_create_vthunder_system_dns(self):

        device_id = 'dev001'
        object_id = 'obj001'
        vthunder_system_dns_primary_ip_address = '10.0.0.1'
        vthunder_system_dns_secondary_ip_address = '10.0.0.2'

        res = self.get_msa_instance()\
                .create_vthunder_system_dns(device_id, object_id,
                                    vthunder_system_dns_primary_ip_address,
                                    vthunder_system_dns_secondary_ip_address)

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_delete_vthunder_system_dns(self):

        device_id = 'dev001'
        object_id = 'obj001'
        vthunder_system_dns_primary_ip_address = '10.0.0.1'
        vthunder_system_dns_secondary_ip_address = '10.0.0.2'

        res = self.get_msa_instance()\
                .delete_vthunder_system_dns(device_id, object_id,
                                    vthunder_system_dns_primary_ip_address,
                                    vthunder_system_dns_secondary_ip_address)

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_create_vthunder_system_snmp_trap(self):

        device_id = 'dev001'
        object_id = 'obj001'
        address = '10.0.0.1'
        version = '102'
        community_name = 'abc'

        res = self.get_msa_instance()\
                .create_vthunder_system_snmp_trap(device_id, object_id,
                                                address,
                                                version,
                                                community_name)

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_update_vthunder_system_snmp_trap(self):

        device_id = 'dev001'
        object_id = 'obj001'
        address = '10.0.0.1'
        version = '102'
        community_name = 'abc'
        address_delete = '10.0.0.2'
        version_delete = '202'
        community_name_delete = 'xyz'

        res = self.get_msa_instance()\
                .update_vthunder_system_snmp_trap(device_id, object_id,
                                                address,
                                                version,
                                                community_name,
                                                address_delete,
                                                version_delete,
                                                community_name_delete)

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_delete_vthunder_system_snmp_trap(self):

        device_id = 'dev001'
        object_id = 'obj001'
        address = '10.0.0.1'
        version = '102'
        community_name = 'abc'

        res = self.get_msa_instance()\
                .delete_vthunder_system_snmp_trap(device_id, object_id,
                                                address,
                                                version,
                                                community_name)

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_create_vthunder_system_snmp_enable(self):

        device_id = 'dev001'
        object_id = 'obj001'

        res = self.get_msa_instance()\
                .create_vthunder_system_snmp_enable(device_id, object_id)

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_delete_vthunder_system_snmp_enable(self):

        device_id = 'dev001'
        object_id = 'obj001'

        res = self.get_msa_instance()\
                .delete_vthunder_system_snmp_enable(device_id, object_id)

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_create_vthunder_system_snmp(self):

        device_id = 'dev001'
        object_id = 'obj001'
        address = '10.0.0.1'
        netmask = '255.255.255.0'

        res = self.get_msa_instance()\
                .create_vthunder_system_snmp(device_id, object_id,
                                                        address,
                                                        netmask
                                                        )

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_delete_vthunder_system_snmp(self):

        device_id = 'dev001'
        object_id = 'obj001'

        res = self.get_msa_instance()\
                .delete_vthunder_system_snmp(device_id, object_id)

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_create_vthunder_system_syslog(self):

        device_id = 'dev001'
        object_id = 'obj001'
        vthunder_system_syslog_ip_address = '10.0.0.1'

        res = self.get_msa_instance()\
                .create_vthunder_system_syslog(device_id, object_id,
                                        vthunder_system_syslog_ip_address)

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_delete_vthunder_system_syslog(self):

        device_id = 'dev001'
        object_id = 'obj001'
        vthunder_system_syslog_ip_address = '10.0.0.1'

        res = self.get_msa_instance()\
                .delete_vthunder_system_syslog(device_id, object_id,
                                        vthunder_system_syslog_ip_address)

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_create_vthunder_system_ntp(self):

        device_id = 'dev001'
        object_id = 'obj001'
        action = 'start'
        fortigate_vm_ntp_primary = '10.0.0.1'
        fortigate_vm_ntp_secondary = '10.0.0.2'

        res = self.get_msa_instance()\
                .create_vthunder_system_ntp(device_id, object_id, action,
                                            fortigate_vm_ntp_primary,
                                            fortigate_vm_ntp_secondary)

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_update_vthunder_system_ntp(self):

        device_id = 'dev001'
        object_id = 'obj001'
        action = 'start'
        member = 'abc'
        member_delete = 'xyz'

        res = self.get_msa_instance()\
                .update_vthunder_system_ntp(device_id, object_id,
                                        action, member, member_delete)

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_delete_vthunder_system_ntp(self):

        device_id = 'dev001'
        object_id = 'obj001'
        member = 'abc'

        res = self.get_msa_instance()\
                .delete_vthunder_system_ntp(device_id, object_id,
                                        member)

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_create_vthunder_network_routes(self):

        device_id = 'dev001'
        object_id = 'obj001'
        vthunder_network_routes_network_address = '10.0.0.1'
        vthunder_network_routes_netmask = '255.255.255.0'
        vthunder_network_routes_gateway_address = '10.0.0.2'

        res = self.get_msa_instance()\
                .create_vthunder_network_routes(device_id, object_id,
                                vthunder_network_routes_network_address,
                                vthunder_network_routes_netmask,
                                vthunder_network_routes_gateway_address)

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_delete_vthunder_network_routes(self):

        device_id = 'dev001'
        object_id = 'obj001'
        vthunder_network_routes_network_address = '10.0.0.1'
        vthunder_network_routes_netmask = '255.255.255.0'
        vthunder_network_routes_gateway_address = '10.0.0.2'

        res = self.get_msa_instance()\
                .delete_vthunder_network_routes(device_id, object_id,
                                vthunder_network_routes_network_address,
                                vthunder_network_routes_netmask,
                                vthunder_network_routes_gateway_address)

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_create_vthunder_system_admin_account(self):

        device_id = 'dev001'
        object_id = 'obj001'
        vthunder_system_user_password = '9ass123'

        res = self.get_msa_instance()\
                .create_vthunder_system_admin_account(device_id, object_id,
                                vthunder_system_user_password)

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_update_vthunder_system_admin_account(self):

        device_id = 'dev001'
        object_id = 'obj001'
        vthunder_system_user_password = '9ass123'

        res = self.get_msa_instance()\
                .update_vthunder_system_admin_account(device_id, object_id,
                                vthunder_system_user_password)

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_delete_vthunder_system_admin_account(self):

        device_id = 'dev001'
        object_id = 'obj001'

        res = self.get_msa_instance()\
                .delete_vthunder_system_admin_account(device_id, object_id)

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_create_vthunder_network_interface_mng_service(self):

        device_id = 'dev001'
        object_id = 'obj001'
        vthunder_network_interface_snmp_action = 'yes'
        vthunder_network_interface_ssh_action = 'yes'
        vthunder_network_interface_https_action = 'yes'
        vthunder_network_interface_ping_action = 'yes'

        res = self.get_msa_instance()\
                .create_vthunder_network_interface_mng_service(device_id,
                                    object_id,
                                    vthunder_network_interface_snmp_action,
                                    vthunder_network_interface_ssh_action,
                                    vthunder_network_interface_https_action,
                                    vthunder_network_interface_ping_action)

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_delete_vthunder_network_interface_mng_service(self):

        device_id = 'dev001'
        object_id = 'obj001'

        res = self.get_msa_instance()\
                .delete_vthunder_network_interface_mng_service(device_id,
                                                object_id
                                        )
        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_create_vthunder_network_vlan(self):

        device_id = 'dev001'
        object_id = 'obj001'
        interface_number = 'Asia/Tokyo',
        vlan_description = 'abcd'

        res = self.get_msa_instance()\
                .create_vthunder_network_vlan(device_id, object_id,
                                                        interface_number,
                                                        vlan_description)

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_delete_vthunder_network_vlan(self):

        device_id = 'dev001'
        object_id = 'obj001'

        res = self.get_msa_instance()\
                .delete_vthunder_network_vlan(device_id, object_id)

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_create_vthunder_network_ve(self):

        device_id = 'dev001'
        object_id = 'obj001'
        ipv4_address = '10.0.0.1'
        netmask = '255.255.255.0'
        description = 'abcd'

        res = self.get_msa_instance()\
                .create_vthunder_network_ve(device_id, object_id,
                                            ipv4_address,
                                            netmask,
                                            description)

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_delete_vthunder_network_ve(self):

        device_id = 'dev001'
        object_id = 'obj001'
        ipv4_address = '10.0.0.1'
        netmask = '255.255.255.0'
        description = 'abcd'

        res = self.get_msa_instance()\
                .delete_vthunder_network_ve(device_id, object_id,
                                            ipv4_address,
                                            netmask,
                                            description)

        print(inspect.currentframe().f_code.co_name)
        pprint(res)
        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_create_vthunder_network_enable(self):

        device_id = 'dev001'
        object_id = '1'

        res = self.get_msa_instance()\
                .create_vthunder_network_enable(device_id, object_id)

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_delete_vthunder_network_enalbe(self):

        device_id = 'dev001'
        object_id = '1'

        res = self.get_msa_instance()\
                .delete_vthunder_network_enable(device_id, object_id)

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_create_vthunder_network_vlan_interface(self):

        device_id = 'dev001'
        object_id = 1000

        vthunder_network_vlan_untagged_interface_number = 10
        vthunder_network_virtual_interface_ip_address = '10.0.0.1'
        vthunder_network_virtual_interface_netmask = '255.255.255.0'
        vthunder_network_vlan_description = 'UnitTest'

        res = self.get_msa_instance()\
                .create_vthunder_network_vlan_interface(device_id, object_id,
                            vthunder_network_vlan_untagged_interface_number,
                            vthunder_network_virtual_interface_ip_address,
                            vthunder_network_virtual_interface_netmask,
                            vthunder_network_vlan_description
                            )

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_update_vthunder_network_vlan_interface(self):

        device_id = 'dev001'
        object_id = 1000

        vthunder_network_vlan_untagged_interface_number = 10
        vthunder_network_virtual_interface_ip_address = '10.0.0.1'
        vthunder_network_virtual_interface_netmask = '255.255.255.0'
        vthunder_network_vlan_description = 'UnitTest'

        res = self.get_msa_instance()\
                .update_vthunder_network_vlan_interface(device_id, object_id,
                            vthunder_network_vlan_untagged_interface_number,
                            vthunder_network_virtual_interface_ip_address,
                            vthunder_network_virtual_interface_netmask,
                            vthunder_network_vlan_description
                            )

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_delete_vthunder_network_vlan_interface(self):

        device_id = 'dev001'
        object_id = 1000

        res = self.get_msa_instance()\
                .delete_vthunder_network_vlan_interface(device_id, object_id)

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_create_vthunder_ipv6_ve(self):

        device_id = 'dev001'
        object_id = 1000

        ipv6_address = 'dead:beaf::1'
        netmask = 48
        vlan_description = 'UnitTest'

        res = self.get_msa_instance()\
                .create_vthunder_ipv6_ve(device_id, object_id,
                                   ipv6_address,
                                   netmask,
                                   vlan_description
                                   )

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_delete_vthunder_ipv6_ve(self):

        device_id = 'dev001'
        object_id = 1000

        ipv6_address = 'dead:beaf::1'
        netmask = 48
        vlan_description = 'UnitTest'

        res = self.get_msa_instance()\
                .delete_vthunder_ipv6_ve(device_id, object_id,
                                   ipv6_address,
                                   netmask,
                                   vlan_description
                                   )

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_create_vthunder_ipv6_dns(self):

        device_id = 'dev001'
        object_id = 'host001'

        primary_dnsserver = 'dead:beaf::1'
        secondary_dnsserver = 'dead:beaf::2'

        res = self.get_msa_instance()\
                .create_vthunder_ipv6_dns(device_id, object_id,
                                   primary_dnsserver,
                                   secondary_dnsserver
                                   )

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_delete_vthunder_ipv6_dns(self):

        device_id = 'dev001'
        object_id = 'host001'

        primary_dnsserver = 'dead:beaf::1'
        secondary_dnsserver = 'dead:beaf::2'

        res = self.get_msa_instance()\
                .delete_vthunder_ipv6_dns(device_id, object_id,
                                   primary_dnsserver,
                                   secondary_dnsserver
                                   )

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_create_vthunder_ipv6_ntp(self):

        device_id = 'dev001'
        object_id = 'host001'

        is_prefer = 'enable'
        ipv6_address = 'dead:beaf::2'

        res = self.get_msa_instance()\
                .create_vthunder_ipv6_ntp(device_id, object_id,
                                   is_prefer,
                                   ipv6_address
                                   )

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_delete_vthunder_ipv6_ntp(self):

        device_id = 'dev001'
        object_id = 'host001'

        ipv6_address = 'dead:beaf::2'

        res = self.get_msa_instance()\
                .delete_vthunder_ipv6_ntp(device_id, object_id,
                                   ipv6_address
                                   )

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_create_vthunder_ipv6_staticroute(self):

        device_id = 'dev001'
        object_id = 100

        destination_ipv6_address = '::'
        destination_netmask = 0
        ipv6_address = 'dead:beaf::2'

        res = self.get_msa_instance()\
                .create_vthunder_ipv6_staticroute(device_id, object_id,
                                   destination_ipv6_address,
                                   destination_netmask,
                                   ipv6_address
                                   )

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_delete_vthunder_ipv6_staticroute(self):

        device_id = 'dev001'
        object_id = 100

        destination_ipv6_address = '::'
        destination_netmask = 0
        ipv6_address = 'dead:beaf::2'

        res = self.get_msa_instance()\
                .delete_vthunder_ipv6_staticroute(device_id, object_id,
                                   destination_ipv6_address,
                                   destination_netmask,
                                   ipv6_address
                                   )

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)
