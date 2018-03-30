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

        # Execute SQL
        # -------------------------------------------------------------------
        con, cur = self.connect_db()
        param_vals = ['test_create_id-0ac6cb428b23', '2016-12-31 23:59:59',
                      'test_update_id-0ac6cb428b23', '2016-12-31 23:59:59',
                      0, '10.50.60.50',
                      '{"status": 1, "node_id": "node_id-11111111111", ' +\
                      '"tenant_name": "tenant_name001"}']
        cur.execute("INSERT INTO NAL_GLOBAL_IP_MNG(create_id, " +
                    "create_date, update_id, update_date, delete_flg, " +
                    "global_ip, extension_info) VALUES " +
                    "(%s, %s, %s, %s, %s, %s, %s)",
                    param_vals)

        cur.execute('SELECT last_insert_id() FROM NAL_GLOBAL_IP_MNG')
        global ID1
        ID1 = cur.fetchall()[0][0]
        self.cut_db(con, cur)
        # -------------------------------------------------------------------
        con, cur = self.connect_db()
        param_vals = ['test_create_id-0ac6cb428b23', '2016-12-31 23:59:59',
                      'test_update_id-0ac6cb428b23', '2016-12-31 23:59:59',
                      0, '10.50.60.50',
                      '{"status": 2, "node_id": "node_id-11111111111", ' +\
                      '"tenant_name": "tenant_name001"}']
        cur.execute("INSERT INTO NAL_GLOBAL_IP_MNG(create_id, " +
                    "create_date, update_id, update_date, delete_flg, " +
                    "global_ip, extension_info) VALUES " +
                    "(%s, %s, %s, %s, %s, %s, %s)",
                    param_vals)
        cur.execute('SELECT last_insert_id() FROM NAL_GLOBAL_IP_MNG')
        global ID2
        ID2 = cur.fetchall()[0][0]
        self.cut_db(con, cur)
        # -------------------------------------------------------------------
        con, cur = self.connect_db()
        param_vals = ['test_create_id-0ac6cb428b23', '2016-12-31 23:59:59',
                      'test_update_id-0ac6cb428b23', '2016-12-31 23:59:59',
                      0, '10.50.60.50',
                      '{"status": 3, "node_id": "node_id-11111111111", ' +\
                      '"tenant_name": "tenant_name002"}']
        cur.execute("INSERT INTO NAL_GLOBAL_IP_MNG(create_id, " +
                    "create_date, update_id, update_date, delete_flg, " +
                    "global_ip, extension_info) VALUES " +
                    "(%s, %s, %s, %s, %s, %s, %s)",
                    param_vals)
        cur.execute('SELECT last_insert_id() FROM NAL_GLOBAL_IP_MNG')
        global ID3
        ID3 = cur.fetchall()[0][0]
        self.cut_db(con, cur)
        # -------------------------------------------------------------------
        con, cur = self.connect_db()
        param_vals = ['test_create_id-0ac6cb428b23', '2016-12-31 23:59:59',
                      'test_update_id-0ac6cb428b23', '2016-12-31 23:59:59',
                      0, '10.50.60.50',
                      '{"status": 4, "node_id": "node_id-11111111111", ' +\
                      '"tenant_name": "tenant_name002"}']
        cur.execute("INSERT INTO NAL_GLOBAL_IP_MNG(create_id, " +
                    "create_date, update_id, update_date, delete_flg, " +
                    "global_ip, extension_info) VALUES " +
                    "(%s, %s, %s, %s, %s, %s, %s)",
                    param_vals)
        cur.execute('SELECT last_insert_id() FROM NAL_GLOBAL_IP_MNG')
        global ID4
        ID4 = cur.fetchall()[0][0]
        self.cut_db(con, cur)
        # -------------------------------------------------------------------
        con, cur = self.connect_db()
        param_vals = ['test_create_id-0ac6cb428b23', '2016-12-31 23:59:59',
                      'test_update_id-0ac6cb428b23', '2016-12-31 23:59:59',
                      1, '10.50.60.50',
                      '{"status": 1, "node_id": "node_id-11111111111", ' +\
                      '"tenant_name": "tenant_name001"}']
        cur.execute("INSERT INTO NAL_GLOBAL_IP_MNG(create_id, " +
                    "create_date, update_id, update_date, delete_flg, " +
                    "global_ip, extension_info) VALUES " +
                    "(%s, %s, %s, %s, %s, %s, %s)",
                    param_vals)
        cur.execute('SELECT last_insert_id() FROM NAL_GLOBAL_IP_MNG')
        global ID5
        ID5 = cur.fetchall()[0][0]
        self.cut_db(con, cur)
        # -------------------------------------------------------------------

    def destroy_fixtures(self):
        pass
        con, cur = self.connect_db()

        # Execute SQL
        param_vals = ['test_create_id-0ac6cb428b23']
        cur.execute("DELETE FROM NAL_GLOBAL_IP_MNG WHERE " +
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

    def test_select_api_sel_all(self):

        request_params = {
            'request_id': 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx',
            'resource': 'global-ip-addresses',
            'method': 'GET',
            'id': []
        }

        res = router.Router().routing(request_params)

        status = res['status']
        res_data = res['message'].decode('utf-8')
        res_data = json.loads(res_data)

        # Check to get number
        self.assertEqual(status, '200 OK')
        self.assertGreaterEqual(len(res_data), 1)

    def test_select_api_sel_id(self):

        request_params = {
            'request_id': 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx',
            'resource': 'global-ip-addresses',
            'method': 'GET',
            'id': [ID1]
        }

        res = router.Router().routing(request_params)

        status = res['status']
        res_data = res['message'].decode('utf-8')
        res_data = json.loads(res_data)

        # Check to get number
        self.assertEqual(status, '200 OK')
        self.assertEqual(len(res_data), 1)

        # Check the contents of the data
        self.assertEqual(res_data[0]['create_id'],
                         'test_create_id-0ac6cb428b23')
        self.assertEqual(res_data[0]['create_date'],
                         '2016-12-31 23:59:59')
        self.assertEqual(res_data[0]['update_id'],
                         'test_update_id-0ac6cb428b23')
        self.assertEqual(res_data[0]['update_date'],
                         '2016-12-31 23:59:59')
        self.assertEqual(res_data[0]['delete_flg'], '0')
        self.assertEqual(res_data[0]['ID'], ID1)
        self.assertEqual(res_data[0]['global_ip'], '10.50.60.50')
        self.assertEqual(res_data[0].get('extension_info', ''), '')
        self.assertEqual(res_data[0]['status'], 1)
        self.assertEqual(res_data[0]['node_id'], 'node_id-11111111111')
        self.assertEqual(res_data[0]['tenant_name'], 'tenant_name001')

    def test_select_api_sel_query1(self):

        request_params = {
            'query': {
                'global_ip': '10.50.60.50',
            },
            'resource': 'global-ip-addresses',
            'method': 'GET',
            'id': []
        }

        res = router.Router().routing(request_params)

        status = res['status']
        res_data = res['message'].decode('utf-8')
        res_data = json.loads(res_data)

        # Check to get number
        self.assertEqual(status, '200 OK')
        self.assertEqual(len(res_data), 5)

    def test_select_api_sel_query2(self):

        request_params = {
            'query': {
                'global_ip': '10.50.60.50',
                'tenant_name': 'tenant_name001',
            },
            'resource': 'global-ip-addresses',
            'method': 'GET',
            'id': []
        }

        res = router.Router().routing(request_params)

        status = res['status']
        res_data = res['message'].decode('utf-8')
        res_data = json.loads(res_data)

        # Check to get number
        self.assertEqual(status, '200 OK')
        self.assertEqual(len(res_data), 3)

    def test_select_api_sel_query3(self):

        request_params = {
            'query': {
                'global_ip': '10.50.60.50',
                'tenant_name': 'tenant_name001',
                'status': '2',
            },
            'resource': 'global-ip-addresses',
            'method': 'GET',
            'id': []
        }

        res = router.Router().routing(request_params)

        status = res['status']
        res_data = res['message'].decode('utf-8')
        res_data = json.loads(res_data)

        # Check to get number
        self.assertEqual(status, '200 OK')
        self.assertEqual(len(res_data), 1)
        self.assertEqual(res_data[0]['ID'], ID2)

    def test_insert_api(self):

        insert_params = {
            'create_id': 'test_create_id-0ac6cb428b23',
            'update_id': 'test_update_id-11',
            'delete_flg': 0,
            'global_ip': '10.50.60.51',
            'status': 0,
            'node_id': '',
            'tenant_name': ''
        }
        request_params = {
            'request_id': 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx',
            'body': insert_params,
            'query': {},
            'resource': 'global-ip-addresses',
            'method': 'POST',
            'id': []
        }

        res = router.Router().routing(request_params)

        status = res['status']
        res_data = res['message'].decode('utf-8')
        res_data = json.loads(res_data)

        self.assertEqual(status, '200 OK')
        self.assertEqual(len(res_data), 1)
        self.assertTrue('ID' in res_data)

        # select check
        request_params = {
            'request_id': 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx',
            'query': {
                'create_id': 'test_create_id-0ac6cb428b23',
                'update_id': 'test_update_id-11',
                'delete_flg': 0,
                'global_ip': '10.50.60.51',
                'status': 0,
                'node_id': '',
                'tenant_name': ''
            },
            'resource': 'global-ip-addresses',
            'method': 'GET',
            'id': []
        }

        res = router.Router().routing(request_params)

        status = res['status']
        res_data = res['message'].decode('utf-8')
        res_data = json.loads(res_data)

        # Check to get number
        self.assertEqual(status, '200 OK')
        self.assertEqual(len(res_data), 1)

        # Check the contents of the data
        self.assertEqual(res_data[0]['create_id'],
                         'test_create_id-0ac6cb428b23')
        self.assertEqual(res_data[0]['update_id'],
                         'test_update_id-11')
        self.assertEqual(res_data[0]['delete_flg'], '0')
        self.assertEqual(res_data[0]['global_ip'], '10.50.60.51')
        self.assertEqual(res_data[0].get('extension_info', ''), '')
        self.assertEqual(res_data[0]['status'], 0)
        self.assertEqual(res_data[0]['node_id'], '')
        self.assertEqual(res_data[0]['tenant_name'], '')

    def test_update_api(self):

        update_params = {
            'update_id': 'test_update_id-12',
            'global_ip': '10.50.60.52',
            'status': "",
            'tenant_name': 'tenant_id-ad4c-4cc6ea276a55',
            'node_id': 'node_id-ad4c-4cc6ea276a55'
        }
        request_params = {
            'request_id': 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx',
            'body': update_params,
            'query': {},
            'resource': 'global-ip-addresses',
            'method': 'PUT',
            'id': [ID1]
        }

        res = router.Router().routing(request_params)

        status = res['status']
        res_data = res['message'].decode('utf-8')
        res_data = json.loads(res_data)

        self.assertEqual(status, '200 OK')
        self.assertEqual(res_data, True)

        # select check
        request_params = {
            'resource': 'global-ip-addresses',
            'method': 'GET',
            'id': [ID1]
        }

        res = router.Router().routing(request_params)

        status = res['status']
        res_data = res['message'].decode('utf-8')
        res_data = json.loads(res_data)

        # Check to get number
        self.assertEqual(status, '200 OK')
        self.assertEqual(len(res_data), 1)

        # Check the contents of the data
        self.assertEqual(res_data[0]['create_id'],
                         'test_create_id-0ac6cb428b23')
        self.assertEqual(res_data[0]['update_id'],
                         'test_update_id-12')
        self.assertEqual(res_data[0]['delete_flg'], '0')
        self.assertEqual(res_data[0]['global_ip'], '10.50.60.52')
        self.assertEqual(res_data[0].get('extension_info', ''), '')
        self.assertEqual(res_data[0]['status'], '')
        self.assertEqual(res_data[0]['node_id'], 'node_id-ad4c-4cc6ea276a55')
        self.assertEqual(res_data[0]['tenant_name'], 'tenant_id-ad4c-4cc6ea276a55')

    def test_delete_api(self):

        request_params = {
            'request_id': 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx',
            'body': {},
            'query': {},
            'resource': 'global-ip-addresses',
            'method': 'DELETE',
            'id': [ID1]
        }

        res = router.Router().routing(request_params)

        status = res['status']
        res_data = res['message'].decode('utf-8')
        res_data = json.loads(res_data)

        self.assertEqual(status, '200 OK')
        self.assertEqual(res_data, True)

        con, cur = self.connect_db()

        cur.execute("SELECT ID FROM NAL_GLOBAL_IP_MNG " +
                    "WHERE ID = %s", [ID1])

        self.assertEqual(cur.fetchall(), [])

        self.cut_db(con, cur)

    def test_select_api_valid_error1(self):

        request_params = {
            'query': {
                'global_ip': '10.50.60.50',
                'tenant_name': 'tenant_name001',
                'status': '2',
            },
            'resource': '',
            'method': 'GET',
            'id': []
        }

        res = router.Router().routing(request_params)

        status = res['status']
        res_data = res['message'].decode('utf-8')
        res_data = json.loads(res_data)

        # Check to get number
        self.assertEqual(status, '400 Bad Request')

    def test_select_api_valid_error2(self):

        request_params = {
            'query': {
                'global_ip': '10.50.60.50',
                'tenant_name': 'tenant_name001',
                'status': '2',
            },
            'resource': 'global-ip-addresses',
            'method': '',
            'id': []
        }

        res = router.Router().routing(request_params)

        status = res['status']
        res_data = res['message'].decode('utf-8')
        res_data = json.loads(res_data)

        # Check to get number
        self.assertEqual(status, '400 Bad Request')

    def test_select_api_valid_error3(self):

        request_params = {
            'query': {
                'global_ip': '10.50.60.50',
                'tenant_name': 'tenant_name001',
                'status': '2',
            },
            'resource': 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxx',
            'method': 'GET',
            'id': []
        }

        res = router.Router().routing(request_params)

        status = res['status']
        res_data = res['message'].decode('utf-8')
        res_data = json.loads(res_data)

        # Check to get number
        self.assertEqual(status, '404 NotFound')

    def test_select_api_err_notfound(self):

        request_params = {
            'request_id': 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx',
            'body': {},
            'query': {},
            'resource': 'global-ip-addresses',
            'method': 'GET',
            'id': [0]
        }

        res = router.Router().routing(request_params)

        status = res['status']
        res_data = res['message'].decode('utf-8')
        res_data = json.loads(res_data)

        self.assertEqual(status, '200 OK')
        self.assertEqual(len(res_data), 0)

    def test_update_api_err_notfound(self):

        update_params = {
            'update_id': 'test_update_id-12',
            'global_ip': '10.50.60.52',
            'status': "",
            'tenant_name': 'tenant_id-ad4c-4cc6ea276a55',
            'node_id': 'node_id-ad4c-4cc6ea276a55'
        }
        request_params = {
            'request_id': 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx',
            'body': update_params,
            'query': {},
            'resource': 'global-ip-addresses',
            'method': 'PUT',
            'id': [0]
        }

        res = router.Router().routing(request_params)

        status = res['status']
        res_data = res['message'].decode('utf-8')
        res_data = json.loads(res_data)

        self.assertEqual(status, '404 NotFound')
        self.assertEqual(res_data,
            'An object with the specified identifier was not found.')

    def test_delete_api_err_notfound(self):

        request_params = {
            'request_id': 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx',
            'body': {},
            'query': {},
            'resource': 'global-ip-addresses',
            'method': 'DELETE',
            'id': [0]
        }

        res = router.Router().routing(request_params)

        status = res['status']
        res_data = res['message'].decode('utf-8')
        res_data = json.loads(res_data)

        self.assertEqual(status, '404 NotFound')
        self.assertEqual(res_data,
            'An object with the specified identifier was not found.')
