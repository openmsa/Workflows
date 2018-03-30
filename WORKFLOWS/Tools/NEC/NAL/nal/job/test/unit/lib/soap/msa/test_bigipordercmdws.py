import inspect
import unittest

from job.auto.extension import routingpod
from job.lib.soap.msa import bigipordercmdws
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

        msa_instance = bigipordercmdws.BigIpOrderCommandWs(
                            job_instance.job_config,
                            job_instance.nal_endpoint_config,
                            pod_id)

        return msa_instance

    def test_create_big_ip_partition(self):

        device_id = 'dev001'
        partition_id = 'partition001'

        msa = self.get_msa_instance()
        res = msa.create_big_ip_partition(device_id, partition_id)

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_delete_big_ip_partition(self):

        device_id = 'dev001'
        partition_id = 'partition001'

        msa = self.get_msa_instance()
        res = msa.delete_big_ip_partition(device_id, partition_id)

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_create_big_ip_route_domain(self):

        device_id = 'dev001'
        partition_id = 'partition001'
        rtdomain_id = 'rt001'

        msa = self.get_msa_instance()
        res = msa.create_big_ip_route_domain(
                        device_id, partition_id, rtdomain_id)

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_delete_big_ip_route_domain(self):

        device_id = 'dev001'
        partition_id = 'partition001'

        msa = self.get_msa_instance()
        res = msa.delete_big_ip_route_domain(device_id, partition_id)

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_create_big_ip_default_route_domain(self):

        device_id = 'dev001'
        partition_id = 'partition001'
        rtdomain_id = 'rt001'

        msa = self.get_msa_instance()
        res = msa.create_big_ip_default_route_domain(
                        device_id, partition_id, rtdomain_id)

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_delete_big_ip_default_route_domain(self):

        device_id = 'dev001'
        partition_id = 'partition001'

        msa = self.get_msa_instance()
        res = msa.delete_big_ip_default_route_domain(device_id, partition_id)

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_create_big_ip_vlan(self):

        device_id = 'dev001'
        partition_id = 'partition001'
        vlan_name = 'vlan001'
        params_interface_name = 'ifname1234'
        vlan_id = '10001'

        msa = self.get_msa_instance()
        res = msa.create_big_ip_vlan(device_id, partition_id,
                                    vlan_name,
                                    params_interface_name,
                                    vlan_id)

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_delete_big_ip_vlan(self):

        device_id = 'dev001'
        partition_id = 'partition001'
        vlan_name = 'vlan001'

        msa = self.get_msa_instance()
        res = msa.delete_big_ip_vlan(device_id, partition_id, vlan_name)

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_create_big_ip_physical_ip(self):

        device_id = 'dev001'
        partition_id = 'partition001'
        physical_ip_name = 'ip001'
        ip_address = '10.0.0.1'
        netmask = '24'
        vlan_name = 'vlan001'

        msa = self.get_msa_instance()
        res = msa.create_big_ip_physical_ip(device_id, partition_id,
                                           physical_ip_name,
                                           ip_address,
                                           netmask,
                                           vlan_name)

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_delete_big_ip_physical_ip(self):

        device_id = 'dev001'
        partition_id = 'partition001'
        physical_ip_name = 'ip001'

        msa = self.get_msa_instance()
        res = msa.delete_big_ip_physical_ip(device_id, partition_id,
                                           physical_ip_name)
        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_create_big_ip_vip(self):

        device_id = 'dev001'
        partition_id = 'partition001'
        vip_name = 'vip001'
        ip_address = '10.0.0.1'
        netmask = '24'
        vlan_name = 'vlan001'
        traffic_name = 'tr001'

        msa = self.get_msa_instance()
        res = msa.create_big_ip_vip(device_id, partition_id,
                                            vip_name,
                                            ip_address,
                                            netmask,
                                            vlan_name,
                                            traffic_name)

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_delete_big_ip_vip(self):

        device_id = 'dev001'
        partition_id = 'partition001'
        vip_name = 'vip001'

        msa = self.get_msa_instance()
        res = msa.delete_big_ip_vip(device_id, partition_id, vip_name)

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_create_big_ip_user_manager(self):

        device_id = 'dev001'
        object_id = 'partition001'
        user_id = 'user123'
        role_name = 'manager'
        password = 'password123'

        msa = self.get_msa_instance()
        res = msa.create_big_ip_user_manager(device_id, object_id,
                                            user_id,
                                            role_name,
                                            password)

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_delete_big_ip_user_manager(self):

        device_id = 'dev001'
        object_id = 'partition001'
        user_id = 'user123'

        msa = self.get_msa_instance()
        res = msa.delete_big_ip_user_manager(device_id, object_id,
                                            user_id)

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_create_big_ip_user_certificate_manager(self):

        device_id = 'dev001'
        object_id = 'partition001'
        user_id = 'user123'
        role_name = 'certificate-manager'
        password = 'password123'

        msa = self.get_msa_instance()
        res = msa.create_big_ip_user_certificate_manager(device_id, object_id,
                                            user_id,
                                            role_name,
                                            password)

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_delete_big_ip_user_certificate_manager(self):

        device_id = 'dev001'
        object_id = 'partition001'
        user_id = 'user123'

        msa = self.get_msa_instance()
        res = msa.delete_big_ip_user_certificate_manager(device_id, object_id,
                                            user_id)

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_create_f5_big_ip_physical_ipv6(self):

        device_id = 'dev001'
        object_id = 'partition_id123_2016_IP'
        partition_id = 'partition_id123'
        address = '2001:db8::e'
        netmask = '48'
        vlan_name = 'partition_id123_2016'

        msa = self.get_msa_instance()
        res = msa.create_f5_big_ip_physical_ipv6(device_id, object_id,
                                          partition_id,
                                          address,
                                          netmask,
                                          vlan_name)

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_delete_f5_big_ip_physical_ipv6(self):

        device_id = 'dev001'
        object_id = 'partition_id123_2016_IP'
        partition_id = 'partition_id123'
        self_ipv6_end_number = 1

        msa = self.get_msa_instance()
        res = msa.delete_f5_big_ip_physical_ipv6(device_id,
                                                 object_id,
                                                 partition_id,
                                                 self_ipv6_end_number)

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_create_f5_big_ip_ipv6(self):

        device_id = 'dev001'
        object_id = 'partition_id123_2016_IP'
        partition_id = 'partition_id123'
        address = '2001:db8::e'
        netmask = '48'
        vlan_name = 'partition_id123_2016'
        traffic_name = 'tr001'

        msa = self.get_msa_instance()
        res = msa.create_f5_big_ip_ipv6(device_id, partition_id,
                                    object_id,
                                    address,
                                    netmask,
                                    vlan_name,
                                    traffic_name)

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_delete_f5_big_ip_ipv6(self):

        device_id = 'dev001'
        object_id = 'partition_id123_2016_IP'
        partition_id = 'partition_id123'
        self_ipv6_end_number = 1

        msa = self.get_msa_instance()
        res = msa.delete_f5_big_ip_ipv6(device_id, object_id,
                                            partition_id,
                                            self_ipv6_end_number)

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_create_big_ip_route(self):

        device_id = 'dev001'
        object_id = 'partition_id123_2016_IP'
        route = '0.0.0.0/0'
        gateway = '10.58.10.1'

        msa = self.get_msa_instance()
        res = msa.create_big_ip_route(device_id, object_id, route, gateway)

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_delete_big_ip_route(self):

        device_id = 'dev001'
        object_id = 'partition_id123_2016_IP'
        route = '0.0.0.0/0'

        msa = self.get_msa_instance()
        res = msa.delete_big_ip_route(device_id, object_id, route)

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_create_f5_big_ip_ipv6_static_route(self):

        device_id = 'dev001'
        object_id = 'partition_id123_2016_IP'
        ipv6_route = '::/0'
        gateway_ipv6_address = '2001:db8::e'
        is_default_gateway = 'yes'
        route_name = 'defaultGWv6'
        destination_ipv6_address = '::'
        destination_ipv6_netmask = '0'

        msa = self.get_msa_instance()
        res = msa.create_f5_big_ip_ipv6_static_route(device_id,
                                               object_id,
                                               ipv6_route,
                                               gateway_ipv6_address,
                                               is_default_gateway,
                                               route_name,
                                               destination_ipv6_address,
                                               destination_ipv6_netmask)

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_delete_f5_big_ip_ipv6_static_route(self):

        device_id = 'dev001'
        object_id = 'partition_id123_2016_IP'
        route_name = 'defaultGWv6'

        msa = self.get_msa_instance()
        res = msa.delete_f5_big_ip_ipv6_static_route(device_id,
                                               object_id,
                                               route_name)

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)
