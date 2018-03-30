import json
import mysql.connector
import os
import sys
import unittest
import urllib.request
import urllib.parse

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../../../')
from rest.api import router
from rest.conf import config


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

        con, cur = self.connect_db()

        global extension_info
        extension_info = {
            'group_id': 'group_idxxxxxxxxxx',
            'dc_id': 'dc_idxxxxxxxxxx',
            'tenant_name': 'tenant_namexxxxxxxxxx',
            'pod_id': 'pod_idxxxxxxxxxx',
            'tenant_id': 'tenant_idxxxxxxxxxx',
            'IaaS_region_id': 'IaaS_region_idxxxxxxxxxx',
            'IaaS_tenant_id': 'IaaS_tenant_idxxxxxxxxxx',
            'IaaS_network_type': 'IaaS_network_typexxxxxxxxxx',
            'IaaS_network_id': 'IaaS_network_idxxxxxxxxxx',
            'IaaS_network_name': 'IaaS_network_namexxxxxxxxxx',
            'IaaS_segmentation_id': 'IaaS_segmentation_idxxxxxxxxxx',
            'IaaS_subnet_id': 'IaaS_subnet_id_xxxxxxxxxx',
            'IaaS_subnet_id_v6': 'IaaS_subnet_id_v6_xxxxxxxxxx',
            'wan_network_id': 'wan_network_idxxxxxxxxxx',
            'default_gateway': 'default_gatewayxxxxxxxxxx',
            'vrrp_address': 'vrrp_addressxxxxxxxxxx',
            'ce1_address': 'ce1_addressxxxxxxxxxx',
            'ce2_address': 'ce2_addressxxxxxxxxxx',
            'vrrp_address_v6': 'dead:beaf::1',
            'ce1_address_v6': 'dead:beaf::2',
            'ce2_address_v6': 'dead:beaf::3',
            'ce1_info': '{"aaa":"aaaaaaaa","bbb":"bbbbbb","ccc":"ccccccc"}',
            'ce2_info': '{"aaa":"aaaaaaaa","bbb":"bbbbbb","ccc":"ccccccc"}',
        }

        # Execute SQL
        param_vals = ['test_create_id-0ac6cb428b23', '2016-12-31 23:59:59',
                      'test_update_id-0ac6cb428b23', '2016-12-31 23:59:59',
                      0,
                      json.dumps(extension_info)]
        cur.execute("INSERT INTO WIM_DC_CONNECT_MEMBER_MNG " +
                    "(create_id, create_date, update_id, update_date, " +
                    "delete_flg, extension_info) " +
                    " VALUES (%s, %s, %s, %s, %s, %s)", param_vals)

        cur.execute('SELECT last_insert_id() FROM WIM_DC_CONNECT_MEMBER_MNG')
        global ID
        ID = cur.fetchall()[0][0]

        self.cut_db(con, cur)

    def destroy_fixtures(self):

        con, cur = self.connect_db()

        # Execute SQL
        param_vals = ['test_create_id-0ac6cb428b23']
        cur.execute("DELETE FROM WIM_DC_CONNECT_MEMBER_MNG WHERE " +
                    "create_id = %s", param_vals)

        self.cut_db(con, cur)

    def connect_db(self):
            # Connect Database
            con = mysql.connector.connect(
                host=getattr(config, 'MYSQL_HOSTNAME', ''),
                db=getattr(config, 'MYSQL_DBNAME', ''),
                user=getattr(config, 'MYSQL_USERID', ''),
                passwd=getattr(config, 'MYSQL_PASSWORD', ''),
                buffered=True)

            # Set Autocommit Off
            con.autocommit = False

            # Open Cursor
            cur = con.cursor()

            return con, cur

    def cut_db(self, con, cur):
        # Commit Transaction
        con.commit()

        # Close Cursor
        cur.close()

        # Close Database
        con.close()

    def test_select_api(self):

        request_params = {
            'query': {
                'delete_flg': '0', 'ID': ID
            },
            'resource': 'dc-con-members',
            'method': 'GET',
            'id': []
        }

        res = router.Router().routing(request_params)
        status = res['status']
        res_data = res['message'].decode('utf-8')
        res_data = json.loads(res_data)

        self.assertEqual(status, '200 OK')
        self.assertEqual(len(res_data), 1)
        self.assertEqual(res_data[0]['ID'], ID)
        self.assertEqual(res_data[0]['create_id'],
                         'test_create_id-0ac6cb428b23')
        self.assertEqual(res_data[0]['update_id'],
                         'test_update_id-0ac6cb428b23')
        self.assertEqual(res_data[0]['delete_flg'], '0')
        self.assertEqual(res_data[0].get('extension_info', ''), '')

        for key in extension_info:
            self.assertEqual(res_data[0].get(key), extension_info[key])

    def test_insert_api(self):

        insert_params = {
            'create_id': 'test_create_id-0ac6cb428b23',
            'update_id': 'test_create_id-0ac6cb428b23',
            'delete_flg': 0,
            'group_id': 'group_id-bb6d-6bb9bd380a11',
            'dc_id': 'dc_id-bb6d-6bb9bd380a11',
            'tenant_name': 'tenant_namexxxxxxxxxx',
            'pod_id': 'pod_idxxxxxxxxxx',
            'tenant_id': 'tenant_id-bb6d-6bb9bd380a11',
            'IaaS_region_id': 'IaaS_region_idxxxxxxxxxx',
            'IaaS_tenant_id': 'IaaS_tenant_idxxxxxxxxxx',
            'IaaS_network_type': 'xlan',
            'IaaS_network_id': 'IaaS_network_id-bb6d-6bb9bd380a11',
            'IaaS_network_name': 'IaaS_network_namexxxxxxxxxx',
            'IaaS_segmentation_id': 'IaaS_segmentation_id-bb6d-6bb9bd380a11',
            'IaaS_subnet_id': 'IaaS_subnet_id_xxxxxxxxxx',
            'IaaS_subnet_id_v6': 'IaaS_subnet_id_v6_xxxxxxxxxx',
            'wan_network_id': 'wan_network_id-bb6d-6bb9bd380a11',
            'default_gateway': '10.10.10.10',
            'vrrp_address': 'vrrp_addressxxxxxxxxxx',
            'ce1_address': 'ce1_addressxxxxxxxxxx',
            'ce2_address': 'ce2_addressxxxxxxxxxx',
            'vrrp_address_v6': 'dead:beaf::1',
            'ce1_address_v6': 'dead:beaf::2',
            'ce2_address_v6': 'dead:beaf::3',
            'ce1_info': '{"aaa":"aaaaaaaa","bbb":"bbbbbb","ccc":"ccccccc"}',
            'ce2_info': '{"aaa":"aaaaaaaa","bbb":"bbbbbb","ccc":"ccccccc"}',
        }
        request_params = {
            'body': insert_params,
            'query': {},
            'resource': 'dc-con-members',
            'method': 'POST',
            'id': []
        }

        res = router.Router().routing(request_params)
        status = res['status']
        res_data = res['message'].decode('utf-8')
        res_data = json.loads(res_data)

        # Assertion
        self.assertEqual(status, '200 OK')
        self.assertEqual(len(res_data), 1)
        self.assertTrue('ID' in res_data)

        # Assertion(check select)
        request_params = {
            'query': {
                'group_id': 'group_id-bb6d-6bb9bd380a11',
                'dc_id': 'dc_id-bb6d-6bb9bd380a11',
                'tenant_name': 'tenant_namexxxxxxxxxx',
                'pod_id': 'pod_idxxxxxxxxxx',
                'tenant_id': 'tenant_id-bb6d-6bb9bd380a11',
            },
            'resource': 'dc-con-members',
            'method': 'GET',
            'id': []
        }
        res = router.Router().routing(request_params)
        status = res['status']
        res_data = res['message'].decode('utf-8')
        res_data = json.loads(res_data)

        self.assertEqual(status, '200 OK')
        self.assertEqual(len(res_data), 1)

        for key in insert_params:
            if key == 'delete_flg':
                self.assertEqual(res_data[0].get(key), str(insert_params[key]))
            else:
                self.assertEqual(res_data[0].get(key), insert_params[key])

    def test_update_api(self):

        update_params = {
            'update_id': 'test_update_id-0ac6cb428b23',
            'group_id': 'group_id-ad4c-4cc6ea276a55',
            'dc_id': 'dc_id-ad4c-4cc6ea276a55',
            'tenant_id': 'tenant_id-ad4c-4cc6ea276a55',
            'wan_network_id': 'wan_network_id-ad4c-4cc6ea276a55',
            'ce1_info': '{}',
            'ce2_info': '{}',
            'IaaS_network_type': 'xlan',
            'IaaS_network_id': 'IaaS_network_id-ad4c-4cc6ea276a55',
            'IaaS_segmentation_id': 'IaaS_segmentation_id-ad4c-4cc6ea276a55',
            'IaaS_subnet_id': 'IaaS_subnet_id_xxxxxxxxxx',
            'IaaS_subnet_id_v6': 'IaaS_subnet_id_v6_xxxxxxxxxx',
            'vrrp_address_v6': 'dead:beaf::1',
            'ce1_address_v6': 'dead:beaf::2',
            'ce2_address_v6': 'dead:beaf::3',
        }
        request_params = {
            'body': update_params,
            'query': {},
            'resource': 'dc-con-members',
            'method': 'PUT',
            'id': [ID]
        }

        res = router.Router().routing(request_params)
        status = res['status']
        res_data = res['message'].decode('utf-8')
        res_data = json.loads(res_data)

        # Assertion
        self.assertEqual(status, '200 OK')
        self.assertEqual(res_data, True)

        # Assertion(check select)
        request_params = {
            'query': {},
            'resource': 'dc-con-members',
            'method': 'GET',
            'id': [ID]
        }
        res = router.Router().routing(request_params)
        status = res['status']
        res_data = res['message'].decode('utf-8')
        res_data = json.loads(res_data)

        self.assertEqual(status, '200 OK')
        self.assertEqual(len(res_data), 1)

        for key in update_params:
            if key == 'delete_flg':
                self.assertEqual(res_data[0].get(key), str(update_params[key]))
            else:
                self.assertEqual(res_data[0].get(key), update_params[key])

    def test_delete_api(self):

        request_params = {
            'body': {},
            'query': {},
            'resource': 'dc-con-members',
            'method': 'DELETE',
            'id': [ID]
        }

        res = router.Router().routing(request_params)
        status = res['status']
        res_data = res['message'].decode('utf-8')
        res_data = json.loads(res_data)

        # Assertion
        self.assertEqual(status, '200 OK')
        self.assertEqual(res_data, True)

        # Assertion(Select Check)
        con, cur = self.connect_db()
        cur.execute("SELECT ID FROM WIM_DC_CONNECT_MEMBER_MNG WHERE ID = %s",
                    [ID])
        self.assertEqual(cur.fetchall(), [])
        self.cut_db(con, cur)
