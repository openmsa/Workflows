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

        # Execute SQL
        param_vals = ['test_create_id-0ac6cb428b23', '2016-12-31 23:59:59',
                      'test_update_id-0ac6cb428b23', '2016-12-31 23:59:59', 0,
                      'tenant_id-dd7e-0ac6cb428b23',
                      '{"IaaS_region_id": "IaaS_region_id001",' +
                      '"IaaS_tenant_id": "IaaS_tenant_id002",' +
                      '"tenant_info":' +
                      '"{\\"pod_id\\":\\\"pod_id1234567890\\",' +
                      '\\"msa_customer_name\\":\\"name001\\",' +
                      '\\"msa_customer_ID\\":10}"}']
        cur.execute("INSERT INTO NAL_TENANT_MNG(create_id, create_date, " +
                    "update_id, update_date, delete_flg, tenant_name, " +
                    "extension_info) VALUES " +
                    "(%s, %s, %s, %s, %s, %s, %s)",
                    param_vals)

        cur.execute('SELECT last_insert_id() FROM NAL_TENANT_MNG')
        global ID
        ID = cur.fetchall()[0][0]

        self.cut_db(con, cur)

    def destroy_fixtures(self):

        con, cur = self.connect_db()

        # Execute SQL
        param_vals = ['test_create_id-0ac6cb428b23']
        cur.execute("DELETE FROM NAL_TENANT_MNG WHERE " +
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
            'resource': 'tenants',
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
        self.assertEqual(res_data[0]['create_id'],
                         'test_create_id-0ac6cb428b23')
        self.assertEqual(res_data[0]['create_id'],
                         'test_create_id-0ac6cb428b23')
        self.assertEqual(res_data[0]['delete_flg'], '0')
        self.assertEqual(res_data[0]['tenant_name'], 'tenant_id-dd7e-0ac6cb428b23')
        self.assertEqual(res_data[0].get('extension_info', ''), '')
        self.assertEqual(res_data[0]['IaaS_region_id'], 'IaaS_region_id001')
        self.assertEqual(res_data[0]['IaaS_tenant_id'], 'IaaS_tenant_id002')

        tenant_info = json.loads(res_data[0]['tenant_info'])
        self.assertEqual(tenant_info.get('pod_id'), 'pod_id1234567890')
        self.assertEqual(tenant_info.get('msa_customer_name'), 'name001')
        self.assertEqual(tenant_info.get('msa_customer_ID'), 10)

    def test_insert_api(self):

        tenant_info = {
            'pod_id': 'pod_id001',
            'description': 'description',
            'enabled': True,
            'id': 'xxxx-xxxxx-xxxxx-xxxx',
            'name': 'tenant001',
            'msa_customer_name': 'msa_customer_name001',
            'msa_customer_ID': 100,
        }
        tenant_info_json = json.dumps(tenant_info)

        insert_params = {
            'create_id': 'test_create_id-0ac6cb428b23',
            'update_id': 'test_create_id-0ac6cb428b23',
            'delete_flg': 0,
            'tenant_name': 'tenant_id-bb6d-6bb9bd380555',
            'IaaS_region_id': 'IaaS_region_id-bb6d-6bb9bd380a11',
            'IaaS_tenant_id': 'IaaS_tenant_id-bb6d-6bb9bd380a11',
            'tenant_info': tenant_info_json,
        }
        request_params = {
            'body': insert_params,
            'query': {},
            'resource': 'tenants',
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
                'tenant_name': 'tenant_id-bb6d-6bb9bd380555',
            },
            'resource': 'tenants',
            'method': 'GET',
            'id': []
        }
        res = router.Router().routing(request_params)
        status = res['status']
        res_data = res['message'].decode('utf-8')
        res_data = json.loads(res_data)

        self.assertEqual(status, '200 OK')
        self.assertEqual(len(res_data), 1)
        self.assertEqual(res_data[0]['create_id'],
                         'test_create_id-0ac6cb428b23')
        self.assertEqual(res_data[0]['update_id'],
                         'test_create_id-0ac6cb428b23')
        self.assertEqual(res_data[0]['delete_flg'], '0')
        self.assertEqual(res_data[0]['tenant_name'],
                         'tenant_id-bb6d-6bb9bd380555')
        self.assertEqual(res_data[0].get('extension_info', ''), '')
        self.assertEqual(res_data[0]['IaaS_region_id'],
                         'IaaS_region_id-bb6d-6bb9bd380a11')
        self.assertEqual(res_data[0]['IaaS_tenant_id'],
                         'IaaS_tenant_id-bb6d-6bb9bd380a11')

        tenant_info = json.loads(res_data[0]['tenant_info'])
        self.assertEqual(tenant_info.get('pod_id'), tenant_info['pod_id'])
        self.assertEqual(tenant_info.get('description'),
                            tenant_info['description'])
        self.assertEqual(tenant_info.get('enabled'), True)
        self.assertEqual(tenant_info.get('id'), tenant_info['id'])
        self.assertEqual(tenant_info.get('name'), tenant_info['name'])
        self.assertEqual(tenant_info.get('msa_customer_name'),
                            tenant_info['msa_customer_name'])
        self.assertEqual(tenant_info.get('msa_customer_ID'), 100)

    def test_update_api(self):

        tenant_info = {
            'pod_id': 'pod_id001',
            'description': 'description',
            'enabled': True,
            'id': '1111-1111-11111-1111',
            'name': 'tenant001',
            'msa_customer_name': 'msa_customer_name001',
            'msa_customer_ID': 100,
        }
        tenant_info_json = json.dumps(tenant_info)

        update_params = {
            'update_id': 'test_update_id-0ac6cb428b23',
            'IaaS_region_id': 'IaaS_region_id-ad4c-4cc6ea276a55',
            'IaaS_tenant_id': 'IaaS_tenant_id-ad4c-4cc6ea276a55',
            'tenant_name': 'tenant_id-ad4c-4cc6ea276a55',
            'tenant_info': tenant_info_json,
        }
        request_params = {
            'body': update_params,
            'query': {},
            'resource': 'tenants',
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
                'tenant_name': 'tenant_id-ad4c-4cc6ea276a55',
            },
            'resource': 'tenants',
            'method': 'GET',
            'id': []
        }
        res = router.Router().routing(request_params)
        status = res['status']
        res_data = res['message'].decode('utf-8')
        res_data = json.loads(res_data)

        self.assertEqual(status, '200 OK')
        self.assertEqual(len(res_data), 1)
        self.assertEqual(res_data[0]['update_id'],
                         'test_update_id-0ac6cb428b23')
        self.assertEqual(res_data[0]['tenant_name'],
                         'tenant_id-ad4c-4cc6ea276a55')
        self.assertEqual(res_data[0]['IaaS_region_id'],
                         'IaaS_region_id-ad4c-4cc6ea276a55')
        self.assertEqual(res_data[0]['IaaS_tenant_id'],
                         'IaaS_tenant_id-ad4c-4cc6ea276a55')

        tenant_info = json.loads(res_data[0]['tenant_info'])
        self.assertEqual(tenant_info.get('pod_id'), tenant_info['pod_id'])
        self.assertEqual(tenant_info.get('description'),
                            tenant_info['description'])
        self.assertEqual(tenant_info.get('enabled'), True)
        self.assertEqual(tenant_info.get('id'), '1111-1111-11111-1111')
        self.assertEqual(tenant_info.get('name'), tenant_info['name'])
        self.assertEqual(tenant_info.get('msa_customer_name'),
                            tenant_info['msa_customer_name'])
        self.assertEqual(tenant_info.get('msa_customer_ID'), 100)

    def test_delete_api(self):

        request_params = {
            'body': {},
            'query': {},
            'resource': 'tenants',
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

        cur.execute("SELECT * FROM NAL_TENANT_MNG WHERE ID = %s", [ID])

        self.assertEqual(cur.fetchall(), [])

        self.cut_db(con, cur)
