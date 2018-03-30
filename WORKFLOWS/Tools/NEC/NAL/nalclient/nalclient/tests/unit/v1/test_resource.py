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


"""Test nalclient/v1/resource.py."""
from datetime import datetime
import os
import sys
import testtools

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../../../../')

from nalclient.tests.unit import utils
from nalclient.v1 import resource


def get_datetime(str_date):
    """Get datetime.
        :param str_date: String of date.
    """
    return datetime.strptime(str_date + 'T00:00:00.000000',
                             '%Y-%m-%dT%H:%M:%S.%f')

fixtures_resource_data_detail_101 = \
    {'create_id': 'test_user-414b-aa5e-dedbeef00101',
     'create_date': get_datetime('2016-12-31'),
     'update_id': 'test_user-414b-aa5e-dedbeef00101',
     'update_date': get_datetime('2016-12-31'),
     'delete_flg': '0',
     'ID': '101'}

fixtures_resource_data_detail_102 = \
    {'create_id': 'test_user-414b-aa5e-dedbeef00101',
     'create_date': get_datetime('2016-12-31'),
     'update_id': 'test_user-414b-aa5e-dedbeef00101',
     'update_date': get_datetime('2016-12-31'),
     'delete_flg': '0',
     'ID': '102'}

fixtures_resource_data_detail_103 = \
    {'create_id': 'test_user-414b-aa5e-dedbeef00101',
     'create_date': get_datetime('2016-12-31'),
     'update_id': 'test_user-414b-aa5e-dedbeef00101',
     'update_date': get_datetime('2016-12-31'),
     'delete_flg': '0',
     'ID': '103'}

fixtures_resource_data_detail_201 = \
    {'create_id': 'test_user-414b-aa5e-dedbeef00101',
     'create_date': get_datetime('2016-12-31'),
     'update_id': 'test_user-414b-aa5e-dedbeef00101',
     'update_date': get_datetime('2016-12-31'),
     'delete_flg': '0',
     'ID': '201'}

fixtures_resource_data_detail_202 = \
    {'create_id': 'test_user-414b-aa5e-dedbeef00101',
     'create_date': get_datetime('2016-12-31'),
     'update_id': 'test_user-414b-aa5e-dedbeef00101',
     'update_date': get_datetime('2016-12-31'),
     'delete_flg': '0',
     'ID': '202'}

fixtures_resource_data_detail_203 = \
    {'create_id': 'test_user-414b-aa5e-dedbeef00101',
     'create_date': get_datetime('2016-12-31'),
     'update_id': 'test_user-414b-aa5e-dedbeef00101',
     'update_date': get_datetime('2016-12-31'),
     'delete_flg': '0',
     'ID': '203'}


# from nalclient.v1 import client
#  request fixtures
#    (request url, request header, request parameter).
fixtures = {
    '/Nal/resource/': {
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
    '/Nal/resource/?function_type=all_resource': {
        'GET': {
            'data': [
                fixtures_resource_data_detail_101,
                fixtures_resource_data_detail_102,
                fixtures_resource_data_detail_103,
                fixtures_resource_data_detail_201,
                fixtures_resource_data_detail_202,
                fixtures_resource_data_detail_203
            ]
        }
    },
    '/Nal/resource/?IaaS_tenant_id=test_user-414b-aa5e-dedbeef00101'
    '&function_type=all_resource': {
        'GET': {
            'data': [
                fixtures_resource_data_detail_101,
                fixtures_resource_data_detail_102,
                fixtures_resource_data_detail_203
            ]
        }
    }
}


class ResourceManagerTest(testtools.TestCase):
    """ResourceManager Test class."""

    def setUp(self):
        """Setup test class."""
        super(ResourceManagerTest, self).setUp()
        self.api = utils.FakeAPI(fixtures)
        self.mgr = resource.ResourceManager(self.api)

    def test_create(self):
        """Test create method."""
        kwargs = {
            'operation_id': 'test_user-414b-aa5e-dedbeef00101',
            'IaaS_tenant_id': 'tenantid-414b-aa5e-dedbeef00101',
            'IaaS_tenant_name': 'test_tenant',
            'IaaS_region_id': 'regionid-414b-aa5e-dedbeef00101',
            'function_type': 'globalip'
        }

        self.mgr.create(kwargs)

        expect = [('POST', '/Nal/resource/', {},
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
            'function_type': 'globalip'
        }

        self.mgr.update(kwargs)

        expect = [('PUT', '/Nal/resource/', {},
                   sorted(kwargs.items(), key=lambda x: x[0]))]

        self.assertEqual(expect, self.api.calls)

    def test_delete(self):
        """Test delete method."""
        kwargs = {
            'operation_id': 'test_user-414b-aa5e-dedbeef00101',
            'IaaS_tenant_id': 'tenantid-414b-aa5e-dedbeef00101',
            'IaaS_region_id': 'regionid-414b-aa5e-dedbeef00101',
            'function_type': 'globalip'
        }

        self.mgr.delete(kwargs)

        expect = [('DELETE', '/Nal/resource/', {},
                   sorted(kwargs.items(), key=lambda x: x[0]))]

        self.assertEqual(expect, self.api.calls)

    def test_get_all(self):
        """Test get method."""
        kwargs = {'function_type': 'all_resource'}

        resource = list(self.mgr.get(kwargs))

        url = '/Nal/resource/?' \
            'function_type=%s' % ('all_resource')
        expect = [('GET', url, {}, None)]

        self.assertEqual(expect, self.api.calls)
        self.assertEqual(6, len(resource))
        self.assertEqual('101', resource[0]['ID'])
        self.assertEqual('102', resource[1]['ID'])
        self.assertEqual('103', resource[2]['ID'])
        self.assertEqual('201', resource[3]['ID'])
        self.assertEqual('202', resource[4]['ID'])
        self.assertEqual('203', resource[5]['ID'])

    def test_get_all_tenant(self):
        """Test get method."""
        kwargs = {'IaaS_tenant_id': 'test_user-414b-aa5e-dedbeef00101',
                  'function_type': 'all_resource'}

        resource = list(self.mgr.get(kwargs))

        url = '/Nal/resource/?' \
            'IaaS_tenant_id=%s&function_type=%s' % \
            ('test_user-414b-aa5e-dedbeef00101',
             'all_resource')
        expect = [('GET', url, {}, None)]

        self.assertEqual(expect, self.api.calls)
        self.assertEqual(3, len(resource))
        self.assertEqual('101', resource[0]['ID'])
        self.assertEqual('102', resource[1]['ID'])
        self.assertEqual('203', resource[2]['ID'])
