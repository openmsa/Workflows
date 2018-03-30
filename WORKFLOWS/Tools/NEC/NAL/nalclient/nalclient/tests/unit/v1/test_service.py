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


"""Test nalclient/v1/service.py."""
from datetime import datetime
import os
import sys
import testtools

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../../../../')

from nalclient.tests.unit import utils
from nalclient.v1 import service


def get_datetime(str_date):
    """Get datetime.
        :param str_date: String of date.
    """
    return datetime.strptime(str_date + 'T00:00:00.000000',
                             '%Y-%m-%dT%H:%M:%S.%f')

fixtures_service_data_detail_101 = {
    "create_id": "system",
    "create_date": get_datetime('2016-12-31'),
    "update_id": "system",
    "update_date": get_datetime('2016-12-31'),
    "delete_flg": "0",
    "ID": "101",
    "group_id": "group_id_00001",
    "group_name": "dc_gru_1",
    "group_type": "1",
    "tenant_name": "admin",
    "IaaS_tenant_id": "a0d58ee41a364026a1031aca2548fd03",
    "task_status": "1",
    "my_group_flg": "1"
}

fixtures_service_data_detail_102 = {
    "create_id": "system",
    "create_date": get_datetime('2016-12-31'),
    "update_id": "system",
    "update_date": get_datetime('2016-12-31'),
    "delete_flg": "0",
    "ID": "102",
    "group_id": "group_id_00002",
    "group_name": "dc_gru_2",
    "group_type": "2",
    "tenant_name": "admin",
    "IaaS_tenant_id": "a0d58ee41a364026a1031aca2548fd03",
    "task_status": "1"
}

fixtures_service_data_detail_201 = {
    "create_id": "system",
    "create_date": get_datetime('2016-12-31'),
    "update_id": "system",
    "update_date": get_datetime('2016-12-31'),
    "delete_flg": "0",
    "ID": "201",
    "group_id": "group_id_00021",
    "group_name": "dc_gru_21",
    "group_type": "1",
    "tenant_name": "admin",
    "IaaS_tenant_id": "ea128ee41a364026a1031aca2548bc53",
    "task_status": "1",
    "my_group_flg": "1"
}

fixtures_service_data_detail_202 = {
    "create_id": "system",
    "create_date": get_datetime('2016-12-31'),
    "update_id": "system",
    "update_date": get_datetime('2016-12-31'),
    "delete_flg": "0",
    "ID": "202",
    "group_id": "group_id_00022",
    "group_name": "dc_gru_22",
    "group_type": "2",
    "tenant_name": "admin",
    "IaaS_tenant_id": "ea128ee41a364026a1031aca2548bc53",
    "task_status": "1"
}


fixtures = {
    '/Nal/service/': {
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
    '/Nal/service/?function_type=dcconnect': {
        'GET': {
            'data': [
                fixtures_service_data_detail_101,
                fixtures_service_data_detail_102,
                fixtures_service_data_detail_201,
                fixtures_service_data_detail_202
            ]
        }
    },
    '/Nal/service/?IaaS_tenant_id=tenant_id_00001'
    '&function_type=dcconnect': {
        'GET': {
            'data': [
                fixtures_service_data_detail_101,
                fixtures_service_data_detail_102
            ]
        }
    },
    '/Nal/service/?function_type=dcconnect&group_id=group_id_00001': {
        'GET': {
            'data': [
                fixtures_service_data_detail_101
            ]
        }
    },
    '/Nal/service/?IaaS_tenant_id=tenant_id_00001'
    '&function_type=dcconnect&group_id=group_id_00002': {
        'GET': {
            'data': [
                fixtures_service_data_detail_102
            ]
        }
    },
}


class ServiceManagerTest(testtools.TestCase):
    """ServiceManager Test class."""

    def setUp(self):
        """Setup test class."""
        super(ServiceManagerTest, self).setUp()
        self.api = utils.FakeAPI(fixtures)
        self.mgr = service.ServiceManager(self.api)

    def test_create(self):
        """Test create method."""
        kwargs = {
            'operation_id': 'test_user-414b-aa5e-dedbeef00101',
            'IaaS_tenant_id': 'tenantid-414b-aa5e-dedbeef00101',
            'IaaS_tenant_name': 'test_tenant',
            'IaaS_region_id': 'regionid-414b-aa5e-dedbeef00101',
            'IaaS_network_type': 'vxlan',
            'IaaS_network_id': 'netid-414b-aa5e-dedbeef00101',
            'network_name': 'test_network',
            'dc_id': 'dcid-414b-aa5e-dedbeef00101',
            'fw_ip_address': '10.20.30.11',
            'function_type': 'dcconnect'
        }

        self.mgr.create(kwargs)

        expect = [('POST', '/Nal/service/', {},
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
            'function_type': 'dcconnect'
        }

        self.mgr.update(kwargs)

        expect = [('PUT', '/Nal/service/', {},
                   sorted(kwargs.items(), key=lambda x: x[0]))]

        self.assertEqual(expect, self.api.calls)

    def test_delete(self):
        """Test delete method."""
        kwargs = {
            'operation_id': 'test_user-414b-aa5e-dedbeef00101',
            'IaaS_tenant_id': 'tenantid-414b-aa5e-dedbeef00101',
            'IaaS_region_id': 'regionid-414b-aa5e-dedbeef00101',
            'dc_id': 'dcid-414b-aa5e-dedbeef00101',
            'function_type': 'dcconnect'
        }

        self.mgr.delete(kwargs)

        expect = [('DELETE', '/Nal/service/', {},
                   sorted(kwargs.items(), key=lambda x: x[0]))]

        self.assertEqual(expect, self.api.calls)

    def test_get_all(self):
        """Test get method."""
        kwargs = {'function_type': 'dcconnect'}

        service = list(self.mgr.get(kwargs))

        url = '/Nal/service/?' \
            'function_type=%s' % ('dcconnect')
        expect = [('GET', url, {}, None)]

        self.assertEqual(expect, self.api.calls)
        self.assertEqual(4, len(service))
        self.assertEqual('101', service[0]['ID'])
        self.assertEqual('102', service[1]['ID'])
        self.assertEqual('201', service[2]['ID'])
        self.assertEqual('202', service[3]['ID'])

    def test_get_all_tenant(self):
        """Test get method."""
        kwargs = {'IaaS_tenant_id': 'tenant_id_00001',
                  'function_type': 'dcconnect'}

        service = list(self.mgr.get(kwargs))

        url = '/Nal/service/?' \
            'IaaS_tenant_id=%s&function_type=%s' % \
            ('tenant_id_00001',
             'dcconnect')
        expect = [('GET', url, {}, None)]

        self.assertEqual(expect, self.api.calls)
        self.assertEqual(2, len(service))
        self.assertEqual('101', service[0]['ID'])
        self.assertEqual('102', service[1]['ID'])

    def test_get_detail(self):
        """Test get method."""
        kwargs = {'function_type': 'dcconnect',
                  'group_id': 'group_id_00001'}

        service = list(self.mgr.get(kwargs))

        url = '/Nal/service/?' \
            'function_type=%s&group_id=%s' % \
            ('dcconnect',
             'group_id_00001')
        expect = [('GET', url, {}, None)]

        self.assertEqual(expect, self.api.calls)
        self.assertEqual(1, len(service))
        self.assertEqual('101', service[0]['ID'])

    def test_get_all_params(self):
        """Test get method."""
        kwargs = {'IaaS_tenant_id': 'tenant_id_00001',
                  'function_type': 'dcconnect',
                  'group_id': 'group_id_00002'}

        service = list(self.mgr.get(kwargs))

        url = '/Nal/service/?' \
            'IaaS_tenant_id=%s&function_type=%s&group_id=%s' % \
            ('tenant_id_00001',
             'dcconnect',
             'group_id_00002')
        expect = [('GET', url, {}, None)]

        self.assertEqual(expect, self.api.calls)
        self.assertEqual(1, len(service))
        self.assertEqual('102', service[0]['ID'])
