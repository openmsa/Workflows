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
from nec_portal.dashboards.project.node import fixture
from nec_portal.dashboards.project.node import panel  # noqa
from nec_portal.local import nal_portal_settings

from openstack_dashboard import api
from openstack_dashboard.test import helpers as test


NODE_INDEX_URL = reverse('horizon:project:node:index')
NODE_CREATE_URL = reverse('horizon:project:node:create')
NODE_DETAIL_URL = 'horizon:project:node:detail'
NODE_UPDATE_URL = 'horizon:project:node:update'

NODE_RETURN_MAPPING = getattr(nal_portal_settings, 'NODE_RETURN_MAPPING', None)
NODE_DETAIL_DISPLAY_COLUMNS = \
    getattr(nal_portal_settings, 'PROJECT_NODE_DETAIL_DISPLAY_COLUMNS', None)

NETWORK_LIST_FOR_TENANT_RETURN = \
    [{'id': 'IaaS_network_id-xxxx1', 'name': 'network_nameA'},
     {'id': 'IaaS_network_id-xxxx2', 'name': 'network_nameB'}]


class NodeViewTests(test.TestCase):

    @test.create_stubs({nal_api: ('get_nodes',)})
    def test_index_multi_data(self):

        node_data = []
        for data in fixture.NODE_DATA_LIST:
            node_data.append(Node(data,
                                  NODE_RETURN_MAPPING['all_node']['Virtual']))

        nal_api.get_nodes(IsA(http.HttpRequest),
                          IsA('str'),
                          func_type='all_node').AndReturn(node_data)

        self.mox.ReplayAll()
        res = self.client.get(NODE_INDEX_URL)
        self.assertNoFormErrors(res)
        self.assertTemplateUsed(res, 'project/node/index.html')
        self.assertItemsEqual(res.context['table'].data, node_data)

    @test.create_stubs({nal_api: ('get_nodes',)})
    def test_index_no_data(self):

        node_data = []

        nal_api.get_nodes(IsA(http.HttpRequest),
                          IsA('str'),
                          func_type='all_node').AndReturn(node_data)

        self.mox.ReplayAll()
        res = self.client.get(NODE_INDEX_URL)
        self.assertNoFormErrors(res)
        self.assertTemplateUsed(res, 'project/node/index.html')
        self.assertItemsEqual(res.context['table'].data, [])

    @test.create_stubs({nal_api: ('get_nodes',)})
    def test_index_api_error(self):

        nal_api.get_nodes(IsA(http.HttpRequest),
                          IsA('str'),
                          func_type='all_node').AndRaise(OSError)

        self.mox.ReplayAll()
        res = self.client.get(NODE_INDEX_URL)

        self.assertTemplateUsed(res, 'project/node/index.html')
        self.assertItemsEqual(res.context['table'].data, [])
        self.assertMessageCount(res, error=1)

    @test.create_stubs({nal_api: ('get_nodes',)})
    def test_index_api_error_handle(self):

        nal_api.get_nodes(IsA(http.HttpRequest),
                          IsA('str'),
                          func_type='all_node')\
            .AndRaise(exceptions.NotAvailable())

        self.mox.ReplayAll()
        res = self.client.get(NODE_INDEX_URL)
        self.assertItemsEqual(res.context['table'].data, [])

    @test.create_stubs({nal_api: ('get_nodes',)})
    @test.create_stubs({api.neutron: ('network_list_for_tenant',)})
    def test_detail_with_network_data(self):

        node_data = {}
        obj_id = '|'.join(['vfw',
                           str(fixture.NODE_DATA_VFW['vnf_info'][0]['ID'])])
        for key, value in NODE_RETURN_MAPPING['vfw'].iteritems():
            if isinstance(value, dict):
                node_data[key] = []
                for node_row in fixture.NODE_DATA_VFW[key]:
                    node_data[key].append(Node(node_row, value))

        nal_api.get_nodes(IsA(http.HttpRequest),
                          rec_id=obj_id.split('|')[1],
                          func_type=obj_id.split('|')[0]).AndReturn(node_data)

        network_list = []
        for network_data in NETWORK_LIST_FOR_TENANT_RETURN:
            network_list.append(Network(network_data))
        api.neutron.network_list_for_tenant(IsA(http.HttpRequest),
                                IsA('str')).AndReturn(network_list)

        self.mox.ReplayAll()
        res = self.client.get(reverse(NODE_DETAIL_URL,
                                      kwargs={"node_id": obj_id}))
        self.assertNoFormErrors(res)
        self.assertTemplateUsed(res, 'project/node/detail.html')
        for i, detail in \
                enumerate(NODE_DETAIL_DISPLAY_COLUMNS['vfw']['detail']):
            self.assertItemsEqual(res.context['node'][i][0], detail[0])

    @test.create_stubs({nal_api: ('get_nodes',)})
    @test.create_stubs({api.neutron: ('network_list_for_tenant',)})
    def test_detail_without_network_data(self):

        node_data = {}
        obj_id = '|'.join(['vlb',
                           str(fixture.NODE_DATA_NO_NET['vnf_info'][0]['ID'])])
        for key, value in NODE_RETURN_MAPPING['vlb'].iteritems():
            if isinstance(value, dict):
                node_data[key] = []
                for node_row in fixture.NODE_DATA_NO_NET[key]:
                    node_data[key].append(Node(node_row, value))

        nal_api.get_nodes(IsA(http.HttpRequest),
                          rec_id=obj_id.split('|')[1],
                          func_type=obj_id.split('|')[0]).AndReturn(node_data)

        network_list = []
        for network_data in NETWORK_LIST_FOR_TENANT_RETURN:
            network_list.append(Network(network_data))
        api.neutron.network_list_for_tenant(IsA(http.HttpRequest),
                                IsA('str')).AndReturn(network_list)

        self.mox.ReplayAll()
        res = self.client.get(reverse(NODE_DETAIL_URL,
                                      kwargs={"node_id": obj_id}))
        self.assertNoFormErrors(res)
        self.assertTemplateUsed(res, 'project/node/detail.html')
        for i, detail in \
                enumerate(NODE_DETAIL_DISPLAY_COLUMNS['vlb']['detail']):
            self.assertItemsEqual(res.context['node'][i][0], detail[0])

    @test.create_stubs({nal_api: ('get_nodes',)})
    @test.create_stubs({api.neutron: ('network_list_for_tenant',)})
    def test_detail_pfw(self):
        node_data = {}
        obj_id = '|'.join(['pfw',
                           str(fixture.NODE_DATA_PFW['pnf_info'][0]['ID'])])
        for key, value in NODE_RETURN_MAPPING['pfw'].iteritems():
            if isinstance(value, dict):
                node_data[key] = []
                for node_row in fixture.NODE_DATA_PFW[key]:
                    node_data[key].append(Node(node_row, value))

        nal_api.get_nodes(IsA(http.HttpRequest),
                          rec_id=obj_id.split('|')[1],
                          func_type=obj_id.split('|')[0]).AndReturn(node_data)

        network_list = []
        for network_data in NETWORK_LIST_FOR_TENANT_RETURN:
            network_list.append(Network(network_data))
        api.neutron.network_list_for_tenant(IsA(http.HttpRequest),
                                IsA('str')).AndReturn(network_list)

        self.mox.ReplayAll()
        res = self.client.get(reverse(NODE_DETAIL_URL,
                                      kwargs={"node_id": obj_id}))
        self.assertNoFormErrors(res)
        self.assertTemplateUsed(res, 'project/node/detail.html')

        detail_info = NODE_DETAIL_DISPLAY_COLUMNS['pfw']
        for i, detail in enumerate(detail_info['detail']):
            self.assertItemsEqual(res.context['node'][i][0], detail[0])

    @test.create_stubs({nal_api: ('get_nodes',)})
    @test.create_stubs({api.neutron: ('network_list_for_tenant',)})
    def test_detail_plb(self):
        node_data = {}
        obj_id = '|'.join(['plb',
                           str(fixture.NODE_DATA_PLB['pnf_info'][0]['ID'])])
        for key, value in NODE_RETURN_MAPPING['plb'].iteritems():
            if isinstance(value, dict):
                node_data[key] = []
                for node_row in fixture.NODE_DATA_PLB[key]:
                    node_data[key].append(Node(node_row, value))

        nal_api.get_nodes(IsA(http.HttpRequest),
                          rec_id=obj_id.split('|')[1],
                          func_type=obj_id.split('|')[0]).AndReturn(node_data)

        network_list = []
        for network_data in NETWORK_LIST_FOR_TENANT_RETURN:
            network_list.append(Network(network_data))
        api.neutron.network_list_for_tenant(IsA(http.HttpRequest),
                                IsA('str')).AndReturn(network_list)

        self.mox.ReplayAll()
        res = self.client.get(reverse(NODE_DETAIL_URL,
                                      kwargs={"node_id": obj_id}))
        self.assertNoFormErrors(res)
        self.assertTemplateUsed(res, 'project/node/detail.html')

        detail_info = NODE_DETAIL_DISPLAY_COLUMNS['plb']
        for i, detail in enumerate(detail_info['detail']):
            self.assertItemsEqual(res.context['node'][i][0], detail[0])

    @test.create_stubs({nal_api: ('get_nodes',)})
    def test_detail_api_error(self):
        obj_id = '|'.join(['vfw',
                           str(fixture.NODE_DATA_VFW['vnf_info'][0]['ID'])])
        nal_api.get_nodes(IsA(http.HttpRequest),
                          rec_id=obj_id.split('|')[1],
                          func_type=obj_id.split('|')[0]
                          ).AndRaise(OSError)

        node_data = []
        for data in fixture.NODE_DATA_LIST:
            node_data.append(Node(data,
                                  NODE_RETURN_MAPPING['all_node']['Virtual']))

        nal_api.get_nodes(IsA(http.HttpRequest),
                          IsA('str'),
                          func_type='all_node').AndReturn(node_data)

        self.mox.ReplayAll()
        res = self.client.get(reverse(NODE_DETAIL_URL,
                                      kwargs={"node_id": obj_id}))
        self.assertRedirects(res, NODE_INDEX_URL)

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
                                network_id='network_id_00001').\
            AndReturn(subnet_data)

        self.mox.ReplayAll()

        res = self.client.get(NODE_CREATE_URL)
        self.assertNoFormErrors(res)
        self.assertTemplateUsed(res, 'project/node/create.html')

    @test.create_stubs({nal_api: ('get_nodes',)})
    @test.create_stubs({api.neutron: ('network_list_for_tenant',)})
    def test_create_network_error(self):
        api.neutron.network_list_for_tenant(IsA(http.HttpRequest),
                                            IsA('str')).AndRaise(OSError)

        node_data = []
        for data in fixture.NODE_DATA_LIST:
            node_data.append(Node(data,
                                  NODE_RETURN_MAPPING['all_node']['Virtual']))

        nal_api.get_nodes(IsA(http.HttpRequest),
                          IsA('str'),
                          func_type='all_node').AndReturn(node_data)

        self.mox.ReplayAll()
        res = self.client.post(NODE_CREATE_URL)
        self.assertRedirects(res, NODE_INDEX_URL)

    @test.create_stubs({nal_api: ('get_nodes',)})
    @test.create_stubs({api.neutron: ('network_list_for_tenant',
                                      'subnet_list')})
    def test_create_subnet_error(self):
        network_list = [{'id': 'network_id_00001', 'name': 'network_nameA'},
                        {'id': 'network_id_00002', 'name': 'network_nameB'},
                        {'id': 'network_id_00003', 'name': 'network_nameC'}]

        network_data = []
        for data in network_list:
            network_data.append(Network(data))

        api.neutron.network_list_for_tenant(IsA(http.HttpRequest),
                                            IsA('str')).AndReturn(network_data)

        api.neutron.subnet_list(IsA(http.HttpRequest),
                                network_id='network_id_00001').\
            AndRaise(OSError)

        node_data = []
        for data in fixture.NODE_DATA_LIST:
            node_data.append(Node(data,
                                  NODE_RETURN_MAPPING['all_node']['Virtual']))

        nal_api.get_nodes(IsA(http.HttpRequest),
                          IsA('str'),
                          func_type='all_node').AndReturn(node_data)

        self.mox.ReplayAll()
        res = self.client.post(NODE_CREATE_URL)
        self.assertRedirects(res, NODE_INDEX_URL)

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
                                network_id='network_id_00001').\
            AndReturn(subnet_data)
        api.neutron.subnet_list(IsA(http.HttpRequest),
                                network_id='network_id_00002').\
            AndReturn(subnet_data)

        self.mox.ReplayAll()

        self.assertRaises(exceptions.NotAvailable,
                          self.client.get,
                          NODE_CREATE_URL)

    @test.create_stubs({api.neutron: ('network_list_for_tenant',
                                      'subnet_list',
                                      'subnet_get',
                                      'network_get')})
    @test.create_stubs({nal_api: ('create_node',)})
    def test_create_vfw(self):
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
                                network_id='network_id_00001').\
            AndReturn(subnet_data)

        subnet_data = {'id': 'subnet_id_00001',
                       'network_id': 'network_id_00001',
                       'cidr': '10.70.70.0/24',
                       'ip_version': 4}
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

        nal_api.create_node(IsA(http.HttpRequest),
                            IsA({})).AndReturn(True)

        self.mox.ReplayAll()

        formData = {'apl_type': '1',
                    'type': '1',
                    'device_type-1-1': '4',
                    'device_type-1-2': '3',
                    'device_type-2-1': '1',
                    'device_type-2-2': '1',
                    'subnet': 'subnet_id_00001',
                    'host_name': 'host_name',
                    'webclient_ip': '10.20.30.40',
                    'ntp_ip': '10.20.30.41',
                    'zabbix_vip_ip': '10.20.30.42',
                    'zabbix_01_ip': '10.20.30.43',
                    'zabbix_02_ip': '10.20.30.44',
                    'static_route_ip': '10.20.30.45',
                    'description': 'xxxxxxxxxxxxxxxxxxxx'}
        res = self.client.post(NODE_CREATE_URL, formData)

        self.assertNoFormErrors(res)
        self.assertMessageCount(success=1)

    @test.create_stubs({api.neutron: ('network_list_for_tenant',
                                      'subnet_list',
                                      'subnet_get',
                                      'network_get')})
    @test.create_stubs({nal_api: ('create_node',)})
    def test_create_vlb(self):
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

        subnet_data = {'id': 'subnet_id_00001',
                       'network_id': 'network_id_00001',
                       'cidr': '10.70.70.0/24',
                       'ip_version': 4}
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

        nal_api.create_node(IsA(http.HttpRequest),
                            IsA({})).AndReturn(True)

        self.mox.ReplayAll()

        formData = {'apl_type': '1',
                    'type': '2',
                    'device_type-1-1': '4',
                    'device_type-1-2': '3',
                    'device_type-2-1': '1',
                    'device_type-2-2': '1',
                    'subnet': 'subnet_id_00001',
                    'host_name': 'host_name',
                    'admin_id': 'admin_id_00001',
                    'admin_pw': 'password',
                    'fw_ip_address': '192.168.10.50',
                    'description': 'xxxxxxxxxxxxxxxxxxxx'}
        res = self.client.post(NODE_CREATE_URL, formData)

        self.assertNoFormErrors(res)
        self.assertMessageCount(success=1)

    @test.create_stubs({api.neutron: ('network_list_for_tenant',
                                      'subnet_list',
                                      'subnet_get',
                                      'network_get')})
    @test.create_stubs({nal_api: ('create_node',)})
    def test_create_pfw(self):
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

        subnet_data = {'id': 'subnet_id_00001',
                       'network_id': 'network_id_00001',
                       'cidr': '10.70.70.0/24',
                       'ip_version': 4}
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

        nal_api.create_node(IsA(http.HttpRequest),
                            IsA({})).AndReturn(True)

        self.mox.ReplayAll()

        formData = {'apl_type': '2',
                    'type': '1',
                    'device_type-1-1': '4',
                    'device_type-1-2': '3',
                    'device_type-2-1': '1',
                    'device_type-2-2': '1',
                    'subnet': 'subnet_id_00001',
                    'redundant_configuration_flg': '0',
                    'vdom_name': 'Host Name(Vdom Name)',
                    'admin_prof_name': 'xxxxxx',
                    'user_account_id': 'account_id_00001',
                    'account_password': 'p@ssw0rd',
                    'description': 'xxxxxxxxxxxxxxxxxxxx'}
        res = self.client.post(NODE_CREATE_URL, formData)

        self.assertNoFormErrors(res)
        self.assertMessageCount(success=1)

    @test.create_stubs({api.neutron: ('network_list_for_tenant',
                                      'subnet_list',
                                      'subnet_get',
                                      'network_get')})
    @test.create_stubs({nal_api: ('create_node',)})
    def test_create_plb(self):
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

        subnet_data = {'id': 'subnet_id_00001',
                       'network_id': 'network_id_00001',
                       'cidr': '10.70.70.0/24',
                       'ip_version': 4}
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

        nal_api.create_node(IsA(http.HttpRequest),
                            IsA({})).AndReturn(True)

        self.mox.ReplayAll()

        formData = {'apl_type': '2',
                    'type': '2',
                    'device_type-1-1': '4',
                    'device_type-1-2': '3',
                    'device_type-2-1': '1',
                    'device_type-2-2': '1',
                    'subnet': 'subnet_id_00001',
                    'redundant_configuration_flg': '0',
                    'partition_id': 'partition_id_00001',
                    'route_domain_id': 'route_domain_id_00001',
                    'mng_user_account_id': 'account_id_00001',
                    'mng_account_password': 'p@ssw0rd',
                    'certificate_user_account_id': 'account_id_00001',
                    'certificate_account_password': 'p@ssw0rd',
                    'fw_ip_address': '192.168.10.50',
                    'description': 'xxxxxxxxxxxxxxxxxxxx'}
        res = self.client.post(NODE_CREATE_URL, formData)

        self.assertNoFormErrors(res)
        self.assertMessageCount(success=1)

    @test.create_stubs({api.neutron: ('network_list_for_tenant',
                                      'subnet_list',)})
    @test.create_stubs({nal_api: ('create_node',)})
    def test_create_paramerter_error(self):
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

        formData = {'apl_type': '1',
                    'type': '1',
                    'device_type-1-1': '1',
                    'device_type-1-2': '3',
                    'device_type-2-1': '1',
                    'device_type-2-2': '1',
                    'subnet': 'subnet_id_00001',
                    'webclient_ip': '10.20.30.41',
                    'ntp_ip': '10.20.30.41',
                    'zabbix_vip_ip': '10.20.30.42',
                    'zabbix_01_ip': '10.20.30.43',
                    'zabbix_02_ip': '10.20.30.44',
                    'static_route_ip': '10.20.30.45',
                    'description': 'xxxxxxxxxxxxxxxxxxxx'}
        res = self.client.post(NODE_CREATE_URL, formData)

        self.assertFormError(res, 'form', 'host_name',
                             ['This field is required.'])

    @test.create_stubs({api.neutron: ('network_list_for_tenant',
                                      'subnet_list',
                                      'subnet_get',
                                      'network_get')})
    @test.create_stubs({nal_api: ('get_nodes',)})
    def test_create_network_detail_error(self):
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

        subnet_data = {'id': 'subnet_id_00001',
                       'network_id': 'network_id_00001',
                       'cidr': '10.70.70.0/24',
                       'ip_version': 4}
        api.neutron.subnet_get(IsA(http.HttpRequest),
                               'subnet_id_00001') \
            .AndReturn(Network(subnet_data))

        api.neutron.network_get(IsA(http.HttpRequest),
                                'network_id_00001').AndRaise(OSError)

        node_data = []
        for data in fixture.NODE_DATA_LIST:
            node_data.append(Node(data,
                                  NODE_RETURN_MAPPING['all_node']['Virtual']))

        nal_api.get_nodes(IsA(http.HttpRequest),
                          IsA('str'),
                          func_type='all_node').AndReturn(node_data)

        self.mox.ReplayAll()

        formData = {'apl_type': '1',
                    'type': '1',
                    'device_type-1-1': '4',
                    'device_type-1-2': '3',
                    'device_type-2-1': '1',
                    'device_type-2-2': '1',
                    'subnet': 'subnet_id_00001',
                    'host_name': 'host_name',
                    'webclient_ip': '10.20.30.40',
                    'ntp_ip': '10.20.30.41',
                    'zabbix_vip_ip': '10.20.30.42',
                    'zabbix_01_ip': '10.20.30.43',
                    'zabbix_02_ip': '10.20.30.44',
                    'static_route_ip': '10.20.30.45',
                    'description': 'xxxxxxxxxxxxxxxxxxxx'}

        res = self.client.post(NODE_CREATE_URL, formData)
        self.assertRedirects(res, NODE_INDEX_URL)

    @test.create_stubs({api.neutron: ('network_list_for_tenant',
                                      'subnet_list',
                                      'subnet_get',
                                      'network_get')})
    @test.create_stubs({nal_api: ('create_node',
                                  'get_nodes')})
    def test_create_api_error(self):
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

        subnet_data = {'id': 'subnet_id_00001',
                       'network_id': 'network_id_00001',
                       'cidr': '10.70.70.0/24',
                       'ip_version': 4}
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

        nal_api.create_node(IsA(http.HttpRequest),
                            IsA({})).AndRaise(OSError)

        self.mox.ReplayAll()

        formData = {'apl_type': '1',
                    'type': '1',
                    'device_type-1-1': '4',
                    'device_type-1-2': '3',
                    'device_type-2-1': '1',
                    'device_type-2-2': '1',
                    'subnet': 'subnet_id_00001',
                    'host_name': 'host_name',
                    'webclient_ip': '10.20.30.40',
                    'ntp_ip': '10.20.30.41',
                    'zabbix_vip_ip': '10.20.30.42',
                    'zabbix_01_ip': '10.20.30.43',
                    'zabbix_02_ip': '10.20.30.44',
                    'static_route_ip': '10.20.30.45',
                    'description': 'xxxxxxxxxxxxxxxxxxxx'}

        self.assertRaises(OSError,
                          self.client.post,
                          NODE_CREATE_URL,
                          formData)

    @test.create_stubs({api.neutron: ('network_list_for_tenant',
                                      'subnet_list',
                                      'subnet_get',
                                      'network_get')})
    @test.create_stubs({nal_api: ('create_node',
                                  'get_nodes')})
    def test_create_api_error_handle(self):
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

        subnet_data = {'id': 'subnet_id_00001',
                       'network_id': 'network_id_00001',
                       'cidr': '10.70.70.0/24',
                       'ip_version': 4}
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

        nal_api.create_node(IsA(http.HttpRequest),
                            IsA({})).AndRaise(exceptions.NotAvailable())

        self.mox.ReplayAll()

        formData = {'apl_type': '1',
                    'type': '1',
                    'device_type-1-1': '4',
                    'device_type-1-2': '3',
                    'device_type-2-1': '1',
                    'device_type-2-2': '1',
                    'subnet': 'subnet_id_00001',
                    'host_name': 'host_name',
                    'webclient_ip': '10.20.30.40',
                    'ntp_ip': '10.20.30.41',
                    'zabbix_vip_ip': '10.20.30.42',
                    'zabbix_01_ip': '10.20.30.43',
                    'zabbix_02_ip': '10.20.30.44',
                    'static_route_ip': '10.20.30.45',
                    'description': 'xxxxxxxxxxxxxxxxxxxx'}

        res = self.client.post(NODE_CREATE_URL, formData)

        self.assertTemplateUsed(res, 'project/node/create.html')

    @test.create_stubs({api.neutron: ('network_list_for_tenant',
                                      'subnet_list')})
    @test.create_stubs({nal_api: ('get_nodes',)})
    def test_update_input_column(self):
        network_list = [{'id': 'network_id_00001', 'name': 'network_nameA'}]
        subnet_list = [{'id': 'subnet_id_00001', 'name': 'subnet_nameA',
                        'cidr': '10.70.70.0/24', 'ip_version': 4},
                       {'id': 'subnet_id_00002', 'name': 'subnet_nameB',
                        'cidr': '10.70.71.0/24', 'ip_version': 4},
                       {'id': 'subnet_id_00003', 'name': 'subnet_nameC',
                        'cidr': '10.70.72.0/24', 'ip_version': 4}]

        node_data = {}
        obj_id = '|'.join(['vfw',
                           str(fixture.NODE_DATA_VFW['vnf_info'][0]['ID'])])
        for key, value in NODE_RETURN_MAPPING['vfw'].iteritems():
            if isinstance(value, dict):
                node_data[key] = []
                for node_row in fixture.NODE_DATA_VFW[key]:
                    node_data[key].append(Node(node_row, value))

        nal_api.get_nodes(IsA(http.HttpRequest),
                          rec_id=obj_id.split('|')[1],
                          func_type=obj_id.split('|')[0]).AndReturn(node_data)

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

        res = self.client.get(reverse(NODE_UPDATE_URL,
                                      args=(obj_id, 'interface')))
        self.assertNoFormErrors(res)
        self.assertTemplateUsed(res, 'project/node/update.html')

    @test.create_stubs({api.neutron: ('network_get',
                                      'subnet_list')})
    @test.create_stubs({nal_api: ('get_nodes',)})
    def test_update_add_ipv6_first_time(self):
        network_detail = {'provider__network_type': 'i_network_typeA',
                          'id': 'network_id_00001',
                          'provider__segmentation_id': 'segment_id_00001',
                          'name': 'network_nameA',
                          'router__external': 'network_typeA'}
        subnet_list = [{'id': 'subnet_id_00001', 'name': 'subnet_nameA',
                        'cidr': '10.70.70.0/24', 'ip_version': 4},
                       {'id': 'subnet_id_v6_00001', 'name': 'subnet_nameAA',
                        'cidr': '1234:5678::abc0/124', 'ip_version': 6},
                       {'id': 'subnet_id_00003', 'name': 'subnet_nameC',
                        'cidr': '10.70.72.0/24', 'ip_version': 4}]

        node_data = {}
        obj_id = '|'.join(['vfw',
                           str(fixture.NODE_DATA_VFW['vnf_info'][0]['ID']),
                           'port_id_00001'])
        for key, value in NODE_RETURN_MAPPING['vfw'].iteritems():
            if isinstance(value, dict):
                node_data[key] = []
                for node_row in fixture.NODE_DATA_VFW[key]:
                    node_data[key].append(Node(node_row, value))

        nal_api.get_nodes(IsA(http.HttpRequest),
                          rec_id=obj_id.split('|')[1],
                          func_type=obj_id.split('|')[0]).AndReturn(node_data)

        network_data = Network(network_detail)
        subnet_data = []
        for data in subnet_list:
            subnet_data.append(Network(data))

        api.neutron.network_get(IsA(http.HttpRequest),
                                'network_id_00001').AndReturn(network_data)

        api.neutron.subnet_list(IsA(http.HttpRequest),
                                network_id='network_id_00001')\
            .AndReturn(subnet_data)

        self.mox.ReplayAll()

        res = self.client.get(reverse(NODE_UPDATE_URL,
                                      args=(obj_id, 'IPv6Add')))
        self.assertNoFormErrors(res)
        self.assertTemplateUsed(res, 'project/node/update.html')

    @test.create_stubs({api.neutron: ('network_get',
                                      'subnet_list')})
    @test.create_stubs({nal_api: ('get_nodes',)})
    def test_update_add_ipv6_second_time(self):
        network_detail = {'provider__network_type': 'i_network_typeB',
                          'id': 'network_id_00002',
                          'provider__segmentation_id': 'segment_id_00002',
                          'name': 'network_nameB',
                          'router__external': 'network_typeB'}
        subnet_list = [{'id': 'subnet_id_00002', 'name': 'subnet_nameB',
                        'cidr': '10.50.79.191/24', 'ip_version': 4},
                       {'id': 'subnet_id_v6_00002', 'name': 'subnet_nameBB',
                        'cidr': '1234:5678::abc0/124', 'ip_version': 6},
                       {'id': 'subnet_id_00003', 'name': 'subnet_nameC',
                        'cidr': '10.70.72.0/24', 'ip_version': 4}]

        node_data = {}
        obj_id = '|'.join(['vlb',
                           str(fixture.NODE_DATA_VLB['vnf_info'][0]['ID']),
                           'port_id_00002'])
        for key, value in NODE_RETURN_MAPPING['vlb'].iteritems():
            if isinstance(value, dict):
                node_data[key] = []
                for node_row in fixture.NODE_DATA_VLB[key]:
                    node_data[key].append(Node(node_row, value))

        nal_api.get_nodes(IsA(http.HttpRequest),
                          rec_id=obj_id.split('|')[1],
                          func_type=obj_id.split('|')[0]).AndReturn(node_data)

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

        res = self.client.get(reverse(NODE_UPDATE_URL,
                                      args=(obj_id, 'IPv6Add')))
        self.assertNoFormErrors(res)
        self.assertTemplateUsed(res, 'project/node/update.html')

    @test.create_stubs({nal_api: ('get_nodes',)})
    def test_update_check(self):
        node_data = {}
        obj_id = '|'.join(['vfw',
                           str(fixture.NODE_DATA_VFW['vnf_info'][0]['ID'])])
        for key, value in NODE_RETURN_MAPPING['vfw'].iteritems():
            if isinstance(value, dict):
                node_data[key] = []
                for node_row in fixture.NODE_DATA_VFW[key]:
                    node_data[key].append(Node(node_row, value))

        nal_api.get_nodes(IsA(http.HttpRequest),
                          rec_id=obj_id.split('|')[1],
                          func_type=obj_id.split('|')[0]).AndReturn(node_data)

        nal_api.get_nodes(IsA(http.HttpRequest),
                          rec_id=obj_id.split('|')[1],
                          func_type=obj_id.split('|')[0]).AndReturn(node_data)

        self.mox.ReplayAll()

        res = self.client.get(reverse(NODE_UPDATE_URL,
                                      args=(obj_id, 'license')))
        self.assertNoFormErrors(res)
        self.assertTemplateUsed(res, 'project/node/update.html')
        self.assertEqual(res.context['text'], IsA('str'))

    @test.create_stubs({api.neutron: ('network_list_for_tenant',
                                      'subnet_list')})
    @test.create_stubs({nal_api: ('get_nodes',)})
    def test_update_interface_no_subnets_error(self):
        network_list = [{'id': 'network_id_00001', 'name': 'network_nameA'}]
        subnet_list = [{'id': 'subnet_id_00001', 'name': 'subnet_nameA',
                        'cidr': '10.70.70.0/24', 'ip_version': 4},
                       {'id': 'subnet_id_00002', 'name': 'subnet_nameB',
                        'cidr': '10.70.71.0/24', 'ip_version': 4}]

        node_data = {}
        obj_id = '|'.join(['vfw',
                           str(fixture.NODE_DATA_VFW['vnf_info'][0]['ID'])])
        for key, value in NODE_RETURN_MAPPING['vfw'].iteritems():
            if isinstance(value, dict):
                node_data[key] = []
                for node_row in fixture.NODE_DATA_VFW[key]:
                    node_data[key].append(Node(node_row, value))

        nal_api.get_nodes(IsA(http.HttpRequest),
                          rec_id=obj_id.split('|')[1],
                          func_type=obj_id.split('|')[0]).AndReturn(node_data)

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

        self.assertRaises(exceptions.NotAvailable,
                          self.client.get,
                          reverse(NODE_UPDATE_URL, args=(obj_id, 'interface')))

    @test.create_stubs({api.neutron: ('network_get',
                                      'subnet_list')})
    @test.create_stubs({nal_api: ('get_nodes',)})
    def test_update_add_ipv6_no_subnets_error(self):
        network_detail = {'provider__network_type': 'i_network_typeA',
                          'id': 'network_id_00001',
                          'provider__segmentation_id': 'segment_id_00001',
                          'name': 'network_nameA',
                          'router__external': 'network_typeA'}
        subnet_list = [{'id': 'subnet_id_00001', 'name': 'subnet_nameA',
                        'cidr': '10.70.70.0/24', 'ip_version': 4},
                       {'id': 'subnet_id_00002', 'name': 'subnet_nameB',
                        'cidr': '10.70.71.0/24', 'ip_version': 4},
                       {'id': 'subnet_id_00003', 'name': 'subnet_nameC',
                        'cidr': '10.70.72.0/24', 'ip_version': 4}]

        node_data = {}
        obj_id = '|'.join(['vfw',
                           str(fixture.NODE_DATA_VFW['vnf_info'][0]['ID']),
                           'port_id_00001'])
        for key, value in NODE_RETURN_MAPPING['vfw'].iteritems():
            if isinstance(value, dict):
                node_data[key] = []
                for node_row in fixture.NODE_DATA_VFW[key]:
                    node_data[key].append(Node(node_row, value))

        nal_api.get_nodes(IsA(http.HttpRequest),
                          rec_id=obj_id.split('|')[1],
                          func_type=obj_id.split('|')[0]).AndReturn(node_data)

        network_data = Network(network_detail)
        subnet_data = []
        for data in subnet_list:
            subnet_data.append(Network(data))

        api.neutron.network_get(IsA(http.HttpRequest),
                                'network_id_00001').AndReturn(network_data)

        api.neutron.subnet_list(IsA(http.HttpRequest),
                                network_id='network_id_00001')\
            .AndReturn(subnet_data)

        self.mox.ReplayAll()

        self.assertRaises(exceptions.NotAvailable,
                          self.client.get,
                          reverse(NODE_UPDATE_URL, args=(obj_id, 'IPv6Add')))

    @test.create_stubs({api.neutron: ('network_list_for_tenant',)})
    @test.create_stubs({nal_api: ('get_nodes',)})
    def test_update_network_error(self):
        node_data = {}
        obj_id = '|'.join(['vfw',
                           str(fixture.NODE_DATA_VFW['vnf_info'][0]['ID'])])
        for key, value in NODE_RETURN_MAPPING['vfw'].iteritems():
            if isinstance(value, dict):
                node_data[key] = []
                for node_row in fixture.NODE_DATA_VFW[key]:
                    node_data[key].append(Node(node_row, value))

        nal_api.get_nodes(IsA(http.HttpRequest),
                          rec_id=obj_id.split('|')[1],
                          func_type=obj_id.split('|')[0]).AndReturn(node_data)

        api.neutron.network_list_for_tenant(IsA(http.HttpRequest),
                                            IsA('str')).AndRaise(OSError)

        node_data = []
        for data in fixture.NODE_DATA_LIST:
            node_data.append(Node(data,
                                  NODE_RETURN_MAPPING['all_node']['Virtual']))

        nal_api.get_nodes(IsA(http.HttpRequest),
                          IsA('str'),
                          func_type='all_node').AndReturn(node_data)

        self.mox.ReplayAll()

        res = self.client.get(reverse(NODE_UPDATE_URL,
                                       args=(obj_id, 'interface')))
        self.assertRedirects(res, NODE_INDEX_URL)

    @test.create_stubs({api.neutron: ('network_list_for_tenant',
                                      'subnet_list',
                                      'subnet_get',
                                      'network_get')})
    @test.create_stubs({nal_api: ('get_nodes',
                                  'update_node')})
    def test_update_input_column_success(self):
        network_list = [{'id': 'network_id_00001', 'name': 'network_nameA'}]
        subnet_list = [{'id': 'subnet_id_00001', 'name': 'subnet_nameA',
                        'cidr': '10.70.70.0/24', 'ip_version': 4},
                       {'id': 'subnet_id_00002', 'name': 'subnet_nameB',
                        'cidr': '10.70.71.0/24', 'ip_version': 4},
                       {'id': 'subnet_id_00003', 'name': 'subnet_nameC',
                        'cidr': '10.70.72.0/24', 'ip_version': 4}]

        node_data = {}
        obj_id = '|'.join(['vfw',
                           str(fixture.NODE_DATA_VFW['vnf_info'][0]['ID'])])
        for key, value in NODE_RETURN_MAPPING['vfw'].iteritems():
            if isinstance(value, dict):
                node_data[key] = []
                for node_row in fixture.NODE_DATA_VFW[key]:
                    node_data[key].append(Node(node_row, value))

        nal_api.get_nodes(IsA(http.HttpRequest),
                          rec_id=obj_id.split('|')[1],
                          func_type=obj_id.split('|')[0]).AndReturn(node_data)

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

        subnet_data = {'id': 'subnet_id_00003',
                       'network_id': 'network_id_00001',
                       'cidr': '10.70.72.0/24',
                       'ip_version': 4}
        api.neutron.subnet_get(IsA(http.HttpRequest),
                               'subnet_id_00003') \
            .AndReturn(Network(subnet_data))

        network_data = {'provider__network_type': 'i_network_typeA',
                        'id': 'network_id_00001',
                        'provider__segmentation_id': 'segment_id_00001',
                        'name': 'network_nameA',
                        'router__external': 'network_typeA'}
        api.neutron.network_get(IsA(http.HttpRequest),
                                'network_id_00001') \
            .AndReturn(Network(network_data))

        nal_api.update_node(IsA(http.HttpRequest),
                            IsA({})).AndReturn(True)

        self.mox.ReplayAll()

        formData = {'node_id': obj_id.split('|')[1],
                    'function_type': obj_id.split('|')[0],
                    'device_type': '1',
                    'update_type': 'interface',
                    'subnet': 'subnet_id_00003',
                    'zone_name': 'zone_name'}
        res = self.client.post(reverse(NODE_UPDATE_URL,
                                       args=(obj_id, 'interface')),
                               formData)
        self.assertNoFormErrors(res)
        self.assertMessageCount(success=1)

    @test.create_stubs({api.neutron: ('subnet_list',
                                      'subnet_get',
                                      'network_get')})
    @test.create_stubs({nal_api: ('get_nodes',
                                  'update_node')})
    def test_update_add_ipv6_vfw_first_time_success(self):
        network_detail = {'provider__network_type': 'i_network_typeA',
                          'id': 'network_id_00001',
                          'provider__segmentation_id': 'segment_id_00001',
                          'name': 'network_nameA',
                          'router__external': 'network_typeA'}
        subnet_list = [{'id': 'subnet_id_00001', 'name': 'subnet_nameA',
                        'cidr': '10.70.70.0/24', 'ip_version': 4},
                       {'id': 'subnet_id_v6_00001', 'name': 'subnet_nameAA',
                        'cidr': '1234:5678::abc0/124', 'ip_version': 6},
                       {'id': 'subnet_id_00003', 'name': 'subnet_nameC',
                        'cidr': '10.70.72.0/24', 'ip_version': 4}]

        node_data = {}
        obj_id = '|'.join(['vfw',
                           str(fixture.NODE_DATA_VFW['vnf_info'][0]['ID']),
                           'port_id_00001'])
        for key, value in NODE_RETURN_MAPPING['vfw'].iteritems():
            if isinstance(value, dict):
                node_data[key] = []
                for node_row in fixture.NODE_DATA_VFW[key]:
                    node_data[key].append(Node(node_row, value))

        nal_api.get_nodes(IsA(http.HttpRequest),
                          rec_id=obj_id.split('|')[1],
                          func_type=obj_id.split('|')[0]).AndReturn(node_data)

        network_data = Network(network_detail)
        subnet_data = []
        for data in subnet_list:
            subnet_data.append(Network(data))

        api.neutron.network_get(IsA(http.HttpRequest),
                                'network_id_00001').AndReturn(network_data)

        api.neutron.subnet_list(IsA(http.HttpRequest),
                                network_id='network_id_00001')\
            .AndReturn(subnet_data)

        subnet_data = {'id': 'subnet_id_v6_00001',
                       'network_id': 'network_id_00001',
                       'cidr': '1234:5678::abc0/124',
                       'ip_version': 6}
        api.neutron.subnet_get(IsA(http.HttpRequest),
                               'subnet_id_v6_00001') \
            .AndReturn(Network(subnet_data))

        api.neutron.network_get(IsA(http.HttpRequest),
                                'network_id_00001').AndReturn(network_data)

        nal_api.update_node(IsA(http.HttpRequest),
                            IsA({})).AndReturn(True)

        self.mox.ReplayAll()

        formData = {'node_id': obj_id.split('|')[1],
                    'function_type': obj_id.split('|')[0],
                    'device_type': '1',
                    'update_type': 'IPv6Add',
                    'subnet': 'subnet_id_v6_00001',
                    'ip_v6_pub_auto_set_flg': 1,
                    'fixed_ip_v6_pub': '',
                    'static_route_ip_ipv6': '1234:5678::abc3',
                    'port_id': 'port_id_00001'}
        res = self.client.post(reverse(NODE_UPDATE_URL,
                                       args=(obj_id, 'IPv6Add')),
                               formData)
        self.assertNoFormErrors(res)
        self.assertMessageCount(success=1)

    @test.create_stubs({api.neutron: ('subnet_list',
                                      'subnet_get',
                                      'network_get')})
    @test.create_stubs({nal_api: ('get_nodes',
                                  'update_node')})
    def test_update_add_ipv6_vfw_second_time_success(self):
        network_detail = {'provider__network_type': 'i_network_typeB',
                          'id': 'network_id_00002',
                          'provider__segmentation_id': 'segment_id_00002',
                          'name': 'network_nameB',
                          'router__external': 'network_typeB'}
        subnet_list = [{'id': 'subnet_id_00002', 'name': 'subnet_nameB',
                        'cidr': '10.50.79.191/24', 'ip_version': 4},
                       {'id': 'subnet_id_v6_00002', 'name': 'subnet_nameBB',
                        'cidr': '1234:5678::abc0/124', 'ip_version': 6},
                       {'id': 'subnet_id_00003', 'name': 'subnet_nameC',
                        'cidr': '10.70.72.0/24', 'ip_version': 4}]

        node_data = {}
        obj_id = '|'.join(['vfw',
                           str(fixture.NODE_DATA_VFW['vnf_info'][0]['ID']),
                           'port_id_00002'])
        for key, value in NODE_RETURN_MAPPING['vfw'].iteritems():
            if isinstance(value, dict):
                node_data[key] = []
                for node_row in fixture.NODE_DATA_VFW[key]:
                    if 'ip_address_v6' in node_row \
                            and node_row['port_id'] == 'port_id_00001':
                        node_row['ip_address_v6'] = '1234:5678::abcd'
                        node_row['IaaS_subnet_id_v6'] = 'subnet_id_v6_00001'
                    node_data[key].append(Node(node_row, value))

        nal_api.get_nodes(IsA(http.HttpRequest),
                          rec_id=obj_id.split('|')[1],
                          func_type=obj_id.split('|')[0]).AndReturn(node_data)

        network_data = Network(network_detail)
        subnet_data = []
        for data in subnet_list:
            subnet_data.append(Network(data))

        api.neutron.network_get(IsA(http.HttpRequest),
                                'network_id_00002').AndReturn(network_data)

        api.neutron.subnet_list(IsA(http.HttpRequest),
                                network_id='network_id_00002')\
            .AndReturn(subnet_data)

        subnet_data = {'id': 'subnet_id_v6_00002',
                       'network_id': 'network_id_00002',
                       'cidr': '1234:5678::abc0/124',
                       'ip_version': 6}
        api.neutron.subnet_get(IsA(http.HttpRequest),
                               'subnet_id_v6_00002') \
            .AndReturn(Network(subnet_data))

        api.neutron.network_get(IsA(http.HttpRequest),
                                'network_id_00002').AndReturn(network_data)

        nal_api.update_node(IsA(http.HttpRequest),
                            IsA({})).AndReturn(True)

        self.mox.ReplayAll()

        formData = {'node_id': obj_id.split('|')[1],
                    'function_type': obj_id.split('|')[0],
                    'device_type': '1',
                    'update_type': 'IPv6Add',
                    'subnet': 'subnet_id_v6_00002',
                    'port_id': 'port_id_00002'}
        res = self.client.post(reverse(NODE_UPDATE_URL,
                                       args=(obj_id, 'IPv6Add')),
                               formData)
        self.assertNoFormErrors(res)
        self.assertMessageCount(success=1)

    @test.create_stubs({api.neutron: ('subnet_list',
                                      'subnet_get',
                                      'network_get')})
    @test.create_stubs({nal_api: ('get_nodes',
                                  'update_node')})
    def test_update_add_ipv6_pfw_success(self):
        network_detail = {'provider__network_type': 'i_network_typeA',
                          'id': 'network_id_00001',
                          'provider__segmentation_id': 'segment_id_00001',
                          'name': 'network_nameA',
                          'router__external': 'network_typeA'}
        subnet_list = [{'id': 'subnet_id_00001', 'name': 'subnet_nameA',
                        'cidr': '10.70.70.0/24', 'ip_version': 4},
                       {'id': 'subnet_id_v6_00001', 'name': 'subnet_nameAA',
                        'cidr': '1234:5678::abc0/124', 'ip_version': 6},
                       {'id': 'subnet_id_00003', 'name': 'subnet_nameC',
                        'cidr': '10.70.72.0/24', 'ip_version': 4}]

        node_data = {}
        obj_id = '|'.join(['pfw',
                           str(fixture.NODE_DATA_PFW['pnf_info'][0]['ID']),
                           'port_id_00001'])
        for key, value in NODE_RETURN_MAPPING['pfw'].iteritems():
            if isinstance(value, dict):
                node_data[key] = []
                for node_row in fixture.NODE_DATA_PFW[key]:
                    node_data[key].append(Node(node_row, value))

        nal_api.get_nodes(IsA(http.HttpRequest),
                          rec_id=obj_id.split('|')[1],
                          func_type=obj_id.split('|')[0]).AndReturn(node_data)

        network_data = Network(network_detail)
        subnet_data = []
        for data in subnet_list:
            subnet_data.append(Network(data))

        api.neutron.network_get(IsA(http.HttpRequest),
                                'network_id_00001').AndReturn(network_data)

        api.neutron.subnet_list(IsA(http.HttpRequest),
                                network_id='network_id_00001')\
            .AndReturn(subnet_data)

        subnet_data = {'id': 'subnet_id_v6_00001',
                       'network_id': 'network_id_00001',
                       'cidr': '1234:5678::abc0/124',
                       'ip_version': 6}
        api.neutron.subnet_get(IsA(http.HttpRequest),
                               'subnet_id_v6_00001') \
            .AndReturn(Network(subnet_data))

        api.neutron.network_get(IsA(http.HttpRequest),
                                'network_id_00001').AndReturn(network_data)

        nal_api.update_node(IsA(http.HttpRequest),
                            IsA({})).AndReturn(True)

        self.mox.ReplayAll()

        formData = {'node_id': obj_id.split('|')[1],
                    'function_type': obj_id.split('|')[0],
                    'device_type': '1',
                    'update_type': 'IPv6Add',
                    'subnet': 'subnet_id_v6_00001',
                    'ip_v6_pub_auto_set_flg': 1,
                    'fixed_ip_v6_pub': '',
                    'ip_v6_ext_auto_set_flg': 0,
                    'fixed_ip_v6_ext': '1234:5678::abc3',
                    'port_id': 'port_id_00001'}
        res = self.client.post(reverse(NODE_UPDATE_URL,
                                       args=(obj_id, 'IPv6Add')),
                               formData)
        self.assertNoFormErrors(res)
        self.assertMessageCount(success=1)

    @test.create_stubs({api.neutron: ('subnet_list',
                                      'subnet_get',
                                      'network_get')})
    @test.create_stubs({nal_api: ('get_nodes',
                                  'update_node')})
    def test_update_add_ipv6_vlb_success(self):
        network_detail = {'provider__network_type': 'i_network_typeB',
                          'id': 'network_id_00002',
                          'provider__segmentation_id': 'segment_id_00002',
                          'name': 'network_nameB',
                          'router__external': 'network_typeB'}
        subnet_list = [{'id': 'subnet_id_00002', 'name': 'subnet_nameB',
                        'cidr': '10.50.79.191/24', 'ip_version': 4},
                       {'id': 'subnet_id_v6_00002', 'name': 'subnet_nameBB',
                        'cidr': '1234:5678::abc0/124', 'ip_version': 6},
                       {'id': 'subnet_id_00003', 'name': 'subnet_nameC',
                        'cidr': '10.70.72.0/24', 'ip_version': 4}]

        node_data = {}
        obj_id = '|'.join(['vlb',
                           str(fixture.NODE_DATA_VLB['vnf_info'][0]['ID']),
                           'port_id_00002'])
        for key, value in NODE_RETURN_MAPPING['vlb'].iteritems():
            if isinstance(value, dict):
                node_data[key] = []
                for node_row in fixture.NODE_DATA_VLB[key]:
                    node_data[key].append(Node(node_row, value))

        nal_api.get_nodes(IsA(http.HttpRequest),
                          rec_id=obj_id.split('|')[1],
                          func_type=obj_id.split('|')[0]).AndReturn(node_data)

        network_data = Network(network_detail)
        subnet_data = []
        for data in subnet_list:
            subnet_data.append(Network(data))

        api.neutron.network_get(IsA(http.HttpRequest),
                                'network_id_00002').AndReturn(network_data)

        api.neutron.subnet_list(IsA(http.HttpRequest),
                                network_id='network_id_00002')\
            .AndReturn(subnet_data)

        subnet_data = {'id': 'subnet_id_v6_00002',
                       'network_id': 'network_id_00002',
                       'cidr': '1234:5678::abc0/124',
                       'ip_version': 6}
        api.neutron.subnet_get(IsA(http.HttpRequest),
                               'subnet_id_v6_00002') \
            .AndReturn(Network(subnet_data))

        api.neutron.network_get(IsA(http.HttpRequest),
                                'network_id_00002').AndReturn(network_data)

        nal_api.update_node(IsA(http.HttpRequest),
                            IsA({})).AndReturn(True)

        self.mox.ReplayAll()

        formData = {'node_id': obj_id.split('|')[1],
                    'function_type': obj_id.split('|')[0],
                    'device_type': '1',
                    'update_type': 'IPv6Add',
                    'subnet': 'subnet_id_v6_00002',
                    'fw_ip_v6_address': '1234:abcd::1',
                    'port_id': 'port_id_00002'}
        res = self.client.post(reverse(NODE_UPDATE_URL,
                                       args=(obj_id, 'IPv6Add')),
                               formData)
        self.assertNoFormErrors(res)
        self.assertMessageCount(success=1)

    @test.create_stubs({api.neutron: ('subnet_list',
                                      'subnet_get',
                                      'network_get')})
    @test.create_stubs({nal_api: ('get_nodes',
                                  'update_node')})
    def test_update_add_ipv6_plb_success(self):
        network_detail = {'provider__network_type': 'i_network_typeB',
                          'id': 'network_id_00002',
                          'provider__segmentation_id': 'segment_id_00002',
                          'name': 'network_nameB',
                          'router__external': 'network_typeB'}
        subnet_list = [{'id': 'subnet_id_00002', 'name': 'subnet_nameB',
                        'cidr': '10.50.79.191/24', 'ip_version': 4},
                       {'id': 'subnet_id_v6_00002', 'name': 'subnet_nameBB',
                        'cidr': '1234:5678::abc0/124', 'ip_version': 6},
                       {'id': 'subnet_id_00003', 'name': 'subnet_nameC',
                        'cidr': '10.70.72.0/24', 'ip_version': 4}]

        node_data = {}
        obj_id = '|'.join(['plb',
                           str(fixture.NODE_DATA_PLB['pnf_info'][0]['ID']),
                           'port_id_00002'])
        for key, value in NODE_RETURN_MAPPING['plb'].iteritems():
            if isinstance(value, dict):
                node_data[key] = []
                for node_row in fixture.NODE_DATA_PLB[key]:
                    node_data[key].append(Node(node_row, value))

        nal_api.get_nodes(IsA(http.HttpRequest),
                          rec_id=obj_id.split('|')[1],
                          func_type=obj_id.split('|')[0]).AndReturn(node_data)

        network_data = Network(network_detail)
        subnet_data = []
        for data in subnet_list:
            subnet_data.append(Network(data))

        api.neutron.network_get(IsA(http.HttpRequest),
                                'network_id_00002').AndReturn(network_data)

        api.neutron.subnet_list(IsA(http.HttpRequest),
                                network_id='network_id_00002')\
            .AndReturn(subnet_data)

        subnet_data = {'id': 'subnet_id_v6_00002',
                       'network_id': 'network_id_00002',
                       'cidr': '1234:5678::abc0/124',
                       'ip_version': 6}
        api.neutron.subnet_get(IsA(http.HttpRequest),
                               'subnet_id_v6_00002') \
            .AndReturn(Network(subnet_data))

        api.neutron.network_get(IsA(http.HttpRequest),
                                'network_id_00002').AndReturn(network_data)

        nal_api.update_node(IsA(http.HttpRequest),
                            IsA({})).AndReturn(True)

        self.mox.ReplayAll()

        formData = {'node_id': obj_id.split('|')[1],
                    'function_type': obj_id.split('|')[0],
                    'device_type': '1',
                    'update_type': 'IPv6Add',
                    'subnet': 'subnet_id_v6_00002',
                    'fw_ip_v6_address': '1234:abcd::1',
                    'port_id': 'port_id_00002'}
        res = self.client.post(reverse(NODE_UPDATE_URL,
                                       args=(obj_id, 'IPv6Add')),
                               formData)
        self.assertNoFormErrors(res)
        self.assertMessageCount(success=1)

    @test.create_stubs({nal_api: ('get_nodes',
                                  'update_node')})
    def test_update_check_success(self):
        node_data = {}
        obj_id = '|'.join(['vfw',
                           str(fixture.NODE_DATA_VFW['vnf_info'][0]['ID'])])
        for key, value in NODE_RETURN_MAPPING['vfw'].iteritems():
            if isinstance(value, dict):
                node_data[key] = []
                for node_row in fixture.NODE_DATA_VFW[key]:
                    node_data[key].append(Node(node_row, value))

        nal_api.get_nodes(IsA(http.HttpRequest),
                          rec_id=obj_id.split('|')[1],
                          func_type=obj_id.split('|')[0]).AndReturn(node_data)

        nal_api.update_node(IsA(http.HttpRequest),
                            IsA({})).AndReturn(True)

        self.mox.ReplayAll()

        formData = {'node_id': obj_id.split('|')[1],
                    'function_type': obj_id.split('|')[0],
                    'type': '1',
                    'device_type': '1',
                    'update_type': 'license'}
        res = self.client.post(reverse(NODE_UPDATE_URL,
                                       args=(obj_id, 'license')),
                               formData)
        self.assertNoFormErrors(res)
        self.assertMessageCount(success=1)

    @test.create_stubs({api.neutron: ('network_list_for_tenant',
                                      'subnet_list')})
    @test.create_stubs({nal_api: ('get_nodes',)})
    def test_update_input_column_parameter_error(self):
        network_list = [{'id': 'network_id_00001', 'name': 'network_nameA'}]
        subnet_list = [{'id': 'subnet_id_00001', 'name': 'subnet_nameA',
                        'cidr': '10.70.70.0/24', 'ip_version': 4},
                       {'id': 'subnet_id_00002', 'name': 'subnet_nameB',
                        'cidr': '10.70.71.0/24', 'ip_version': 4},
                       {'id': 'subnet_id_00003', 'name': 'subnet_nameC',
                        'cidr': '10.70.72.0/24', 'ip_version': 4}]

        node_data = {}
        obj_id = '|'.join(['vfw',
                           str(fixture.NODE_DATA_VFW['vnf_info'][0]['ID'])])
        for key, value in NODE_RETURN_MAPPING['vfw'].iteritems():
            if isinstance(value, dict):
                node_data[key] = []
                for node_row in fixture.NODE_DATA_VFW[key]:
                    node_data[key].append(Node(node_row, value))
        node_data['vnf_info'][0].device_type = '3'

        nal_api.get_nodes(IsA(http.HttpRequest),
                          rec_id=obj_id.split('|')[1],
                          func_type=obj_id.split('|')[0]).AndReturn(node_data)

        network_data = []
        subnet_data = []
        for data in network_list:
            network_data.append(Network(data))
        for data in subnet_list:
            subnet_data.append(Network(data))

        api.neutron.network_list_for_tenant(IsA(http.HttpRequest),
                                            IsA('str')).AndReturn(network_data)

        api.neutron.subnet_list(IsA(http.HttpRequest),
                                network_id='network_id_00001').\
            AndReturn(subnet_data)

        self.mox.ReplayAll()

        formData = {'node_id': obj_id.split('|')[1],
                    'func_type': obj_id.split('|')[0],
                    'update_type': 'interface',
                    'network': 'network_id_00001'}
        res = self.client.post(reverse(NODE_UPDATE_URL,
                                       args=(obj_id, 'interface')),
                               formData)
        self.assertFormError(res, 'form', 'device_type',
                             ['This field is required.'])

    @test.create_stubs({api.neutron: ('network_list_for_tenant',
                                      'subnet_list',
                                      'subnet_get',
                                      'network_get')})
    @test.create_stubs({nal_api: ('get_nodes',)})
    def test_update_input_column_network_error(self):
        network_list = [{'id': 'network_id_00001', 'name': 'network_nameA'}]
        subnet_list = [{'id': 'subnet_id_00001', 'name': 'subnet_nameA',
                        'cidr': '10.70.70.0/24', 'ip_version': 4},
                       {'id': 'subnet_id_00002', 'name': 'subnet_nameB',
                        'cidr': '10.70.71.0/24', 'ip_version': 4},
                       {'id': 'subnet_id_00003', 'name': 'subnet_nameC',
                        'cidr': '10.70.72.0/24', 'ip_version': 4}]

        node_data = {}
        obj_id = '|'.join(['vfw',
                           str(fixture.NODE_DATA_VFW['vnf_info'][0]['ID'])])
        for key, value in NODE_RETURN_MAPPING['vfw'].iteritems():
            if isinstance(value, dict):
                node_data[key] = []
                for node_row in fixture.NODE_DATA_VFW[key]:
                    node_data[key].append(Node(node_row, value))

        nal_api.get_nodes(IsA(http.HttpRequest),
                          rec_id=obj_id.split('|')[1],
                          func_type=obj_id.split('|')[0]).AndReturn(node_data)

        network_data = []
        subnet_data = []
        for data in network_list:
            network_data.append(Network(data))
        for data in subnet_list:
            subnet_data.append(Network(data))

        api.neutron.network_list_for_tenant(IsA(http.HttpRequest),
                                            IsA('str')).AndReturn(network_data)

        api.neutron.subnet_list(IsA(http.HttpRequest),
                                network_id='network_id_00001').\
            AndReturn(subnet_data)

        subnet_data = {'id': 'subnet_id_00003',
                       'network_id': 'network_id_00001',
                       'cidr': '10.70.72.0/24',
                       'ip_version': 4}
        api.neutron.subnet_get(IsA(http.HttpRequest),
                               'subnet_id_00003') \
            .AndReturn(Network(subnet_data))

        api.neutron.network_get(IsA(http.HttpRequest),
                                'network_id_00001').AndRaise(OSError)

        node_data = []
        for data in fixture.NODE_DATA_LIST:
            node_data.append(Node(data,
                                  NODE_RETURN_MAPPING['all_node']['Virtual']))

        nal_api.get_nodes(IsA(http.HttpRequest),
                          IsA('str'),
                          func_type='all_node').AndReturn(node_data)

        self.mox.ReplayAll()

        formData = {'node_id': obj_id.split('|')[1],
                    'function_type': obj_id.split('|')[0],
                    'device_type': '1',
                    'update_type': 'interface',
                    'subnet': 'subnet_id_00003'}

        res = self.client.post(reverse(NODE_UPDATE_URL,
                                       args=(obj_id, 'interface')),
                               formData)
        self.assertRedirects(res, NODE_INDEX_URL)

    @test.create_stubs({nal_api: ('get_nodes',
                                  'update_node')})
    def test_update_api_error(self):
        node_data = {}
        obj_id = '|'.join(['vfw',
                           str(fixture.NODE_DATA_VFW['vnf_info'][0]['ID'])])
        for key, value in NODE_RETURN_MAPPING['vfw'].iteritems():
            if isinstance(value, dict):
                node_data[key] = []
                for node_row in fixture.NODE_DATA_VFW[key]:
                    node_data[key].append(Node(node_row, value))

        nal_api.get_nodes(IsA(http.HttpRequest),
                          rec_id=obj_id.split('|')[1],
                          func_type=obj_id.split('|')[0]).AndReturn(node_data)

        nal_api.update_node(IsA(http.HttpRequest),
                            IsA({})).AndRaise(OSError)

        self.mox.ReplayAll()

        formData = {'node_id': obj_id.split('|')[1],
                    'function_type': obj_id.split('|')[0],
                    'type': '1',
                    'device_type': '1',
                    'update_type': 'license'}
        self.assertRaises(OSError,
                          self.client.post,
                          reverse(NODE_UPDATE_URL, args=(obj_id, 'license')),
                          formData)

    @test.create_stubs({nal_api: ('get_nodes',
                                  'update_node')})
    def test_update_api_error_handle(self):
        node_data = {}
        obj_id = '|'.join(['vfw',
                           str(fixture.NODE_DATA_VFW['vnf_info'][0]['ID'])])
        for key, value in NODE_RETURN_MAPPING['vfw'].iteritems():
            if isinstance(value, dict):
                node_data[key] = []
                for node_row in fixture.NODE_DATA_VFW[key]:
                    node_data[key].append(Node(node_row, value))

        nal_api.get_nodes(IsA(http.HttpRequest),
                          rec_id=obj_id.split('|')[1],
                          func_type=obj_id.split('|')[0]).AndReturn(node_data)

        nal_api.get_nodes(IsA(http.HttpRequest),
                          rec_id=obj_id.split('|')[1],
                          func_type=obj_id.split('|')[0]).AndReturn(node_data)

        nal_api.update_node(IsA(http.HttpRequest),
                            IsA({})).AndRaise(exceptions.NotAvailable())

        self.mox.ReplayAll()

        formData = {'node_id': obj_id.split('|')[1],
                    'function_type': obj_id.split('|')[0],
                    'device_type': '1',
                    'type': '1',
                    'update_type': 'license'}
        res = self.client.post(reverse(NODE_UPDATE_URL,
                                       args=(obj_id, 'license')),
                               formData)

        self.assertTemplateUsed(res, 'project/node/update.html')

    @test.create_stubs({nal_api: ('get_nodes',
                                  'delete_node')})
    def test_delete(self):
        node_data = []
        for data in fixture.NODE_DATA_LIST:
            node_data.append(Node(data,
                                  NODE_RETURN_MAPPING['all_node']['Virtual']))

        node_detail_data = {}
        for key, value in NODE_RETURN_MAPPING['vfw'].iteritems():
            if isinstance(value, dict):
                node_detail_data[key] = []
                for node_row in fixture.NODE_DATA_VFW[key]:
                    node_detail_data[key].append(Node(node_row, value))

        nal_api.get_nodes(IsA(http.HttpRequest),
                          IsA('str'),
                          func_type='all_node').AndReturn(node_data)

        nal_api.get_nodes(IsA(http.HttpRequest),
                          rec_id=str(fixture.NODE_DATA_LIST[0]['ID']),
                          func_type='vfw').AndReturn(node_detail_data)

        nal_api.delete_node(IsA(http.HttpRequest),
                            'vfw',
                            str(fixture.NODE_DATA_LIST[0]['ID']),
                            '1',
                            '0') \
            .AndReturn(True)

        self.mox.ReplayAll()

        obj_id = '|'.join(['vfw', str(fixture.NODE_DATA_LIST[0]['ID'])])
        formData = {'action': 'node__delete__%s' % obj_id}
        res = self.client.post(NODE_INDEX_URL, formData)

        self.assertRedirectsNoFollow(res, NODE_INDEX_URL)

    @test.create_stubs({nal_api: ('get_nodes',
                                  'delete_node')})
    def test_delete_api_error(self):
        node_data = []
        for data in fixture.NODE_DATA_LIST:
            node_data.append(Node(data,
                                  NODE_RETURN_MAPPING['all_node']['Virtual']))

        node_detail_data = {}
        for key, value in NODE_RETURN_MAPPING['vfw'].iteritems():
            if isinstance(value, dict):
                node_detail_data[key] = []
                for node_row in fixture.NODE_DATA_VFW[key]:
                    node_detail_data[key].append(Node(node_row, value))

        nal_api.get_nodes(IsA(http.HttpRequest),
                          IsA('str'),
                          func_type='all_node').AndReturn(node_data)

        nal_api.get_nodes(IsA(http.HttpRequest),
                          rec_id=str(fixture.NODE_DATA_LIST[0]['ID']),
                          func_type='vfw').AndReturn(node_detail_data)

        nal_api.delete_node(IsA(http.HttpRequest),
                            'vfw',
                            str(fixture.NODE_DATA_LIST[0]['ID']),
                            '1',
                            '0').AndRaise(OSError)

        node_data = []
        for data in fixture.NODE_DATA_LIST:
            node_data.append(Node(data,
                                  NODE_RETURN_MAPPING['all_node']['Virtual']))

        nal_api.get_nodes(IsA(http.HttpRequest),
                          IsA('str'),
                          func_type='all_node').AndReturn(node_data)

        self.mox.ReplayAll()

        obj_id = '|'.join(['vfw', str(fixture.NODE_DATA_LIST[0]['ID'])])
        formData = {'action': 'node__delete__%s' % obj_id}

        res = self.client.post(NODE_INDEX_URL, formData)
        self.assertRedirects(res, NODE_INDEX_URL)

    @test.create_stubs({api.neutron: ('network_list_for_tenant',
                                      'port_get')})
    @test.create_stubs({nal_api: ('get_nodes',
                                  'update_node')})
    def test_network_delete(self):
        network_list = [{'id': 'network_id_00001', 'name': 'network_nameA'},
                        {'id': 'network_id_00002', 'name': 'network_nameB'}]
        port_info = {
            'id': 'port_id_00001',
            'fixed_ips': [
                {
                    "subnet_id": "a0304c3a-4f08-4c43-88af-d796509c97d2",
                    "ip_address": "10.0.0.1"
                }
            ]
        }

        node_data = {}
        obj_id = '|'.join(['vfw',
                           str(fixture.NODE_DATA_VFW['vnf_info'][0]['ID'])])
        for key, value in NODE_RETURN_MAPPING['vfw'].iteritems():
            if isinstance(value, dict):
                node_data[key] = []
                for node_row in fixture.NODE_DATA_VFW[key]:
                    node_data[key].append(Node(node_row, value))

        nal_api.get_nodes(IsA(http.HttpRequest),
                          rec_id=obj_id.split('|')[1],
                          func_type=obj_id.split('|')[0]).AndReturn(node_data)

        network_data = []
        for data in network_list:
            network_data.append(Network(data))

        api.neutron.network_list_for_tenant(IsA(http.HttpRequest),
                                            IsA('str')).AndReturn(network_data)

        nal_api.get_nodes(IsA(http.HttpRequest),
                          rec_id=obj_id.split('|')[1],
                          func_type=obj_id.split('|')[0]).AndReturn(node_data)

        port_data = Network(port_info)
        IaaS_port_id = fixture.NODE_DATA_VFW['port_info'][0]['IaaS_port_id']
        api.neutron.port_get(IsA(http.HttpRequest),
                             IaaS_port_id).AndReturn(port_data)

        nal_api.update_node(IsA(http.HttpRequest),
                            IsA({})).AndReturn(True)

        self.mox.ReplayAll()

        net_obj_id = '|'.join(
            ['vfw',
             str(fixture.NODE_DATA_VFW['vnf_info'][0]['ID']),
             str(fixture.NODE_DATA_VFW['port_info'][0]['port_id'])])
        formData = {'action': 'networks__delete__%s' % net_obj_id}
        res = self.client.post(reverse(NODE_DETAIL_URL,
                                       kwargs={"node_id": obj_id}),
                               formData)

        self.assertRedirectsNoFollow(res, reverse(NODE_DETAIL_URL,
                                                  kwargs={"node_id": obj_id}))

    @test.create_stubs({api.neutron: ('network_list_for_tenant',
                                      'port_get')})
    @test.create_stubs({nal_api: ('get_nodes',
                                  'update_node')})
    def test_network_delete_api_error(self):
        network_list = [{'id': 'network_id_00001', 'name': 'network_nameA'},
                        {'id': 'network_id_00002', 'name': 'network_nameB'}]
        port_info = {
            'id': 'port_id_00001',
            'fixed_ips': [
                {
                    "subnet_id": "a0304c3a-4f08-4c43-88af-d796509c97d2",
                    "ip_address": "10.0.0.1"
                }
            ]
        }

        node_data = {}
        obj_id = '|'.join(['vfw',
                           str(fixture.NODE_DATA_VFW['vnf_info'][0]['ID'])])
        for key, value in NODE_RETURN_MAPPING['vfw'].iteritems():
            if isinstance(value, dict):
                node_data[key] = []
                for node_row in fixture.NODE_DATA_VFW[key]:
                    node_data[key].append(Node(node_row, value))

        nal_api.get_nodes(IsA(http.HttpRequest),
                          rec_id=obj_id.split('|')[1],
                          func_type=obj_id.split('|')[0]).AndReturn(node_data)

        network_data = []
        for data in network_list:
            network_data.append(Network(data))

        api.neutron.network_list_for_tenant(IsA(http.HttpRequest),
                                            IsA('str')).AndReturn(network_data)

        nal_api.get_nodes(IsA(http.HttpRequest),
                          rec_id=obj_id.split('|')[1],
                          func_type=obj_id.split('|')[0]).AndReturn(node_data)

        port_data = Network(port_info)
        IaaS_port_id = fixture.NODE_DATA_VFW['port_info'][0]['IaaS_port_id']
        api.neutron.port_get(IsA(http.HttpRequest),
                             IaaS_port_id).AndReturn(port_data)

        nal_api.update_node(IsA(http.HttpRequest),
                            IsA({})).AndRaise(OSError)

        self.mox.ReplayAll()

        net_obj_id = '|'.join(
            ['vfw',
             str(fixture.NODE_DATA_VFW['vnf_info'][0]['ID']),
             str(fixture.NODE_DATA_VFW['port_info'][0]['port_id'])])
        formData = {'action': 'networks__delete__%s' % net_obj_id}
        res = self.client.post(reverse(NODE_DETAIL_URL,
                                       kwargs={"node_id": obj_id}),
                               formData)
        self.assertRedirectsNoFollow(res, reverse(NODE_DETAIL_URL,
                                                  kwargs={"node_id": obj_id}))

    @test.create_stubs({nal_api: ('get_nodes',)})
    def test_row_update(self):

        node_data = {}
        obj_id = '|'.join(['vlb',
                           str(fixture.NODE_DATA_VLB['vnf_info'][0]['ID'])])
        for key, value in NODE_RETURN_MAPPING['vlb'].iteritems():
            if isinstance(value, dict):
                node_data[key] = []
                for node_row in fixture.NODE_DATA_VLB[key]:
                    node_data[key].append(Node(node_row, value))

        nal_api.get_nodes(IsA(http.HttpRequest),
                          rec_id=obj_id.split('|')[1],
                          func_type=obj_id.split('|')[0]).AndReturn(node_data)

        node_data = []
        for data in fixture.NODE_DATA_LIST:
            node_data.append(Node(data,
                                  NODE_RETURN_MAPPING['all_node']['Virtual']))

        nal_api.get_nodes(IsA(http.HttpRequest),
                          IsA('str'),
                          func_type='all_node').AndReturn(node_data)

        self.mox.ReplayAll()

        params = {'action': 'row_update',
                  'table': 'node',
                  'obj_id': obj_id,
                  }
        res = self.client.get('?'.join([NODE_INDEX_URL, urlencode(params)]))
        self.assertContains(res,
                            fixture.NODE_DATA_VLB['vnf_info'][0]['node_name'])


class Node(object):
    """Node class"""
    def __init__(self, return_obj, mapping):

        for key, value in mapping.iteritems():
                self.__dict__[key] = return_obj.get(value, None)


class Network(object):
    """Network class"""
    def __init__(self, network_data):

        for key, value in network_data.iteritems():
                self.__dict__[key] = value
