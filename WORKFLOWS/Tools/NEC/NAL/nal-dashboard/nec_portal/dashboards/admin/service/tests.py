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


from mox3.mox import IsA  # noqa

from socket import timeout as socket_timeout  # noqa

from django.core.urlresolvers import reverse
from django import http
from django.utils.http import urlencode
from horizon import exceptions

from nec_portal.api import nal_api
from nec_portal.dashboards.admin.service import fixture
from nec_portal.dashboards.admin.service import panel  # noqa
from nec_portal.local import nal_portal_settings

from openstack_dashboard import api
from openstack_dashboard.test import helpers as test


SERVICE_INDEX_URL = reverse('horizon:admin:service:index')
SERVICE_DETAIL_URL = 'horizon:admin:service:detail'

SERVICE_RETURN_MAPPING = getattr(nal_portal_settings,
                                 'SERVICE_RETURN_MAPPING', None)
SERVICE_DETAIL_DISPLAY_COLUMNS = \
    getattr(nal_portal_settings, 'SERVICE_DETAIL_DISPLAY_COLUMNS', None)

TENANT_LIST_RETURN = [{'id': 'aaa8f50f82da4370813e6ea797b1fb87',
                       'name': 'network_nameA'},
                      {'id': 'bbb8f50f82da4370813e6ea797b1fb87',
                       'name': 'network_nameB'},
                      {'id': 'ccc8f50f82da4370813e6ea797b1fb87',
                       'name': 'network_nameC'}]


class ServiceAdminViewTests(test.BaseAdminViewTests):

    @test.create_stubs({nal_api: ('get_services',)})
    @test.create_stubs({api.keystone: ('tenant_list',)})
    def test_index_multi_data(self):
        tenant_data = []
        tenant_names = {}
        for data in TENANT_LIST_RETURN:
            tenant_data.append(Tenant(data))
            tenant_names[data['id']] = data['name']

        service_data = []
        check_service_data = []
        for data in fixture.SERVICE_DATA_LIST:
            service = Service(data, SERVICE_RETURN_MAPPING['all_dcconnect'])
            service_data.append(service)
            service.tenant_name = tenant_names.get(service.tenant_id, None)
            check_service_data.append(service)

        nal_api.get_services(IsA(http.HttpRequest),
                             func_type='all_dcconnect').AndReturn(service_data)

        api.keystone.tenant_list(IsA(http.HttpRequest),
                                 paginate=True).AndReturn([tenant_data, True])

        self.mox.ReplayAll()
        res = self.client.get(SERVICE_INDEX_URL)
        self.assertNoFormErrors(res)
        self.assertTemplateUsed(res, 'admin/service/index.html')
        self.assertItemsEqual(res.context['table'].data, check_service_data)

    @test.create_stubs({nal_api: ('get_services',)})
    @test.create_stubs({api.keystone: ('tenant_list',)})
    def test_index_no_data(self):
        tenant_data = []
        for data in TENANT_LIST_RETURN:
            tenant_data.append(Tenant(data))

        service_data = []
        nal_api.get_services(IsA(http.HttpRequest),
                             func_type='all_dcconnect').AndReturn(service_data)

        api.keystone.tenant_list(IsA(http.HttpRequest),
                                 paginate=True).AndReturn([tenant_data, True])

        self.mox.ReplayAll()
        res = self.client.get(SERVICE_INDEX_URL)
        self.assertNoFormErrors(res)
        self.assertTemplateUsed(res, 'admin/service/index.html')
        self.assertItemsEqual(res.context['table'].data, [])

    @test.create_stubs({nal_api: ('get_services',)})
    @test.create_stubs({api.keystone: ('tenant_list',)})
    def test_index_api_error(self):
        tenant_data = []
        for data in TENANT_LIST_RETURN:
            tenant_data.append(Tenant(data))

        nal_api.get_services(IsA(http.HttpRequest),
                             func_type='all_dcconnect').AndRaise(OSError)

        api.keystone.tenant_list(IsA(http.HttpRequest),
                                 paginate=True).AndReturn([tenant_data, True])

        self.mox.ReplayAll()
        res = self.client.get(SERVICE_INDEX_URL)

        self.assertTemplateUsed(res, 'admin/service/index.html')
        self.assertItemsEqual(res.context['table'].data, [])
        self.assertMessageCount(res, error=1)

    @test.create_stubs({nal_api: ('get_services',)})
    @test.create_stubs({api.keystone: ('tenant_list',)})
    def test_index_api_error_handle(self):
        tenant_data = []
        for data in TENANT_LIST_RETURN:
            tenant_data.append(Tenant(data))

        nal_api.get_services(
            IsA(http.HttpRequest),
            func_type='all_dcconnect').AndRaise(exceptions.NotAvailable())

        self.mox.ReplayAll()
        res = self.client.get(SERVICE_INDEX_URL)
        self.assertItemsEqual(res.context['table'].data, [])

    @test.create_stubs({nal_api: ('get_services',)})
    @test.create_stubs({api.keystone: ('tenant_list',)})
    def test_index_tenant_error(self):
        service_data = []
        for data in fixture.SERVICE_DATA_LIST:
            service = Service(data, SERVICE_RETURN_MAPPING['all_dcconnect'])
            service_data.append(service)

        nal_api.get_services(IsA(http.HttpRequest),
                             func_type='all_dcconnect').AndReturn(service_data)

        api.keystone.tenant_list(IsA(http.HttpRequest),
                                 paginate=True).AndRaise(OSError)

        self.mox.ReplayAll()
        res = self.client.get(SERVICE_INDEX_URL)

        self.assertTemplateUsed(res, 'admin/service/index.html')
        self.assertItemsEqual(res.context['table'].data, service_data)
        self.assertMessageCount(res, error=1)

    @test.create_stubs({nal_api: ('get_services',)})
    @test.create_stubs({api.keystone: ('tenant_get',)})
    def test_detail_in_dc_member(self):

        service_data = {}
        obj_id = '|'.join(
            ['dcconnect',
             str(fixture.SERVICE_DATA_DEFAULT['dc_group_info'][0]['group_id'])]
        )
        for key, value in SERVICE_RETURN_MAPPING['dcconnect'].iteritems():
            if isinstance(value, dict):
                service_data[key] = []
                for service_row in fixture.SERVICE_DATA_DEFAULT[key]:
                    service_data[key].append(Service(service_row, value))

        nal_api.get_services(
            IsA(http.HttpRequest),
            group_id=obj_id.split('|')[1],
            func_type=obj_id.split('|')[0]).AndReturn(service_data)

        tenant_data = Tenant({'id': 'aaa8f50f82da4370813e6ea797b1fb87',
                              'name': 'network_nameA'})
        api.keystone.tenant_get(IsA(http.HttpRequest),
                                IsA('str')).AndReturn(tenant_data)

        self.mox.ReplayAll()
        res = self.client.get(reverse(SERVICE_DETAIL_URL,
                                      kwargs={"group_id": obj_id}))
        self.assertNoFormErrors(res)
        self.assertTemplateUsed(res, 'admin/service/detail.html')
        for i, detail in enumerate(
                SERVICE_DETAIL_DISPLAY_COLUMNS['dcconnect']['detail']):
            if i == 0:
                self.assertItemsEqual(res.context['service'][0],
                                      ['Tenant Name', 'network_nameA'])
            else:
                pass
            self.assertItemsEqual(
                res.context['service'][i + 1][0], detail[0])

    @test.create_stubs({nal_api: ('get_services',)})
    @test.create_stubs({api.keystone: ('tenant_get',)})
    def test_detail_out_dc_member(self):

        service_data = {}
        dc_group_info = fixture.SERVICE_DATA_OUT_OF_MEMBER['dc_group_info']
        obj_id = '|'.join(
            ['dcconnect',
             str(dc_group_info[0]['group_id'])]
        )
        for key, value in SERVICE_RETURN_MAPPING['dcconnect'].iteritems():
            if isinstance(value, dict):
                service_data[key] = []
                for service_row in fixture.SERVICE_DATA_OUT_OF_MEMBER[key]:
                    service_data[key].append(Service(service_row, value))

        nal_api.get_services(
            IsA(http.HttpRequest),
            group_id=obj_id.split('|')[1],
            func_type=obj_id.split('|')[0]).AndReturn(service_data)

        tenant_data = Tenant({'id': 'aaa8f50f82da4370813e6ea797b1fb87',
                              'name': 'network_nameA'})
        api.keystone.tenant_get(IsA(http.HttpRequest),
                                IsA('str')).AndReturn(tenant_data)

        self.mox.ReplayAll()
        res = self.client.get(reverse(SERVICE_DETAIL_URL,
                                      kwargs={"group_id": obj_id}))
        self.assertNoFormErrors(res)
        self.assertTemplateUsed(res, 'admin/service/detail.html')
        for i, detail in enumerate(
                SERVICE_DETAIL_DISPLAY_COLUMNS['dcconnect']['detail']):
            if i == 0:
                self.assertItemsEqual(res.context['service'][0],
                                      ['Tenant Name', 'network_nameA'])
            else:
                pass
            self.assertItemsEqual(
                res.context['service'][i + 1][0], detail[0])

    @test.create_stubs({nal_api: ('get_services',)})
    @test.create_stubs({api.keystone: ('tenant_get',)})
    def test_detail_without_member_data(self):

        service_data = {}
        dc_group_info = fixture.SERVICE_DATA_NO_MEMBER_LIST['dc_group_info']
        obj_id = '|'.join(
            ['dcconnect',
             str(dc_group_info[0]['group_id'])]
        )
        for key, value in SERVICE_RETURN_MAPPING['dcconnect'].iteritems():
            if isinstance(value, dict):
                service_data[key] = []
                for service_row in fixture.SERVICE_DATA_NO_MEMBER_LIST[key]:
                    service_data[key].append(Service(service_row, value))

        nal_api.get_services(
            IsA(http.HttpRequest),
            group_id=obj_id.split('|')[1],
            func_type=obj_id.split('|')[0]).AndReturn(service_data)

        tenant_data = Tenant({'id': 'aaa8f50f82da4370813e6ea797b1fb87',
                              'name': 'network_nameA'})
        api.keystone.tenant_get(IsA(http.HttpRequest),
                                IsA('str')).AndReturn(tenant_data)

        self.mox.ReplayAll()
        res = self.client.get(reverse(SERVICE_DETAIL_URL,
                                      kwargs={"group_id": obj_id}))
        self.assertNoFormErrors(res)
        self.assertTemplateUsed(res, 'admin/service/detail.html')
        for i, detail in enumerate(
                SERVICE_DETAIL_DISPLAY_COLUMNS['dcconnect']['detail']):
            if i == 0:
                self.assertItemsEqual(res.context['service'][0],
                                      ['Tenant Name', 'network_nameA'])
            else:
                pass
            self.assertItemsEqual(
                res.context['service'][i + 1][0], detail[0])

    @test.create_stubs({nal_api: ('get_services',)})
    @test.create_stubs({api.keystone: ('tenant_get',)})
    def test_detail_without_network_data(self):

        service_data = {}
        dc_group_info = fixture.SERVICE_DATA_NO_NETWORK_LIST['dc_group_info']
        obj_id = '|'.join(
            ['dcconnect',
             str(dc_group_info[0]['group_id'])]
        )
        for key, value in SERVICE_RETURN_MAPPING['dcconnect'].iteritems():
            if isinstance(value, dict):
                service_data[key] = []
                for service_row in fixture.SERVICE_DATA_NO_NETWORK_LIST[key]:
                    service_data[key].append(Service(service_row, value))

        nal_api.get_services(
            IsA(http.HttpRequest),
            group_id=obj_id.split('|')[1],
            func_type=obj_id.split('|')[0]).AndReturn(service_data)

        tenant_data = Tenant({'id': 'aaa8f50f82da4370813e6ea797b1fb87',
                              'name': 'network_nameA'})
        api.keystone.tenant_get(IsA(http.HttpRequest),
                                IsA('str')).AndReturn(tenant_data)

        self.mox.ReplayAll()
        res = self.client.get(reverse(SERVICE_DETAIL_URL,
                                      kwargs={"group_id": obj_id}))
        self.assertNoFormErrors(res)
        self.assertTemplateUsed(res, 'admin/service/detail.html')
        for i, detail in enumerate(
                SERVICE_DETAIL_DISPLAY_COLUMNS['dcconnect']['detail']):
            if i == 0:
                self.assertItemsEqual(res.context['service'][0],
                                      ['Tenant Name', 'network_nameA'])
            else:
                pass
            self.assertItemsEqual(
                res.context['service'][i + 1][0], detail[0])

    @test.create_stubs({nal_api: ('get_services',)})
    @test.create_stubs({api.keystone: ('tenant_list',)})
    def test_detail_api_error(self):
        dc_group_info = fixture.SERVICE_DATA_DEFAULT['dc_group_info']
        obj_id = '|'.join(['dcconnect',
                           str(dc_group_info[0]['group_id'])])
        nal_api.get_services(IsA(http.HttpRequest),
                             group_id=obj_id.split('|')[1],
                             func_type=obj_id.split('|')[0]
                             ).AndRaise(OSError)

        tenant_data = []
        tenant_names = {}
        for data in TENANT_LIST_RETURN:
            tenant_data.append(Tenant(data))
            tenant_names[data['id']] = data['name']

        service_data = []
        check_service_data = []
        for data in fixture.SERVICE_DATA_LIST:
            service = Service(data, SERVICE_RETURN_MAPPING['all_dcconnect'])
            service_data.append(service)
            service.tenant_name = tenant_names.get(service.tenant_id, None)
            check_service_data.append(service)

        nal_api.get_services(IsA(http.HttpRequest),
                             func_type='all_dcconnect').AndReturn(service_data)

        api.keystone.tenant_list(IsA(http.HttpRequest),
                                 paginate=True).AndReturn([tenant_data, True])

        self.mox.ReplayAll()

        res = self.client.get(reverse(SERVICE_DETAIL_URL,
                                      kwargs={"group_id": obj_id}))
        self.assertRedirects(res, SERVICE_INDEX_URL)

    @test.create_stubs({nal_api: ('get_services',)})
    @test.create_stubs({api.keystone: ('tenant_list',)})
    def test_detail_api_error_handle(self):
        dc_group_info = fixture.SERVICE_DATA_DEFAULT['dc_group_info']
        obj_id = '|'.join(['dcconnect',
                           str(dc_group_info[0]['group_id'])])

        nal_api.get_services(IsA(http.HttpRequest),
                             group_id=obj_id.split('|')[1],
                             func_type=obj_id.split('|')[0]
                             ).AndRaise(exceptions.NotAvailable())

        tenant_data = []
        tenant_names = {}
        for data in TENANT_LIST_RETURN:
            tenant_data.append(Tenant(data))
            tenant_names[data['id']] = data['name']

        service_data = []
        check_service_data = []
        for data in fixture.SERVICE_DATA_LIST:
            service = Service(data, SERVICE_RETURN_MAPPING['all_dcconnect'])
            service_data.append(service)
            service.tenant_name = tenant_names.get(service.tenant_id, None)
            check_service_data.append(service)

        nal_api.get_services(IsA(http.HttpRequest),
                             func_type='all_dcconnect').AndReturn(service_data)

        api.keystone.tenant_list(IsA(http.HttpRequest),
                                 paginate=True).AndReturn([tenant_data, True])

        self.mox.ReplayAll()
        res = self.client.get(reverse(SERVICE_DETAIL_URL,
                                      kwargs={"group_id": obj_id}))
        self.assertRedirects(res, SERVICE_INDEX_URL)

    @test.create_stubs({nal_api: ('get_services',)})
    @test.create_stubs({api.keystone: ('tenant_get',
                                       'tenant_list')})
    def test_detail_tenant_error(self):
        service_data = {}
        obj_id = '|'.join(
            ['dcconnect',
             str(fixture.SERVICE_DATA_DEFAULT['dc_group_info'][0]['group_id'])]
        )
        for key, value in SERVICE_RETURN_MAPPING['dcconnect'].iteritems():
            if isinstance(value, dict):
                service_data[key] = []
                for service_row in fixture.SERVICE_DATA_DEFAULT[key]:
                    service_data[key].append(Service(service_row, value))

        nal_api.get_services(
            IsA(http.HttpRequest),
            group_id=obj_id.split('|')[1],
            func_type=obj_id.split('|')[0]).AndReturn(service_data)

        api.keystone.tenant_get(IsA(http.HttpRequest),
                                IsA('str')).AndRaise(OSError)

        tenant_data = []
        tenant_names = {}
        for data in TENANT_LIST_RETURN:
            tenant_data.append(Tenant(data))
            tenant_names[data['id']] = data['name']

        service_data = []
        check_service_data = []
        for data in fixture.SERVICE_DATA_LIST:
            service = Service(data, SERVICE_RETURN_MAPPING['all_dcconnect'])
            service_data.append(service)
            service.tenant_name = tenant_names.get(service.tenant_id, None)
            check_service_data.append(service)

        nal_api.get_services(IsA(http.HttpRequest),
                             func_type='all_dcconnect').AndReturn(service_data)

        api.keystone.tenant_list(IsA(http.HttpRequest),
                                 paginate=True).AndReturn([tenant_data, True])

        self.mox.ReplayAll()
        res = self.client.get(reverse(SERVICE_DETAIL_URL,
                                      kwargs={"group_id": obj_id}))
        self.assertRedirects(res, SERVICE_INDEX_URL)

    @test.create_stubs({nal_api: ('get_services',)})
    @test.create_stubs({api.keystone: ('tenant_list',
                                       'tenant_get')})
    def test_row_update(self):

        dc_group_info = fixture.SERVICE_DATA_NO_MEMBER_LIST['dc_group_info']
        service_data = {}
        obj_id = '|'.join(
            ['dcconnect',
             str(dc_group_info[0]['group_id'])]
        )
        for key, value in SERVICE_RETURN_MAPPING['dcconnect'].iteritems():
            if isinstance(value, dict):
                service_data[key] = []
                for service_row in fixture.SERVICE_DATA_NO_MEMBER_LIST[key]:
                    service_data[key].append(Service(service_row, value))

        nal_api.get_services(
            IsA(http.HttpRequest),
            group_id=obj_id.split('|')[1],
            func_type=obj_id.split('|')[0]).AndReturn(service_data)

        tenant_data = Tenant({'id': 'aaa8f50f82da4370813e6ea797b1fb87',
                              'name': 'network_nameA'})
        api.keystone.tenant_get(IsA(http.HttpRequest),
                                IsA('str')).AndReturn(tenant_data)

        tenant_list = [{'id': 'aaa8f50f82da4370813e6ea797b1fb87',
                        'name': 'network_nameA'},
                       {'id': 'bbb8f50f82da4370813e6ea797b1fb87',
                        'name': 'network_nameB'},
                       {'id': 'ccc8f50f82da4370813e6ea797b1fb87',
                        'name': 'network_nameC'}]
        tenant_data = []
        tenant_names = {}
        for data in tenant_list:
            tenant_data.append(Tenant(data))
            tenant_names[data['id']] = data['name']

        service_data = []
        check_service_data = []
        for data in fixture.SERVICE_DATA_LIST:
            service = Service(data, SERVICE_RETURN_MAPPING['all_dcconnect'])
            service_data.append(service)
            service.tenant_name = tenant_names.get(service.tenant_id, None)
            check_service_data.append(service)

        nal_api.get_services(IsA(http.HttpRequest),
                             func_type='all_dcconnect').AndReturn(service_data)

        api.keystone.tenant_list(IsA(http.HttpRequest),
                                 paginate=True).AndReturn([tenant_data, True])

        self.mox.ReplayAll()

        params = {'action': 'row_update',
                  'table': 'service',
                  'obj_id': obj_id,
                  }
        res = self.client.get('?'.join([SERVICE_INDEX_URL, urlencode(params)]))
        self.assertContains(res, dc_group_info[0]['group_name'])


class Service(object):
    """Service class"""
    def __init__(self, return_obj, mapping):

        for key, value in mapping.iteritems():
                self.__dict__[key] = return_obj.get(value, None)


class Tenant(object):
    """Tenant class"""
    def __init__(self, network_data):

        for key, value in network_data.iteritems():
                self.__dict__[key] = value
