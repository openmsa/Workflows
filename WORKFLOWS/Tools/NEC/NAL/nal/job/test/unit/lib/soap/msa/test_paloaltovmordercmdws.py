import inspect
import unittest

from job.auto.extension import routingpod
from job.lib.soap.msa import paloaltovmordercmdws
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

        msa_instance = paloaltovmordercmdws.PaloaltoVmOrderCommandWs(
                            job_instance.job_config,
                            job_instance.nal_endpoint_config,
                            pod_id)

        return msa_instance

    def test_create_paloalto_vm_system_common(self):

        device_id = 'dev001'
        object_id = 'obj001'
        paloalto_vm_system_timezone = 'Asia/Tokyo'

        res = self.get_msa_instance()\
                .create_paloalto_vm_system_common(device_id,
                                        object_id,
                                        paloalto_vm_system_timezone)
        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_delete_paloalto_vm_system_common(self):

        device_id = 'dev001'
        object_id = 'obj001'
        paloalto_vm_system_timezone = 'Asia/Tokyo'

        res = self.get_msa_instance()\
                .delete_paloalto_vm_system_common(device_id,
                                        object_id,
                                        paloalto_vm_system_timezone)
        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_create_paloalto_vm_vsys_zone(self):

        device_id = 'dev001'
        object_id = 'obj001'

        res = self.get_msa_instance()\
                .create_paloalto_vm_vsys_zone(device_id,
                                        object_id)

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_delete_paloalto_vm_vsys_zone(self):

        device_id = 'dev001'
        object_id = 'obj001'

        res = self.get_msa_instance()\
                .delete_paloalto_vm_vsys_zone(device_id,
                                        object_id)

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_create_paloalto_vm_vsys_zone_mapping(self):

        device_id = 'dev001'
        object_id = 'obj001'
        paloalto_vm_vsys_zone_interface = 'if001'
        paloalto_vm_vsys_zone_name = 'name001'

        res = self.get_msa_instance()\
                .create_paloalto_vm_vsys_zone_mapping(device_id,
                                        object_id,
                                        paloalto_vm_vsys_zone_interface,
                                        paloalto_vm_vsys_zone_name
                                        )
        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_delete_paloalto_vm_vsys_zone_mapping(self):

        device_id = 'dev001'
        object_id = 'obj001'
        paloalto_vm_vsys_zone_name = 'name001'

        res = self.get_msa_instance()\
                .delete_paloalto_vm_vsys_zone_mapping(device_id,
                                        object_id,
                                        paloalto_vm_vsys_zone_name
                                        )
        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_create_paloalto_vm_network_vrouter_mapping(self):

        device_id = 'dev001'
        object_id = 'obj001'
        interface_name = 'if001'

        res = self.get_msa_instance()\
                .create_paloalto_vm_network_vrouter_mapping(device_id,
                                        object_id,
                                        interface_name
                                        )
        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_delete_paloalto_vm_network_vrouter_mapping(self):

        device_id = 'dev001'
        object_id = 'obj001'

        res = self.get_msa_instance()\
                .delete_paloalto_vm_network_vrouter_mapping(device_id,
                                        object_id
                                        )
        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_create_paloalto_vm_network_interface(self):

        device_id = 'dev001'
        object_id = 'obj001'
        paloalto_vm_network_interface_ip_address = '10.0.0.1'
        paloalto_vm_network_interface_netmask = '255.255.255.0'
        paloalto_vm_network_profile_name = 'profile123'

        res = self.get_msa_instance()\
                .create_paloalto_vm_network_interface(device_id,
                                object_id,
                                paloalto_vm_network_interface_ip_address,
                                paloalto_vm_network_interface_netmask,
                                paloalto_vm_network_profile_name
                                        )
        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_delete_paloalto_vm_network_interface(self):

        device_id = 'dev001'
        object_id = 'obj001'

        res = self.get_msa_instance()\
                .delete_paloalto_vm_network_interface(device_id,
                                object_id
                                )
        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_create_paloalto_vm_system_dns(self):

        device_id = 'dev001'
        object_id = 'obj001'
        paloalto_vm_system_dns_primary = '10.0.0.1'
        paloalto_vm_system_dns_secondary = '255.255.255.0'

        res = self.get_msa_instance()\
                .create_paloalto_vm_system_dns(device_id,
                                object_id,
                                paloalto_vm_system_dns_primary,
                                paloalto_vm_system_dns_secondary
                                        )
        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_delete_paloalto_vm_system_dns(self):

        device_id = 'dev001'
        object_id = 'obj001'

        res = self.get_msa_instance()\
                .delete_paloalto_vm_system_dns(device_id,
                                object_id
                                        )
        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_create_paloalto_vm_logsetting_snmp(self):

        device_id = 'dev001'
        object_id = 'obj001'
        name = 'aaa'
        address = '10.0.0.1'
        community_name = 'xyz'

        res = self.get_msa_instance()\
                .create_paloalto_vm_logsetting_snmp(device_id,
                                                object_id,
                                                name,
                                                address,
                                                community_name
                                        )
        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_delete_paloalto_vm_logsetting_snmp(self):

        device_id = 'dev001'
        object_id = 'obj001'

        res = self.get_msa_instance()\
                .delete_paloalto_vm_logsetting_snmp(device_id,
                                                object_id
                                        )
        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_create_paloalto_vm_logsetting_snmp_mapping(self):

        device_id = 'dev001'
        object_id = 'obj001'
        paloalto_vm_logsetting_snmp_profile = 'xyz'

        res = self.get_msa_instance()\
                .create_paloalto_vm_logsetting_snmp_mapping(device_id,
                                                object_id,
                                paloalto_vm_logsetting_snmp_profile
                                        )
        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_delete_paloalto_vm_logsetting_snmp_mapping(self):

        device_id = 'dev001'
        object_id = 'obj001'

        res = self.get_msa_instance()\
                .delete_paloalto_vm_logsetting_snmp_mapping(device_id,
                                                object_id
                                        )
        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_create_paloalto_vm_logsetting_syslog(self):

        device_id = 'dev001'
        object_id = 'obj001'
        name = 'xyz'
        address = '10.0.0.1'

        res = self.get_msa_instance()\
                .create_paloalto_vm_logsetting_syslog(device_id,
                                                object_id,
                                                name,
                                                address
                                        )
        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_delete_paloalto_vm_logsetting_syslog(self):

        device_id = 'dev001'
        object_id = 'obj001'

        res = self.get_msa_instance()\
                .delete_paloalto_vm_logsetting_syslog(device_id,
                                                object_id
                                        )
        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_create_paloalto_vm_logsetting_syslog_mapping(self):

        device_id = 'dev001'
        object_id = 'obj001'
        paloalto_vm_logsetting_syslog_profile = 'xyz'

        res = self.get_msa_instance()\
                .create_paloalto_vm_logsetting_syslog_mapping(device_id,
                                                object_id,
                                paloalto_vm_logsetting_syslog_profile
                                        )
        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_delete_paloalto_vm_logsetting_syslog_mapping(self):

        device_id = 'dev001'
        object_id = 'obj001'

        res = self.get_msa_instance()\
                .delete_paloalto_vm_logsetting_syslog_mapping(device_id,
                                                object_id
                                        )
        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_create_paloalto_vm_system_ntp(self):

        device_id = 'dev001'
        object_id = 'obj001'
        paloalto_vm_system_primary_ntp_server = 'abc'
        paloalto_vm_system_secondary_ntp_server = 'xyz'

        res = self.get_msa_instance()\
                .create_paloalto_vm_system_ntp(device_id,
                                                object_id,
                                paloalto_vm_system_primary_ntp_server,
                                paloalto_vm_system_secondary_ntp_server
                                        )
        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_delete_paloalto_vm_system_ntp(self):

        device_id = 'dev001'
        object_id = 'obj001'

        res = self.get_msa_instance()\
                .delete_paloalto_vm_system_ntp(device_id,
                                                object_id
                                        )
        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_create_paloalto_vm_network_static_route(self):

        device_id = 'dev001'
        object_id = 'obj001'
        paloalto_vm_network_staticroute_destination_address = '10.0.0.1'
        paloalto_vm_network_staticroute_destination_netmask = '255.255.255.0'
        paloalto_vm_network_staticroute_nexthop_address = '10.0.0.2'
        paloalto_vm_network_staticroute_source_interface = 'if001'

        res = self.get_msa_instance()\
                .create_paloalto_vm_network_static_route(device_id,
                                                object_id,
                    paloalto_vm_network_staticroute_destination_address,
                    paloalto_vm_network_staticroute_destination_netmask,
                    paloalto_vm_network_staticroute_nexthop_address,
                    paloalto_vm_network_staticroute_source_interface
                                        )
        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_delete_paloalto_vm_network_static_route(self):

        device_id = 'dev001'
        object_id = 'obj001'

        res = self.get_msa_instance()\
                .delete_paloalto_vm_network_static_route(device_id,
                                                object_id
                                        )
        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_create_paloalto_vm_system_users(self):

        device_id = 'dev001'
        object_id = 'obj001'
        paloalto_vm_system_user_password = 'aaa'

        res = self.get_msa_instance()\
                .create_paloalto_vm_system_users(device_id,
                                                object_id,
                                            paloalto_vm_system_user_password
                                        )
        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_delete_paloalto_vm_system_users(self):

        device_id = 'dev001'
        object_id = 'obj001'

        res = self.get_msa_instance()\
                .delete_paloalto_vm_system_users(device_id,
                                                object_id
                                        )
        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_create_paloalto_vm_network_interface_mng_profile(self):

        device_id = 'dev001'
        object_id = 'obj001'
        paloalto_vm_network_interface_snmp_action = 'yes'
        paloalto_vm_network_interface_ssh_action = 'yes'
        paloalto_vm_network_interface_https_action = 'yes'
        paloalto_vm_network_interface_ping_action = 'yes'

        res = self.get_msa_instance()\
                .create_paloalto_vm_network_interface_mng_profile(device_id,
                                    object_id,
                                    paloalto_vm_network_interface_snmp_action,
                                    paloalto_vm_network_interface_ssh_action,
                                    paloalto_vm_network_interface_https_action,
                                    paloalto_vm_network_interface_ping_action)

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_delete_paloalto_vm_network_interface_mng_profile(self):

        device_id = 'dev001'
        object_id = 'obj001'

        res = self.get_msa_instance()\
                .delete_paloalto_vm_network_interface_mng_profile(device_id,
                                                object_id
                                        )
        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_create_paloalto_vm_ipv6_enable(self):

        device_id = 'dev001'
        object_id = 'obj001'
        is_ipv6firewalling = 'enable'

        res = self.get_msa_instance()\
            .create_paloalto_vm_ipv6_enable(device_id, object_id,
                                        is_ipv6firewalling)
        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_create_paloalto_vm_ipv6_interface(self):

        device_id = 'dev001'
        object_id = 'obj001'
        ipv6_address = 'dead:beef::4'
        netmask = 48

        res = self.get_msa_instance()\
            .create_paloalto_vm_ipv6_interface(device_id, object_id,
                                        ipv6_address,
                                        netmask)
        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_delete_paloalto_vm_ipv6_interface(self):

        device_id = 'dev001'
        object_id = 'obj001'

        res = self.get_msa_instance()\
            .delete_paloalto_vm_ipv6_interface(device_id, object_id)
        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_create_paloalto_vm_ipv6_interface_enable(self):

        device_id = 'dev001'
        object_id = 'obj001'

        res = self.get_msa_instance()\
            .create_paloalto_vm_ipv6_interface_enable(device_id, object_id)
        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_delete_paloalto_vm_ipv6_interface_enable(self):

        device_id = 'dev001'
        object_id = 'obj001'

        res = self.get_msa_instance()\
            .delete_paloalto_vm_ipv6_interface_enable(device_id, object_id)
        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_create_paloalto_vm_ipv6_dns(self):

        device_id = 'dev001'
        object_id = 'obj001'
        dns_primary = 'dead:beef::4'
        dns_secondary = 'dead:beef::5'

        res = self.get_msa_instance()\
            .create_paloalto_vm_ipv6_dns(device_id, object_id,
                                                dns_primary,
                                                dns_secondary)
        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_delete_paloalto_vm_ipv6_dns(self):

        device_id = 'dev001'
        object_id = 'obj001'

        res = self.get_msa_instance()\
            .delete_paloalto_vm_ipv6_dns(device_id, object_id)
        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_create_paloalto_vm_ipv6_ntp(self):

        device_id = 'dev001'
        object_id = 'obj001'
        primary_ntp_server = 'dead:beef::4'
        secondary_ntp_server = 'dead:beef::5'

        res = self.get_msa_instance()\
            .create_paloalto_vm_ipv6_ntp(device_id, object_id,
                                                primary_ntp_server,
                                                secondary_ntp_server)
        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_delete_paloalto_vm_ipv6_ntp(self):

        device_id = 'dev001'
        object_id = 'obj001'

        res = self.get_msa_instance()\
            .delete_paloalto_vm_ipv6_ntp(device_id, object_id)
        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_create_paloalto_vm_ipv6_staticroute(self):

        device_id = 'dev001'
        object_id = 'obj001'
        destination_ipv6_address = 'dead:beef::4'
        destination_netmask = 48
        ipv6_address = 'dead:beef::5'
        source_interface = 'eth0'

        res = self.get_msa_instance()\
            .create_paloalto_vm_ipv6_staticroute(device_id, object_id,
                                                destination_ipv6_address,
                                                destination_netmask,
                                                ipv6_address,
                                                source_interface)
        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_delete_paloalto_vm_ipv6_staticroute(self):

        device_id = 'dev001'
        object_id = 'obj001'

        res = self.get_msa_instance()\
            .delete_paloalto_vm_ipv6_staticroute(device_id, object_id)
        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_create_paloalto_vm_permittedip(self):

        device_id = 'dev001'
        permitted_ip_number = 10
        profile_name = 'profile001'
        ip_address = 'dead:beef::5'
        netmask = 48

        res = self.get_msa_instance()\
            .create_paloalto_vm_permittedip(device_id, permitted_ip_number,
                                                    profile_name,
                                                    ip_address,
                                                    netmask)

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_delete_paloalto_vm_permittedip(self):

        device_id = 'dev001'
        permitted_ip_number = 10
        profile_name = 'profile001'
        ip_address = 'dead:beef::5'
        netmask = 48

        res = self.get_msa_instance()\
            .delete_paloalto_vm_permittedip(device_id, permitted_ip_number,
                                                    profile_name,
                                                    ip_address,
                                                    netmask)

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)
