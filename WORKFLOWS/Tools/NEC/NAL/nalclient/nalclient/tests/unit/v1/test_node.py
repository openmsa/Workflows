#  Licensed under the Apache License, Version 2.0 (the "License"); you may
#  not use this file except in compliance with the License. You may obtain
#  a copy of the License at
#  
#       http://www.apache.org/licenses/LICENSE-2.0
#  
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#  WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#  License for the specific language governing permissions and limitations
#  under the License.
#  
#  COPYRIGHT  (C)  NEC  CORPORATION  2017
#  


"""Test nalclient/v1/node.py."""
from datetime import datetime
import os
import sys
import testtools

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../../../../')

from nalclient.tests.unit import utils
from nalclient.v1 import node


def get_datetime(str_date):
    """Get datetime.
        :param str_date: String of date.
    """
    return datetime.strptime(str_date + 'T00:00:00.000000',
                             '%Y-%m-%dT%H:%M:%S.%f')

fixtures_node_data_detail_101 = \
    {'create_id': 'test_user-414b-aa5e-dedbeef00101',
     'create_date': get_datetime('2016-12-31'),
     'update_id': 'test_user-414b-aa5e-dedbeef00101',
     'update_date': get_datetime('2016-12-31'),
     'delete_flg': '0',
     'ID': '101',
     'type': '1',
     'device_type': '1',
     'tenant_id': 'tenantid-414b-aa5e-dedbeef00101',
     'pod_id': 'podid-414b-aa5e-dedbeef00101',
     'node_id': 'nodeid-414b-aa5e-dedbeef00101',
     'node_name': 'node_name',
     'node_detail': '{}',
     'server_id': 'srvid-414b-aa5e-dedbeef00101',
     'server_info': '{}',
     'MSA_device_id': 'msaid-414b-aa5e-dedbeef00101'}

fixtures_node_data_detail_102 = \
    {'create_id': 'test_user-414b-aa5e-dedbeef00101',
     'create_date': get_datetime('2016-12-31'),
     'update_id': 'test_user-414b-aa5e-dedbeef00101',
     'update_date': get_datetime('2016-12-31'),
     'delete_flg': '0',
     'ID': '102',
     'type': '1',
     'device_type': '2',
     'tenant_id': 'tenantid-414b-aa5e-dedbeef00101',
     'pod_id': 'podid-414b-aa5e-dedbeef00101',
     'node_id': 'nodeid-414b-aa5e-dedbeef00101',
     'node_name': 'node_name',
     'node_detail': '{}',
     'server_id': 'srvid-414b-aa5e-dedbeef00101',
     'server_info': '{}',
     'MSA_device_id': 'msaid-414b-aa5e-dedbeef00101'}

fixtures_node_data_detail_103 = \
    {'create_id': 'test_user-414b-aa5e-dedbeef00101',
     'create_date': get_datetime('2016-12-31'),
     'update_id': 'test_user-414b-aa5e-dedbeef00101',
     'update_date': get_datetime('2016-12-31'),
     'delete_flg': '0',
     'ID': '103',
     'type': '2',
     'device_type': '1',
     'tenant_id': 'tenantid-414b-aa5e-dedbeef00101',
     'pod_id': 'podid-414b-aa5e-dedbeef00101',
     'node_id': 'nodeid-414b-aa5e-dedbeef00101',
     'node_name': 'node_name',
     'node_detail': '{}',
     'server_id': 'srvid-414b-aa5e-dedbeef00101',
     'server_info': '{}',
     'MSA_device_id': 'msaid-414b-aa5e-dedbeef00101'}

fixtures_node_data_detail_201 = \
    {'create_id': 'test_user-414b-aa5e-dedbeef00101',
     'create_date': get_datetime('2016-12-31'),
     'update_id': 'test_user-414b-aa5e-dedbeef00101',
     'update_date': get_datetime('2016-12-31'),
     'delete_flg': '0',
     'ID': '201',
     'type': '1',
     'device_type': '1',
     'tenant_id': 'tenantid-414b-aa5e-dedbeef00101',
     'device_user_name': 'device_user_name',
     'status': '1',
     'device_id': 'devid-414b-aa5e-dedbeef00101',
     'redundant_configuration_flg': '0',
     'device_name_master': 'device_master_name',
     'actsby_flag_master': 'act',
     'device_detail_master': '{}',
     'master_ip_address': '10.50.60.5',
     'master_MSA_device_id': 'masterid',
     'device_name_slave': 'device_slave_name',
     'device_detail_slave': '{}',
     'actsby_flag_slave': 'act',
     'slave_ip_address': '10.50.80.12',
     'slave_MSA_device_id': 'slaveid'}

fixtures_node_data_detail_202 = \
    {'create_id': 'test_user-414b-aa5e-dedbeef00101',
     'create_date': get_datetime('2016-12-31'),
     'update_id': 'test_user-414b-aa5e-dedbeef00101',
     'update_date': get_datetime('2016-12-31'),
     'delete_flg': '0',
     'ID': '202',
     'type': '1',
     'device_type': '2',
     'tenant_id': 'tenantid-414b-aa5e-dedbeef00101',
     'device_user_name': 'device_user_name',
     'status': '1',
     'device_id': 'devid-414b-aa5e-dedbeef00101',
     'redundant_configuration_flg': '0',
     'device_name_master': 'device_master_name',
     'actsby_flag_master': 'act',
     'device_detail_master': '{}',
     'master_ip_address': '10.50.60.5',
     'master_MSA_device_id': 'masterid',
     'device_name_slave': 'device_slave_name',
     'device_detail_slave': '{}',
     'actsby_flag_slave': 'act',
     'slave_ip_address': '10.50.80.12',
     'slave_MSA_device_id': 'slaveid'}

fixtures_node_data_detail_203 = \
    {'create_id': 'test_user-414b-aa5e-dedbeef00101',
     'create_date': get_datetime('2016-12-31'),
     'update_id': 'test_user-414b-aa5e-dedbeef00101',
     'update_date': get_datetime('2016-12-31'),
     'delete_flg': '0',
     'ID': '203',
     'type': '2',
     'device_type': '1',
     'tenant_id': 'tenantid-414b-aa5e-dedbeef00101',
     'device_user_name': 'device_user_name',
     'status': '1',
     'device_id': 'devid-414b-aa5e-dedbeef00101',
     'redundant_configuration_flg': '0',
     'device_name_master': 'device_master_name',
     'actsby_flag_master': 'act',
     'device_detail_master': '{}',
     'master_ip_address': '10.50.60.5',
     'master_MSA_device_id': 'masterid',
     'device_name_slave': 'device_slave_name',
     'device_detail_slave': '{}',
     'actsby_flag_slave': 'act',
     'slave_ip_address': '10.50.80.12',
     'slave_MSA_device_id': 'slaveid'}


# from nalclient.v1 import client
#  request fixtures
#    (request url, request header, request parameter).
fixtures = {
    '/Nal/node/': {
        'POST': {
            "result": {
                "status": "success",
                "error-code": "NAL100000",
                "message": "Create job is running."
            },
            "request-id": "xxxxxxxxxxxxxxxxx"
        },
        'PUT': {
            "result": {
                "status": "success",
                "error-code": "NAL100000",
                "message": "Update job is running."
            },
            "request-id": "xxxxxxxxxxxxxxxxx"
        },
        'DELETE': {
            "result": {
                "status": "success",
                "error-code": "NAL100000",
                "message": "Delete job is running."
            },
            "request-id": "xxxxxxxxxxxxxxxxx"
        }
    },
    '/Nal/node/?function_type=all_node': {
        'GET': {
            'data': [
                fixtures_node_data_detail_101,
                fixtures_node_data_detail_102,
                fixtures_node_data_detail_103,
                fixtures_node_data_detail_201,
                fixtures_node_data_detail_202,
                fixtures_node_data_detail_203
            ]
        }
    },
    '/Nal/node/?IaaS_tenant_id=test_user-414b-aa5e-dedbeef00101'
    '&function_type=all_node': {
        'GET': {
            'data': [
                fixtures_node_data_detail_101,
                fixtures_node_data_detail_102,
                fixtures_node_data_detail_203
            ]
        }
    },
    '/Nal/node/?apl_type=1&function_type=all_node': {
        'GET': {
            'data': [
                fixtures_node_data_detail_101,
                fixtures_node_data_detail_102,
                fixtures_node_data_detail_103
            ]
        }
    },
    '/Nal/node/?function_type=all_node&type=1': {
        'GET': {
            'data': [
                fixtures_node_data_detail_101,
                fixtures_node_data_detail_102,
                fixtures_node_data_detail_201,
                fixtures_node_data_detail_202
            ]
        }
    },
    '/Nal/node/?device_type=1&function_type=all_node': {
        'GET': {
            'data': [
                fixtures_node_data_detail_101,
                fixtures_node_data_detail_103,
                fixtures_node_data_detail_201,
                fixtures_node_data_detail_203
            ]
        }
    },
    '/Nal/node/?IaaS_tenant_id=test_user-414b-aa5e-dedbeef00101'
    '&apl_type=1&device_type=1&function_type=all_node&type=1': {
        'GET': {
            'data': [
                fixtures_node_data_detail_102
            ]
        }
    },
    '/Nal/node/?ID=test_node-414b-aa5e-dedbeef00101&function_type=vfw': {
        'GET': {
            'data': [
                fixtures_node_data_detail_101
            ]
        }
    },
    '/Nal/node/?ID=test_node-414b-aa5e-dedbeef00101&function_type=pfw': {
        'GET': {
            'data': [
                fixtures_node_data_detail_103
            ]
        }
    },
    '/Nal/node/?ID=test_node-414b-aa5e-dedbeef00101&function_type=vlb': {
        'GET': {
            'data': [
                fixtures_node_data_detail_201
            ]
        }
    },
    '/Nal/node/?ID=test_node-414b-aa5e-dedbeef00101&function_type=plb': {
        'GET': {
            'data': [
                fixtures_node_data_detail_203
            ]
        }
    }
}


class NodeManagerTest(testtools.TestCase):
    """CatalogManager Test class."""

    def setUp(self):
        """Setup test class."""
        super(NodeManagerTest, self).setUp()
        self.api = utils.FakeAPI(fixtures)
        self.mgr = node.NodeManager(self.api)

    def test_create(self):
        """Test create method."""
        kwargs = {
            'operation_id': 'test_user-414b-aa5e-dedbeef00101',
            'IaaS_tenant_id': 'tenantid-414b-aa5e-dedbeef00101',
            'IaaS_tenant_name': 'test_tenant',
            'IaaS_region_id': 'regionid-414b-aa5e-dedbeef00101',
            'host_name': 'test_host',
            'device_name': 'test_device',
            'type': '1',
            'device_type': '1',
            'IaaS_network_type': 'vxlan',
            'IaaS_network_id': 'netid-414b-aa5e-dedbeef00101',
            'network_name': 'test_network',
            'InterSecWebClientIpAddress': '10.20.30.10',
            'InterSecNtpIpAddress': '10.20.30.11',
            'function_type': 'vfw'
        }

        self.mgr.create(kwargs)

        expect = [('POST', '/Nal/node/', {},
                   sorted(kwargs.items(), key=lambda x: x[0]))]

        self.assertEqual(expect, self.api.calls)

    def test_update(self):
        """Test update method."""
        kwargs = {
            'operation_id': 'test_user-414b-aa5e-dedbeef00101',
            'IaaS_tenant_id': 'tenantid-414b-aa5e-dedbeef00101',
            'IaaS_tenant_name': 'test_tenant',
            'IaaS_region_id': 'regionid-414b-aa5e-dedbeef00101',
            'IaaS_network_type': 'vxlan',
            'IaaS_network_id': 'netid-414b-aa5e-dedbeef00101',
            'network_name': 'test_network',
            'node_id': 'nodeid-414b-aa5e-dedbeef00101',
            'pavmZoneName': 'pavm_Zone_Name',
            'function_type': 'vfw_port_p'
        }

        self.mgr.update(kwargs)

        expect = [('PUT', '/Nal/node/', {},
                   sorted(kwargs.items(), key=lambda x: x[0]))]

        self.assertEqual(expect, self.api.calls)

    def test_delete(self):
        """Test delete method."""
        kwargs = {
            'operation_id': 'test_user-414b-aa5e-dedbeef00101',
            'IaaS_tenant_id': 'tenantid-414b-aa5e-dedbeef00101',
            'IaaS_region_id': 'regionid-414b-aa5e-dedbeef00101',
            'node_id': 'nodeid-414b-aa5e-dedbeef00101',
            'function_type': 'vfw'
        }

        self.mgr.delete(kwargs)

        expect = [('DELETE', '/Nal/node/', {},
                   sorted(kwargs.items(), key=lambda x: x[0]))]

        self.assertEqual(expect, self.api.calls)

    def test_get_all(self):
        """Test get method."""
        kwargs = {'function_type': 'all_node'}

        node = list(self.mgr.get(kwargs))

        url = '/Nal/node/?' \
            'function_type=%s' % ('all_node')
        expect = [('GET', url, {}, None)]

        self.assertEqual(expect, self.api.calls)
        self.assertEqual(6, len(node))
        self.assertEqual('101', node[0]['ID'])
        self.assertEqual('102', node[1]['ID'])
        self.assertEqual('103', node[2]['ID'])
        self.assertEqual('201', node[3]['ID'])
        self.assertEqual('202', node[4]['ID'])
        self.assertEqual('203', node[5]['ID'])

    def test_get_all_tenant(self):
        """Test get method."""
        kwargs = {'IaaS_tenant_id': 'test_user-414b-aa5e-dedbeef00101',
                  'function_type': 'all_node'}

        node = list(self.mgr.get(kwargs))

        url = '/Nal/node/?' \
            'IaaS_tenant_id=%s&function_type=%s' % \
            ('test_user-414b-aa5e-dedbeef00101',
             'all_node')
        expect = [('GET', url, {}, None)]

        self.assertEqual(expect, self.api.calls)
        self.assertEqual(3, len(node))
        self.assertEqual('101', node[0]['ID'])
        self.assertEqual('102', node[1]['ID'])
        self.assertEqual('203', node[2]['ID'])

    def test_get_all_apl_type(self):
        """Test get method."""
        kwargs = {'apl_type': '1',
                  'function_type': 'all_node'}

        node = list(self.mgr.get(kwargs))

        url = '/Nal/node/?' \
            'apl_type=%s&function_type=%s' % \
            ('1',
             'all_node')
        expect = [('GET', url, {}, None)]

        self.assertEqual(expect, self.api.calls)
        self.assertEqual(3, len(node))
        self.assertEqual('101', node[0]['ID'])
        self.assertEqual('102', node[1]['ID'])
        self.assertEqual('103', node[2]['ID'])

    def test_get_all_type(self):
        """Test get method."""
        kwargs = {'type': '1',
                  'function_type': 'all_node'}

        node = list(self.mgr.get(kwargs))

        url = '/Nal/node/?' \
            'function_type=%s&type=%s' % \
            ('all_node',
             '1')
        expect = [('GET', url, {}, None)]

        self.assertEqual(expect, self.api.calls)
        self.assertEqual(4, len(node))
        self.assertEqual('101', node[0]['ID'])
        self.assertEqual('102', node[1]['ID'])
        self.assertEqual('201', node[2]['ID'])
        self.assertEqual('202', node[3]['ID'])

    def test_get_all_device_type(self):
        """Test get method."""
        kwargs = {'device_type': '1',
                  'function_type': 'all_node'}

        node = list(self.mgr.get(kwargs))

        url = '/Nal/node/?' \
            'device_type=%s&function_type=%s' % \
            ('1',
             'all_node')
        expect = [('GET', url, {}, None)]

        self.assertEqual(expect, self.api.calls)
        self.assertEqual(4, len(node))
        self.assertEqual('101', node[0]['ID'])
        self.assertEqual('103', node[1]['ID'])
        self.assertEqual('201', node[2]['ID'])
        self.assertEqual('203', node[3]['ID'])

    def test_get_all_params(self):
        """Test get method."""
        kwargs = {'IaaS_tenant_id': 'test_user-414b-aa5e-dedbeef00101',
                  'apl_type': '1',
                  'type': '1',
                  'device_type': '1',
                  'function_type': 'all_node'}

        node = list(self.mgr.get(kwargs))

        url = '/Nal/node/?' \
            'IaaS_tenant_id=%s&apl_type=%s&device_type=%s&' \
            'function_type=%s&type=%s' % \
            ('test_user-414b-aa5e-dedbeef00101',
             '1',
             '1',
             'all_node',
             '1')
        expect = [('GET', url, {}, None)]

        self.assertEqual(expect, self.api.calls)
        self.assertEqual(1, len(node))
        self.assertEqual('102', node[0]['ID'])

    def test_get_vfw(self):
        """Test get method."""
        kwargs = {'ID': 'test_node-414b-aa5e-dedbeef00101',
                  'function_type': 'vfw'}

        node = list(self.mgr.get(kwargs))

        url = '/Nal/node/?' \
            'ID=%s&function_type=%s' % \
            ('test_node-414b-aa5e-dedbeef00101',
             'vfw')
        expect = [('GET', url, {}, None)]

        self.assertEqual(expect, self.api.calls)
        self.assertEqual(1, len(node))
        self.assertEqual('101', node[0]['ID'])

    def test_get_pfw(self):
        """Test get method."""
        kwargs = {'ID': 'test_node-414b-aa5e-dedbeef00101',
                  'function_type': 'pfw'}

        node = list(self.mgr.get(kwargs))

        url = '/Nal/node/?' \
            'ID=%s&function_type=%s' % \
            ('test_node-414b-aa5e-dedbeef00101',
             'pfw')
        expect = [('GET', url, {}, None)]

        self.assertEqual(expect, self.api.calls)
        self.assertEqual(1, len(node))
        self.assertEqual('103', node[0]['ID'])

    def test_get_vlb(self):
        """Test get method."""
        kwargs = {'ID': 'test_node-414b-aa5e-dedbeef00101',
                  'function_type': 'vlb'}

        node = list(self.mgr.get(kwargs))

        url = '/Nal/node/?' \
            'ID=%s&function_type=%s' % \
            ('test_node-414b-aa5e-dedbeef00101',
             'vlb')
        expect = [('GET', url, {}, None)]

        self.assertEqual(expect, self.api.calls)
        self.assertEqual(1, len(node))
        self.assertEqual('201', node[0]['ID'])

    def test_get_plb(self):
        """Test get method."""
        kwargs = {'ID': 'test_node-414b-aa5e-dedbeef00101',
                  'function_type': 'plb'}

        node = list(self.mgr.get(kwargs))

        url = '/Nal/node/?' \
            'ID=%s&function_type=%s' % \
            ('test_node-414b-aa5e-dedbeef00101',
             'plb')
        expect = [('GET', url, {}, None)]

        self.assertEqual(expect, self.api.calls)
        self.assertEqual(1, len(node))
        self.assertEqual('203', node[0]['ID'])
