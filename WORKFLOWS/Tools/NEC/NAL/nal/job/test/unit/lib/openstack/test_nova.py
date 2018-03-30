import datetime
import json
import time
import unittest

from job.conf import config
from job.lib.openstack.keystone import tokens
from job.lib.openstack.nova import flavors
from job.lib.openstack.nova import servers
from job.lib.openstack.quantum import networks
from job.lib.openstack.quantum import ports
from job.lib.openstack.quantum import subnets


class TestSelectAPI(unittest.TestCase):
    # Do a test of Select.

#     ENDPOINT_URL = 'http://10.58.79.171:35357/v3'
#     REGION_ID = 'RegionOne'
#     ADMIN_TENANT_ID = '8cc49b2e5ce04eebbcbfeb4eab05bd90'

#     ENDPOINT_URL = 'http://10.58.70.211:35357/v3'
#     REGION_ID = 'RegionOne'
#     ADMIN_TENANT_ID = '997f827897374719a55f573c0ff033bf'

#     WAIT_TIME_CREATE_SERVER = 90
#     IMAGE_ID = '149a462d-6a2c-453f-92c5-1d65867f16bd'

    ENDPOINT_URL = 'http://localhost:80/rest_openstack/index.py/min/v3'
    REGION_ID = 'region_unit_test1'
    ADMIN_TENANT_ID = '9ba7d56906cc4d0cbe055e06971b12a7'

    WAIT_TIME_CREATE_SERVER = 0
    IMAGE_ID = '55f7012b-4c5b-4fb8-90c7-2e1e1205e128'

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

    def test_nova(self):

        import random
        mac_address = []
        for i in range(6):
            mac_address.append('%02x' % random.choice(range(1, 256)))

        print(':'.join(mac_address))


        endpoint = self.ENDPOINT_URL
        tenant_id = self.ADMIN_TENANT_ID
        admin_user_name = 'admin'
        admin_password = 'i-portal'
        sv_name = 'sv_ksp'
        nw_name = 'nw_ksp'
        subnet_name = 'subnet_ksp'
        port_name = 'port_ksp'
        cidr = '0.0.0.0/27'

        imageRef = self.IMAGE_ID
        flavorRef = '1'

        network_list = [
            {
                'uuid': '',
                'port': '',
            }
        ]

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
                                .create_network(endpoint_array, nw_name_new)
        print('create_network')
        print(json.dumps(res))

        # Create Subnet
        nw_id_new = res['network']['id']
        subnet_name_new = subnet_name \
                    + datetime.datetime.today().strftime('%Y%m%d%H%M%S')
        res = subnets.OscQuantumSubnets(job_config)\
            .create_subnet(endpoint_array, nw_id_new, cidr, subnet_name_new)
        print('create_subnet')
        print(json.dumps(res))

        # Create Port
        subnet_id_new = res['subnet']['id']
        port_name_new = port_name \
                    + datetime.datetime.today().strftime('%Y%m%d%H%M%S')
        res = ports.OscQuantumPorts(job_config)\
                    .create_port(endpoint_array, nw_id_new, port_name_new)
        port_id_new = res['port']['id']
        print('create_port')
        print(json.dumps(res))

        # List Server
        res = servers.OscServers(job_config)\
                                .list_servers(endpoint_array)
        print('list_servers')
        print(json.dumps(res))

        # Assertion
        self.assertGreaterEqual(len(res), 1)

        # List Flavors
        res = flavors.OscNovaFlavors(job_config)\
                .list_flavors(endpoint_array)
        print('list_flavors')
        print(json.dumps(res))

        # Assertion
        self.assertGreaterEqual(len(res), 1)

        # Create Server
        sv_name_new = sv_name \
                    + datetime.datetime.today().strftime('%Y%m%d%H%M%S')
        network_list[0]['uuid'] = nw_id_new
        network_list[0]['port'] = port_id_new
        res = servers.OscServers(job_config).create_server(
            endpoint_array, sv_name_new, imageRef, flavorRef, network_list)
        print('create_server')
        print(json.dumps(res))

        # Assertion
        self.assertGreaterEqual(len(res), 1)

        time.sleep(self.WAIT_TIME_CREATE_SERVER)

        # Get Server
        server_id_new = res['server']['id']
        res = servers.OscServers(job_config)\
                                .get_server(endpoint_array, server_id_new)
        print('get_server')
        print(json.dumps(res))

        # Assertion
        self.assertGreaterEqual(len(res), 1)

        # Action Server(Resume)
        actionkey = servers.OscServers(job_config).SERVER_ACTION_RESUME
        res = servers.OscServers(job_config)\
                .action_server(endpoint_array, server_id_new, actionkey)
        print('action_server(resume)')
        print(json.dumps(res))

        # Assertion
        self.assertEqual(len(res), 0)

        # Action Server(Reset Network)
        actionkey = servers.OscServers(job_config).SERVER_ACTION_RESETNETWORK
        res = servers.OscServers(job_config)\
                .action_server(endpoint_array, server_id_new, actionkey)
        print('action_server(reset network)')
        print(json.dumps(res))

        # Assertion
        self.assertEqual(len(res), 0)

        # Action Server(Suspend)
        actionkey = servers.OscServers(job_config).SERVER_ACTION_SUSPEND
        res = servers.OscServers(job_config)\
                .action_server(endpoint_array, server_id_new, actionkey)
        print('action_server(suspend)')
        print(json.dumps(res))

        # Assertion
        self.assertEqual(len(res), 0)

        # Action Server(Reboot)
        actionkey = servers.OscServers(job_config).SERVER_ACTION_REBOOT
        boottype = servers.OscServers(job_config).SERVER_REBOOT_TYPE_SOFT
        res = servers.OscServers(job_config).action_server(
                        endpoint_array, server_id_new, actionkey, boottype)
        print('action_server(reboot)')
        print(json.dumps(res))

        # Assertion
        self.assertEqual(len(res), 0)

        # Action Server(Resize)
        actionkey = servers.OscServers(job_config).SERVER_ACTION_RESIZE
        res = servers.OscServers(job_config)\
                .action_server(endpoint_array, server_id_new, None, '2')
        print('action_server(resize)')
        print(json.dumps(res))

        # Assertion
        self.assertEqual(len(res), 0)

        # Action Server(Confirm Resize)
        actionkey = servers.OscServers(job_config).SERVER_ACTION_CONFIRMRESIZE
        res = servers.OscServers(job_config)\
                .action_server(endpoint_array, server_id_new, actionkey)
        print('action_server(confirm resize)')
        print(json.dumps(res))

        # Assertion
        self.assertEqual(len(res), 0)

        # Action Server(OS Start)
        actionkey = servers.OscServers(job_config).SERVER_ACTION_OS_START
        res = servers.OscServers(job_config)\
                .action_server(endpoint_array, server_id_new, actionkey)
        print('action_server(os start)')
        print(json.dumps(res))

        # Assertion
        self.assertEqual(len(res), 0)

        # Action Server(OS Stop)
        actionkey = servers.OscServers(job_config).SERVER_ACTION_OS_STOP
        res = servers.OscServers(job_config)\
                .action_server(endpoint_array, server_id_new, actionkey)
        print('action_server(os stop)')
        print(json.dumps(res))

        # Assertion
        self.assertEqual(len(res), 0)

        # Action Server(Get Console)
        actionkey = servers.OscServers(job_config).SERVER_ACTION_GETCONSOLE
        res = servers.OscServers(job_config).action_server(
            endpoint_array, server_id_new, actionkey, None, None, 'xvpvnc')
        print('action_server(get console)')
        print(json.dumps(res))

        # Assertion
        self.assertGreaterEqual(len(res), 1)

        # Action Server(Status Pause)
        actionkey = servers.OscServers(job_config).SERVER_STATUS_PAUSE
        res = servers.OscServers(job_config)\
                .action_server(endpoint_array, server_id_new, actionkey)
        print('action_server(status pause)')
        print(json.dumps(res))

        # Assertion
        self.assertEqual(len(res), 0)

        # Attach Interface
        res = servers.OscServers(job_config)\
                .attach_interface(endpoint_array, server_id_new, port_id_new)
        print('attach_interface')
        print(json.dumps(res))

        # Assertion
        self.assertGreaterEqual(len(res), 1)

        # List Interfaces
        res = servers.OscServers(job_config)\
                .list_interfaces(endpoint_array, server_id_new)
        print('list_interfaces')
        print(json.dumps(res))

        # Assertion
        self.assertGreaterEqual(len(res), 1)

        # List Flavors
        res = flavors.OscNovaFlavors(job_config).list_flavors(endpoint_array)
        print('list_flavors')
        print(json.dumps(res))

        # Assertion
        self.assertGreaterEqual(len(res), 1)

        # Detach Interface
        res = servers.OscServers(job_config)\
                .detach_interface(endpoint_array, server_id_new, port_id_new)
        print('detach_interface')
        print(json.dumps(res))

        # Assertion
        self.assertEqual(len(res), 0)

        # List Server
        res = servers.OscServers(job_config)\
                                .list_servers(endpoint_array)
        print('list_servers')
        print(json.dumps(res))

        # Assertion
        self.assertGreaterEqual(len(res), 1)

        # Delete Port
        res = ports.OscQuantumPorts(job_config)\
                                .delete_port(endpoint_array, port_id_new)
        print('delete_port')
        print(json.dumps(res))

        # Delete Subnet
        res = subnets.OscQuantumSubnets(job_config)\
                            .delete_subnet(endpoint_array, subnet_id_new)
        print('delete_subnet')
        print(json.dumps(res))

        # Delete Network
        res = networks.OscQuantumNetworks(job_config)\
                                .delete_network(endpoint_array, nw_id_new)
        print('delete_network')
        print(json.dumps(res))

        # Delete Server
        res = servers.OscServers(job_config)\
                                .delete_server(endpoint_array, server_id_new)
        print('delete_server')
        print(json.dumps(res))

        # Assertion
        self.assertEqual(len(res), 0)

    def test_nova_endpoint_not_found(self):

        endpoint = self.ENDPOINT_URL
        tenant_id = self.ADMIN_TENANT_ID
        admin_user_name = 'admin'
        admin_password = 'i-portal'
        imageRef = '55f7012b-4c5b-4fb8-90c7-2e1e1205e128'
        flavorRef = '2'

        network_list = [
            {
                'uuid': '6141844163e191152455519bc83d2bda',
                'port': 'b411cd48241a5d2bc11b02cac16e2f91',
            }
        ]

        job_config = config.JobConfig()

        token = tokens.OscTokens(job_config).create_token(
                                admin_user_name, admin_password, endpoint)

        endpoint_array = tokens.OscTokens(job_config).get_endpoints(
            endpoint, token, admin_user_name, admin_password, tenant_id)

        endpoint_array['region_id'] = 'regionNotfound'

        # Create Server
        try:
            servers.OscServers(job_config).create_server(endpoint_array,
                            'sv_name_new', imageRef, flavorRef, network_list)

        except SystemError as e:
            if e.args[0] != servers.OscServers.EXCEPT_MSG08:
                raise
