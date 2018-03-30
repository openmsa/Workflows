import json
import os
import sys
import unittest
import urllib.error
import urllib.request
import urllib.parse

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../../../')
from rest.common import exception
from rest.lib import database


class TestSelectAPI(unittest.TestCase):
    # Do a test of Select.

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

        db = database.LibDatabase()
        con = db._connect_db()

        # Open Cursor
        cur = con.cursor()

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

        con.commit()

        # Close Cursor
        cur.close()

        # Close Database
        con.close()

    def destroy_fixtures(self):

        db = database.LibDatabase()
        con = db._connect_db()

        # Open Cursor
        cur = con.cursor()

        # Execute SQL
        param_vals = ['test_create_id-0ac6cb428b23']
        cur.execute("DELETE FROM NAL_GLOBAL_IP_MNG WHERE " +
                    "create_id = %s", param_vals)

        # Commit Transaction
        con.commit()

        # Close Cursor
        cur.close()

        # Close Database
        con.close()

    def test_select_api(self):

        url = 'http://localhost:8081/index.py/global-ip-addresses'
        params = {'delete_flg': 0,
                  'create_id': 'test_create_id'}

        query = ''
        for key in params:
            if len(query) > 0:
                query += '&'
            else:
                query = '?'
            query += key + '=' + str(params[key])

        url += query

        res = urllib.request.urlopen(url)

        res_data = res.read().decode('utf-8')
        res_data = json.loads(res_data)

        # Check Status Code
        self.assertEqual(res.status, 200)

    def test_select_api_error(self):

        url = 'http://localhost/index.py/aaaaaaaaaaaaaaaaaa'
        params = {'delete_flg': 0,
                  'create_id': 'can_not_select_id'}

        query = ''
        for key in params:
            if len(query) > 0:
                query += '&'
            else:
                query = '?'
            query += key + '=' + str(params[key])

        url += query

        with self.assertRaises(urllib.error.HTTPError) as e:
            urllib.request.urlopen(url)

        error = e.exception
        self.assertEquals(error.code, 404)
