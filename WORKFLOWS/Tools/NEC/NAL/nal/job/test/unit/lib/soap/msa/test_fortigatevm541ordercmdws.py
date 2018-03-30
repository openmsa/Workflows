import inspect
import unittest

from job.auto.extension import routingpod
from job.lib.soap.msa import fortigatevm541ordercmdws
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

        job_input = {'type': 1, 'device_type': 2,
                     'operation_id': 'TestSoapUser'}

        job_instance = routingpod.RoutingPod()
        ret = job_instance.routing_pod(job_input)

        pod_id = ret['pod_id']

        msa_instance = fortigatevm541ordercmdws.FortigateVm541OrderCommandWs(
                            job_instance.job_config,
                            job_instance.nal_endpoint_config,
                            pod_id)

        return msa_instance

    def test_create_fortigate_vm_system_common(self):

        device_id = 'dev001'
        host_name = 'host001'
        fortigate_vm_system_common_language = 'Japanese'
        fortigate_vm_system_common_timezone = 'Asia/Tokyo'

        msa = self.get_msa_instance()
        res = msa.create_fortigate_vm_system_common(device_id,
                                        host_name,
                                        fortigate_vm_system_common_language,
                                        fortigate_vm_system_common_timezone)

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_delete_fortigate_vm_system_common(self):

        device_id = 'dev001'
        host_name = 'host001'

        msa = self.get_msa_instance()
        res = msa.delete_fortigate_vm_system_common(device_id, host_name)

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_create_fortigate_vm_interface(self):

        device_id = 'dev001'
        port = '80'
        fortigate_vm_interface_ip_address = '192.168.0.1'
        fortigate_vm_interface_netmask = '255.255.255.0'
        fortigate_vm_interface_service_ping_action = 'ping'
        fortigate_vm_interface_service_https_action = 'post'
        fortigate_vm_interface_service_ssh_action = '?'

        msa = self.get_msa_instance()
        res = msa.create_fortigate_vm_interface(device_id,
                                port,
                                fortigate_vm_interface_ip_address,
                                fortigate_vm_interface_netmask,
                                fortigate_vm_interface_service_ping_action,
                                fortigate_vm_interface_service_https_action,
                                fortigate_vm_interface_service_ssh_action)

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_delete_fortigate_vm_interface(self):

        device_id = 'dev001'
        port = '80'

        msa = self.get_msa_instance()
        res = msa.delete_fortigate_vm_interface(device_id, port)

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_create_fortigate_vm_admin_account(self):

        device_id = 'dev001'
        fortigate_vm_account_name = 'taro'
        fortigate_vm_account_password = 'taro123'
        fortigate_vm_account_profile = 'user'

        msa = self.get_msa_instance()
        res = msa.create_fortigate_vm_admin_account(device_id,
                                fortigate_vm_account_name,
                                fortigate_vm_account_password,
                                fortigate_vm_account_profile)
        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_create_fortigate_vm_dns(self):

        device_id = 'dev001'
        host_name = 'host001'
        fortigate_vm_dns_primary = 'dns1'
        fortigate_vm_dns_secondary = 'dns2'

        msa = self.get_msa_instance()
        res = msa.create_fortigate_vm_dns(device_id,
                                    host_name,
                                    fortigate_vm_dns_primary,
                                    fortigate_vm_dns_secondary)

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_create_fortigate_vm_ntp(self):

        device_id = 'dev001'
        host_name = 'host001'
        fortigate_vm_ntp_sync_action = 'sync'
        fortigate_vm_ntp_sync_interval = '10'
        fortigate_vm_ntp_primary = '10.0.0.1'
        fortigate_vm_ntp_secondary = '10.0.0.2'

        msa = self.get_msa_instance()
        res = msa.create_fortigate_vm_ntp(device_id,
                                    host_name,
                                    fortigate_vm_ntp_sync_action,
                                    fortigate_vm_ntp_sync_interval,
                                    fortigate_vm_ntp_primary,
                                    fortigate_vm_ntp_secondary)

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_create_fortigate_vm_router_static(self):

        device_id = 'dev001'
        num = '100'
        dummy = 'dummy'
        fortigate_vm_firewall_router_default_gateway_action = 'start'
        fortigate_vm_firewall_router_default_gateway_address = '10.0.0.1'
        fortigate_vm_firewall_router_static_network_address = '10.0.0.2'
        fortigate_vm_firewall_router_static_network_mask = '255.255.255.0'
        fortigate_vm_firewall_router_static_device = 'dev001'

        msa = self.get_msa_instance()
        res = msa.create_fortigate_vm_router_static(device_id,
                        num,
                        dummy,
                        fortigate_vm_firewall_router_default_gateway_action,
                        fortigate_vm_firewall_router_default_gateway_address,
                        fortigate_vm_firewall_router_static_network_address,
                        fortigate_vm_firewall_router_static_network_mask,
                        fortigate_vm_firewall_router_static_device)

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_create_fortigate_vm_ipv6_gui_enable(self):

        device_id = 'dev001'
        host_name = 'host001'

        msa = self.get_msa_instance()
        res = msa.create_fortigate_vm_ipv6_gui_enable(device_id, host_name)

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_delete_fortigate_vm_ipv6_gui_enable(self):

        device_id = 'dev001'
        host_name = 'host001'

        msa = self.get_msa_instance()
        res = msa.delete_fortigate_vm_ipv6_gui_enable(device_id, host_name)

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_create_fortigate_vm_ipv6_interface(self):

        device_id = 'dev001'
        interface_name = 'eth0'

        ipv6_address = 'dead:beaf::1'
        netmask = 48
        is_ping = 'enable'
        is_https = 'enable'
        is_ssh = 'enable'

        msa = self.get_msa_instance()
        res = msa.create_fortigate_vm_ipv6_interface(
                                            device_id, interface_name,
                                            ipv6_address,
                                            netmask,
                                            is_ping,
                                            is_https,
                                            is_ssh
                                            )

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_delete_fortigate_vm_ipv6_interface(self):

        device_id = 'dev001'
        interface_name = 'eth0'

        ipv6_address = 'dead:beaf::1'
        netmask = 48

        msa = self.get_msa_instance()
        res = msa.delete_fortigate_vm_ipv6_interface(
                                            device_id, interface_name,
                                            ipv6_address,
                                            netmask
                                            )

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_create_fortigate_vm_ipv6_dns(self):

        device_id = 'dev001'
        host_name = 'host001'

        dns_primary = 'dead:beaf::1'
        dns_secondary = 'dead:beaf::2'

        msa = self.get_msa_instance()
        res = msa.create_fortigate_vm_ipv6_dns(device_id, host_name,
                                            dns_primary,
                                            dns_secondary)

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_delete_fortigate_vm_ipv6_dns(self):

        device_id = 'dev001'
        host_name = 'host001'

        msa = self.get_msa_instance()
        res = msa.delete_fortigate_vm_ipv6_dns(device_id, host_name)

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_create_fortigate_vm_ipv6_ntp(self):

        device_id = 'dev001'
        host_name = 'host001'

        ipv6_address = 'dead:beaf::1'
        sync_interval = 10

        msa = self.get_msa_instance()
        res = msa.create_fortigate_vm_ipv6_ntp(device_id, host_name,
                                            ipv6_address,
                                            sync_interval)

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_delete_fortigate_vm_ipv6_ntp(self):

        device_id = 'dev001'
        host_name = 'host001'

        ipv6_address = 'dead:beaf::1'

        msa = self.get_msa_instance()
        res = msa.delete_fortigate_vm_ipv6_ntp(device_id, host_name,
                                            ipv6_address)

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_create_fortigate_vm_ipv6_staticroute(self):

        device_id = 'dev001'
        router_static_no = 100

        is_default_gateway = 'yes'
        gateway_ipv6_address = 'dead:beaf::1'
        destination_ipv6_address = 'dead:beaf::2'
        destination_netmask = 48
        source_interface = 'eth1'

        msa = self.get_msa_instance()
        res = msa.create_fortigate_vm_ipv6_staticroute(
                                            device_id, router_static_no,
                                            is_default_gateway,
                                            gateway_ipv6_address,
                                            destination_ipv6_address,
                                            destination_netmask,
                                            source_interface)

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_delete_fortigate_vm_ipv6_staticroute(self):

        device_id = 'dev001'
        router_static_no = 100

        msa = self.get_msa_instance()
        res = msa.delete_fortigate_vm_ipv6_staticroute(
                                            device_id, router_static_no)

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)
