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

        con, cur = self.connect_db()

        global extension_info
        extension_info = {
            'tenant_name': 'xxxxxxxxxx',
            'pod_id': 'xxxxxxxxxx',
            'tenant_id': 'xxxxxxxxxx',
            'IaaS_region_id': 'xxxxxxxxxx',
            'IaaS_tenant_id': 'xxxxxxxxxx',
            'IaaS_network_id': 'xxxxxxxxxx',
            'IaaS_network_type': 'xxxxxxxxxx',
            'IaaS_segmentation_id': 'xxxxxxxxxx',
            'vlan_id': 'xxxxxxxxxx',
            'vxlangw_pod_id': 'xxxxxxxxxx',
            'rule_id': 'xxxxxxxxxx',
            'nal_vlan_info': '{"aaa":"aaaaaaaa","bbb":"bbbbbb","ccc":"ccccccc"}'
        }

        # Execute SQL
        param_vals = ['test_create_id-0ac6cb428b23', '2016-12-31 23:59:59',
                      'test_update_id-0ac6cb428b23', '2016-12-31 23:59:59', 0,
                      'network_id-dd7e-0ac6cb428b23',
                      json.dumps(extension_info)]
        cur.execute("INSERT INTO NAL_VIRTUAL_LAN_MNG(create_id, " +
                    "create_date, update_id, update_date, delete_flg, " +
                    "network_id, extension_info) VALUES " +
                    "(%s, %s, %s, %s, %s, %s, %s)",
                    param_vals)

        cur.execute('SELECT last_insert_id() FROM NAL_VIRTUAL_LAN_MNG')
        global ID
        ID = cur.fetchall()[0][0]

        self.cut_db(con, cur)

    def destroy_fixtures(self):

        con, cur = self.connect_db()

        # Execute SQL
        param_vals = ['test_create_id-0ac6cb428b23']
        cur.execute("DELETE FROM NAL_VIRTUAL_LAN_MNG WHERE " +
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
            'resource': 'vlans',
            'method': 'GET',
            'id': []
        }

        res = router.Router().routing(request_params)
        status = res['status']
        res_data = res['message'].decode('utf-8')
        res_data = json.loads(res_data)

        # Assertion
        self.assertEqual(status, '200 OK')
        self.assertEqual(len(res_data), 1)
        self.assertEqual(res_data[0]['ID'], ID)
        self.assertEqual(res_data[0]['create_id'],
                         'test_create_id-0ac6cb428b23')
        self.assertEqual(res_data[0]['create_id'],
                         'test_create_id-0ac6cb428b23')
        self.assertEqual(res_data[0]['delete_flg'], '0')
        self.assertEqual(res_data[0]['network_id'],
                         'network_id-dd7e-0ac6cb428b23')
        self.assertEqual(res_data[0].get('extension_info', ''), '')
        self.assertEqual(res_data[0]['tenant_name'],
                         extension_info['tenant_name'])
        self.assertEqual(res_data[0]['pod_id'], extension_info['pod_id'])
        self.assertEqual(res_data[0]['tenant_id'], extension_info['tenant_id'])
        self.assertEqual(res_data[0]['IaaS_region_id'],
                         extension_info['IaaS_region_id'])
        self.assertEqual(res_data[0]['IaaS_tenant_id'],
                         extension_info['IaaS_tenant_id'])
        self.assertEqual(res_data[0]['IaaS_network_id'],
                         extension_info['IaaS_network_id'])
        self.assertEqual(res_data[0]['IaaS_network_type'],
                         extension_info['IaaS_network_type'])
        self.assertEqual(res_data[0]['IaaS_segmentation_id'],
                         extension_info['IaaS_segmentation_id'])
        self.assertEqual(res_data[0]['vlan_id'], extension_info['vlan_id'])
        self.assertEqual(res_data[0]['vxlangw_pod_id'],
                         extension_info['vxlangw_pod_id'])
        self.assertEqual(res_data[0]['rule_id'], extension_info['rule_id'])

        assert_info = json.loads(extension_info['nal_vlan_info'])
        nal_vlan_info = json.loads(res_data[0]['nal_vlan_info'])
        for key in assert_info:
            self.assertEqual(nal_vlan_info.get(key), assert_info[key])

    def test_insert_api(self):

        insert_params = {
            'create_id': 'test_create_id-0ac6cb428b23',
            'update_id': 'test_create_id-0ac6cb428b23',
            'delete_flg': 0,
            'network_id': 'network_id-bb6d-6bb9bd380a11',
        }
        insert_params.update(extension_info)

        request_params = {
            'body': insert_params,
            'query': {},
            'resource': 'vlans',
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
                'network_id': 'network_id-bb6d-6bb9bd380a11',
            },
            'resource': 'vlans',
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

        assert_info = json.loads(extension_info['nal_vlan_info'])
        nal_vlan_info = json.loads(res_data[0]['nal_vlan_info'])
        for key in assert_info:
            self.assertEqual(nal_vlan_info.get(key), assert_info[key])

    def test_update_api(self):

        update_params = {
            'update_id': 'test_update_id-0ac6cb428b23',
            'tenant_id': 'tenant_id-ad4c-4cc6ea276a55',
            'network_id': 'network_id-ad4c-4cc6ea276a55',
            'vlan_id': 502
        }
        update_params.update(extension_info)

        request_params = {
            'body': update_params,
            'query': {},
            'resource': 'vlans',
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
            'query': {
                'network_id': 'network_id-ad4c-4cc6ea276a55',
            },
            'resource': 'vlans',
            'method': 'GET',
            'id': []
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

        assert_info = json.loads(extension_info['nal_vlan_info'])
        nal_vlan_info = json.loads(res_data[0]['nal_vlan_info'])
        for key in assert_info:
            self.assertEqual(nal_vlan_info.get(key), assert_info[key])

    def test_delete_api(self):

        request_params = {
            'body': {},
            'query': {},
            'resource': 'vlans',
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

        con, cur = self.connect_db()

        cur.execute("SELECT ID FROM NAL_VIRTUAL_LAN_MNG WHERE ID = %s", [ID])

        self.assertEqual(cur.fetchall(), [])

        self.cut_db(con, cur)
