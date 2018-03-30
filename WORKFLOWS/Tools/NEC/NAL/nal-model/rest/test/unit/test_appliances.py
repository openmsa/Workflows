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
            'tenant_name': 'tenant_namexxxxxxxxxx',
            'pod_id': 'pod_idxxxxxxxxxx',
            'tenant_id': 'tenant_idxxxxxxxxxx',
            'apl_type': 'apl_typexxxxxxxxxx',
            'type': 'typexxxxxxxxxx',
            'device_type': 'device_typexxxxxxxxxx',
            'task_status': 'task_statusxxxxxxxxxx',
            'err_info': 'err_infoxxxxxxxxxx',
            'description': 'descriptionxxxxxxxxxx',
            'node_name': 'node_namexxxxxxxxxx',
            'node_detail': '{"aaa":"aaaaaaaa","bbb":"bbbbbb","ccc":"ccccccc"}',
            'MSA_device_id': 'MSA_device_idxxxxxxxxxx',
            'server_id': 'server_idxxxxxxxxxx',
            'server_info': '{"aaa":"aaaaaaaa","bbb":"bbbbbb","ccc":"ccccccc"}',
            'device_user_name': 'device_user_namexxxxxxxxxx',
            'status': 'statusxxxxxxxxxx',
            'redundant_configuration_flg':
                    'redundant_configuration_flgxxxxxxxxxx',
            'device_name_master': 'device_name_masterxxxxxxxxxx',
            'actsby_flag_master': 'actsby_flag_masterxxxxxxxxxx',
            'device_detail_master':
                '    {"aaa":"aaaaaaaa","bbb":"bbbbbb","ccc":"ccccccc"}',
            'master_ip_address': 'master_ip_addressxxxxxxxxxx',
            'master_MSA_device_id': 'master_MSA_device_idxxxxxxxxxx',
            'device_name_slave': 'device_name_slavexxxxxxxxxx',
            'actsby_flag_slave': 'actsby_flag_slavexxxxxxxxxx',
            'device_detail_slave':
                    '{"aaa":"aaaaaaaa","bbb":"bbbbbb","ccc":"ccccccc"}',
            'slave_ip_address': 'slave_ip_addressxxxxxxxxxx',
            'slave_MSA_device_id': 'slave_MSA_device_idxxxxxxxxxx',
            'partition_id_seq': '10',
            'vsys_id_seq': '10',
        }

        # Execute SQL
        param_vals = ['test_create_id-0ac6cb428b23', '2016-12-31 23:59:59',
                      'test_update_id-0ac6cb428b23', '2016-12-31 23:59:59',
                      0,
                      'node_id-dd7e-0ac6cb428b23',
                      json.dumps(extension_info)]
        cur.execute("INSERT INTO NAL_APL_MNG(create_id, create_date, " +
                    "update_id, update_date, delete_flg, " +
                    "node_id, extension_info) VALUES " +
                    "(%s, %s, %s, %s, %s, %s, %s)", param_vals)

        cur.execute('SELECT last_insert_id() FROM NAL_APL_MNG')
        global ID
        ID = cur.fetchall()[0][0]

        self.cut_db(con, cur)

    def destroy_fixtures(self):

        con, cur = self.connect_db()

        # Execute SQL
        param_vals = ['test_create_id-0ac6cb428b23']
        cur.execute("DELETE FROM NAL_APL_MNG WHERE " +
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
            'resource': 'appliances',
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
        self.assertEqual(res_data[0]['create_id'],
                         'test_create_id-0ac6cb428b23')
        self.assertEqual(res_data[0]['delete_flg'], '0')
        self.assertEqual(res_data[0]['node_id'],
                         'node_id-dd7e-0ac6cb428b23')
        self.assertEqual(res_data[0].get('extension_info', ''), '')

        for key in extension_info:
            self.assertEqual(res_data[0].get(key), extension_info[key])

    def test_insert_api(self):

        insert_params = {
            'create_id': 'test_create_id-0ac6cb428b23',
            'update_id': 'test_create_id-0ac6cb428b23',
            'delete_flg': 0,
            'node_id': 'apl_id-bb6d-6bb9bd380a11',
            'tenant_name': 'tenant_name001',
            'pod_id': 'pod_id001',
            'tenant_id': 'tenant_id001',
            'apl_type': 1,
            'type': 4,
            'device_type': 3,
            'task_status': 'task_status001',
            'err_info': 'err_info001',
            'description': 'description001',
            'node_name': 'node_name001',
            'node_detail': '{}',
            'MSA_device_id': 201,
            'server_id': 'server_id001',
            'server_info': '{}',
        }
        request_params = {
            'body': insert_params,
            'query': {},
            'resource': 'appliances',
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
                'node_id': 'apl_id-bb6d-6bb9bd380a11',
            },
            'resource': 'appliances',
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
            'tenant_id': 'tenant_id-ad4c-4cc6ea276a55',
            'node_id': 'node_id-bb6d-6bb9bd380a11',
            'apl_type': 2,
            'node_name': 'node_name001',
        }
        request_params = {
            'body': update_params,
            'query': {},
            'resource': 'appliances',
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
                'node_id': 'node_id-bb6d-6bb9bd380a11',
            },
            'resource': 'appliances',
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
            self.assertEqual(res_data[0].get(key), update_params[key])

    def test_delete_api(self):

        request_params = {
            'body': {},
            'query': {},
            'resource': 'appliances',
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

        cur.execute("SELECT ID FROM NAL_APL_MNG WHERE ID = %s", [ID])

        self.assertEqual(cur.fetchall(), [])

        self.cut_db(con, cur)
