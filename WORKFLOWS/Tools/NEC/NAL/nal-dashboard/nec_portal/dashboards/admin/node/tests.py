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
from nec_portal.dashboards.admin.node.conf import setting as node_setting
from nec_portal.dashboards.admin.node import fixture
from nec_portal.dashboards.admin.node import panel  # noqa
from nec_portal.local import nal_portal_settings

from openstack_dashboard import api
from openstack_dashboard.test import helpers as test

NODE_INDEX_URL = reverse('horizon:admin:node:index')
NODE_DETAIL_URL = 'horizon:admin:node:detail'
NODE_UPDATE_URL = 'horizon:admin:node:update'

NODE_RETURN_MAPPING = getattr(nal_portal_settings, 'NODE_RETURN_MAPPING', None)
NODE_DETAIL_DISPLAY_COLUMNS = \
    getattr(nal_portal_settings, 'ADMIN_NODE_DETAIL_DISPLAY_COLUMNS', None)

TENANT_LIST_RETURN = \
    [{'id': 'aaa8f50f82da4370813e6ea797b1fb87', 'name': 'network_nameA'},
     {'id': 'bbb8f50f82da4370813e6ea797b1fb87', 'name': 'network_nameB'},
     {'id': 'ccc8f50f82da4370813e6ea797b1fb87', 'name': 'network_nameC'}]

NETWORK_LIST_FOR_TENANT_RETURN = \
    [{'id': 'IaaS_network_id-xxxx1', 'name': 'network_nameA'},
     {'id': 'IaaS_network_id-xxxx2', 'name': 'network_nameB'}]

class NodeAdminViewTests(test.BaseAdminViewTests):

    @test.create_stubs({nal_api: ('get_nodes',)})
    @test.create_stubs({api.keystone: ('tenant_list',)})
    def test_index_multi_data(self):
        tenant_names = {}
        tenant_list = []
        for data in TENANT_LIST_RETURN:
            tenant_list.append(Tenant(data))
            tenant_names[data['id']] = data['name']

        node_data = []
        check_node_data = []
        for data in fixture.NODE_DATA_LIST:
            node = Node(data, NODE_RETURN_MAPPING['all_node']['Virtual'])
            node_data.append(node)
            node.tenant_name = tenant_names.get(node.tenant_id, None)
            check_node_data.append(node)

        nal_api.get_nodes(IsA(http.HttpRequest),
                          func_type='all_node').AndReturn(node_data)

        api.keystone.tenant_list(IsA(http.HttpRequest),
                                 paginate=True).AndReturn([tenant_list, True])

        self.mox.ReplayAll()
        res = self.client.get(NODE_INDEX_URL)
        self.assertNoFormErrors(res)
        self.assertTemplateUsed(res, 'admin/node/index.html')
        self.assertItemsEqual(res.context['table'].data, check_node_data)

    @test.create_stubs({nal_api: ('get_nodes',)})
    @test.create_stubs({api.keystone: ('tenant_list',)})
    def test_index_no_data(self):
        node_data = []
        nal_api.get_nodes(IsA(http.HttpRequest),
                          func_type='all_node').AndReturn(node_data)

        tenant_list = []
        for data in TENANT_LIST_RETURN:
            tenant_list.append(Tenant(data))
        api.keystone.tenant_list(IsA(http.HttpRequest),
                                 paginate=True).AndReturn([tenant_list, True])

        self.mox.ReplayAll()
        res = self.client.get(NODE_INDEX_URL)
        self.assertNoFormErrors(res)
        self.assertTemplateUsed(res, 'admin/node/index.html')
        self.assertItemsEqual(res.context['table'].data, [])

    @test.create_stubs({nal_api: ('get_nodes',)})
    @test.create_stubs({api.keystone: ('tenant_list',)})
    def test_index_api_error(self):

        nal_api.get_nodes(IsA(http.HttpRequest),
                          func_type='all_node').AndRaise(OSError)

        tenant_list = []
        for data in TENANT_LIST_RETURN:
            tenant_list.append(Tenant(data))
        api.keystone.tenant_list(IsA(http.HttpRequest),
                                 paginate=True).AndReturn([tenant_list, True])

        self.mox.ReplayAll()
        res = self.client.get(NODE_INDEX_URL)

        self.assertTemplateUsed(res, 'admin/node/index.html')
        self.assertItemsEqual(res.context['table'].data, [])
        self.assertMessageCount(res, error=1)

    @test.create_stubs({nal_api: ('get_nodes',)})
    @test.create_stubs({api.keystone: ('tenant_list',)})
    def test_index_api_error_handle(self):

        nal_api.get_nodes(IsA(http.HttpRequest),
                          func_type='all_node')\
            .AndRaise(exceptions.NotAvailable())

        tenant_list = []
        for data in TENANT_LIST_RETURN:
            tenant_list.append(Tenant(data))
        api.keystone.tenant_list(IsA(http.HttpRequest),
                                 paginate=True).AndReturn([tenant_list, True])

        self.mox.ReplayAll()
        res = self.client.get(NODE_INDEX_URL)
        self.assertItemsEqual(res.context['table'].data, [])

    @test.create_stubs({nal_api: ('get_nodes',)})
    @test.create_stubs({api.keystone: ('tenant_list',)})
    def test_index_tenant_error(self):
        node_data = []
        for data in fixture.NODE_DATA_LIST:
            node = Node(data, NODE_RETURN_MAPPING['all_node']['Virtual'])
            node_data.append(node)

        nal_api.get_nodes(IsA(http.HttpRequest),
                          func_type='all_node').AndReturn(node_data)

        api.keystone.tenant_list(IsA(http.HttpRequest),
                                 paginate=True).AndRaise(OSError)

        self.mox.ReplayAll()
        res = self.client.get(NODE_INDEX_URL)

        self.assertTemplateUsed(res, 'admin/node/index.html')
        self.assertItemsEqual(res.context['table'].data, node_data)
        self.assertMessageCount(res, error=1)

    @test.create_stubs({nal_api: ('get_nodes',)})
    @test.create_stubs({api.keystone: ('tenant_get',)})
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

        tenant_data = Tenant({'id': 'aaa8f50f82da4370813e6ea797b1fb87',
                              'name': 'network_nameA'})

        api.keystone.tenant_get(IsA(http.HttpRequest),
                                IsA('str')).AndReturn(tenant_data)

        self.mox.ReplayAll()
        res = self.client.get(reverse(NODE_DETAIL_URL,
                                      kwargs={"node_id": obj_id}))
        self.assertNoFormErrors(res)
        self.assertTemplateUsed(res, 'admin/node/detail.html')
        for i, detail \
                in enumerate(NODE_DETAIL_DISPLAY_COLUMNS['vfw']['detail']):
            self.assertItemsEqual(res.context['node'][i][0], detail[0])

    @test.create_stubs({nal_api: ('get_nodes',)})
    @test.create_stubs({api.keystone: ('tenant_get',)})
    @test.create_stubs({api.neutron: ('network_list_for_tenant',)})
    def test_detail_without_network_data(self):

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

        network_list = []
        for network_data in NETWORK_LIST_FOR_TENANT_RETURN:
            network_list.append(Network(network_data))

        api.neutron.network_list_for_tenant(IsA(http.HttpRequest),
                                IsA('str')).AndReturn(network_list)

        tenant_data = Tenant({'id': 'aaa8f50f82da4370813e6ea797b1fb87',
                              'name': 'network_nameA'})

        api.keystone.tenant_get(IsA(http.HttpRequest),
                                IsA('str')).AndReturn(tenant_data)

        self.mox.ReplayAll()
        res = self.client.get(reverse(NODE_DETAIL_URL,
                                      kwargs={"node_id": obj_id}))
        self.assertNoFormErrors(res)
        self.assertTemplateUsed(res, 'admin/node/detail.html')
        for i, detail \
                in enumerate(NODE_DETAIL_DISPLAY_COLUMNS['vlb']['detail']):
            self.assertItemsEqual(res.context['node'][i][0], detail[0])

    @test.create_stubs({nal_api: ('get_nodes',)})
    @test.create_stubs({api.keystone: ('tenant_get',)})
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

        tenant_data = Tenant({'id': 'aaa8f50f82da4370813e6ea797b1fb87',
                              'name': 'network_nameA'})

        api.keystone.tenant_get(IsA(http.HttpRequest),
                                IsA('str')).AndReturn(tenant_data)

        self.mox.ReplayAll()
        res = self.client.get(reverse(NODE_DETAIL_URL,
                                      kwargs={"node_id": obj_id}))
        self.assertNoFormErrors(res)
        self.assertTemplateUsed(res, 'admin/node/detail.html')
        for i, detail \
                in enumerate(NODE_DETAIL_DISPLAY_COLUMNS['pfw']['detail']):
            self.assertItemsEqual(res.context['node'][i][0], detail[0])

    @test.create_stubs({nal_api: ('get_nodes',)})
    @test.create_stubs({api.keystone: ('tenant_get',)})
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

        tenant_data = Tenant({'id': 'aaa8f50f82da4370813e6ea797b1fb87',
                              'name': 'network_nameA'})

        api.keystone.tenant_get(IsA(http.HttpRequest),
                                IsA('str')).AndReturn(tenant_data)

        self.mox.ReplayAll()
        res = self.client.get(reverse(NODE_DETAIL_URL,
                                      kwargs={"node_id": obj_id}))
        self.assertNoFormErrors(res)
        self.assertTemplateUsed(res, 'admin/node/detail.html')
        for i, detail \
                in enumerate(NODE_DETAIL_DISPLAY_COLUMNS['plb']['detail']):
            self.assertItemsEqual(res.context['node'][i][0], detail[0])

    @test.create_stubs({nal_api: ('get_nodes',)})
    @test.create_stubs({api.keystone: ('tenant_list',)})
    def test_detail_api_error(self):
        obj_id = '|'.join(['vfw',
                           str(fixture.NODE_DATA_VFW['vnf_info'][0]['ID'])])
        nal_api.get_nodes(IsA(http.HttpRequest),
                          rec_id=obj_id.split('|')[1],
                          func_type=obj_id.split('|')[0]
                          ).AndRaise(OSError)

        tenant_names = {}
        tenant_list = []
        for data in TENANT_LIST_RETURN:
            tenant_list.append(Tenant(data))
            tenant_names[data['id']] = data['name']
        api.keystone.tenant_list(IsA(http.HttpRequest),
                                 paginate=True).AndReturn([tenant_list, True])

        node_data = []
        check_node_data = []
        for data in fixture.NODE_DATA_LIST:
            node = Node(data, NODE_RETURN_MAPPING['all_node']['Virtual'])
            node_data.append(node)
            node.tenant_name = tenant_names.get(node.tenant_id, None)
            check_node_data.append(node)

        nal_api.get_nodes(IsA(http.HttpRequest),
                          func_type='all_node').AndReturn(node_data)

        self.mox.ReplayAll()
        res = self.client.get(reverse(NODE_DETAIL_URL,
                                      kwargs={"node_id": obj_id}))

        self.assertRedirects(res, NODE_INDEX_URL)

    @test.create_stubs({nal_api: ('get_nodes',)})
    @test.create_stubs({api.keystone: ('tenant_get',
                                       'tenant_list')})
    @test.create_stubs({api.neutron: ('network_list_for_tenant',)})
    def test_detail_tenant_error(self):
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

        api.keystone.tenant_get(IsA(http.HttpRequest),
                                IsA('str')).AndRaise(OSError)

        tenant_names = {}
        tenant_list = []
        for data in TENANT_LIST_RETURN:
            tenant_list.append(Tenant(data))
            tenant_names[data['id']] = data['name']
        api.keystone.tenant_list(IsA(http.HttpRequest),
                                 paginate=True).AndReturn([tenant_list, True])

        node_data = []
        check_node_data = []
        for data in fixture.NODE_DATA_LIST:
            node = Node(data, NODE_RETURN_MAPPING['all_node']['Virtual'])
            node_data.append(node)
            node.tenant_name = tenant_names.get(node.tenant_id, None)
            check_node_data.append(node)

        nal_api.get_nodes(IsA(http.HttpRequest),
                          func_type='all_node').AndReturn(node_data)

        self.mox.ReplayAll()
        res = self.client.get(reverse(NODE_DETAIL_URL,
                                      kwargs={"node_id": obj_id}))

        self.assertRedirects(res, NODE_INDEX_URL)

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
        self.assertTemplateUsed(res, 'admin/node/update.html')
        self.assertEqual(res.context['text'], IsA('str'))

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

    @test.create_stubs({nal_api: ('get_nodes',)})
    @test.create_stubs({api.keystone: ('tenant_list',
                                       'tenant_get')})
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

        node_data = []
        check_node_data = []
        for data in fixture.NODE_DATA_LIST:
            node = Node(data, NODE_RETURN_MAPPING['all_node']['Virtual'])
            node_data.append(node)
            node.tenant_name = tenant_names.get(node.tenant_id, None)
            check_node_data.append(node)

        nal_api.get_nodes(IsA(http.HttpRequest),
                          func_type='all_node').AndReturn(node_data)

        api.keystone.tenant_list(IsA(http.HttpRequest),
                                 paginate=True).AndReturn([tenant_data, True])

        self.mox.ReplayAll()

        params = {'action': 'row_update',
                  'table': 'node',
                  'obj_id': obj_id,
                  }
        res = self.client.get('?'.join([NODE_INDEX_URL, urlencode(params)]))
        self.assertContains(res,
                            fixture.NODE_DATA_VLB['vnf_info'][0]['node_name'])

    @test.create_stubs({nal_api: ('get_nodes',)})
    @test.create_stubs({api.keystone: ('tenant_list',
                                       'tenant_get')})
    def test_setting_get_link(self):
        node_table = TestNodeTable()
        link_instance = node_setting.UpdateLicenseLink(table=node_table)

        obj_id = '|'.join(['vfw',
                           str(fixture.NODE_DATA_VFW['vnf_info'][0]['ID'])])
        url_info = \
            link_instance.get_link_url(fixture.NODE_DATA_VFW['vnf_info'][0])
        self.assertEqual(url_info,
                         reverse(NODE_UPDATE_URL, args=(obj_id, 'license')))


class Node(object):
    """Node class"""
    def __init__(self, return_obj, mapping):

        for key, value in mapping.iteritems():
                self.__dict__[key] = return_obj.get(value, None)


class Tenant(object):
    """Tenant class"""
    def __init__(self, network_data):

        for key, value in network_data.iteritems():
                self.__dict__[key] = value


class Network(object):
    """Network class"""
    def __init__(self, network_data):

        for key, value in network_data.iteritems():
                self.__dict__[key] = value


class TestNodeTable(object):
    """Class for get object_id"""
    def get_object_id(self, node):
        obj_id = '|'.join(['vfw',
                           str(fixture.NODE_DATA_VFW['vnf_info'][0]['ID'])])
        return obj_id
