import datetime
import json
import unittest

from job.conf import config
from job.lib.openstack.keystone import tokens
from job.lib.openstack.quantum import networks
from job.lib.openstack.quantum import ports
from job.lib.openstack.quantum import subnets


class TestSelectAPI(unittest.TestCase):
    # Do a test of Select.

#     ENDPOINT_URL = 'http://10.58.79.171:35357/v3'
#     REGION_ID = 'RegionOne'
#     ADMIN_TENANT_ID = '8cc49b2e5ce04eebbcbfeb4eab05bd90'

    ENDPOINT_URL = 'http://localhost:80/rest_openstack/index.py/min/v3'
    REGION_ID = 'region_unit_test1'
    ADMIN_TENANT_ID = '9ba7d56906cc4d0cbe055e06971b12a7'

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

    def test_quantum(self):

        endpoint = self.ENDPOINT_URL
        tenant_id = self.ADMIN_TENANT_ID
        admin_user_name = 'admin'
        admin_password = 'i-portal'
        nw_name = 'nw_ksp'
        subnet_name = 'subnet_ksp'
        port_name = 'port_ksp'
        cidr_ipv4 = '10.0.0.0/24'
        cidr_ipv6 = '2001:db8::/48'
        fixed_ips_ip_address_ipv4 = '10.0.0.1'
        fixed_ips_ip_address_ipv6 = '2001:DB8::10'

        port_id_list = []

        job_config = config.JobConfig()

        token = tokens.OscTokens(job_config).create_token(
                                admin_user_name, admin_password, endpoint)
        print('create_token')
        print(token)

        endpoint_array = tokens.OscTokens(job_config).get_endpoints(
            endpoint, token, admin_user_name, admin_password, tenant_id)
        print('get_endpoints')
        print(json.dumps(endpoint_array))

        endpoint_array['region_id'] = self.REGION_ID

        # Create Network
        nw_name_new = nw_name \
                        + datetime.datetime.today().strftime('%Y%m%d%H%M%S')
        res = networks.OscQuantumNetworks(job_config)\
                                .create_network(endpoint_array,
                                                nw_name_new,
                                                True,
                                                False,
                                                None,
                                                None
                                                )
        print('create_network')
        print(json.dumps(res))

        # Assertion
        self.assertGreaterEqual(len(res), 1)

        # Get Network
        nw_id_new = res['network']['id']
        res = networks.OscQuantumNetworks(job_config)\
                                    .get_network(endpoint_array, nw_id_new)
        print('get_network')
        print(json.dumps(res))

        # Assertion
        self.assertGreaterEqual(len(res), 1)

        # List Networks
        res = networks.OscQuantumNetworks(job_config)\
                                            .list_networks(endpoint_array)
        print('list_networks')
        print(json.dumps(res))

        # Assertion
        self.assertGreaterEqual(len(res), 1)

        # Create Subnet
        subnet_name_new = subnet_name \
                    + datetime.datetime.today().strftime('%Y%m%d%H%M%S')
        res = subnets.OscQuantumSubnets(job_config)\
            .create_subnet(
                endpoint_array, nw_id_new, cidr_ipv4, subnet_name_new,
                                    tenant_id, '4', fixed_ips_ip_address_ipv4)
        print('create_subnet')
        print(json.dumps(res))

        # Assertion
        self.assertGreaterEqual(len(res), 1)

        # Get Subnet
        subnet_id_new_ipv4 = res['subnet']['id']
        res = subnets.OscQuantumSubnets(job_config)\
                                .get_subnet(endpoint_array, subnet_id_new_ipv4)
        print('get_subnet')
        print(json.dumps(res))

        # Assertion
        self.assertGreaterEqual(len(res), 1)

        # Create Subnet
        subnet_name_new = subnet_name \
                    + datetime.datetime.today().strftime('%Y%m%d%H%M%S')
        res = subnets.OscQuantumSubnets(job_config)\
            .create_subnet(
                endpoint_array, nw_id_new, cidr_ipv6, subnet_name_new, '', '6')
        print('create_subnet')
        print(json.dumps(res))

        # Assertion
        self.assertGreaterEqual(len(res), 1)

        subnet_id_new_ipv6 = res['subnet']['id']

        # List Subnets
        res = subnets.OscQuantumSubnets(job_config)\
                                            .list_subnets(endpoint_array)
        print('list_subnets')
        print(json.dumps(res))

        # Assertion
        self.assertGreaterEqual(len(res), 1)

        # Create Port
        port_name_new = port_name + '-1-' \
                    + datetime.datetime.today().strftime('%Y%m%d%H%M%S')
        res = ports.OscQuantumPorts(job_config)\
                    .create_port(endpoint_array,
                                 nw_id_new,
                                 port_name_new,
                                 True
                                 )
        print('create_port')
        print(json.dumps(res))

        port_id_list.append(res['port']['id'])

        # Assertion
        self.assertGreaterEqual(len(res), 1)

        # Get Port
        res = ports.OscQuantumPorts(job_config)\
                                    .get_port(endpoint_array, port_id_list[0])

        print('get_port')
        print(json.dumps(res))

        # Assertion
        self.assertGreaterEqual(len(res), 1)

        # Create Port
        port_name_new = port_name + '-2-' \
                    + datetime.datetime.today().strftime('%Y%m%d%H%M%S')
        res = ports.OscQuantumPorts(job_config)\
                    .create_port(endpoint_array,
                                 nw_id_new,
                                 port_name_new,
                                 True,
                                 subnet_id_new_ipv4
                                 )
        print('create_port')
        print(json.dumps(res))

        port_id_list.append(res['port']['id'])

        # Create Port
        port_name_new = port_name + '-3-' \
                    + datetime.datetime.today().strftime('%Y%m%d%H%M%S')
        res = ports.OscQuantumPorts(job_config)\
                    .create_port(endpoint_array,
                                 nw_id_new,
                                 port_name_new,
                                 True,
                                 subnet_id_new_ipv6
                                 )
        print('create_port')
        print(json.dumps(res))

        port_id_list.append(res['port']['id'])

        # Create Port
        port_name_new = port_name + '-4-' \
                    + datetime.datetime.today().strftime('%Y%m%d%H%M%S')
        res = ports.OscQuantumPorts(job_config)\
                    .create_port(endpoint_array,
                                 nw_id_new,
                                 port_name_new,
                                 True,
                                 '',
                                 '10.0.0.10'
                                 )
        print('create_port')
        print(json.dumps(res))

        port_id_list.append(res['port']['id'])

        # Assertion
        self.assertGreaterEqual(len(res), 1)

        # List Ports
        res = ports.OscQuantumPorts(job_config).list_ports(endpoint_array)
        print('list_ports')
        print(json.dumps(res))

        # Assertion
        self.assertGreaterEqual(len(res), 1)

        for port_id in port_id_list:

            # Detach Port
            res = ports.OscQuantumPorts(job_config)\
                            .detach_port_device(endpoint_array, port_id)
            print('detach_port_device')
            print(json.dumps(res))

            # Assertion
            self.assertGreaterEqual(len(res), 1)

            # Delete Port
            res = ports.OscQuantumPorts(job_config)\
                                    .delete_port(endpoint_array, port_id)
            print('delete_port')
            print(json.dumps(res))

            # Assertion
            self.assertEqual(len(res), 0)

        # Create Port(Dual Stack)
        fixed_ips = [
            {
                'subnet_id': subnet_id_new_ipv4,
                'ip_address': fixed_ips_ip_address_ipv4,
            },
            {
                'subnet_id': subnet_id_new_ipv6,
                'ip_address': fixed_ips_ip_address_ipv6,
            }
        ]
        port_name_new = port_name \
                    + datetime.datetime.today().strftime('%Y%m%d%H%M%S')
        res = ports.OscQuantumPorts(job_config)\
                .create_port_dual_stack(
                    endpoint_array, nw_id_new, port_name_new, True, fixed_ips)
        print('create_port_dual_stack')
        print(json.dumps(res))

        port_id_new = res['port']['id']

        # Get Port
        res = ports.OscQuantumPorts(job_config)\
                                    .get_port(endpoint_array, port_id_new)
        print('get_port(create_port_dual_stack)')
        print(json.dumps(res))

        # Update Port
        fixed_ips = [
            {
                'subnet_id': subnet_id_new_ipv4,
                'ip_address': fixed_ips_ip_address_ipv4,
            },
            {
                'subnet_id': subnet_id_new_ipv6,
                'ip_address': fixed_ips_ip_address_ipv6,
            },
        ]
        res = ports.OscQuantumPorts(job_config)\
            .update_port(endpoint_array, port_id_new, port_name_new + 'upd',
                         False, fixed_ips)
        print('update_port')
        print(json.dumps(res))

        # Assertion
        self.assertGreaterEqual(len(res), 1)

        # Get Port
        res = ports.OscQuantumPorts(job_config)\
                                    .get_port(endpoint_array, port_id_new)
        print('get_port(update_port)')
        print(json.dumps(res))

        # Delete Port
        res = ports.OscQuantumPorts(job_config)\
                                .delete_port(endpoint_array, port_id_new)
        print('delete_port')
        print(json.dumps(res))

        # Assertion
        self.assertEqual(len(res), 0)

        # List Ports
        res = ports.OscQuantumPorts(job_config).list_ports(endpoint_array)
        print('list_ports')
        print(json.dumps(res))

        # Assertion
        self.assertGreaterEqual(len(res), 1)

        # Delete Subnet
        res = subnets.OscQuantumSubnets(job_config)\
                            .delete_subnet(endpoint_array, subnet_id_new_ipv4)
        print('delete_subnet')
        print(json.dumps(res))

        # Assertion
        self.assertEqual(len(res), 0)

        res = subnets.OscQuantumSubnets(job_config)\
                            .delete_subnet(endpoint_array, subnet_id_new_ipv6)
        print('delete_subnet')
        print(json.dumps(res))

        # Assertion
        self.assertEqual(len(res), 0)

        # Delete Network
        res = networks.OscQuantumNetworks(job_config)\
                                .delete_network(endpoint_array, nw_id_new)
        print('delete_network')
        print(json.dumps(res))

        # Assertion
        self.assertEqual(len(res), 0)

    def test_quantum_endpoint_not_found(self):

        endpoint = self.ENDPOINT_URL
        tenant_id = self.ADMIN_TENANT_ID
        admin_user_name = 'admin'
        admin_password = 'i-portal'
        nw_name = 'nw_ksp'

        job_config = config.JobConfig()

        token = tokens.OscTokens(job_config).create_token(
                                admin_user_name, admin_password, endpoint)

        endpoint_array = tokens.OscTokens(job_config).get_endpoints(
            endpoint, token, admin_user_name, admin_password, tenant_id)

        endpoint_array['region_id'] = 'regionNotfound'

        nw_name_new = nw_name \
                        + datetime.datetime.today().strftime('%Y%m%d%H%M%S')

        # Create Network
        try:
            networks.OscQuantumNetworks(job_config)\
                                .create_network(endpoint_array, nw_name_new)

        except SystemError as e:
            if e.args[0] != networks.OscQuantumNetworks.EXCEPT_MSG08:
                raise
