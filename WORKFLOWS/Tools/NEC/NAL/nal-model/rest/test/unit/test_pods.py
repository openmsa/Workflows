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
                      'pod_id-dd7e-0ac6cb428b23',
                      '{"use_type": 1, "ops_version": 1, "weight": "", "region_id": "regionOne"}']
        cur.execute("INSERT INTO NAL_POD_MNG(create_id, create_date, " +
                    "update_id, update_date, delete_flg, pod_id, " +
                    "extension_info) VALUES " +
                    "(%s, %s, %s, %s, %s, %s, %s)", param_vals)

        cur.execute('SELECT last_insert_id() FROM NAL_POD_MNG')
        global ID
        ID = cur.fetchall()[0][0]

        self.cut_db(con, cur)

    def destroy_fixtures(self):

        con, cur = self.connect_db()

        # Execute SQL
        param_vals = ['test_create_id-0ac6cb428b23']
        cur.execute("DELETE FROM NAL_POD_MNG WHERE " +
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
            'resource': 'pods',
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

    def test_insert_api(self):

        insert_params = {
            'create_id': 'test_create_id-0ac6cb428b23',
            'update_id': 'test_create_id-0ac6cb428b23',
            'delete_flg': 0,
            'pod_id': 'pod_id-bb6d-6bb9bd380a11',
            'use_type': 3,
            'ops_version': 2,
            'weight': 5,
            'region_id': 'regionTwo',
        }
        request_params = {
            'body': insert_params,
            'query': {},
            'resource': 'pods',
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
                'pod_id': 'pod_id-bb6d-6bb9bd380a11',
            },
            'resource': 'pods',
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
        self.assertEqual(res_data[0]['pod_id'], 'pod_id-bb6d-6bb9bd380a11')
        self.assertEqual(res_data[0].get('extension_info', ''), '')
        self.assertEqual(res_data[0]['use_type'], 3)
        self.assertEqual(res_data[0]['ops_version'], 2)
        self.assertEqual(res_data[0]['weight'], 5)
        self.assertEqual(res_data[0]['region_id'], 'regionTwo')

    def test_update_api(self):

        update_params = {
            'update_id': 'test_update_id-0ac6cb428b23',
            'pod_id': 'pod_id-ad4c-4cc6ea276a55',
            'weight': 10,
            'region_id': 'regionThree',
        }
        request_params = {
            'body': update_params,
            'query': {},
            'resource': 'pods',
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
            },
            'resource': 'pods',
            'method': 'GET',
            'id': [ID]
        }
        res = router.Router().routing(request_params)
        status = res['status']
        res_data = res['message'].decode('utf-8')
        res_data = json.loads(res_data)

        self.assertEqual(status, '200 OK')
        self.assertEqual(len(res_data), 1)
        self.assertEqual(res_data[0]['update_id'],
                         'test_update_id-0ac6cb428b23')
        self.assertEqual(res_data[0]['delete_flg'], '0')
        self.assertEqual(res_data[0]['pod_id'], 'pod_id-ad4c-4cc6ea276a55')
        self.assertEqual(res_data[0].get('extension_info', ''), '')
        self.assertEqual(res_data[0]['weight'], 10)
        self.assertEqual(res_data[0]['region_id'], 'regionThree')

    def test_delete_api(self):

        request_params = {
            'body': {},
            'query': {},
            'resource': 'pods',
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

        # Assertion(check select)
        con, cur = self.connect_db()
        cur.execute("SELECT ID FROM NAL_POD_MNG WHERE ID = %s", [ID])
        self.assertEqual(cur.fetchall(), [])
        self.cut_db(con, cur)
