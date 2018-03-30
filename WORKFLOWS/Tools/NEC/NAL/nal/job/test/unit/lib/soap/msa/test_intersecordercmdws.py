import inspect
import unittest

from job.auto.extension import routingpod
from job.lib.soap.msa import intersecordercmdws
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

        msa_instance = intersecordercmdws.IntersecOrderCommandWs(
                            job_instance.job_config,
                            job_instance.nal_endpoint_config,
                            pod_id)

        return msa_instance

    def test_create_intersec_sg_startup(self):

        device_id = 'dev001'
        instance_name = 'host001'
        license_key = 'key001'

        res = self.get_msa_instance()\
            .create_intersec_sg_startup(device_id, instance_name,
                                            license_key)
        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_create_intersec_sg_nw(self):

        device_id = 'dev001'
        nic_number = 1
        ip_address = '10.0.0.1'
        subnet = '255.255.255.0'

        msa = self.get_msa_instance()
        res = msa.create_intersec_sg_nw(device_id, nic_number,
                                        ip_address,
                                        subnet)
        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_update_intersec_sg_nw(self):

        device_id = 'dev001'
        nic_number = 1
        ip_address = '10.0.0.1'
        subnet = '255.255.255.0'

        msa = self.get_msa_instance()
        res = msa.update_intersec_sg_nw(device_id, nic_number,
                                        ip_address,
                                        subnet)
        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_delete_intersec_sg_nw(self):

        device_id = 'dev001'
        nic_number = 1

        res = self.get_msa_instance()\
            .delete_intersec_sg_nw(device_id, nic_number)

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_create_intersec_sg_reboot(self):

        device_id = 'dev001'

        res = self.get_msa_instance().create_intersec_sg_reboot(device_id)

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_create_intersec_sg_zabbix(self):

        device_id = 'dev001'
        instance_name = 'host001'
        zabbix_vip_ip_address = '192.168.0.1'
        zabbix01_ip_address = '10.0.0.1'
        zabbix02_ip_address = '10.0.0.2'

        res = self.get_msa_instance().create_intersec_sg_zabbix(device_id,
                                        instance_name,
                                        zabbix_vip_ip_address,
                                        zabbix01_ip_address,
                                        zabbix02_ip_address)

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_create_intersec_sg_ntp(self):

        device_id = 'dev001'
        ip_address = '192.168.0.1'

        res = self.get_msa_instance().create_intersec_sg_ntp(device_id,
                                        ip_address)

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_create_intersec_sg_default_gw(self):

        device_id = 'dev001'
        gw_ip_address = '192.168.0.1'

        res = self.get_msa_instance()\
            .create_intersec_sg_default_gw(device_id, gw_ip_address)

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_create_intersec_sg_static_route(self):

        device_id = 'dev001'
        dst_ip_address = '10.0.0.1'
        dst_subnet = '255.255.255.0'
        gw_ip_address = '192.168.0.1'

        res = self.get_msa_instance()\
            .create_intersec_sg_static_route(device_id,
                                            dst_ip_address,
                                            dst_subnet,
                                            gw_ip_address)
        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_create_intersec_lb_startup(self):

        device_id = 'dev001'
        instance_name = 'host001'
        ip_address = '10.0.0.1'
        license_key = 'key001'

        res = self.get_msa_instance()\
            .create_intersec_lb_startup(device_id,
                                            instance_name,
                                            ip_address,
                                            license_key)
        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_create_intersec_lb_nw(self):

        device_id = 'dev001'
        nic_number = 1
        ip_address = '10.0.0.1'
        subnet = '255.255.255.0'
        broadcast_address = '10.255.255.255'

        res = self.get_msa_instance().create_intersec_lb_nw(device_id,
                                            nic_number,
                                            ip_address,
                                            subnet,
                                            broadcast_address)
        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_update_intersec_lb_nw(self):

        device_id = 'dev001'
        nic_number = 1
        ip_address = '10.0.0.1'
        subnet = '255.255.255.0'
        broadcast_address = '10.255.255.255'

        res = self.get_msa_instance().update_intersec_lb_nw(device_id,
                                            nic_number,
                                            ip_address,
                                            subnet,
                                            broadcast_address)
        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_delete_intersec_lb_nw(self):

        device_id = 'dev001'
        nic_number = 1

        res = self.get_msa_instance()\
                        .delete_intersec_lb_nw(device_id, nic_number)

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_create_intersec_lb_reboot(self):

        device_id = 'dev001'

        res = self.get_msa_instance().create_intersec_lb_reboot(device_id)

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_create_intersec_lb_zabbix(self):

        device_id = 'dev001'
        instance_name = 'host001'
        zabbix_vip_ip_address = '192.168.0.1'
        zabbix01_ip_address = '10.0.0.1'
        zabbix02_ip_address = '10.0.0.2'

        res = self.get_msa_instance()\
            .create_intersec_lb_zabbix(device_id, instance_name,
                                        zabbix_vip_ip_address,
                                        zabbix01_ip_address,
                                        zabbix02_ip_address)
        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_create_intersec_lb_ntp(self):

        device_id = 'dev001'
        ip_address = '192.168.0.1'

        res = self.get_msa_instance()\
                .create_intersec_lb_ntp(device_id, ip_address)
        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_create_intersec_lb_default_gw(self):

        device_id = 'dev001'
        gw_ip_address = '192.168.0.1'
        nic_number = 1

        res = self.get_msa_instance()\
                .create_intersec_lb_default_gw(device_id,
                                            gw_ip_address, nic_number)
        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_create_intersec_lb_static_route(self):

        device_id = 'dev001'
        dst_ip_address = '10.0.0.1'
        dst_subnet = '255.255.255.0'
        gw_ip_address = '192.168.0.1'

        res = self.get_msa_instance()\
                .create_intersec_lb_static_route(device_id,
                                            dst_ip_address,
                                                dst_subnet,
                                                gw_ip_address)
        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_check_boot_complete_sg(self):

        device_id = 'dev001'

        res = self.get_msa_instance()\
                .check_boot_complete_sg(device_id)

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_check_boot_complete_lb(self):

        device_id = 'dev001'

        res = self.get_msa_instance()\
                .check_boot_complete_lb(device_id)

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_create_nec_intersecvmsg_ipv6_interface(self):

        device_id = 'dev001'
        object_id = '0'
        ipv6_address = 'dead:beef::3'
        netmask = 48

        res = self.get_msa_instance()\
            .create_nec_intersecvmsg_ipv6_interface(device_id, object_id,
                                            ipv6_address,
                                            netmask)

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_delete_nec_intersecvmsg_ipv6_interface(self):

        device_id = 'dev001'
        object_id = '0'

        res = self.get_msa_instance()\
            .delete_nec_intersecvmsg_ipv6_interface(device_id, object_id)

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_create_nec_intersecvmsg_ipv6_staticroute(self):

        device_id = 'dev001'
        object_id = '0'
        destination_ipv6_address = 'dead:beef::3'
        destination_netmask = 48
        ipv6_address = 'dead:beef::4'

        res = self.get_msa_instance()\
            .create_nec_intersecvmsg_ipv6_staticroute(device_id, object_id,
                                            destination_ipv6_address,
                                            destination_netmask,
                                            ipv6_address)

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_delete_nec_intersecvmsg_ipv6_staticroute(self):

        device_id = 'dev001'
        object_id = '0'
        destination_ipv6_address = 'dead:beef::3'
        destination_netmask = 48
        ipv6_address = 'dead:beef::4'

        res = self.get_msa_instance()\
            .delete_nec_intersecvmsg_ipv6_staticroute(device_id, object_id,
                                            destination_ipv6_address,
                                            destination_netmask,
                                            ipv6_address)

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_create_nec_intersecvmsg_ipv6_defaultgw(self):

        device_id = 'dev001'
        object_id = 'host001'
        ipv6_address = 'dead:beef::4'
        source_interface = 'eth0'

        res = self.get_msa_instance()\
            .create_nec_intersecvmsg_ipv6_defaultgw(device_id, object_id,
                                            ipv6_address,
                                            source_interface)

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_delete_nec_intersecvmsg_ipv6_defaultgw(self):

        device_id = 'dev001'
        object_id = 'host001'
        ipv6_address = 'dead:beef::4'
        source_interface = 'eth0'

        res = self.get_msa_instance()\
            .delete_nec_intersecvmsg_ipv6_defaultgw(device_id, object_id,
                                            ipv6_address,
                                            source_interface)

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_create_nec_intersecvmsg_ipv6_dns(self):

        device_id = 'dev001'
        object_id = 'host001'
        ipv6_address = 'dead:beef::4'

        res = self.get_msa_instance()\
            .create_nec_intersecvmsg_ipv6_dns(device_id, object_id,
                                            ipv6_address)

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_delete_nec_intersecvmsg_ipv6_dns(self):

        device_id = 'dev001'
        object_id = 'host001'
        ipv6_address = 'dead:beef::4'

        res = self.get_msa_instance()\
            .delete_nec_intersecvmsg_ipv6_dns(device_id, object_id,
                                            ipv6_address)

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_create_nec_intersecvmsg_ipv6_ntp(self):

        device_id = 'dev001'
        object_id = 'host001'
        ipv6_address = 'dead:beef::4'

        res = self.get_msa_instance()\
            .create_nec_intersecvmsg_ipv6_ntp(device_id, object_id,
                                            ipv6_address)

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_delete_nec_intersecvmsg_ipv6_ntp(self):

        device_id = 'dev001'
        object_id = 'host001'
        ipv6_address = 'dead:beef::4'

        res = self.get_msa_instance()\
            .delete_nec_intersecvmsg_ipv6_ntp(device_id, object_id,
                                            ipv6_address)

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)
