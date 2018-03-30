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
from nec_portal.dashboards.project.service import fixture
from nec_portal.dashboards.project.service import panel  # noqa
from nec_portal.local import nal_portal_settings

from openstack_dashboard import api
from openstack_dashboard.test import helpers as test


SERVICE_INDEX_URL = reverse('horizon:project:service:index')
SERVICE_CREATE_URL = reverse('horizon:project:service:create')
SERVICE_DETAIL_URL = 'horizon:project:service:detail'
SERVICE_UPDATE_URL = 'horizon:project:service:update'

SERVICE_RETURN_MAPPING = getattr(nal_portal_settings,
                                 'SERVICE_RETURN_MAPPING', None)
SERVICE_DETAIL_DISPLAY_COLUMNS = \
    getattr(nal_portal_settings, 'SERVICE_DETAIL_DISPLAY_COLUMNS', None)
SERVICE_TYPE_MAPPING = getattr(nal_portal_settings,
                               'SERVICE_TYPE_MAPPING', None)
NAL_CONSTRUCT_SERVICE_TYPE = getattr(nal_portal_settings,
                                     'NAL_CONSTRUCT_SERVICE_TYPE', None)


class ServiceViewTests(test.TestCase):

    @test.create_stubs({nal_api: ('get_services',)})
    def test_index_multi_data(self):

        service_data = []
        for data in fixture.SERVICE_DATA_LIST:
            service_data.append(
                Service(data,
                        SERVICE_RETURN_MAPPING['all_dcconnect']))

        nal_api.get_services(IsA(http.HttpRequest),
                             IsA('str'),
                             func_type='all_dcconnect').AndReturn(service_data)

        self.mox.ReplayAll()
        res = self.client.get(SERVICE_INDEX_URL)
        self.assertNoFormErrors(res)
        self.assertTemplateUsed(res, 'project/service/index.html')
        self.assertItemsEqual(res.context['table'].data, service_data)

    @test.create_stubs({nal_api: ('get_services',)})
    def test_index_no_data(self):

        service_data = []

        nal_api.get_services(IsA(http.HttpRequest),
                             IsA('str'),
                             func_type='all_dcconnect').AndReturn(service_data)

        self.mox.ReplayAll()
        res = self.client.get(SERVICE_INDEX_URL)
        self.assertNoFormErrors(res)
        self.assertTemplateUsed(res, 'project/service/index.html')
        self.assertItemsEqual(res.context['table'].data, [])

    @test.create_stubs({nal_api: ('get_services',)})
    def test_index_api_error(self):

        nal_api.get_services(IsA(http.HttpRequest),
                             IsA('str'),
                             func_type='all_dcconnect').AndRaise(OSError)

        self.mox.ReplayAll()
        res = self.client.get(SERVICE_INDEX_URL)

        self.assertTemplateUsed(res, 'project/service/index.html')
        self.assertItemsEqual(res.context['table'].data, [])
        self.assertMessageCount(res, error=1)

    @test.create_stubs({nal_api: ('get_services',)})
    def test_index_api_error_handle(self):

        nal_api.get_services(
            IsA(http.HttpRequest),
            IsA('str'),
            func_type='all_dcconnect').AndRaise(exceptions.NotAvailable())

        self.mox.ReplayAll()
        res = self.client.get(SERVICE_INDEX_URL)
        self.assertItemsEqual(res.context['table'].data, [])

    @test.create_stubs({nal_api: ('get_services',)})
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

        nal_api.get_services(
            IsA(http.HttpRequest),
            group_id=obj_id.split('|')[1],
            func_type=obj_id.split('|')[0]).AndReturn(service_data)

        nal_api.get_services(
            IsA(http.HttpRequest),
            group_id=obj_id.split('|')[1],
            func_type=obj_id.split('|')[0]).AndReturn(service_data)

        nal_api.get_services(
            IsA(http.HttpRequest),
            group_id=obj_id.split('|')[1],
            func_type=obj_id.split('|')[0]).AndReturn(service_data)

        nal_api.get_services(
            IsA(http.HttpRequest),
            group_id=obj_id.split('|')[1],
            func_type=obj_id.split('|')[0]).AndReturn(service_data)

        self.mox.ReplayAll()
        res = self.client.get(reverse(SERVICE_DETAIL_URL,
                                      kwargs={"group_id": obj_id}))
        self.assertNoFormErrors(res)
        self.assertTemplateUsed(res, 'project/service/detail.html')
        for i, detail in enumerate(
                SERVICE_DETAIL_DISPLAY_COLUMNS['dcconnect']['detail']):
            self.assertItemsEqual(res.context['service'][i][0], detail[0])

    @test.create_stubs({nal_api: ('get_services',)})
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

        nal_api.get_services(
            IsA(http.HttpRequest),
            group_id=obj_id.split('|')[1],
            func_type=obj_id.split('|')[0]).AndReturn(service_data)

        nal_api.get_services(
            IsA(http.HttpRequest),
            group_id=obj_id.split('|')[1],
            func_type=obj_id.split('|')[0]).AndReturn(service_data)

        nal_api.get_services(
            IsA(http.HttpRequest),
            group_id=obj_id.split('|')[1],
            func_type=obj_id.split('|')[0]).AndReturn(service_data)

        nal_api.get_services(
            IsA(http.HttpRequest),
            group_id=obj_id.split('|')[1],
            func_type=obj_id.split('|')[0]).AndReturn(service_data)

        self.mox.ReplayAll()
        res = self.client.get(reverse(SERVICE_DETAIL_URL,
                                      kwargs={"group_id": obj_id}))
        self.assertNoFormErrors(res)
        self.assertTemplateUsed(res, 'project/service/detail.html')
        for i, detail in enumerate(
                SERVICE_DETAIL_DISPLAY_COLUMNS['dcconnect']['detail']):
            self.assertItemsEqual(res.context['service'][i][0], detail[0])

    @test.create_stubs({nal_api: ('get_services',)})
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

        nal_api.get_services(
            IsA(http.HttpRequest),
            group_id=obj_id.split('|')[1],
            func_type=obj_id.split('|')[0]).AndReturn(service_data)

        nal_api.get_services(
            IsA(http.HttpRequest),
            group_id=obj_id.split('|')[1],
            func_type=obj_id.split('|')[0]).AndReturn(service_data)

        nal_api.get_services(
            IsA(http.HttpRequest),
            group_id=obj_id.split('|')[1],
            func_type=obj_id.split('|')[0]).AndReturn(service_data)

        nal_api.get_services(
            IsA(http.HttpRequest),
            group_id=obj_id.split('|')[1],
            func_type=obj_id.split('|')[0]).AndReturn(service_data)

        self.mox.ReplayAll()
        res = self.client.get(reverse(SERVICE_DETAIL_URL,
                                      kwargs={"group_id": obj_id}))
        self.assertNoFormErrors(res)
        self.assertTemplateUsed(res, 'project/service/detail.html')
        for i, detail in enumerate(
                SERVICE_DETAIL_DISPLAY_COLUMNS['dcconnect']['detail']):
            self.assertItemsEqual(res.context['service'][i][0], detail[0])

    @test.create_stubs({nal_api: ('get_services',)})
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

        nal_api.get_services(
            IsA(http.HttpRequest),
            group_id=obj_id.split('|')[1],
            func_type=obj_id.split('|')[0]).AndReturn(service_data)

        nal_api.get_services(
            IsA(http.HttpRequest),
            group_id=obj_id.split('|')[1],
            func_type=obj_id.split('|')[0]).AndReturn(service_data)

        nal_api.get_services(
            IsA(http.HttpRequest),
            group_id=obj_id.split('|')[1],
            func_type=obj_id.split('|')[0]).AndReturn(service_data)

        nal_api.get_services(
            IsA(http.HttpRequest),
            group_id=obj_id.split('|')[1],
            func_type=obj_id.split('|')[0]).AndReturn(service_data)

        self.mox.ReplayAll()
        res = self.client.get(reverse(SERVICE_DETAIL_URL,
                                      kwargs={"group_id": obj_id}))
        self.assertNoFormErrors(res)
        self.assertTemplateUsed(res, 'project/service/detail.html')
        for i, detail in enumerate(
                SERVICE_DETAIL_DISPLAY_COLUMNS['dcconnect']['detail']):
            self.assertItemsEqual(res.context['service'][i][0], detail[0])

    @test.create_stubs({nal_api: ('get_services',)})
    def test_detail_api_error(self):
        dc_group_info = fixture.SERVICE_DATA_DEFAULT['dc_group_info']
        obj_id = '|'.join(['dcconnect',
                           str(dc_group_info[0]['group_id'])])
        nal_api.get_services(IsA(http.HttpRequest),
                             group_id=obj_id.split('|')[1],
                             func_type=obj_id.split('|')[0]
                             ).AndRaise(OSError)

        service_data = []
        for data in fixture.SERVICE_DATA_LIST:
            service_data.append(
                Service(data,
                        SERVICE_RETURN_MAPPING['all_dcconnect']))

        nal_api.get_services(IsA(http.HttpRequest),
                             IsA('str'),
                             func_type='all_dcconnect').AndReturn(service_data)

        self.mox.ReplayAll()
        res = self.client.get(reverse(SERVICE_DETAIL_URL,
                                      kwargs={"group_id": obj_id}))
        self.assertRedirects(res, SERVICE_INDEX_URL)

    @test.create_stubs({nal_api: ('get_services',)})
    def test_detail_api_error_handle(self):
        dc_group_info = fixture.SERVICE_DATA_DEFAULT['dc_group_info']
        obj_id = '|'.join(['dcconnect',
                           str(dc_group_info[0]['group_id'])])

        nal_api.get_services(IsA(http.HttpRequest),
                             group_id=obj_id.split('|')[1],
                             func_type=obj_id.split('|')[0]
                             ).AndRaise(exceptions.NotAvailable())

        nal_api.get_services(IsA(http.HttpRequest),
                             IsA('str'),
                             func_type='all_dcconnect').AndReturn([])

        self.mox.ReplayAll()
        res = self.client.get(reverse(SERVICE_DETAIL_URL,
                                      kwargs={"group_id": obj_id}))
        self.assertRedirects(res, SERVICE_INDEX_URL)

    @test.create_stubs({api.neutron: ('network_list_for_tenant',
                                      'subnet_list')})
    def test_create(self):
        network_list = [{'id': 'network_id_00001', 'name': 'network_nameA'}]
        subnet_list = [{'id': 'subnet_id_00001', 'name': 'subnet_nameA',
                        'cidr': '10.70.70.0/24', 'ip_version': 4},
                       {'id': 'subnet_id_00002', 'name': 'subnet_nameB',
                        'cidr': '10.70.71.0/24', 'ip_version': 4},
                       {'id': 'subnet_id_00003', 'name': 'subnet_nameC',
                        'cidr': '10.70.72.0/24', 'ip_version': 4}]

        network_data = []
        subnet_data = []
        for data in network_list:
            network_data.append(Network(data))
        for data in subnet_list:
            subnet_data.append(Network(data))

        api.neutron.network_list_for_tenant(IsA(http.HttpRequest),
                                            IsA('str')).AndReturn(network_data)

        api.neutron.subnet_list(IsA(http.HttpRequest),
                                network_id='network_id_00001')\
            .AndReturn(subnet_data)

        self.mox.ReplayAll()

        res = self.client.get(SERVICE_CREATE_URL)
        self.assertNoFormErrors(res)
        self.assertTemplateUsed(res, 'project/service/create.html')

    @test.create_stubs({nal_api: ('get_services',)})
    @test.create_stubs({api.neutron: ('network_list_for_tenant',)})
    def test_create_network_error(self):
        api.neutron.network_list_for_tenant(IsA(http.HttpRequest),
                                            IsA('str')).AndRaise(OSError)

        service_data = []
        for data in fixture.SERVICE_DATA_LIST:
            service_data.append(
                Service(data,
                        SERVICE_RETURN_MAPPING['all_dcconnect']))

        nal_api.get_services(IsA(http.HttpRequest),
                             IsA('str'),
                             func_type='all_dcconnect').AndReturn(service_data)

        self.mox.ReplayAll()
        res = self.client.get(SERVICE_CREATE_URL)
        self.assertRedirects(res, SERVICE_INDEX_URL)

    @test.create_stubs({nal_api: ('get_services',)})
    @test.create_stubs({api.neutron: ('network_list_for_tenant',
                                      'subnet_list')})
    def test_create_subnet_error(self):
        network_list = [{'id': 'network_id_00001', 'name': 'network_nameA'}]

        network_data = []
        for data in network_list:
            network_data.append(Network(data))

        api.neutron.network_list_for_tenant(IsA(http.HttpRequest),
                                            IsA('str')).AndReturn(network_data)

        api.neutron.subnet_list(IsA(http.HttpRequest),
                                network_id='network_id_00001')\
            .AndRaise(OSError)

        service_data = []
        for data in fixture.SERVICE_DATA_LIST:
            service_data.append(
                Service(data,
                        SERVICE_RETURN_MAPPING['all_dcconnect']))

        nal_api.get_services(IsA(http.HttpRequest),
                             IsA('str'),
                             func_type='all_dcconnect').AndReturn(service_data)

        self.mox.ReplayAll()
        res = self.client.get(SERVICE_CREATE_URL)
        self.assertRedirects(res, SERVICE_INDEX_URL)

    @test.create_stubs({api.neutron: ('network_list_for_tenant',
                                      'subnet_list')})
    def test_create_no_subnets_error(self):
        network_list = [{'id': 'network_id_00001', 'name': 'network_nameA'},
                        {'id': 'network_id_00002', 'name': 'network_nameB'}]

        network_data = []
        subnet_data = []
        for data in network_list:
            network_data.append(Network(data))

        api.neutron.network_list_for_tenant(IsA(http.HttpRequest),
                                            IsA('str')).AndReturn(network_data)

        api.neutron.subnet_list(IsA(http.HttpRequest),
                                network_id='network_id_00001')\
            .AndReturn(subnet_data)
        api.neutron.subnet_list(IsA(http.HttpRequest),
                                network_id='network_id_00002')\
            .AndReturn(subnet_data)

        self.mox.ReplayAll()

        self.assertRaises(exceptions.NotAvailable,
                          self.client.get,
                          SERVICE_CREATE_URL)

    @test.create_stubs({api.neutron: ('network_list_for_tenant',
                                      'subnet_list',
                                      'subnet_get',
                                      'network_get')})
    @test.create_stubs({nal_api: ('get_services',
                                  'create_service')})
    def test_create_service(self):
        if NAL_CONSTRUCT_SERVICE_TYPE != 'normal':
            return 0

        network_list = [{'id': 'network_id_00001', 'name': 'network_nameA'}]
        subnet_list = [{'id': 'subnet_id_00001', 'name': 'subnet_nameA',
                        'cidr': '10.70.70.0/24', 'ip_version': 4},
                       {'id': 'subnet_id_00002', 'name': 'subnet_nameB',
                        'cidr': '10.70.71.0/24', 'ip_version': 4},
                       {'id': 'subnet_id_00003', 'name': 'subnet_nameC',
                        'cidr': '10.70.72.0/24', 'ip_version': 4}]

        network_data = []
        subnet_data = []
        for data in network_list:
            network_data.append(Network(data))
        for data in subnet_list:
            subnet_data.append(Network(data))

        api.neutron.network_list_for_tenant(IsA(http.HttpRequest),
                                            IsA('str')).AndReturn(network_data)

        api.neutron.subnet_list(IsA(http.HttpRequest),
                                network_id='network_id_00001')\
            .AndReturn(subnet_data)

        nal_api.get_services(IsA(http.HttpRequest),
                             IsA('str'),
                             func_type='all_dcconnect').AndReturn([])

        subnet_data = {'id': 'subnet_id_00001',
                       'network_id': 'network_id_00001',
                       'cidr': '10.70.70.0/24', 'ip_version': 4}
        api.neutron.subnet_get(IsA(http.HttpRequest),
                               'subnet_id_00001') \
            .AndReturn(Network(subnet_data))

        network_data = {'provider__network_type': 'i_network_typeA',
                        'id': 'network_id_00001',
                        'provider__segmentation_id': 'segment_id_00001',
                        'name': 'network_nameA',
                        'router__external': 'network_typeA'}
        api.neutron.network_get(IsA(http.HttpRequest),
                                'network_id_00001') \
            .AndReturn(Network(network_data))

        nal_api.create_service(IsA(http.HttpRequest),
                               IsA({})).AndReturn(True)

        self.mox.ReplayAll()

        formData = {'service_name': 'serviceA',
                    'service_type': '1',
                    'network': 'network_id_00001',
                    'fw_ip_address': '10.10.10.10',
                    'IaaS_subnet_id': 'subnet_id_00001'}
        res = self.client.post(SERVICE_CREATE_URL, formData)

        self.assertNoFormErrors(res)
        self.assertMessageCount(success=1)

    @test.create_stubs({api.neutron: ('network_list_for_tenant',
                                      'subnet_list',
                                      'subnet_get',
                                      'network_get')})
    @test.create_stubs({nal_api: ('get_services',
                                  'create_service')})
    def test_create_service_cisco(self):
        if NAL_CONSTRUCT_SERVICE_TYPE != 'normal':
            return 0

        network_list = [{'id': 'network_id_00001', 'name': 'network_nameA'}]
        subnet_list = [{'id': 'subnet_id_00001', 'name': 'subnet_nameA',
                        'cidr': '10.70.70.0/24', 'ip_version': 4},
                       {'id': 'subnet_id_00002', 'name': 'subnet_nameB',
                        'cidr': '10.70.71.0/24', 'ip_version': 4},
                       {'id': 'subnet_id_00003', 'name': 'subnet_nameC',
                        'cidr': '10.70.72.0/24', 'ip_version': 4}]

        network_data = []
        subnet_data = []
        for data in network_list:
            network_data.append(Network(data))
        for data in subnet_list:
            subnet_data.append(Network(data))

        api.neutron.network_list_for_tenant(IsA(http.HttpRequest),
                                            IsA('str')).AndReturn(network_data)

        api.neutron.subnet_list(IsA(http.HttpRequest),
                                network_id='network_id_00001')\
            .AndReturn(subnet_data)

        nal_api.get_services(IsA(http.HttpRequest),
                             IsA('str'),
                             func_type='all_dcconnect').AndReturn([])

        subnet_data = {'id': 'subnet_id_00001',
                       'network_id': 'network_id_00001',
                       'cidr': '10.70.70.0/24', 'ip_version': 4}
        api.neutron.subnet_get(IsA(http.HttpRequest),
                               'subnet_id_00001') \
            .AndReturn(Network(subnet_data))

        network_data = {'provider__network_type': 'i_network_typeA',
                        'id': 'network_id_00001',
                        'provider__segmentation_id': 'segment_id_00001',
                        'name': 'network_nameA',
                        'router__external': 'network_typeA'}
        api.neutron.network_get(IsA(http.HttpRequest),
                                'network_id_00001') \
            .AndReturn(Network(network_data))

        nal_api.create_service(IsA(http.HttpRequest),
                               IsA({})).AndReturn(True)

        self.mox.ReplayAll()

        formData = {'service_name': 'serviceB',
                    'service_type': '2',
                    'network': 'network_id_00001',
                    'fw_ip_address': '10.10.10.10',
                    'IaaS_subnet_id': 'subnet_id_00001',
                    'bandwidth': '1',
                    'dns_server_ip_address': '100.96.0.12',
                    'ntp_server_ip_address': '100.96.0.13'}
        res = self.client.post(SERVICE_CREATE_URL, formData)

        self.assertNoFormErrors(res)
        self.assertMessageCount(success=1)

    @test.create_stubs({api.neutron: ('network_list_for_tenant',
                                      'subnet_list')})
    def test_create_paramerter_error(self):
        if NAL_CONSTRUCT_SERVICE_TYPE != 'normal':
            return 0

        network_list = [{'id': 'network_id_00001', 'name': 'network_nameA'}]
        subnet_list = [{'id': 'subnet_id_00001', 'name': 'subnet_nameA',
                        'cidr': '10.70.70.0/24', 'ip_version': 4},
                       {'id': 'subnet_id_00002', 'name': 'subnet_nameB',
                        'cidr': '10.70.71.0/24', 'ip_version': 4},
                       {'id': 'subnet_id_00003', 'name': 'subnet_nameC',
                        'cidr': '10.70.72.0/24', 'ip_version': 4}]

        network_data = []
        subnet_data = []
        for data in network_list:
            network_data.append(Network(data))
        for data in subnet_list:
            subnet_data.append(Network(data))

        api.neutron.network_list_for_tenant(IsA(http.HttpRequest),
                                            IsA('str')).AndReturn(network_data)

        api.neutron.subnet_list(IsA(http.HttpRequest),
                                network_id='network_id_00001')\
            .AndReturn(subnet_data)

        self.mox.ReplayAll()

        formData = {'service_type': '2',
                    'network': 'network_id_00001',
                    'fw_ip_address': '10.10.10.10',
                    'IaaS_subnet_id': 'subnet_id_00001',
                    'bandwidth': '1'}
        res = self.client.post(SERVICE_CREATE_URL, formData)

        self.assertFormError(res, 'form', 'service_name',
                             ['This field is required.'])

    @test.create_stubs({api.neutron: ('network_list_for_tenant',
                                      'subnet_list')})
    @test.create_stubs({nal_api: ('get_services',)})
    def test_create_type_error(self):
        if NAL_CONSTRUCT_SERVICE_TYPE != 'normal':
            return 0

        network_list = [{'id': 'network_id_00001', 'name': 'network_nameA'}]
        subnet_list = [{'id': 'subnet_id_00001', 'name': 'subnet_nameA',
                        'cidr': '10.70.70.0/24', 'ip_version': 4},
                       {'id': 'subnet_id_00002', 'name': 'subnet_nameB',
                        'cidr': '10.70.71.0/24', 'ip_version': 4},
                       {'id': 'subnet_id_00003', 'name': 'subnet_nameC',
                        'cidr': '10.70.72.0/24', 'ip_version': 4}]

        network_data = []
        subnet_data = []
        for data in network_list:
            network_data.append(Network(data))
        for data in subnet_list:
            subnet_data.append(Network(data))

        api.neutron.network_list_for_tenant(IsA(http.HttpRequest),
                                            IsA('str')).AndReturn(network_data)

        api.neutron.subnet_list(IsA(http.HttpRequest),
                                network_id='network_id_00001')\
            .AndReturn(subnet_data)

        service_data = []
        for data in fixture.SERVICE_DATA_LIST:
            service_data.append(
                Service(data,
                        SERVICE_RETURN_MAPPING['all_dcconnect']))

        nal_api.get_services(IsA(http.HttpRequest),
                             IsA('str'),
                             func_type='all_dcconnect').AndReturn(service_data)

        self.mox.ReplayAll()

        formData = {'service_name': 'serviceA',
                    'service_type': '1',
                    'IaaS_subnet_id': 'subnet_id_00001',
                    'fw_ip_address': '10.10.10.10'}

        res = self.client.post(SERVICE_CREATE_URL, formData)

        self.assertTemplateUsed(res, 'project/service/create.html')

    @test.create_stubs({api.neutron: ('network_list_for_tenant',
                                      'subnet_list',
                                      'subnet_get',
                                      'network_get')})
    @test.create_stubs({nal_api: ('get_services',)})
    def test_create_network_detail_error(self):
        if NAL_CONSTRUCT_SERVICE_TYPE != 'normal':
            return 0

        network_list = [{'id': 'network_id_00001', 'name': 'network_nameA'}]
        subnet_list = [{'id': 'subnet_id_00001', 'name': 'subnet_nameA',
                        'cidr': '10.70.70.0/24', 'ip_version': 4},
                       {'id': 'subnet_id_00002', 'name': 'subnet_nameB',
                        'cidr': '10.70.71.0/24', 'ip_version': 4},
                       {'id': 'subnet_id_00003', 'name': 'subnet_nameC',
                        'cidr': '10.70.72.0/24', 'ip_version': 4}]

        network_data = []
        subnet_data = []
        for data in network_list:
            network_data.append(Network(data))
        for data in subnet_list:
            subnet_data.append(Network(data))

        api.neutron.network_list_for_tenant(IsA(http.HttpRequest),
                                            IsA('str')).AndReturn(network_data)

        api.neutron.subnet_list(IsA(http.HttpRequest),
                                network_id='network_id_00001')\
            .AndReturn(subnet_data)

        nal_api.get_services(IsA(http.HttpRequest),
                             IsA('str'),
                             func_type='all_dcconnect').AndReturn([])

        subnet_data = {'id': 'subnet_id_00001',
                       'network_id': 'network_id_00001',
                       'cidr': '10.70.70.0/24', 'ip_version': 4}
        api.neutron.subnet_get(IsA(http.HttpRequest),
                               'subnet_id_00001') \
            .AndReturn(Network(subnet_data))

        api.neutron.network_get(IsA(http.HttpRequest),
                                'network_id_00001').AndRaise(OSError)

        service_data = []
        for data in fixture.SERVICE_DATA_LIST:
            service_data.append(
                Service(data,
                        SERVICE_RETURN_MAPPING['all_dcconnect']))

        nal_api.get_services(IsA(http.HttpRequest),
                             IsA('str'),
                             func_type='all_dcconnect').AndReturn(service_data)

        self.mox.ReplayAll()

        formData = {'service_name': 'serviceA',
                    'service_type': '1',
                    'IaaS_subnet_id': 'subnet_id_00001',
                    'fw_ip_address': '10.10.10.10'}

        res = self.client.post(SERVICE_CREATE_URL,
                               formData)
        self.assertRedirects(res, SERVICE_INDEX_URL)

    @test.create_stubs({api.neutron: ('network_list_for_tenant',
                                      'subnet_list',
                                      'subnet_get',
                                      'network_get')})
    @test.create_stubs({nal_api: ('get_services',
                                  'create_service')})
    def test_create_api_error(self):
        if NAL_CONSTRUCT_SERVICE_TYPE != 'normal':
            return 0

        network_list = [{'id': 'network_id_00001', 'name': 'network_nameA'}]
        subnet_list = [{'id': 'subnet_id_00001', 'name': 'subnet_nameA',
                        'cidr': '10.70.70.0/24', 'ip_version': 4},
                       {'id': 'subnet_id_00002', 'name': 'subnet_nameB',
                        'cidr': '10.70.71.0/24', 'ip_version': 4},
                       {'id': 'subnet_id_00003', 'name': 'subnet_nameC',
                        'cidr': '10.70.72.0/24', 'ip_version': 4}]

        network_data = []
        subnet_data = []
        for data in network_list:
            network_data.append(Network(data))
        for data in subnet_list:
            subnet_data.append(Network(data))

        api.neutron.network_list_for_tenant(IsA(http.HttpRequest),
                                            IsA('str')).AndReturn(network_data)

        api.neutron.subnet_list(IsA(http.HttpRequest),
                                network_id='network_id_00001')\
            .AndReturn(subnet_data)

        nal_api.get_services(IsA(http.HttpRequest),
                             IsA('str'),
                             func_type='all_dcconnect').AndReturn([])

        subnet_data = {'id': 'subnet_id_00001',
                       'network_id': 'network_id_00001',
                       'cidr': '10.70.70.0/24', 'ip_version': 4}
        api.neutron.subnet_get(IsA(http.HttpRequest),
                               'subnet_id_00001') \
            .AndReturn(Network(subnet_data))

        network_data = {'provider__network_type': 'i_network_typeA',
                        'id': 'network_id_00001',
                        'provider__segmentation_id': 'segment_id_00001',
                        'name': 'network_nameA',
                        'router__external': 'network_typeA'}
        api.neutron.network_get(IsA(http.HttpRequest),
                                'network_id_00001') \
            .AndReturn(Network(network_data))

        nal_api.create_service(IsA(http.HttpRequest),
                               IsA({})).AndRaise(OSError)

        self.mox.ReplayAll()

        formData = {'service_name': 'serviceA',
                    'service_type': '1',
                    'IaaS_subnet_id': 'subnet_id_00001',
                    'fw_ip_address': '10.10.10.10'}

        self.assertRaises(OSError,
                          self.client.post,
                          SERVICE_CREATE_URL,
                          formData)

    @test.create_stubs({api.neutron: ('network_list_for_tenant',
                                      'subnet_list',
                                      'subnet_get',
                                      'network_get')})
    @test.create_stubs({nal_api: ('get_services',
                                  'create_service')})
    def test_create_api_error_handle(self):
        if NAL_CONSTRUCT_SERVICE_TYPE != 'normal':
            return 0

        network_list = [{'id': 'network_id_00001', 'name': 'network_nameA'}]
        subnet_list = [{'id': 'subnet_id_00001', 'name': 'subnet_nameA',
                        'cidr': '10.70.70.0/24', 'ip_version': 4},
                       {'id': 'subnet_id_00002', 'name': 'subnet_nameB',
                        'cidr': '10.70.71.0/24', 'ip_version': 4},
                       {'id': 'subnet_id_00003', 'name': 'subnet_nameC',
                        'cidr': '10.70.72.0/24', 'ip_version': 4}]

        network_data = []
        subnet_data = []
        for data in network_list:
            network_data.append(Network(data))
        for data in subnet_list:
            subnet_data.append(Network(data))

        api.neutron.network_list_for_tenant(IsA(http.HttpRequest),
                                            IsA('str')).AndReturn(network_data)

        api.neutron.subnet_list(IsA(http.HttpRequest),
                                network_id='network_id_00001')\
            .AndReturn(subnet_data)

        nal_api.get_services(IsA(http.HttpRequest),
                             IsA('str'),
                             func_type='all_dcconnect').AndReturn([])

        subnet_data = {'id': 'subnet_id_00001',
                       'network_id': 'network_id_00001',
                       'cidr': '10.70.70.0/24', 'ip_version': 4}
        api.neutron.subnet_get(IsA(http.HttpRequest),
                               'subnet_id_00001') \
            .AndReturn(Network(subnet_data))

        network_data = {'provider__network_type': 'i_network_typeA',
                        'id': 'network_id_00001',
                        'provider__segmentation_id': 'segment_id_00001',
                        'name': 'network_nameA',
                        'router__external': 'network_typeA'}
        api.neutron.network_get(IsA(http.HttpRequest),
                                'network_id_00001') \
            .AndReturn(Network(network_data))

        nal_api.create_service(IsA(http.HttpRequest),
                               IsA({})).AndRaise(exceptions.NotAvailable())

        self.mox.ReplayAll()

        formData = {'service_name': 'serviceA',
                    'service_type': '1',
                    'IaaS_subnet_id': 'subnet_id_00001',
                    'fw_ip_address': '10.10.10.10'}

        res = self.client.post(SERVICE_CREATE_URL, formData)

        self.assertTemplateUsed(res, 'project/service/create.html')

    @test.create_stubs({api.neutron: ('network_list_for_tenant',
                                      'subnet_list',
                                      'subnet_get',
                                      'network_get')})
    @test.create_stubs({nal_api: ('get_services',
                                  'create_service')})
    def test_create_service_tunneling_encrypted(self):
        if NAL_CONSTRUCT_SERVICE_TYPE != 'tunneling_encrypted':
            return 0

        network_list = [{'id': 'network_id_00001', 'name': 'network_nameA'}]
        subnet_list = [{'id': 'subnet_id_00001', 'name': 'subnet_nameA',
                        'cidr': '10.70.70.0/24', 'ip_version': 4},
                       {'id': 'subnet_id_00002', 'name': 'subnet_nameB',
                        'cidr': '10.70.71.0/24', 'ip_version': 4},
                       {'id': 'subnet_id_00003', 'name': 'subnet_nameC',
                        'cidr': '10.70.72.0/24', 'ip_version': 4}]

        network_data = []
        subnet_data = []
        for data in network_list:
            network_data.append(Network(data))
        for data in subnet_list:
            subnet_data.append(Network(data))

        api.neutron.network_list_for_tenant(IsA(http.HttpRequest),
                                            IsA('str')).AndReturn(network_data)

        api.neutron.subnet_list(IsA(http.HttpRequest),
                                network_id='network_id_00001')\
            .AndReturn(subnet_data)

        nal_api.get_services(IsA(http.HttpRequest),
                             IsA('str'),
                             func_type='all_dcconnect').AndReturn([])

        subnet_data = {'id': 'subnet_id_00001',
                       'network_id': 'network_id_00001',
                       'cidr': '10.70.70.0/24', 'ip_version': 4}
        api.neutron.subnet_get(IsA(http.HttpRequest),
                               'subnet_id_00001') \
            .AndReturn(Network(subnet_data))

        network_data = {'provider__network_type': 'i_network_typeA',
                        'id': 'network_id_00001',
                        'provider__segmentation_id': 'segment_id_00001',
                        'name': 'network_nameA',
                        'router__external': 'network_typeA'}
        api.neutron.network_get(IsA(http.HttpRequest),
                                'network_id_00001') \
            .AndReturn(Network(network_data))

        nal_api.create_service(IsA(http.HttpRequest),
                               IsA({})).AndReturn(True)

        self.mox.ReplayAll()

        formData = {'service_name': 'serviceB',
                    'service_type': '3',
                    'network': 'network_id_00001',
                    'fw_ip_address': '10.10.10.10',
                    'IaaS_subnet_id': 'subnet_id_00001',
                    'bandwidth': '1'}

        res = self.client.post(SERVICE_CREATE_URL, formData)

        self.assertNoFormErrors(res)
        self.assertMessageCount(success=1)

    @test.create_stubs({api.neutron: ('network_list_for_tenant',
                                      'subnet_list')})
    def test_create_tunneling_encrypted_paramerter_error(self):
        if NAL_CONSTRUCT_SERVICE_TYPE != 'tunneling_encrypted':
            return 0

        network_list = [{'id': 'network_id_00001', 'name': 'network_nameA'}]
        subnet_list = [{'id': 'subnet_id_00001', 'name': 'subnet_nameA',
                        'cidr': '10.70.70.0/24', 'ip_version': 4},
                       {'id': 'subnet_id_00002', 'name': 'subnet_nameB',
                        'cidr': '10.70.71.0/24', 'ip_version': 4},
                       {'id': 'subnet_id_00003', 'name': 'subnet_nameC',
                        'cidr': '10.70.72.0/24', 'ip_version': 4}]

        network_data = []
        subnet_data = []
        for data in network_list:
            network_data.append(Network(data))
        for data in subnet_list:
            subnet_data.append(Network(data))

        api.neutron.network_list_for_tenant(IsA(http.HttpRequest),
                                            IsA('str')).AndReturn(network_data)

        api.neutron.subnet_list(IsA(http.HttpRequest),
                                network_id='network_id_00001')\
            .AndReturn(subnet_data)

        self.mox.ReplayAll()

        formData = {'service_type': '3',
                    'network': 'network_id_00001',
                    'fw_ip_address': '10.10.10.10',
                    'IaaS_subnet_id': 'subnet_id_00001',
                    'bandwidth': '1'}
        res = self.client.post(SERVICE_CREATE_URL, formData)

        self.assertFormError(res, 'form', 'service_name',
                             ['This field is required.'])

    @test.create_stubs({api.neutron: ('network_list_for_tenant',
                                      'subnet_list',
                                      'subnet_get',
                                      'network_get')})
    @test.create_stubs({nal_api: ('get_services',)})
    def test_create_tunneling_encrypted_network_detail_error(self):
        if NAL_CONSTRUCT_SERVICE_TYPE != 'tunneling_encrypted':
            return 0

        network_list = [{'id': 'network_id_00001', 'name': 'network_nameA'}]
        subnet_list = [{'id': 'subnet_id_00001', 'name': 'subnet_nameA',
                        'cidr': '10.70.70.0/24', 'ip_version': 4},
                       {'id': 'subnet_id_00002', 'name': 'subnet_nameB',
                        'cidr': '10.70.71.0/24', 'ip_version': 4},
                       {'id': 'subnet_id_00003', 'name': 'subnet_nameC',
                        'cidr': '10.70.72.0/24', 'ip_version': 4}]

        network_data = []
        subnet_data = []
        for data in network_list:
            network_data.append(Network(data))
        for data in subnet_list:
            subnet_data.append(Network(data))

        api.neutron.network_list_for_tenant(IsA(http.HttpRequest),
                                            IsA('str')).AndReturn(network_data)

        api.neutron.subnet_list(IsA(http.HttpRequest),
                                network_id='network_id_00001')\
            .AndReturn(subnet_data)

        nal_api.get_services(IsA(http.HttpRequest),
                             IsA('str'),
                             func_type='all_dcconnect').AndReturn([])

        subnet_data = {'id': 'subnet_id_00001',
                       'network_id': 'network_id_00001',
                       'cidr': '10.70.70.0/24', 'ip_version': 4}
        api.neutron.subnet_get(IsA(http.HttpRequest),
                               'subnet_id_00001') \
            .AndReturn(Network(subnet_data))

        api.neutron.network_get(IsA(http.HttpRequest),
                                'network_id_00001').AndRaise(OSError)

        self.mox.ReplayAll()

        formData = {'service_name': 'serviceA',
                    'service_type': '3',
                    'IaaS_subnet_id': 'subnet_id_00001',
                    'fw_ip_address': '10.10.10.10',
                    'bandwidth': '1'}

        self.assertRaises(OSError,
                          self.client.post,
                          SERVICE_CREATE_URL,
                          formData)

    @test.create_stubs({api.neutron: ('network_list_for_tenant',
                                      'subnet_list',
                                      'subnet_get',
                                      'network_get')})
    @test.create_stubs({nal_api: ('get_services',
                                  'create_service')})
    def test_create_tunneling_encrypted_api_error(self):
        if NAL_CONSTRUCT_SERVICE_TYPE != 'tunneling_encrypted':
            return 0

        network_list = [{'id': 'network_id_00001', 'name': 'network_nameA'}]
        subnet_list = [{'id': 'subnet_id_00001', 'name': 'subnet_nameA',
                        'cidr': '10.70.70.0/24', 'ip_version': 4},
                       {'id': 'subnet_id_00002', 'name': 'subnet_nameB',
                        'cidr': '10.70.71.0/24', 'ip_version': 4},
                       {'id': 'subnet_id_00003', 'name': 'subnet_nameC',
                        'cidr': '10.70.72.0/24', 'ip_version': 4}]

        network_data = []
        subnet_data = []
        for data in network_list:
            network_data.append(Network(data))
        for data in subnet_list:
            subnet_data.append(Network(data))

        api.neutron.network_list_for_tenant(IsA(http.HttpRequest),
                                            IsA('str')).AndReturn(network_data)

        api.neutron.subnet_list(IsA(http.HttpRequest),
                                network_id='network_id_00001')\
            .AndReturn(subnet_data)

        nal_api.get_services(IsA(http.HttpRequest),
                             IsA('str'),
                             func_type='all_dcconnect').AndReturn([])

        subnet_data = {'id': 'subnet_id_00001',
                       'network_id': 'network_id_00001',
                       'cidr': '10.70.70.0/24', 'ip_version': 4}
        api.neutron.subnet_get(IsA(http.HttpRequest),
                               'subnet_id_00001') \
            .AndReturn(Network(subnet_data))

        network_data = {'provider__network_type': 'i_network_typeA',
                        'id': 'network_id_00001',
                        'provider__segmentation_id': 'segment_id_00001',
                        'name': 'network_nameA',
                        'router__external': 'network_typeA'}
        api.neutron.network_get(IsA(http.HttpRequest),
                                'network_id_00001') \
            .AndReturn(Network(network_data))

        nal_api.create_service(IsA(http.HttpRequest),
                               IsA({})).AndRaise(OSError)

        self.mox.ReplayAll()

        formData = {'service_name': 'serviceA',
                    'service_type': '3',
                    'IaaS_subnet_id': 'subnet_id_00001',
                    'fw_ip_address': '10.10.10.10',
                    'bandwidth': '1'}

        self.assertRaises(OSError,
                          self.client.post,
                          SERVICE_CREATE_URL,
                          formData)

    @test.create_stubs({api.neutron: ('network_list_for_tenant',
                                      'subnet_list',
                                      'subnet_get',
                                      'network_get')})
    @test.create_stubs({nal_api: ('get_services',
                                  'create_service')})
    def test_create_tunneling_encrypted_api_error_handle(self):
        if NAL_CONSTRUCT_SERVICE_TYPE != 'tunneling_encrypted':
            return 0

        network_list = [{'id': 'network_id_00001', 'name': 'network_nameA'}]
        subnet_list = [{'id': 'subnet_id_00001', 'name': 'subnet_nameA',
                        'cidr': '10.70.70.0/24', 'ip_version': 4},
                       {'id': 'subnet_id_00002', 'name': 'subnet_nameB',
                        'cidr': '10.70.71.0/24', 'ip_version': 4},
                       {'id': 'subnet_id_00003', 'name': 'subnet_nameC',
                        'cidr': '10.70.72.0/24', 'ip_version': 4}]

        network_data = []
        subnet_data = []
        for data in network_list:
            network_data.append(Network(data))
        for data in subnet_list:
            subnet_data.append(Network(data))

        api.neutron.network_list_for_tenant(IsA(http.HttpRequest),
                                            IsA('str')).AndReturn(network_data)

        api.neutron.subnet_list(IsA(http.HttpRequest),
                                network_id='network_id_00001')\
            .AndReturn(subnet_data)

        nal_api.get_services(IsA(http.HttpRequest),
                             IsA('str'),
                             func_type='all_dcconnect').AndReturn([])

        subnet_data = {'id': 'subnet_id_00001',
                       'network_id': 'network_id_00001',
                       'cidr': '10.70.70.0/24', 'ip_version': 4}
        api.neutron.subnet_get(IsA(http.HttpRequest),
                               'subnet_id_00001') \
            .AndReturn(Network(subnet_data))

        network_data = {'provider__network_type': 'i_network_typeA',
                        'id': 'network_id_00001',
                        'provider__segmentation_id': 'segment_id_00001',
                        'name': 'network_nameA',
                        'router__external': 'network_typeA'}
        api.neutron.network_get(IsA(http.HttpRequest),
                                'network_id_00001') \
            .AndReturn(Network(network_data))

        nal_api.create_service(IsA(http.HttpRequest),
                               IsA({})).AndRaise(exceptions.NotAvailable())

        self.mox.ReplayAll()

        formData = {'service_name': 'serviceA',
                    'service_type': '3',
                    'IaaS_subnet_id': 'subnet_id_00001',
                    'fw_ip_address': '10.10.10.10',
                    'bandwidth': '1'}

        res = self.client.post(SERVICE_CREATE_URL, formData)

        self.assertTemplateUsed(res, 'project/service/create.html')

    @test.create_stubs({api.neutron: ('network_list_for_tenant',
                                      'subnet_list',
                                      'subnet_get',
                                      'network_get')})
    @test.create_stubs({nal_api: ('get_services',
                                  'create_service')})
    def test_create_service_tunneling_unencrypted(self):
        if NAL_CONSTRUCT_SERVICE_TYPE != 'tunneling_unencrypted':
            return 0

        network_list = [{'id': 'network_id_00001', 'name': 'network_nameA'}]
        subnet_list = [{'id': 'subnet_id_00001', 'name': 'subnet_nameA',
                        'cidr': '10.70.70.0/24', 'ip_version': 4},
                       {'id': 'subnet_id_00002', 'name': 'subnet_nameB',
                        'cidr': '10.70.71.0/24', 'ip_version': 4},
                       {'id': 'subnet_id_00003', 'name': 'subnet_nameC',
                        'cidr': '10.70.72.0/24', 'ip_version': 4}]

        network_data = []
        subnet_data = []
        for data in network_list:
            network_data.append(Network(data))
        for data in subnet_list:
            subnet_data.append(Network(data))

        api.neutron.network_list_for_tenant(IsA(http.HttpRequest),
                                            IsA('str')).AndReturn(network_data)

        api.neutron.subnet_list(IsA(http.HttpRequest),
                                network_id='network_id_00001')\
            .AndReturn(subnet_data)

        nal_api.get_services(IsA(http.HttpRequest),
                             IsA('str'),
                             func_type='all_dcconnect').AndReturn([])

        subnet_data = {'id': 'subnet_id_00001',
                       'network_id': 'network_id_00001',
                       'cidr': '10.70.70.0/24', 'ip_version': 4}
        api.neutron.subnet_get(IsA(http.HttpRequest),
                               'subnet_id_00001') \
            .AndReturn(Network(subnet_data))

        network_data = {'provider__network_type': 'i_network_typeA',
                        'id': 'network_id_00001',
                        'provider__segmentation_id': 'segment_id_00001',
                        'name': 'network_nameA',
                        'router__external': 'network_typeA'}
        api.neutron.network_get(IsA(http.HttpRequest),
                                'network_id_00001') \
            .AndReturn(Network(network_data))

        nal_api.create_service(IsA(http.HttpRequest),
                               IsA({})).AndReturn(True)

        self.mox.ReplayAll()

        formData = {'service_name': 'serviceB',
                    'service_type': '4',
                    'network': 'network_id_00001',
                    'fw_ip_address': '10.10.10.10',
                    'IaaS_subnet_id': 'subnet_id_00001',
                    'bandwidth': '1'}

        res = self.client.post(SERVICE_CREATE_URL, formData)

        self.assertNoFormErrors(res)
        self.assertMessageCount(success=1)

    @test.create_stubs({api.neutron: ('network_list_for_tenant',
                                      'subnet_list')})
    def test_create_tunneling_unencrypted_paramerter_error(self):
        if NAL_CONSTRUCT_SERVICE_TYPE != 'tunneling_unencrypted':
            return 0

        network_list = [{'id': 'network_id_00001', 'name': 'network_nameA'}]
        subnet_list = [{'id': 'subnet_id_00001', 'name': 'subnet_nameA',
                        'cidr': '10.70.70.0/24', 'ip_version': 4},
                       {'id': 'subnet_id_00002', 'name': 'subnet_nameB',
                        'cidr': '10.70.71.0/24', 'ip_version': 4},
                       {'id': 'subnet_id_00003', 'name': 'subnet_nameC',
                        'cidr': '10.70.72.0/24', 'ip_version': 4}]

        network_data = []
        subnet_data = []
        for data in network_list:
            network_data.append(Network(data))
        for data in subnet_list:
            subnet_data.append(Network(data))

        api.neutron.network_list_for_tenant(IsA(http.HttpRequest),
                                            IsA('str')).AndReturn(network_data)

        api.neutron.subnet_list(IsA(http.HttpRequest),
                                network_id='network_id_00001')\
            .AndReturn(subnet_data)

        self.mox.ReplayAll()

        formData = {'service_type': '4',
                    'network': 'network_id_00001',
                    'fw_ip_address': '10.10.10.10',
                    'IaaS_subnet_id': 'subnet_id_00001',
                    'bandwidth': '1'}
        res = self.client.post(SERVICE_CREATE_URL, formData)

        self.assertFormError(res, 'form', 'service_name',
                             ['This field is required.'])

    @test.create_stubs({api.neutron: ('network_list_for_tenant',
                                      'subnet_list',
                                      'subnet_get',
                                      'network_get')})
    @test.create_stubs({nal_api: ('get_services',)})
    def test_create_tunneling_unencrypted_network_detail_error(self):
        if NAL_CONSTRUCT_SERVICE_TYPE != 'tunneling_unencrypted':
            return 0

        network_list = [{'id': 'network_id_00001', 'name': 'network_nameA'}]
        subnet_list = [{'id': 'subnet_id_00001', 'name': 'subnet_nameA',
                        'cidr': '10.70.70.0/24', 'ip_version': 4},
                       {'id': 'subnet_id_00002', 'name': 'subnet_nameB',
                        'cidr': '10.70.71.0/24', 'ip_version': 4},
                       {'id': 'subnet_id_00003', 'name': 'subnet_nameC',
                        'cidr': '10.70.72.0/24', 'ip_version': 4}]

        network_data = []
        subnet_data = []
        for data in network_list:
            network_data.append(Network(data))
        for data in subnet_list:
            subnet_data.append(Network(data))

        api.neutron.network_list_for_tenant(IsA(http.HttpRequest),
                                            IsA('str')).AndReturn(network_data)

        api.neutron.subnet_list(IsA(http.HttpRequest),
                                network_id='network_id_00001')\
            .AndReturn(subnet_data)

        nal_api.get_services(IsA(http.HttpRequest),
                             IsA('str'),
                             func_type='all_dcconnect').AndReturn([])

        subnet_data = {'id': 'subnet_id_00001',
                       'network_id': 'network_id_00001',
                       'cidr': '10.70.70.0/24', 'ip_version': 4}
        api.neutron.subnet_get(IsA(http.HttpRequest),
                               'subnet_id_00001') \
            .AndReturn(Network(subnet_data))

        api.neutron.network_get(IsA(http.HttpRequest),
                                'network_id_00001').AndRaise(OSError)

        self.mox.ReplayAll()

        formData = {'service_name': 'serviceA',
                    'service_type': '4',
                    'IaaS_subnet_id': 'subnet_id_00001',
                    'fw_ip_address': '10.10.10.10',
                    'bandwidth': '1'}

        self.assertRaises(OSError,
                          self.client.post,
                          SERVICE_CREATE_URL,
                          formData)

    @test.create_stubs({api.neutron: ('network_list_for_tenant',
                                      'subnet_list',
                                      'subnet_get',
                                      'network_get')})
    @test.create_stubs({nal_api: ('get_services',
                                  'create_service')})
    def test_create_tunneling_unencrypted_api_error(self):
        if NAL_CONSTRUCT_SERVICE_TYPE != 'tunneling_unencrypted':
            return 0

        network_list = [{'id': 'network_id_00001', 'name': 'network_nameA'}]
        subnet_list = [{'id': 'subnet_id_00001', 'name': 'subnet_nameA',
                        'cidr': '10.70.70.0/24', 'ip_version': 4},
                       {'id': 'subnet_id_00002', 'name': 'subnet_nameB',
                        'cidr': '10.70.71.0/24', 'ip_version': 4},
                       {'id': 'subnet_id_00003', 'name': 'subnet_nameC',
                        'cidr': '10.70.72.0/24', 'ip_version': 4}]

        network_data = []
        subnet_data = []
        for data in network_list:
            network_data.append(Network(data))
        for data in subnet_list:
            subnet_data.append(Network(data))

        api.neutron.network_list_for_tenant(IsA(http.HttpRequest),
                                            IsA('str')).AndReturn(network_data)

        api.neutron.subnet_list(IsA(http.HttpRequest),
                                network_id='network_id_00001')\
            .AndReturn(subnet_data)

        nal_api.get_services(IsA(http.HttpRequest),
                             IsA('str'),
                             func_type='all_dcconnect').AndReturn([])

        subnet_data = {'id': 'subnet_id_00001',
                       'network_id': 'network_id_00001',
                       'cidr': '10.70.70.0/24', 'ip_version': 4}
        api.neutron.subnet_get(IsA(http.HttpRequest),
                               'subnet_id_00001') \
            .AndReturn(Network(subnet_data))

        network_data = {'provider__network_type': 'i_network_typeA',
                        'id': 'network_id_00001',
                        'provider__segmentation_id': 'segment_id_00001',
                        'name': 'network_nameA',
                        'router__external': 'network_typeA'}
        api.neutron.network_get(IsA(http.HttpRequest),
                                'network_id_00001') \
            .AndReturn(Network(network_data))

        nal_api.create_service(IsA(http.HttpRequest),
                               IsA({})).AndRaise(OSError)

        self.mox.ReplayAll()

        formData = {'service_name': 'serviceA',
                    'service_type': '4',
                    'IaaS_subnet_id': 'subnet_id_00001',
                    'fw_ip_address': '10.10.10.10',
                    'bandwidth': '1'}

        self.assertRaises(OSError,
                          self.client.post,
                          SERVICE_CREATE_URL,
                          formData)

    @test.create_stubs({api.neutron: ('network_list_for_tenant',
                                      'subnet_list',
                                      'subnet_get',
                                      'network_get')})
    @test.create_stubs({nal_api: ('get_services',
                                  'create_service')})
    def test_create_tunneling_unencrypted_api_error_handle(self):
        if NAL_CONSTRUCT_SERVICE_TYPE != 'tunneling_unencrypted':
            return 0

        network_list = [{'id': 'network_id_00001', 'name': 'network_nameA'}]
        subnet_list = [{'id': 'subnet_id_00001', 'name': 'subnet_nameA',
                        'cidr': '10.70.70.0/24', 'ip_version': 4},
                       {'id': 'subnet_id_00002', 'name': 'subnet_nameB',
                        'cidr': '10.70.71.0/24', 'ip_version': 4},
                       {'id': 'subnet_id_00003', 'name': 'subnet_nameC',
                        'cidr': '10.70.72.0/24', 'ip_version': 4}]

        network_data = []
        subnet_data = []
        for data in network_list:
            network_data.append(Network(data))
        for data in subnet_list:
            subnet_data.append(Network(data))

        api.neutron.network_list_for_tenant(IsA(http.HttpRequest),
                                            IsA('str')).AndReturn(network_data)

        api.neutron.subnet_list(IsA(http.HttpRequest),
                                network_id='network_id_00001')\
            .AndReturn(subnet_data)

        nal_api.get_services(IsA(http.HttpRequest),
                             IsA('str'),
                             func_type='all_dcconnect').AndReturn([])

        subnet_data = {'id': 'subnet_id_00001',
                       'network_id': 'network_id_00001',
                       'cidr': '10.70.70.0/24', 'ip_version': 4}
        api.neutron.subnet_get(IsA(http.HttpRequest),
                               'subnet_id_00001') \
            .AndReturn(Network(subnet_data))

        network_data = {'provider__network_type': 'i_network_typeA',
                        'id': 'network_id_00001',
                        'provider__segmentation_id': 'segment_id_00001',
                        'name': 'network_nameA',
                        'router__external': 'network_typeA'}
        api.neutron.network_get(IsA(http.HttpRequest),
                                'network_id_00001') \
            .AndReturn(Network(network_data))

        nal_api.create_service(IsA(http.HttpRequest),
                               IsA({})).AndRaise(exceptions.NotAvailable())

        self.mox.ReplayAll()

        formData = {'service_name': 'serviceA',
                    'service_type': '4',
                    'IaaS_subnet_id': 'subnet_id_00001',
                    'fw_ip_address': '10.10.10.10',
                    'bandwidth': '1'}

        res = self.client.post(SERVICE_CREATE_URL, formData)

        self.assertTemplateUsed(res, 'project/service/create.html')

    @test.create_stubs({nal_api: ('get_services',)})
    @test.create_stubs({api.neutron: ('network_list_for_tenant',
                                      'subnet_list')})
    def test_update_member_create(self):
        network_list = [{'id': 'network_id_00001', 'name': 'network_nameA'}]
        subnet_list = [{'id': 'subnet_id_00001', 'name': 'subnet_nameA',
                        'cidr': '10.70.70.0/24', 'ip_version': 4},
                       {'id': 'subnet_id_00002', 'name': 'subnet_nameB',
                        'cidr': '10.70.71.0/24', 'ip_version': 4},
                       {'id': 'subnet_id_00003', 'name': 'subnet_nameC',
                        'cidr': '10.70.72.0/24', 'ip_version': 4}]

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

        network_data = []
        subnet_data = []
        for data in network_list:
            network_data.append(Network(data))
        for data in subnet_list:
            subnet_data.append(Network(data))

        api.neutron.network_list_for_tenant(IsA(http.HttpRequest),
                                            IsA('str')).AndReturn(network_data)

        api.neutron.subnet_list(IsA(http.HttpRequest),
                                network_id='network_id_00001')\
            .AndReturn(subnet_data)

        self.mox.ReplayAll()

        res = self.client.get(reverse(SERVICE_UPDATE_URL,
                                      args=(obj_id, 'member_create')))
        self.assertNoFormErrors(res)
        self.assertTemplateUsed(res, 'project/service/update.html')

    @test.create_stubs({nal_api: ('get_services',)})
    @test.create_stubs({api.neutron: ('network_list_for_tenant',
                                      'subnet_list')})
    def test_update_interface(self):
        network_list = [{'id': 'network_id_00001', 'name': 'network_nameA'}]
        subnet_list = [{'id': 'subnet_id_00001', 'name': 'subnet_nameA',
                        'cidr': '10.70.70.0/24', 'ip_version': 4},
                       {'id': 'subnet_id_00002', 'name': 'subnet_nameB',
                        'cidr': '10.70.71.0/24', 'ip_version': 4},
                       {'id': 'subnet_id_00003', 'name': 'subnet_nameC',
                        'cidr': '10.70.72.0/24', 'ip_version': 4}]

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

        network_data = []
        subnet_data = []
        for data in network_list:
            network_data.append(Network(data))
        for data in subnet_list:
            subnet_data.append(Network(data))

        api.neutron.network_list_for_tenant(IsA(http.HttpRequest),
                                            IsA('str')).AndReturn(network_data)

        api.neutron.subnet_list(IsA(http.HttpRequest),
                                network_id='network_id_00001')\
            .AndReturn(subnet_data)

        self.mox.ReplayAll()

        res = self.client.get(reverse(SERVICE_UPDATE_URL,
                                      args=(obj_id, 'interface')))
        self.assertNoFormErrors(res)
        self.assertTemplateUsed(res, 'project/service/update.html')

    @test.create_stubs({nal_api: ('get_services',)})
    def test_update_bandwidth(self):

        service_data = {}
        obj_id = '|'.join(
            ['dcconnect',
             str(fixture.SERVICE_DATA_CISCO['dc_group_info'][0]['group_id'])]
        )
        for key, value in SERVICE_RETURN_MAPPING['dcconnect'].iteritems():
            if isinstance(value, dict):
                service_data[key] = []
                for service_row in fixture.SERVICE_DATA_CISCO[key]:
                    service_data[key].append(Service(service_row, value))

        nal_api.get_services(
            IsA(http.HttpRequest),
            group_id=obj_id.split('|')[1],
            func_type=obj_id.split('|')[0]).AndReturn(service_data)

        self.mox.ReplayAll()

        res = self.client.get(reverse(SERVICE_UPDATE_URL,
                                      args=(obj_id, 'bandwidth')))
        self.assertNoFormErrors(res)
        self.assertTemplateUsed(res, 'project/service/update.html')

    @test.create_stubs({nal_api: ('get_services',)})
    @test.create_stubs({api.neutron: ('network_list_for_tenant',
                                      'subnet_list')})
    def test_update_setting(self):
        network_list = [{'id': 'network_id_00001', 'name': 'network_nameA'}]
        subnet_list = [{'id': 'subnet_id_00001', 'name': 'subnet_nameA',
                        'cidr': '10.70.70.0/24', 'ip_version': 4},
                       {'id': 'subnet_id_00002', 'name': 'subnet_nameB',
                        'cidr': '10.70.71.0/24', 'ip_version': 4},
                       {'id': 'subnet_id_00003', 'name': 'subnet_nameC',
                        'cidr': '10.70.72.0/24', 'ip_version': 4}]

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

        network_data = []
        subnet_data = []
        for data in network_list:
            network_data.append(Network(data))
        for data in subnet_list:
            subnet_data.append(Network(data))

        api.neutron.network_list_for_tenant(IsA(http.HttpRequest),
                                            IsA('str')).AndReturn(network_data)

        api.neutron.subnet_list(IsA(http.HttpRequest),
                                network_id='network_id_00001')\
            .AndReturn(subnet_data)

        self.mox.ReplayAll()

        res = self.client.get(reverse(SERVICE_UPDATE_URL,
                                      args=(obj_id, 'serviceSetting')))
        self.assertNoFormErrors(res)
        self.assertTemplateUsed(res, 'project/service/update.html')

    @test.create_stubs({nal_api: ('get_services',)})
    @test.create_stubs({api.neutron: ('network_get',
                                      'subnet_list')})
    def test_update_add_ipv6(self):
        network_detail = {'provider__network_type': 'i_network_typeB',
                          'id': 'network_id_00002',
                          'provider__segmentation_id': 'segment_id_00002',
                          'name': 'network_nameA',
                          'router__external': 'network_typeA'}
        subnet_list = [{'id': 'subnet_id_00001', 'name': 'subnet_nameA',
                        'cidr': '10.70.70.0/24', 'ip_version': 4},
                       {'id': 'subnet_id_v6_00001', 'name': 'subnet_nameAA',
                        'cidr': '1234:5678::abc0/124', 'ip_version': 6},
                       {'id': 'subnet_id_00003', 'name': 'subnet_nameC',
                        'cidr': '10.70.72.0/24', 'ip_version': 4}]

        service_data = {}
        obj_id = '|'.join(
            ['dcconnect',
             str(fixture.SERVICE_DATA_CISCO['dc_group_info'][0]['group_id']),
             'subnet_id_00002']
        )
        for key, value in SERVICE_RETURN_MAPPING['dcconnect'].iteritems():
            if isinstance(value, dict):
                service_data[key] = []
                for service_row in fixture.SERVICE_DATA_CISCO[key]:
                    service_data[key].append(Service(service_row, value))

        nal_api.get_services(
            IsA(http.HttpRequest),
            group_id=obj_id.split('|')[1],
            func_type=obj_id.split('|')[0]).AndReturn(service_data)

        network_data = Network(network_detail)
        subnet_data = []
        for data in subnet_list:
            subnet_data.append(Network(data))

        api.neutron.network_get(IsA(http.HttpRequest),
                                'network_id_00002').AndReturn(network_data)

        api.neutron.subnet_list(IsA(http.HttpRequest),
                                network_id='network_id_00002')\
            .AndReturn(subnet_data)

        self.mox.ReplayAll()

        res = self.client.get(reverse(SERVICE_UPDATE_URL,
                                      args=(obj_id, 'serviceIPv6Add')))
        self.assertNoFormErrors(res)
        self.assertTemplateUsed(res, 'project/service/update.html')

    @test.create_stubs({nal_api: ('get_services',)})
    @test.create_stubs({api.neutron: ('network_list_for_tenant',)})
    def test_update_network_error(self):
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

        api.neutron.network_list_for_tenant(IsA(http.HttpRequest),
                                            IsA('str')).AndRaise(OSError)

        service_data = []
        for data in fixture.SERVICE_DATA_LIST:
            service_data.append(
                Service(data,
                        SERVICE_RETURN_MAPPING['all_dcconnect']))

        nal_api.get_services(IsA(http.HttpRequest),
                             IsA('str'),
                             func_type='all_dcconnect').AndReturn(service_data)

        self.mox.ReplayAll()

        res = self.client.get(reverse(SERVICE_UPDATE_URL,
                                      args=(obj_id, 'interface')))
        self.assertRedirects(res, SERVICE_INDEX_URL)

    @test.create_stubs({nal_api: ('get_services',)})
    @test.create_stubs({api.neutron: ('network_list_for_tenant',
                                      'subnet_list')})
    def test_update_subnet_error(self):
        network_list = [{'id': 'network_id_00001', 'name': 'network_nameA'}]

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

        network_data = []
        for data in network_list:
            network_data.append(Network(data))

        api.neutron.network_list_for_tenant(IsA(http.HttpRequest),
                                            IsA('str')).AndReturn(network_data)

        api.neutron.subnet_list(IsA(http.HttpRequest),
                                network_id='network_id_00001')\
            .AndRaise(OSError)

        service_data = []
        for data in fixture.SERVICE_DATA_LIST:
            service_data.append(
                Service(data,
                        SERVICE_RETURN_MAPPING['all_dcconnect']))

        nal_api.get_services(IsA(http.HttpRequest),
                             IsA('str'),
                             func_type='all_dcconnect').AndReturn(service_data)

        self.mox.ReplayAll()
        res = self.client.get(reverse(SERVICE_UPDATE_URL,
                                      args=(obj_id, 'interface')))
        self.assertRedirects(res, SERVICE_INDEX_URL)

    @test.create_stubs({nal_api: ('get_services',)})
    @test.create_stubs({api.neutron: ('network_list_for_tenant',
                                      'subnet_list')})
    def test_update_member_create_no_subnets_error(self):
        network_list = [{'id': 'network_id_00001', 'name': 'network_nameA'},
                        {'id': 'network_id_00002', 'name': 'network_nameB'}]

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

        network_data = []
        subnet_data = []
        for data in network_list:
            network_data.append(Network(data))

        api.neutron.network_list_for_tenant(IsA(http.HttpRequest),
                                            IsA('str')).AndReturn(network_data)

        api.neutron.subnet_list(IsA(http.HttpRequest),
                                network_id='network_id_00001')\
            .AndReturn(subnet_data)

        api.neutron.subnet_list(IsA(http.HttpRequest),
                                network_id='network_id_00002')\
            .AndReturn(subnet_data)

        self.mox.ReplayAll()

        self.assertRaises(exceptions.NotAvailable,
                          self.client.get,
                          reverse(SERVICE_UPDATE_URL,
                                  args=(obj_id, 'member_create')))

    @test.create_stubs({nal_api: ('get_services',)})
    @test.create_stubs({api.neutron: ('network_list_for_tenant',
                                      'subnet_list')})
    def test_update_interface_no_subnets_error(self):
        network_list = [{'id': 'network_id_00001', 'name': 'network_nameA'},
                        {'id': 'network_id_00002', 'name': 'network_nameB'}]

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

        network_data = []
        subnet_data = []
        for data in network_list:
            network_data.append(Network(data))

        api.neutron.network_list_for_tenant(IsA(http.HttpRequest),
                                            IsA('str')).AndReturn(network_data)

        api.neutron.subnet_list(IsA(http.HttpRequest),
                                network_id='network_id_00001')\
            .AndReturn(subnet_data)

        api.neutron.subnet_list(IsA(http.HttpRequest),
                                network_id='network_id_00002')\
            .AndReturn(subnet_data)

        self.mox.ReplayAll()

        self.assertRaises(exceptions.NotAvailable,
                          self.client.get,
                          reverse(SERVICE_UPDATE_URL,
                                  args=(obj_id, 'interface')))

    @test.create_stubs({nal_api: ('get_services',)})
    @test.create_stubs({api.neutron: ('network_get',
                                      'subnet_list')})
    def test_update_add_ipv6_no_subnets_error(self):
        network_detail = {'provider__network_type': 'i_network_typeB',
                          'id': 'network_id_00002',
                          'provider__segmentation_id': 'segment_id_00002',
                          'name': 'network_nameB',
                          'router__external': 'network_typeB'}
        subnet_list = [{'id': 'subnet_id_00001', 'name': 'subnet_nameA',
                        'cidr': '10.70.70.0/24', 'ip_version': 4},
                       {'id': 'subnet_id_00002', 'name': 'subnet_nameB',
                        'cidr': '10.70.71.0/24', 'ip_version': 4},
                       {'id': 'subnet_id_00003', 'name': 'subnet_nameC',
                        'cidr': '10.70.72.0/24', 'ip_version': 4}]

        service_data = {}
        obj_id = '|'.join(
            ['dcconnect',
             str(fixture.SERVICE_DATA_CISCO['dc_group_info'][0]['group_id']),
             'subnet_id_00002']
        )
        for key, value in SERVICE_RETURN_MAPPING['dcconnect'].iteritems():
            if isinstance(value, dict):
                service_data[key] = []
                for service_row in fixture.SERVICE_DATA_CISCO[key]:
                    service_data[key].append(Service(service_row, value))

        nal_api.get_services(
            IsA(http.HttpRequest),
            group_id=obj_id.split('|')[1],
            func_type=obj_id.split('|')[0]).AndReturn(service_data)

        network_data = Network(network_detail)
        subnet_data = []
        for data in subnet_list:
            subnet_data.append(Network(data))

        api.neutron.network_get(IsA(http.HttpRequest),
                                'network_id_00002').AndReturn(network_data)

        api.neutron.subnet_list(IsA(http.HttpRequest),
                                network_id='network_id_00002')\
            .AndReturn(subnet_data)

        self.mox.ReplayAll()

        self.assertRaises(exceptions.NotAvailable,
                          self.client.get,
                          reverse(SERVICE_UPDATE_URL,
                                  args=(obj_id, 'serviceIPv6Add')))

    @test.create_stubs({api.neutron: ('network_list_for_tenant',
                                      'subnet_list',
                                      'subnet_get',
                                      'network_get')})
    @test.create_stubs({nal_api: ('get_services',
                                  'create_service')})
    def test_update_member_success(self):
        network_list = [{'id': 'network_id_00001', 'name': 'network_nameA'}]
        subnet_list = [{'id': 'subnet_id_00001', 'name': 'subnet_nameA',
                        'cidr': '10.70.70.0/24', 'ip_version': 4},
                       {'id': 'subnet_id_00002', 'name': 'subnet_nameB',
                        'cidr': '10.70.71.0/24', 'ip_version': 4},
                       {'id': 'subnet_id_00003', 'name': 'subnet_nameC',
                        'cidr': '10.70.72.0/24', 'ip_version': 4}]

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

        network_data = []
        subnet_data = []
        for data in network_list:
            network_data.append(Network(data))
        for data in subnet_list:
            subnet_data.append(Network(data))

        api.neutron.network_list_for_tenant(IsA(http.HttpRequest),
                                            IsA('str')).AndReturn(network_data)

        api.neutron.subnet_list(IsA(http.HttpRequest),
                                network_id='network_id_00001')\
            .AndReturn(subnet_data)

        subnet_data = {'id': 'subnet_id_00001',
                       'network_id': 'network_id_00001',
                       'cidr': '10.70.70.0/24', 'ip_version': 4}
        api.neutron.subnet_get(IsA(http.HttpRequest),
                               'subnet_id_00001') \
            .AndReturn(Network(subnet_data))

        network_data = {'provider__network_type': 'i_network_typeA',
                        'id': 'network_id_00001',
                        'provider__segmentation_id': 'segment_id_00001',
                        'name': 'network_nameA',
                        'router__external': 'network_typeA'}
        api.neutron.network_get(IsA(http.HttpRequest),
                                'network_id_00001') \
            .AndReturn(Network(network_data))

        nal_api.create_service(IsA(http.HttpRequest),
                               IsA({})).AndReturn(True)

        self.mox.ReplayAll()

        formData = {'group_id': obj_id.split('|')[1],
                    'func_type': obj_id.split('|')[0],
                    'update_type': 'member_create',
                    'fw_ip_address': '10.10.10.10',
                    'IaaS_subnet_id': 'subnet_id_00001',
                    'service_name': 'nameA',
                    'service_type': SERVICE_TYPE_MAPPING['1']}
        res = self.client.post(reverse(SERVICE_UPDATE_URL,
                                       args=(obj_id, 'member_create')),
                               formData)
        self.assertNoFormErrors(res)
        self.assertMessageCount(success=1)

    @test.create_stubs({api.neutron: ('network_list_for_tenant',
                                      'subnet_list',
                                      'subnet_get',
                                      'network_get')})
    @test.create_stubs({nal_api: ('get_services',
                                  'update_service')})
    def test_update_interface_success(self):
        network_list = [{'id': 'network_id_00001', 'name': 'network_nameA'}]
        subnet_list = [{'id': 'subnet_id_00001', 'name': 'subnet_nameA',
                        'cidr': '10.70.70.0/24', 'ip_version': 4},
                       {'id': 'subnet_id_00002', 'name': 'subnet_nameB',
                        'cidr': '10.70.71.0/24', 'ip_version': 4},
                       {'id': 'subnet_id_00003', 'name': 'subnet_nameC',
                        'cidr': '10.70.72.0/24', 'ip_version': 4}]

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

        network_data = []
        subnet_data = []
        for data in network_list:
            network_data.append(Network(data))
        for data in subnet_list:
            subnet_data.append(Network(data))

        api.neutron.network_list_for_tenant(IsA(http.HttpRequest),
                                            IsA('str')).AndReturn(network_data)

        api.neutron.subnet_list(IsA(http.HttpRequest),
                                network_id='network_id_00001')\
            .AndReturn(subnet_data)

        subnet_data = {'id': 'subnet_id_00001',
                       'network_id': 'network_id_00001',
                       'cidr': '10.70.70.0/24', 'ip_version': 4}
        api.neutron.subnet_get(IsA(http.HttpRequest),
                               'subnet_id_00001') \
            .AndReturn(Network(subnet_data))

        network_data = {'provider__network_type': 'i_network_typeA',
                        'id': 'network_id_00001',
                        'provider__segmentation_id': 'segment_id_00001',
                        'name': 'network_nameA',
                        'router__external': 'network_typeA'}
        api.neutron.network_get(IsA(http.HttpRequest),
                                'network_id_00001') \
            .AndReturn(Network(network_data))

        nal_api.update_service(IsA(http.HttpRequest),
                               IsA({})).AndReturn(True)

        self.mox.ReplayAll()

        formData = {'group_id': obj_id.split('|')[1],
                    'func_type': obj_id.split('|')[0],
                    'update_type': 'interface',
                    'IaaS_subnet_id': 'subnet_id_00001',
                    'service_name': 'nameA',
                    'service_type': SERVICE_TYPE_MAPPING['1']}
        res = self.client.post(reverse(SERVICE_UPDATE_URL,
                                       args=(obj_id, 'interface')),
                               formData)
        self.assertNoFormErrors(res)
        self.assertMessageCount(success=1)

    @test.create_stubs({nal_api: ('get_services',
                                  'update_service')})
    def test_update_bandwidth_success(self):

        service_data = {}
        obj_id = '|'.join(
            ['dcconnect',
             str(fixture.SERVICE_DATA_CISCO['dc_group_info'][0]['group_id'])]
        )
        for key, value in SERVICE_RETURN_MAPPING['dcconnect'].iteritems():
            if isinstance(value, dict):
                service_data[key] = []
                for service_row in fixture.SERVICE_DATA_CISCO[key]:
                    service_data[key].append(Service(service_row, value))

        nal_api.get_services(
            IsA(http.HttpRequest),
            group_id=obj_id.split('|')[1],
            func_type=obj_id.split('|')[0]).AndReturn(service_data)

        nal_api.update_service(IsA(http.HttpRequest),
                               IsA({})).AndReturn(True)

        self.mox.ReplayAll()

        formData = {'group_id': obj_id.split('|')[1],
                    'func_type': obj_id.split('|')[0],
                    'update_type': 'bandwidth',
                    'service_name': 'nameA',
                    'service_type': SERVICE_TYPE_MAPPING['2'],
                    'bandwidth': '3'}
        res = self.client.post(reverse(SERVICE_UPDATE_URL,
                                       args=(obj_id, 'bandwidth')),
                               formData)
        self.assertNoFormErrors(res)
        self.assertMessageCount(success=1)

    @test.create_stubs({api.neutron: ('network_list_for_tenant',
                                      'subnet_list')})
    @test.create_stubs({nal_api: ('get_services',
                                  'update_service')})
    def test_update_setting_success(self):
        network_list = [{'id': 'network_id_00001', 'name': 'network_nameA'}]
        subnet_list = [{'id': 'subnet_id_00001', 'name': 'subnet_nameA',
                        'cidr': '10.70.70.0/24', 'ip_version': 4},
                       {'id': 'subnet_id_00002', 'name': 'subnet_nameB',
                        'cidr': '10.70.71.0/24', 'ip_version': 4},
                       {'id': 'subnet_id_00003', 'name': 'subnet_nameC',
                        'cidr': '10.70.72.0/24', 'ip_version': 4}]

        service_data = {}
        obj_id = '|'.join(
            ['dcconnect',
             str(fixture.SERVICE_DATA_CISCO['dc_group_info'][0]['group_id'])]
        )
        for key, value in SERVICE_RETURN_MAPPING['dcconnect'].iteritems():
            if isinstance(value, dict):
                service_data[key] = []
                for service_row in fixture.SERVICE_DATA_CISCO[key]:
                    service_data[key].append(Service(service_row, value))

        nal_api.get_services(
            IsA(http.HttpRequest),
            group_id=obj_id.split('|')[1],
            func_type=obj_id.split('|')[0]).AndReturn(service_data)

        network_data = []
        subnet_data = []
        for data in network_list:
            network_data.append(Network(data))
        for data in subnet_list:
            subnet_data.append(Network(data))

        api.neutron.network_list_for_tenant(IsA(http.HttpRequest),
                                            IsA('str')).AndReturn(network_data)

        api.neutron.subnet_list(IsA(http.HttpRequest),
                                network_id='network_id_00001')\
            .AndReturn(subnet_data)

        nal_api.update_service(IsA(http.HttpRequest),
                               IsA({})).AndReturn(True)

        self.mox.ReplayAll()

        formData = {'group_id': obj_id.split('|')[1],
                    'func_type': obj_id.split('|')[0],
                    'update_type': 'serviceSetting',
                    'service_name': 'nameA',
                    'service_type': SERVICE_TYPE_MAPPING['2'],
                    'dns_server_ip_address': '10.58.79.161',
                    'ntp_server_ip_address': '10.58.79.161',
                    'ntp_server_interface': 'subnet_id_00002',
                    'snmp_server_ip_address': '10.58.79.161',
                    'snmp_server_interface': 'subnet_id_00002',
                    'syslog_server_ip_address': '10.58.79.161',
                    'syslog_server_interface': 'subnet_id_00002'}

        res = self.client.post(reverse(SERVICE_UPDATE_URL,
                                       args=(obj_id, 'serviceSetting')),
                               formData)
        self.assertNoFormErrors(res)
        self.assertMessageCount(success=1)

    @test.create_stubs({api.neutron: ('network_list_for_tenant',
                                      'subnet_list')})
    @test.create_stubs({nal_api: ('get_services',
                                  'update_service')})
    def test_update_setting_no_params(self):
        network_list = [{'id': 'network_id_00001', 'name': 'network_nameA'}]
        subnet_list = [{'id': 'subnet_id_00001', 'name': 'subnet_nameA',
                        'cidr': '10.70.70.0/24', 'ip_version': 4},
                       {'id': 'subnet_id_00002', 'name': 'subnet_nameB',
                        'cidr': '10.70.71.0/24', 'ip_version': 4},
                       {'id': 'subnet_id_00003', 'name': 'subnet_nameC',
                        'cidr': '10.70.72.0/24', 'ip_version': 4}]

        service_data = {}
        obj_id = '|'.join(
            ['dcconnect',
             str(fixture.SERVICE_DATA_CISCO['dc_group_info'][0]['group_id'])]
        )
        for key, value in SERVICE_RETURN_MAPPING['dcconnect'].iteritems():
            if isinstance(value, dict):
                service_data[key] = []
                for service_row in fixture.SERVICE_DATA_CISCO[key]:
                    service_data[key].append(Service(service_row, value))

        nal_api.get_services(
            IsA(http.HttpRequest),
            group_id=obj_id.split('|')[1],
            func_type=obj_id.split('|')[0]).AndReturn(service_data)

        network_data = []
        subnet_data = []
        for data in network_list:
            network_data.append(Network(data))
        for data in subnet_list:
            subnet_data.append(Network(data))

        api.neutron.network_list_for_tenant(IsA(http.HttpRequest),
                                            IsA('str')).AndReturn(network_data)

        api.neutron.subnet_list(IsA(http.HttpRequest),
                                network_id='network_id_00001')\
            .AndReturn(subnet_data)

        nal_api.update_service(IsA(http.HttpRequest),
                               IsA({})).AndReturn(True)

        self.mox.ReplayAll()

        formData = {'group_id': obj_id.split('|')[1],
                    'func_type': obj_id.split('|')[0],
                    'update_type': 'serviceSetting',
                    'service_name': 'nameA',
                    'service_type': SERVICE_TYPE_MAPPING['2']}

        res = self.client.post(reverse(SERVICE_UPDATE_URL,
                                       args=(obj_id, 'serviceSetting')),
                               formData)
        self.assertNoFormErrors(res)
        self.assertMessageCount(success=1)

    @test.create_stubs({api.neutron: ('subnet_list',
                                      'subnet_get',
                                      'network_get')})
    @test.create_stubs({nal_api: ('get_services',
                                  'update_service')})
    def test_update_add_ipv6_success(self):
        network_detail = {'provider__network_type': 'i_network_typeB',
                          'id': 'network_id_00002',
                          'provider__segmentation_id': 'segment_id_00002',
                          'name': 'network_nameB',
                          'router__external': 'network_typeB'}
        subnet_list = [{'id': 'subnet_id_00001', 'name': 'subnet_nameA',
                        'cidr': '10.70.70.0/24', 'ip_version': 4},
                       {'id': 'subnet_id_v6_00002', 'name': 'subnet_nameAA',
                        'cidr': '1234:5678::abc0/124', 'ip_version': 6},
                       {'id': 'subnet_id_00002', 'name': 'subnet_nameB',
                        'cidr': '10.70.72.0/24', 'ip_version': 4}]

        service_data = {}
        obj_id = '|'.join(
            ['dcconnect',
             str(fixture.SERVICE_DATA_CISCO['dc_group_info'][0]['group_id']),
             'subnet_id_00002']
        )
        for key, value in SERVICE_RETURN_MAPPING['dcconnect'].iteritems():
            if isinstance(value, dict):
                service_data[key] = []
                for service_row in fixture.SERVICE_DATA_CISCO[key]:
                    service_data[key].append(Service(service_row, value))

        nal_api.get_services(
            IsA(http.HttpRequest),
            group_id=obj_id.split('|')[1],
            func_type=obj_id.split('|')[0]).AndReturn(service_data)

        network_data = Network(network_detail)
        subnet_data = []
        for data in subnet_list:
            subnet_data.append(Network(data))

        api.neutron.network_get(IsA(http.HttpRequest),
                                'network_id_00002').AndReturn(network_data)

        api.neutron.subnet_list(IsA(http.HttpRequest),
                                network_id='network_id_00002')\
            .AndReturn(subnet_data)

        subnet_data = {'id': 'subnet_id_00002',
                       'network_id': 'network_id_00002',
                       'cidr': '10.70.72.0/24', 'ip_version': 4}
        api.neutron.subnet_get(IsA(http.HttpRequest),
                               'subnet_id_00002') \
            .AndReturn(Network(subnet_data))

        api.neutron.network_get(IsA(http.HttpRequest),
                                'network_id_00002').AndReturn(network_data)

        nal_api.update_service(IsA(http.HttpRequest),
                               IsA({})).AndReturn(True)

        self.mox.ReplayAll()

        formData = {'group_id': obj_id.split('|')[1],
                    'func_type': obj_id.split('|')[0],
                    'update_type': 'serviceIPv6Add',
                    'IaaS_subnet_id': 'subnet_id_00002',
                    'IaaS_subnet_id_v6': 'subnet_id_v6_00002',
                    'fw_ip_v6_address': '1234::5678',
                    'service_name': 'nameA',
                    'service_type': SERVICE_TYPE_MAPPING['1']}
        res = self.client.post(reverse(SERVICE_UPDATE_URL,
                                       args=(obj_id, 'serviceIPv6Add')),
                               formData)
        self.assertNoFormErrors(res)
        self.assertMessageCount(success=1)

    @test.create_stubs({api.neutron: ('network_list_for_tenant',
                                      'subnet_list')})
    @test.create_stubs({nal_api: ('get_services',)})
    def test_update_parameter_error(self):
        network_list = [{'id': 'network_id_00001', 'name': 'network_nameA'}]
        subnet_list = [{'id': 'subnet_id_00001', 'name': 'subnet_nameA',
                        'cidr': '10.70.70.0/24', 'ip_version': 4},
                       {'id': 'subnet_id_00002', 'name': 'subnet_nameB',
                        'cidr': '10.70.71.0/24', 'ip_version': 4},
                       {'id': 'subnet_id_00003', 'name': 'subnet_nameC',
                        'cidr': '10.70.72.0/24', 'ip_version': 4}]

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

        network_data = []
        subnet_data = []
        for data in network_list:
            network_data.append(Network(data))
        for data in subnet_list:
            subnet_data.append(Network(data))

        api.neutron.network_list_for_tenant(IsA(http.HttpRequest),
                                            IsA('str')).AndReturn(network_data)

        api.neutron.subnet_list(IsA(http.HttpRequest),
                                network_id='network_id_00001')\
            .AndReturn(subnet_data)

        self.mox.ReplayAll()

        formData = {'group_id': obj_id.split('|')[1],
                    'func_type': obj_id.split('|')[0],
                    'update_type': 'interface',
                    'IaaS_subnet_id': '',
                    'service_name': 'nameA',
                    'service_type': SERVICE_TYPE_MAPPING['1']}
        res = self.client.post(reverse(SERVICE_UPDATE_URL,
                                       args=(obj_id, 'interface')),
                               formData)

        self.assertFormError(res, 'form', 'IaaS_subnet_id',
                             ['This field is required.'])

    @test.create_stubs({api.neutron: ('network_list_for_tenant',
                                      'subnet_list',
                                      'subnet_get',
                                      'network_get')})
    @test.create_stubs({nal_api: ('get_services',)})
    def test_update_network_get_error(self):
        network_list = [{'id': 'network_id_00001', 'name': 'network_nameA'}]
        subnet_list = [{'id': 'subnet_id_00001', 'name': 'subnet_nameA',
                        'cidr': '10.70.70.0/24', 'ip_version': 4},
                       {'id': 'subnet_id_00002', 'name': 'subnet_nameB',
                        'cidr': '10.70.71.0/24', 'ip_version': 4},
                       {'id': 'subnet_id_00003', 'name': 'subnet_nameC',
                        'cidr': '10.70.72.0/24', 'ip_version': 4}]

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

        network_data = []
        subnet_data = []
        for data in network_list:
            network_data.append(Network(data))
        for data in subnet_list:
            subnet_data.append(Network(data))

        api.neutron.network_list_for_tenant(IsA(http.HttpRequest),
                                            IsA('str')).AndReturn(network_data)

        api.neutron.subnet_list(IsA(http.HttpRequest),
                                network_id='network_id_00001')\
            .AndReturn(subnet_data)

        subnet_data = {'id': 'subnet_id_00001',
                       'network_id': 'network_id_00001',
                       'cidr': '10.70.70.0/24', 'ip_version': 4}
        api.neutron.subnet_get(IsA(http.HttpRequest),
                               'subnet_id_00001') \
            .AndReturn(Network(subnet_data))

        api.neutron.network_get(IsA(http.HttpRequest),
                                'network_id_00001').AndRaise(OSError)

        service_data = []
        for data in fixture.SERVICE_DATA_LIST:
            service_data.append(
                Service(data,
                        SERVICE_RETURN_MAPPING['all_dcconnect']))

        nal_api.get_services(IsA(http.HttpRequest),
                             IsA('str'),
                             func_type='all_dcconnect').AndReturn(service_data)

        self.mox.ReplayAll()

        formData = {'group_id': obj_id.split('|')[1],
                    'func_type': obj_id.split('|')[0],
                    'update_type': 'interface',
                    'IaaS_subnet_id': 'subnet_id_00001',
                    'service_name': 'nameA',
                    'service_type': SERVICE_TYPE_MAPPING['1']}
        res = self.client.post(reverse(SERVICE_UPDATE_URL,
                                       args=(obj_id, 'interface')),
                               formData)

        self.assertRedirects(res, SERVICE_INDEX_URL)

    @test.create_stubs({api.neutron: ('network_list_for_tenant',
                                      'subnet_list',
                                      'subnet_get',
                                      'network_get')})
    @test.create_stubs({nal_api: ('get_services',
                                  'create_service')})
    def test_update_member_api_error(self):
        network_list = [{'id': 'network_id_00001', 'name': 'network_nameA'}]
        subnet_list = [{'id': 'subnet_id_00001', 'name': 'subnet_nameA',
                        'cidr': '10.70.70.0/24', 'ip_version': 4},
                       {'id': 'subnet_id_00002', 'name': 'subnet_nameB',
                        'cidr': '10.70.71.0/24', 'ip_version': 4},
                       {'id': 'subnet_id_00003', 'name': 'subnet_nameC',
                        'cidr': '10.70.72.0/24', 'ip_version': 4}]

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

        network_data = []
        subnet_data = []
        for data in network_list:
            network_data.append(Network(data))
        for data in subnet_list:
            subnet_data.append(Network(data))

        api.neutron.network_list_for_tenant(IsA(http.HttpRequest),
                                            IsA('str')).AndReturn(network_data)

        api.neutron.subnet_list(IsA(http.HttpRequest),
                                network_id='network_id_00001')\
            .AndReturn(subnet_data)

        subnet_data = {'id': 'subnet_id_00001',
                       'network_id': 'network_id_00001',
                       'cidr': '10.70.70.0/24', 'ip_version': 4}
        api.neutron.subnet_get(IsA(http.HttpRequest),
                               'subnet_id_00001') \
            .AndReturn(Network(subnet_data))

        network_data = {'provider__network_type': 'i_network_typeA',
                        'id': 'network_id_00001',
                        'provider__segmentation_id': 'segment_id_00001',
                        'name': 'network_nameA',
                        'router__external': 'network_typeA'}
        api.neutron.network_get(IsA(http.HttpRequest),
                                'network_id_00001') \
            .AndReturn(Network(network_data))

        nal_api.create_service(IsA(http.HttpRequest),
                               IsA({})).AndRaise(OSError)

        self.mox.ReplayAll()

        formData = {'group_id': obj_id.split('|')[1],
                    'func_type': obj_id.split('|')[0],
                    'update_type': 'member_create',
                    'IaaS_subnet_id': 'subnet_id_00001',
                    'fw_ip_address': '10.10.10.10',
                    'service_name': 'nameA',
                    'service_type': SERVICE_TYPE_MAPPING['1']}
        self.assertRaises(OSError,
                          self.client.post,
                          reverse(SERVICE_UPDATE_URL,
                                  args=(obj_id, 'member_create')),
                          formData)

    @test.create_stubs({api.neutron: ('network_list_for_tenant',
                                      'subnet_list',
                                      'subnet_get',
                                      'network_get')})
    @test.create_stubs({nal_api: ('get_services',
                                  'update_service')})
    def test_update_interface_api_error(self):
        network_list = [{'id': 'network_id_00001', 'name': 'network_nameA'}]
        subnet_list = [{'id': 'subnet_id_00001', 'name': 'subnet_nameA',
                        'cidr': '10.70.70.0/24', 'ip_version': 4},
                       {'id': 'subnet_id_00002', 'name': 'subnet_nameB',
                        'cidr': '10.70.71.0/24', 'ip_version': 4},
                       {'id': 'subnet_id_00003', 'name': 'subnet_nameC',
                        'cidr': '10.70.72.0/24', 'ip_version': 4}]

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

        network_data = []
        subnet_data = []
        for data in network_list:
            network_data.append(Network(data))
        for data in subnet_list:
            subnet_data.append(Network(data))

        api.neutron.network_list_for_tenant(IsA(http.HttpRequest),
                                            IsA('str')).AndReturn(network_data)

        api.neutron.subnet_list(IsA(http.HttpRequest),
                                network_id='network_id_00001')\
            .AndReturn(subnet_data)

        subnet_data = {'id': 'subnet_id_00001',
                       'network_id': 'network_id_00001',
                       'cidr': '10.70.70.0/24', 'ip_version': 4}
        api.neutron.subnet_get(IsA(http.HttpRequest),
                               'subnet_id_00001') \
            .AndReturn(Network(subnet_data))

        network_data = {'provider__network_type': 'i_network_typeA',
                        'id': 'network_id_00001',
                        'provider__segmentation_id': 'segment_id_00001',
                        'name': 'network_nameA',
                        'router__external': 'network_typeA'}
        api.neutron.network_get(IsA(http.HttpRequest),
                                'network_id_00001') \
            .AndReturn(Network(network_data))

        nal_api.update_service(IsA(http.HttpRequest),
                               IsA({})).AndRaise(OSError)
        self.mox.ReplayAll()

        formData = {'group_id': obj_id.split('|')[1],
                    'func_type': obj_id.split('|')[0],
                    'update_type': 'interface',
                    'IaaS_subnet_id': 'subnet_id_00001',
                    'service_name': 'nameA',
                    'service_type': SERVICE_TYPE_MAPPING['1']}
        self.assertRaises(OSError,
                          self.client.post,
                          reverse(SERVICE_UPDATE_URL,
                                  args=(obj_id, 'interface')),
                          formData)

    @test.create_stubs({nal_api: ('get_services',
                                  'update_service')})
    def test_update_bandwidth_api_error(self):

        service_data = {}
        obj_id = '|'.join(
            ['dcconnect',
             str(fixture.SERVICE_DATA_CISCO['dc_group_info'][0]['group_id'])]
        )
        for key, value in SERVICE_RETURN_MAPPING['dcconnect'].iteritems():
            if isinstance(value, dict):
                service_data[key] = []
                for service_row in fixture.SERVICE_DATA_CISCO[key]:
                    service_data[key].append(Service(service_row, value))

        nal_api.get_services(
            IsA(http.HttpRequest),
            group_id=obj_id.split('|')[1],
            func_type=obj_id.split('|')[0]).AndReturn(service_data)

        nal_api.update_service(IsA(http.HttpRequest),
                               IsA({})).AndRaise(OSError)
        self.mox.ReplayAll()

        formData = {'group_id': obj_id.split('|')[1],
                    'func_type': obj_id.split('|')[0],
                    'update_type': 'bandwidth',
                    'IaaS_subnet_id': 'subnet_id_00001',
                    'service_name': 'nameA',
                    'service_type': SERVICE_TYPE_MAPPING['2'],
                    'bandwidth': '3'}
        self.assertRaises(OSError,
                          self.client.post,
                          reverse(SERVICE_UPDATE_URL,
                                  args=(obj_id, 'bandwidth')),
                          formData)

    @test.create_stubs({api.neutron: ('network_list_for_tenant',
                                      'subnet_list')})
    @test.create_stubs({nal_api: ('get_services',
                                  'update_service')})
    def test_update_setting_api_error(self):
        network_list = [{'id': 'network_id_00001', 'name': 'network_nameA'}]
        subnet_list = [{'id': 'subnet_id_00001', 'name': 'subnet_nameA',
                        'cidr': '10.70.70.0/24', 'ip_version': 4},
                       {'id': 'subnet_id_00002', 'name': 'subnet_nameB',
                        'cidr': '10.70.71.0/24', 'ip_version': 4},
                       {'id': 'subnet_id_00003', 'name': 'subnet_nameC',
                        'cidr': '10.70.72.0/24', 'ip_version': 4}]

        service_data = {}
        obj_id = '|'.join(
            ['dcconnect',
             str(fixture.SERVICE_DATA_CISCO['dc_group_info'][0]['group_id'])]
        )
        for key, value in SERVICE_RETURN_MAPPING['dcconnect'].iteritems():
            if isinstance(value, dict):
                service_data[key] = []
                for service_row in fixture.SERVICE_DATA_CISCO[key]:
                    service_data[key].append(Service(service_row, value))

        nal_api.get_services(
            IsA(http.HttpRequest),
            group_id=obj_id.split('|')[1],
            func_type=obj_id.split('|')[0]).AndReturn(service_data)

        network_data = []
        subnet_data = []
        for data in network_list:
            network_data.append(Network(data))
        for data in subnet_list:
            subnet_data.append(Network(data))

        api.neutron.network_list_for_tenant(IsA(http.HttpRequest),
                                            IsA('str')).AndReturn(network_data)

        api.neutron.subnet_list(IsA(http.HttpRequest),
                                network_id='network_id_00001')\
            .AndReturn(subnet_data)

        nal_api.update_service(IsA(http.HttpRequest),
                               IsA({})).AndRaise(OSError)
        self.mox.ReplayAll()

        formData = {'group_id': obj_id.split('|')[1],
                    'func_type': obj_id.split('|')[0],
                    'update_type': 'serviceSetting',
                    'IaaS_subnet_id': 'subnet_id_00001',
                    'service_name': 'nameA',
                    'service_type': SERVICE_TYPE_MAPPING['2'],
                    'dns_server_ip_address': '10.58.79.161',
                    'ntp_server_ip_address': '10.58.79.161',
                    'ntp_server_interface': 'subnet_id_00002',
                    'snmp_server_ip_address': '10.58.79.161',
                    'snmp_server_interface': 'subnet_id_00002',
                    'syslog_server_ip_address': '10.58.79.161',
                    'syslog_server_interface': 'subnet_id_00002'}
        self.assertRaises(OSError,
                          self.client.post,
                          reverse(SERVICE_UPDATE_URL,
                                  args=(obj_id, 'serviceSetting')),
                          formData)

    @test.create_stubs({api.neutron: ('network_list_for_tenant',
                                      'subnet_list',
                                      'subnet_get',
                                      'network_get')})
    @test.create_stubs({nal_api: ('get_services',
                                  'create_service')})
    def test_update_member_api_error_handle(self):
        network_list = [{'id': 'network_id_00001', 'name': 'network_nameA'}]
        subnet_list = [{'id': 'subnet_id_00001', 'name': 'subnet_nameA',
                        'cidr': '10.70.70.0/24', 'ip_version': 4},
                       {'id': 'subnet_id_00002', 'name': 'subnet_nameB',
                        'cidr': '10.70.71.0/24', 'ip_version': 4},
                       {'id': 'subnet_id_00003', 'name': 'subnet_nameC',
                        'cidr': '10.70.72.0/24', 'ip_version': 4}]

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

        network_data = []
        subnet_data = []
        for data in network_list:
            network_data.append(Network(data))
        for data in subnet_list:
            subnet_data.append(Network(data))

        api.neutron.network_list_for_tenant(IsA(http.HttpRequest),
                                            IsA('str')).AndReturn(network_data)

        api.neutron.subnet_list(IsA(http.HttpRequest),
                                network_id='network_id_00001')\
            .AndReturn(subnet_data)

        subnet_data = {'id': 'subnet_id_00001',
                       'network_id': 'network_id_00001',
                       'cidr': '10.70.70.0/24', 'ip_version': 4}
        api.neutron.subnet_get(IsA(http.HttpRequest),
                               'subnet_id_00001') \
            .AndReturn(Network(subnet_data))

        network_data = {'provider__network_type': 'i_network_typeA',
                        'id': 'network_id_00001',
                        'provider__segmentation_id': 'segment_id_00001',
                        'name': 'network_nameA',
                        'router__external': 'network_typeA'}
        api.neutron.network_get(IsA(http.HttpRequest),
                                'network_id_00001') \
            .AndReturn(Network(network_data))

        nal_api.create_service(IsA(http.HttpRequest),
                               IsA({})).AndRaise(exceptions.NotAvailable())

        self.mox.ReplayAll()

        formData = {'group_id': obj_id.split('|')[1],
                    'func_type': obj_id.split('|')[0],
                    'update_type': 'member_create',
                    'IaaS_subnet_id': 'subnet_id_00001',
                    'fw_ip_address': '10.10.10.10',
                    'service_name': 'nameA',
                    'service_type': SERVICE_TYPE_MAPPING['1']}
        res = self.client.post(reverse(SERVICE_UPDATE_URL,
                                       args=(obj_id, 'member_create')),
                               formData)

        self.assertTemplateUsed(res, 'project/service/update.html')

    @test.create_stubs({api.neutron: ('network_list_for_tenant',
                                      'subnet_list',
                                      'subnet_get',
                                      'network_get')})
    @test.create_stubs({nal_api: ('get_services',
                                  'update_service')})
    def test_update_interface_error(self):
        network_list = [{'id': 'network_id_00001', 'name': 'network_nameA'}]
        subnet_list = [{'id': 'subnet_id_00001', 'name': 'subnet_nameA',
                        'cidr': '10.70.70.0/24', 'ip_version': 4},
                       {'id': 'subnet_id_00002', 'name': 'subnet_nameB',
                        'cidr': '10.70.71.0/24', 'ip_version': 4},
                       {'id': 'subnet_id_00003', 'name': 'subnet_nameC',
                        'cidr': '10.70.72.0/24', 'ip_version': 4}]

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

        network_data = []
        subnet_data = []
        for data in network_list:
            network_data.append(Network(data))
        for data in subnet_list:
            subnet_data.append(Network(data))

        api.neutron.network_list_for_tenant(IsA(http.HttpRequest),
                                            IsA('str')).AndReturn(network_data)

        api.neutron.subnet_list(IsA(http.HttpRequest),
                                network_id='network_id_00001')\
            .AndReturn(subnet_data)

        subnet_data = {'id': 'subnet_id_00001',
                       'network_id': 'network_id_00001',
                       'cidr': '10.70.70.0/24', 'ip_version': 4}
        api.neutron.subnet_get(IsA(http.HttpRequest),
                               'subnet_id_00001') \
            .AndReturn(Network(subnet_data))

        network_data = {'provider__network_type': 'i_network_typeA',
                        'id': 'network_id_00001',
                        'provider__segmentation_id': 'segment_id_00001',
                        'name': 'network_nameA',
                        'router__external': 'network_typeA'}
        api.neutron.network_get(IsA(http.HttpRequest),
                                'network_id_00001') \
            .AndReturn(Network(network_data))

        nal_api.update_service(IsA(http.HttpRequest),
                               IsA({})).AndRaise(exceptions.NotAvailable())

        self.mox.ReplayAll()

        formData = {'group_id': obj_id.split('|')[1],
                    'func_type': obj_id.split('|')[0],
                    'update_type': 'interface',
                    'IaaS_subnet_id': 'subnet_id_00001',
                    'service_name': 'nameA',
                    'service_type': SERVICE_TYPE_MAPPING['1']}
        res = self.client.post(reverse(SERVICE_UPDATE_URL,
                                       args=(obj_id, 'interface')),
                               formData)

        self.assertTemplateUsed(res, 'project/service/update.html')

    @test.create_stubs({nal_api: ('get_services',
                                  'delete_service')})
    def test_delete(self):
        service_data = []
        for data in fixture.SERVICE_DATA_LIST:
            service_data.append(
                Service(data,
                        SERVICE_RETURN_MAPPING['all_dcconnect']))

        nal_api.get_services(IsA(http.HttpRequest),
                             IsA('str'),
                             func_type='all_dcconnect').AndReturn(service_data)

        service_data = {}
        for key, value in SERVICE_RETURN_MAPPING['dcconnect'].iteritems():
            if isinstance(value, dict):
                service_data[key] = []
                for service_row in fixture.SERVICE_DATA_DEFAULT[key]:
                    service_data[key].append(Service(service_row, value))

        nal_api.get_services(
            IsA(http.HttpRequest),
            group_id=str(fixture.SERVICE_DATA_LIST[0]['group_id']),
            func_type='dcconnect').AndReturn(service_data)

        params = {'function_type': 'dcconnect',
                  'group_id': fixture.SERVICE_DATA_LIST[0]['group_id'],
                  'service_type': fixture.SERVICE_DATA_LIST[0]['group_type'],
                  'apl_type': '1',
                  'type': '3',
                  'device_type': '1'}

        nal_api.delete_service(IsA(http.HttpRequest),
                               params).AndReturn(True)

        self.mox.ReplayAll()

        obj_id = '|'.join(['dcconnect',
                           str(fixture.SERVICE_DATA_LIST[0]['group_id'])])
        formData = {'action': 'service__delete__%s' % obj_id}
        res = self.client.post(SERVICE_INDEX_URL, formData)

        self.assertRedirectsNoFollow(res, SERVICE_INDEX_URL)

    @test.create_stubs({nal_api: ('get_services',
                                  'delete_service')})
    def test_delete_api_error(self):
        service_data = []
        for data in fixture.SERVICE_DATA_LIST:
            service_data.append(
                Service(data,
                        SERVICE_RETURN_MAPPING['all_dcconnect']))

        nal_api.get_services(IsA(http.HttpRequest),
                             IsA('str'),
                             func_type='all_dcconnect').\
            AndReturn(service_data)

        service_data = {}
        for key, value in SERVICE_RETURN_MAPPING['dcconnect'].iteritems():
            if isinstance(value, dict):
                service_data[key] = []
                for service_row in fixture.SERVICE_DATA_DEFAULT[key]:
                    service_data[key].append(Service(service_row, value))

        nal_api.get_services(
            IsA(http.HttpRequest),
            group_id=str(fixture.SERVICE_DATA_LIST[0]['group_id']),
            func_type='dcconnect').AndReturn(service_data)

        params = {'function_type': 'dcconnect',
                  'group_id': fixture.SERVICE_DATA_LIST[0]['group_id'],
                  'service_type': fixture.SERVICE_DATA_LIST[0]['group_type'],
                  'apl_type': '1',
                  'type': '3',
                  'device_type': '1'}

        nal_api.delete_service(IsA(http.HttpRequest),
                               params).AndRaise(OSError)

        service_data = []
        for data in fixture.SERVICE_DATA_LIST:
            service_data.append(
                Service(data,
                        SERVICE_RETURN_MAPPING['all_dcconnect']))

        nal_api.get_services(IsA(http.HttpRequest),
                             IsA('str'),
                             func_type='all_dcconnect').AndReturn(service_data)

        self.mox.ReplayAll()

        obj_id = '|'.join(['dcconnect',
                           str(fixture.SERVICE_DATA_LIST[0]['group_id'])])
        formData = {'action': 'service__delete__%s' % obj_id}

        res = self.client.post(SERVICE_INDEX_URL, formData)
        self.assertRedirects(res, SERVICE_INDEX_URL)

    @test.create_stubs({nal_api: ('get_services',
                                  'delete_service')})
    def test_delete_api_error_handle(self):
        service_list = []
        for data in fixture.SERVICE_DATA_LIST:
            service_list.append(
                Service(data,
                        SERVICE_RETURN_MAPPING['all_dcconnect']))

        nal_api.get_services(IsA(http.HttpRequest),
                             IsA('str'),
                             func_type='all_dcconnect').AndReturn(service_list)

        service_data = {}
        for key, value in SERVICE_RETURN_MAPPING['dcconnect'].iteritems():
            if isinstance(value, dict):
                service_data[key] = []
                for service_row in fixture.SERVICE_DATA_DEFAULT[key]:
                    service_data[key].append(Service(service_row, value))

        nal_api.get_services(
            IsA(http.HttpRequest),
            group_id=str(fixture.SERVICE_DATA_LIST[0]['group_id']),
            func_type='dcconnect').AndReturn(service_data)

        params = {'function_type': 'dcconnect',
                  'group_id': fixture.SERVICE_DATA_LIST[0]['group_id'],
                  'service_type': fixture.SERVICE_DATA_LIST[0]['group_type'],
                  'apl_type': '1',
                  'type': '3',
                  'device_type': '1'}

        nal_api.delete_service(IsA(http.HttpRequest),
                               params).AndRaise(exceptions.NotAvailable())

        nal_api.get_services(IsA(http.HttpRequest),
                             IsA('str'),
                             func_type='all_dcconnect').AndReturn(service_list)

        self.mox.ReplayAll()

        obj_id = '|'.join(['dcconnect',
                           str(fixture.SERVICE_DATA_LIST[0]['group_id'])])
        formData = {'action': 'service__delete__%s' % obj_id}
        res = self.client.post(SERVICE_INDEX_URL, formData)

        self.assertRedirects(res, SERVICE_INDEX_URL)

    @test.create_stubs({nal_api: ('get_services',
                                  'delete_service')})
    def test_member_delete(self):
        service_data = {}
        obj_id = '|'.join(
            ['dcconnect',
             str(fixture.SERVICE_DATA_LIST[0]['group_id'])]
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

        nal_api.get_services(
            IsA(http.HttpRequest),
            group_id=obj_id.split('|')[1],
            func_type=obj_id.split('|')[0]).AndReturn(service_data)

        params = {'function_type': 'dcconnect',
                  'group_id': fixture.SERVICE_DATA_LIST[0]['group_id'],
                  'service_type': fixture.SERVICE_DATA_LIST[0]['group_type'],
                  'apl_type': '1',
                  'type': '3',
                  'device_type': '1'}

        nal_api.delete_service(IsA(http.HttpRequest),
                               params).AndReturn(True)

        self.mox.ReplayAll()

        member_obj_id = \
            str(fixture.SERVICE_DATA_DEFAULT['dc_info'][0]['dc_id'])
        formData = {'action': 'member__delete__%s' % member_obj_id}
        res = self.client.post(reverse(SERVICE_DETAIL_URL,
                                       kwargs={"group_id": obj_id}),
                               formData)

        self.assertRedirectsNoFollow(res, reverse(SERVICE_DETAIL_URL,
                                                  kwargs={"group_id": obj_id}))

    @test.create_stubs({nal_api: ('get_services',
                                  'delete_service')})
    def test_member_delete_api_error(self):
        service_data = {}
        obj_id = '|'.join(
            ['dcconnect',
             str(fixture.SERVICE_DATA_LIST[0]['group_id'])]
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

        nal_api.get_services(
            IsA(http.HttpRequest),
            group_id=obj_id.split('|')[1],
            func_type=obj_id.split('|')[0]).AndReturn(service_data)

        params = {'function_type': 'dcconnect',
                  'group_id': fixture.SERVICE_DATA_LIST[0]['group_id'],
                  'service_type': fixture.SERVICE_DATA_LIST[0]['group_type'],
                  'apl_type': '1',
                  'type': '3',
                  'device_type': '1'}

        nal_api.delete_service(IsA(http.HttpRequest),
                               params).AndRaise(OSError)

        self.mox.ReplayAll()

        member_obj_id = \
            str(fixture.SERVICE_DATA_DEFAULT['dc_info'][0]['dc_id'])
        formData = {'action': 'member__delete__%s' % member_obj_id}

        res = self.client.post(reverse(SERVICE_DETAIL_URL,
                                       kwargs={"group_id": obj_id}),
                               formData)
        self.assertRedirectsNoFollow(res, reverse(SERVICE_DETAIL_URL,
                                                  kwargs={"group_id": obj_id}))

    @test.create_stubs({nal_api: ('get_services',
                                  'delete_service')})
    def test_member_delete_api_error_handle(self):
        service_data = {}
        obj_id = '|'.join(
            ['dcconnect',
             str(fixture.SERVICE_DATA_LIST[0]['group_id'])]
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

        nal_api.get_services(
            IsA(http.HttpRequest),
            group_id=obj_id.split('|')[1],
            func_type=obj_id.split('|')[0]).AndReturn(service_data)

        params = {'function_type': 'dcconnect',
                  'group_id': fixture.SERVICE_DATA_LIST[0]['group_id'],
                  'service_type': fixture.SERVICE_DATA_LIST[0]['group_type'],
                  'apl_type': '1',
                  'type': '3',
                  'device_type': '1'}

        nal_api.delete_service(IsA(http.HttpRequest),
                               params).AndRaise(exceptions.NotAvailable())

        self.mox.ReplayAll()

        member_obj_id = \
            str(fixture.SERVICE_DATA_DEFAULT['dc_info'][0]['dc_id'])
        formData = {'action': 'member__delete__%s' % member_obj_id}
        res = self.client.post(reverse(SERVICE_DETAIL_URL,
                                       kwargs={"group_id": obj_id}),
                               formData)
        self.assertRedirectsNoFollow(res, reverse(SERVICE_DETAIL_URL,
                                                  kwargs={"group_id": obj_id}))

    @test.create_stubs({nal_api: ('get_services',)})
    def test_row_update(self):

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

        service_data = []
        for data in fixture.SERVICE_DATA_LIST:
            service_data.append(
                Service(data,
                        SERVICE_RETURN_MAPPING['all_dcconnect']))

        nal_api.get_services(IsA(http.HttpRequest),
                             IsA('str'),
                             func_type='all_dcconnect').AndReturn(service_data)

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


class Network(object):
    """Network class"""
    def __init__(self, network_data):

        for key, value in network_data.iteritems():
                self.__dict__[key] = value
