import inspect
import unittest

from job.auto.extension import routingpod
from job.lib.soap.msa import fortigateordercmdws
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

        msa_instance = fortigateordercmdws.FortigateOrderCommandWs(
                            job_instance.job_config,
                            job_instance.nal_endpoint_config,
                            pod_id)

        return msa_instance

    def test_create_fortigate_vdom(self):

        device_id = 'dev001'
        object_id = 'obj001'

        msa = self.get_msa_instance()
        res = msa.create_fortigate_vdom(device_id, object_id)

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_delete_fortigate_vdom(self):

        device_id = 'dev001'
        object_id = 'obj001'

        msa = self.get_msa_instance()
        res = msa.delete_fortigate_vdom(device_id, object_id)

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_create_fortigate_vlan_interface(self):

        device_id = 'dev001'
        object_id = 'obj001'
        vdom_name = 'vdom001'
        vlan_id = '1001'
        ip_address = '192.168.0.1'
        netmask = '255.255.255.0'
        port_no = '2001'
        management_flg = '1'

        msa = self.get_msa_instance()
        res = msa.create_fortigate_vlan_interface(device_id, object_id,
                                            vdom_name,
                                            vlan_id,
                                            ip_address,
                                            netmask,
                                            port_no,
                                            management_flg)
        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_update_fortigate_vlan_interface(self):

        device_id = 'dev001'
        object_id = 'obj001'
        vdom_name = 'vdom001'
        vlan_id = '1001'
        ip_address = '192.168.0.1'
        netmask = '255.255.255.0'
        port_no = '2001'
        management_flg = '1'

        msa = self.get_msa_instance()
        res = msa.update_fortigate_vlan_interface(device_id, object_id,
                                            vdom_name,
                                            vlan_id,
                                            ip_address,
                                            netmask,
                                            port_no,
                                            management_flg)
        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_delete_fortigate_vlan_interface(self):

        device_id = 'dev001'
        object_id = 'obj001'

        msa = self.get_msa_instance()
        res = msa.delete_fortigate_vlan_interface(device_id, object_id)
        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_create_fortigate_physical_interface(self):

        device_id = 'dev001'
        object_id = 'obj001'
        vdom_name = 'vdom001'
        ip_address = '192.168.0.1'
        netmask = '255.255.255.0'
        management_flg = 'no'

        msa = self.get_msa_instance()
        res = msa.create_fortigate_physical_interface(device_id, object_id,
                                            vdom_name,
                                            ip_address,
                                            netmask,
                                            management_flg)
        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_update_fortigate_physical_interface(self):

        device_id = 'dev001'
        object_id = 'obj001'
        vdom_name = 'vdom001'
        ip_address = '192.168.0.1'
        netmask = '255.255.255.0'
        management_flg = 'no'

        msa = self.get_msa_instance()
        res = msa.update_fortigate_physical_interface(device_id, object_id,
                                            vdom_name,
                                            ip_address,
                                            netmask,
                                            management_flg)
        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_delete_fortigate_physical_interface(self):

        device_id = 'dev001'
        object_id = 'obj001'

        msa = self.get_msa_instance()
        res = msa.delete_fortigate_physical_interface(device_id, object_id)
        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_create_fortigate_admin_profile(self):

        device_id = 'dev001'
        object_id = 'obj001'
        profile_name = 'profile_name123'

        msa = self.get_msa_instance()
        res = msa.create_fortigate_admin_profile(device_id, object_id,
                                                            profile_name)
        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_delete_fortigate_admin_profile(self):

        device_id = 'dev001'
        object_id = 'obj001'
        profile_name = 'profile_name123'

        msa = self.get_msa_instance()
        res = msa.delete_fortigate_admin_profile(device_id, object_id,
                                                            profile_name)
        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_create_fortigate_admin_user(self):

        device_id = 'dev001'
        object_id = 'obj001'
        vdom_name = 'vdom_name123'
        user_name = 'user_name123'
        password = 'password123'
        admin_prof = 'admin_prof123'

        msa = self.get_msa_instance()
        res = msa.create_fortigate_admin_user(device_id, object_id,
                                                        vdom_name,
                                                        user_name,
                                                        password,
                                                        admin_prof)
        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_delete_fortigate_admin_user(self):

        device_id = 'dev001'
        object_id = 'obj001'
        user_name = 'user_name123'

        msa = self.get_msa_instance()
        res = msa.delete_fortigate_admin_user(device_id, object_id, user_name)
        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_create_fortigate_vlan_ipv6_interface(self):

        device_id = 'dev001'
        object_id = 'eth0'
        vdom_name = 'vdom001'
        vlan_id = '1001'
        ipv6_address = 'dead:beaf::1'
        netmask = 48
        port_no = '2001'
        management_flg = '1'

        msa = self.get_msa_instance()
        res = msa.create_fortigate_vlan_ipv6_interface(
                                            device_id,
                                            object_id,
                                            vdom_name,
                                            vlan_id,
                                            port_no,
                                            management_flg,
                                            ipv6_address,
                                            netmask)

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_delete_fortigate_vlan_ipv6_interface(self):

        device_id = 'dev001'
        object_id = 'eth0'

        msa = self.get_msa_instance()
        res = msa.delete_fortigate_vlan_ipv6_interface(device_id, object_id)
        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_create_fortigate_physical_ipv6_interface(self):

        device_id = 'dev001'
        object_id = 'eth0'
        vdom_name = 'vdom001'
        ipv6_address = 'dead:beaf::1'
        netmask = 48
        management_flg = '1'

        msa = self.get_msa_instance()
        res = msa.create_fortigate_physical_ipv6_interface(
                                            device_id,
                                            object_id,
                                            vdom_name,
                                            management_flg,
                                            ipv6_address,
                                            netmask)

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_delete_fortigate_physical_ipv6_interface(self):

        device_id = 'dev001'
        object_id = 'eth0'
        ipv6_address = 'dead:beaf::1'
        netmask = 48

        msa = self.get_msa_instance()
        res = msa.delete_fortigate_physical_ipv6_interface(
                                            device_id,
                                            object_id,
                                            ipv6_address,
                                            netmask)

        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)
