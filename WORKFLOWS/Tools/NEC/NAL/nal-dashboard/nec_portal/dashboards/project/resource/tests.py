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
from horizon import exceptions

from nec_portal.api import nal_api
from nec_portal.dashboards.project.resource import fixture
from nec_portal.dashboards.project.resource import panel  # noqa
from nec_portal.local import nal_portal_settings

from openstack_dashboard.test import helpers as test


RESOURCE_INDEX_URL = reverse('horizon:project:resource:index')
RESOURCE_CREATE_URL = 'horizon:project:resource:create'
RESOURCE_DETAIL_URL = 'horizon:project:resource:detail'
RESOURCE_UPDATE_URL = 'horizon:project:resource:update'

RESOURCE_RETURN_MAPPING = getattr(nal_portal_settings,
                                  'RESOURCE_RETURN_MAPPING', None)
NODE_RETURN_MAPPING = getattr(nal_portal_settings, 'NODE_RETURN_MAPPING', None)
RESOURCE_DETAIL_DEF = getattr(nal_portal_settings, 'RESOURCE_DETAIL_DEF', None)


class ResourceViewTests(test.TestCase):

    @test.create_stubs({nal_api: ('get_resources',)})
    def test_index_multi_data(self):

        resource_data = {}
        for key, value in RESOURCE_RETURN_MAPPING['all_resource'].iteritems():
            if isinstance(value, dict):
                resource_data[key] = []
                for resource_row in fixture.RESOURCE_DATA_LIST[key]:
                    resource_data[key].append(Resource(resource_row, value))

        nal_api.get_resources(IsA(http.HttpRequest),
                              IsA('str'),
                              func_type='all_resource')\
            .AndReturn(resource_data)

        self.mox.ReplayAll()
        res = self.client.get(RESOURCE_INDEX_URL)
        self.assertNoFormErrors(res)
        self.assertTemplateUsed(res, 'project/resource/index.html')
        self.assertItemsEqual(res.context['table'].data,
                              resource_data['contract_info'])

    @test.create_stubs({nal_api: ('get_resources',)})
    def test_index_no_data(self):

        resource_data = {}
        for key, value in RESOURCE_RETURN_MAPPING['all_resource'].iteritems():
            if isinstance(value, dict):
                resource_data[key] = []

        nal_api.get_resources(IsA(http.HttpRequest),
                              IsA('str'),
                              func_type='all_resource')\
            .AndReturn(resource_data)

        self.mox.ReplayAll()
        res = self.client.get(RESOURCE_INDEX_URL)
        self.assertNoFormErrors(res)
        self.assertTemplateUsed(res, 'project/resource/index.html')
        self.assertItemsEqual(res.context['table'].data, [])

    @test.create_stubs({nal_api: ('get_resources',)})
    def test_index_api_error(self):

        nal_api.get_resources(IsA(http.HttpRequest),
                              IsA('str'),
                              func_type='all_resource').AndRaise(OSError)

        self.mox.ReplayAll()
        res = self.client.get(RESOURCE_INDEX_URL)

        self.assertTemplateUsed(res, 'project/resource/index.html')
        self.assertItemsEqual(res.context['table'].data, [])
        self.assertMessageCount(res, error=1)

    @test.create_stubs({nal_api: ('get_resources',)})
    def test_detail_globalip_data(self):

        resource_data = {}
        obj_id = '|'.join(['ext_globalip',
                           'global_ip',
                           'ext_globalip_table'])
        for key, value in RESOURCE_RETURN_MAPPING['ext_globalip'].iteritems():
            if isinstance(value, dict):
                resource_data[key] = []
                for resource_row in fixture.RESOURCE_DATA_GLOBALIP[key]:
                    resource_data[key].append(Resource(resource_row, value))

        nal_api.get_resources(IsA(http.HttpRequest),
                              IsA('str'),
                              func_type=obj_id.split('|')[0])\
            .AndReturn(resource_data)

        self.mox.ReplayAll()
        res = self.client.get(reverse(RESOURCE_DETAIL_URL,
                                      kwargs={"resource_id": obj_id}))
        self.assertNoFormErrors(res)
        self.assertTemplateUsed(res, 'project/resource/index.html')
        self.assertItemsEqual(res.context['table'].data,
                              resource_data['contract_info'])

    @test.create_stubs({nal_api: ('get_resources',)})
    def test_detail_globalip_no_data(self):

        resource_data = {}
        obj_id = '|'.join(['ext_globalip',
                           'global_ip',
                           'ext_globalip_table'])
        for key, value in RESOURCE_RETURN_MAPPING['ext_globalip'].iteritems():
            if isinstance(value, dict):
                resource_data[key] = []

        nal_api.get_resources(IsA(http.HttpRequest),
                              IsA('str'),
                              func_type=obj_id.split('|')[0])\
            .AndReturn(resource_data)

        self.mox.ReplayAll()
        res = self.client.get(reverse(RESOURCE_DETAIL_URL,
                                      kwargs={"resource_id": obj_id}))
        self.assertNoFormErrors(res)
        self.assertTemplateUsed(res, 'project/resource/index.html')
        self.assertItemsEqual(res.context['table'].data, [])

    @test.create_stubs({nal_api: ('get_resources',)})
    def test_detail_globalip_error(self):
        obj_id = '|'.join(['ext_globalip',
                           'global_ip',
                           'ext_globalip_table'])
        nal_api.get_resources(IsA(http.HttpRequest),
                              IsA('str'),
                              func_type=obj_id.split('|')[0]
                              ).AndRaise(OSError)

        resource_data = {}
        for key, value in RESOURCE_RETURN_MAPPING['all_resource'].iteritems():
            if isinstance(value, dict):
                resource_data[key] = []
                for resource_row in fixture.RESOURCE_DATA_LIST[key]:
                    resource_data[key].append(Resource(resource_row, value))

        nal_api.get_resources(IsA(http.HttpRequest),
                              IsA('str'),
                              func_type='all_resource')\
            .AndReturn(resource_data)

        self.mox.ReplayAll()

        res = self.client.get(reverse(RESOURCE_DETAIL_URL,
                                      kwargs={"resource_id": obj_id}))
        self.assertRedirects(res, RESOURCE_INDEX_URL)

    @test.create_stubs({nal_api: ('get_resources',)})
    def test_detail_resource_data(self):

        resource_data = {}
        obj_id = '|'.join(['appliances',
                           'intersec_sg_ext',
                           'project_base_table'])
        for key, value in RESOURCE_RETURN_MAPPING['appliances'].iteritems():
            if isinstance(value, dict):
                resource_data[key] = []
                for resource_row in fixture.RESOURCE_DATA_VNF[key]:
                    resource_data[key].append(Resource(resource_row, value))

        nal_api.get_resources(IsA(http.HttpRequest),
                              IsA('str'),
                              func_type=obj_id.split('|')[0],
                              add_params=IsA({}))\
            .AndReturn(resource_data)

        self.mox.ReplayAll()
        res = self.client.get(reverse(RESOURCE_DETAIL_URL,
                                      kwargs={"resource_id": obj_id}))
        self.assertNoFormErrors(res)
        self.assertTemplateUsed(res, 'project/resource/index.html')
        self.assertItemsEqual(res.context['table'].data,
                              resource_data['contract_info'])

    @test.create_stubs({nal_api: ('get_resources',)})
    def test_detail_resource_no_data(self):

        resource_data = {}
        obj_id = '|'.join(['appliances',
                           'intersec_sg_ext',
                           'project_base_table'])
        for key, value in RESOURCE_RETURN_MAPPING['appliances'].iteritems():
            if isinstance(value, dict):
                resource_data[key] = []

        nal_api.get_resources(IsA(http.HttpRequest),
                              IsA('str'),
                              func_type=obj_id.split('|')[0],
                              add_params=IsA({}))\
            .AndReturn(resource_data)

        self.mox.ReplayAll()
        res = self.client.get(reverse(RESOURCE_DETAIL_URL,
                                      kwargs={"resource_id": obj_id}))
        self.assertNoFormErrors(res)
        self.assertTemplateUsed(res, 'project/resource/index.html')
        self.assertItemsEqual(res.context['table'].data, [])

    @test.create_stubs({nal_api: ('get_resources',)})
    def test_detail_resource_error(self):
        obj_id = '|'.join(['appliances',
                           'intersec_sg_ext',
                           'project_base_table'])
        nal_api.get_resources(IsA(http.HttpRequest),
                              IsA('str'),
                              func_type=obj_id.split('|')[0],
                              add_params=IsA({})
                              ).AndRaise(OSError)

        resource_data = {}
        for key, value in RESOURCE_RETURN_MAPPING['all_resource'].iteritems():
            if isinstance(value, dict):
                resource_data[key] = []
                for resource_row in fixture.RESOURCE_DATA_LIST[key]:
                    resource_data[key].append(Resource(resource_row, value))

        nal_api.get_resources(IsA(http.HttpRequest),
                              IsA('str'),
                              func_type='all_resource')\
            .AndReturn(resource_data)

        self.mox.ReplayAll()
        res = self.client.get(reverse(RESOURCE_DETAIL_URL,
                                      kwargs={"resource_id": obj_id}))
        self.assertRedirects(res, RESOURCE_INDEX_URL)

    def test_create(self):

        obj_id = '|'.join(['ext_globalip',
                           'globalip'])
        self.mox.ReplayAll()

        res = self.client.get(reverse(RESOURCE_CREATE_URL,
                                      kwargs={"resource_id": obj_id}))
        self.assertNoFormErrors(res)
        self.assertTemplateUsed(res, 'project/resource/create.html')

    @test.create_stubs({nal_api: ('update_resource',)})
    def test_create_globalip(self):

        obj_id = '|'.join(['ext_globalip',
                           'globalip'])
        nal_api.update_resource(IsA(http.HttpRequest),
                                IsA({})).AndReturn(True)

        self.mox.ReplayAll()

        formData = {'resource_kind': 'ext_globalip',
                    'resource_id': obj_id,
                    'count': 1}
        res = self.client.post(reverse(RESOURCE_CREATE_URL,
                                       kwargs={"resource_id": obj_id}),
                               formData)

        self.assertNoFormErrors(res)
        self.assertMessageCount(success=1)

    @test.create_stubs({nal_api: ('update_resource',)})
    def test_create_parameter_error(self):

        obj_id = '|'.join(['ext_globalip',
                           'globalip'])
        nal_api.update_resource(IsA(http.HttpRequest),
                                IsA({})).AndRaise(exceptions.NotAvailable())
        self.mox.ReplayAll()

        formData = {'resource_kind': 'ext_globalip',
                    'resource_id': obj_id,
                    'count': 1}
        res = self.client.post(reverse(RESOURCE_CREATE_URL,
                                       kwargs={"resource_id": obj_id}),
                               formData)

        self.assertTemplateUsed(res, 'project/resource/create.html')

    @test.create_stubs({nal_api: ('update_resource',)})
    def test_create_api_error(self):

        obj_id = '|'.join(['ext_globalip',
                           'globalip'])
        nal_api.update_resource(IsA(http.HttpRequest),
                                IsA({})).AndRaise(OSError)
        self.mox.ReplayAll()

        formData = {'resource_kind': 'ext_globalip',
                    'resource_id': obj_id,
                    'count': 3}

        self.assertRaises(OSError,
                          self.client.post,
                          reverse(RESOURCE_CREATE_URL,
                                  kwargs={"resource_id": obj_id}),
                          formData)

    @test.create_stubs({nal_api: ('get_resources',
                                  'get_nodes')})
    def test_update(self):

        resource_data = {}
        for key, value in RESOURCE_RETURN_MAPPING['ext_globalip'].iteritems():
            if isinstance(value, dict):
                resource_data[key] = []
                for resource_row in fixture.RESOURCE_DATA_GLOBALIP[key]:
                    resource_data[key].append(Resource(resource_row, value))

        node_data = []
        for data in fixture.NODE_DATA_LIST:
            node_data.append(Node(data,
                                  NODE_RETURN_MAPPING['all_node']['Virtual']))

        nal_api.get_resources(IsA(http.HttpRequest),
                              IsA('str'),
                              func_type='ext_globalip')\
            .AndReturn(resource_data)

        nal_api.get_nodes(IsA(http.HttpRequest),
                          IsA('str'),
                          func_type='all_node')\
            .AndReturn(node_data)

        self.mox.ReplayAll()

        obj_id = '|'.join(['ext_globalip',
                           'global_ip',
                           '133'])
        res = self.client.get(reverse(RESOURCE_UPDATE_URL,
                                      kwargs={'resource_id': obj_id,
                                              'update_type': 'change_status'}))
        self.assertNoFormErrors(res)
        self.assertTemplateUsed(res, 'project/resource/update.html')

    @test.create_stubs({nal_api: ('get_resources',
                                  'get_nodes')})
    def test_update_status_none(self):

        resource_data = {}
        for key, value in RESOURCE_RETURN_MAPPING['ext_globalip'].iteritems():
            if isinstance(value, dict):
                resource_data[key] = []
                for resource_row in fixture.RESOURCE_DATA_GLOBALIP[key]:
                    resource_data[key].append(Resource(resource_row, value))

        node_data = []
        for data in fixture.NODE_DATA_LIST:
            node_data.append(Node(data,
                                  NODE_RETURN_MAPPING['all_node']['Virtual']))

        nal_api.get_resources(IsA(http.HttpRequest),
                              IsA('str'),
                              func_type='ext_globalip')\
            .AndReturn(resource_data)

        nal_api.get_nodes(IsA(http.HttpRequest),
                          IsA('str'),
                          func_type='all_node')\
            .AndReturn(node_data)

        self.mox.ReplayAll()

        obj_id = '|'.join(['ext_globalip',
                           'global_ip',
                           '135'])
        res = self.client.get(reverse(RESOURCE_UPDATE_URL,
                                      kwargs={'resource_id': obj_id,
                                              'update_type': 'change_status'}))
        self.assertNoFormErrors(res)
        self.assertTemplateUsed(res, 'project/resource/update.html')

    @test.create_stubs({nal_api: ('get_resources', 'get_nodes',
                                  'update_resource')})
    def test_update_status_success(self):

        resource_data = {}
        for key, value in RESOURCE_RETURN_MAPPING['ext_globalip'].iteritems():
            if isinstance(value, dict):
                resource_data[key] = []
                for resource_row in fixture.RESOURCE_DATA_GLOBALIP[key]:
                    resource_data[key].append(Resource(resource_row, value))

        node_data = []
        for data in fixture.NODE_DATA_LIST:
            node_data.append(Node(data,
                                  NODE_RETURN_MAPPING['all_node']['Virtual']))

        nal_api.get_resources(IsA(http.HttpRequest),
                              IsA('str'),
                              func_type='ext_globalip')\
            .AndReturn(resource_data)

        nal_api.get_nodes(IsA(http.HttpRequest),
                          IsA('str'),
                          func_type='all_node')\
            .AndReturn(node_data)

        nal_api.update_resource(IsA(http.HttpRequest),
                                IsA({})).AndReturn(True)

        self.mox.ReplayAll()

        obj_id = '|'.join(['ext_globalip',
                           'global_ip',
                           '133'])
        formData = {'func_type': 'ext_globalip',
                    'resource': '133',
                    'status': '2',
                    'node_id': 'xxxxx-xxxxx-xxxxx-xxxxx-xxxx1',
                    'update_type': 'change_status'}
        res = self.client.post(reverse(RESOURCE_UPDATE_URL,
                                       args=(obj_id, 'change_status')),
                               formData)
        self.assertNoFormErrors(res)
        self.assertMessageCount(success=1)

    @test.create_stubs({nal_api: ('get_resources', 'get_nodes',
                                  'update_resource')})
    def test_update_parameter_error(self):

        resource_data = {}
        for key, value in RESOURCE_RETURN_MAPPING['ext_globalip'].iteritems():
            if isinstance(value, dict):
                resource_data[key] = []
                for resource_row in fixture.RESOURCE_DATA_GLOBALIP[key]:
                    resource_data[key].append(Resource(resource_row, value))

        node_data = []
        for data in fixture.NODE_DATA_LIST:
            node_data.append(Node(data,
                                  NODE_RETURN_MAPPING['all_node']['Virtual']))

        nal_api.get_resources(IsA(http.HttpRequest),
                              IsA('str'),
                              func_type='ext_globalip')\
            .AndReturn(resource_data)

        nal_api.get_nodes(IsA(http.HttpRequest),
                          IsA('str'),
                          func_type='all_node')\
            .AndReturn(node_data)

        nal_api.update_resource(IsA(http.HttpRequest),
                                IsA({}))\
            .AndRaise(exceptions.NotAvailable())

        self.mox.ReplayAll()

        obj_id = '|'.join(['ext_globalip',
                           'global_ip',
                           '133'])
        formData = {'func_type': 'ext_globalip',
                    'resource': '133',
                    'status': '2',
                    'node_id': 'xxxxx-xxxxx-xxxxx-xxxxx-xxxx1',
                    'update_type': 'change_status'}
        res = self.client.post(reverse(RESOURCE_UPDATE_URL,
                                       args=(obj_id, 'change_status')),
                               formData)

        self.assertTemplateUsed(res, 'project/resource/update.html')

    @test.create_stubs({nal_api: ('get_resources', 'get_nodes',
                                  'update_resource')})
    def test_update_api_error(self):

        resource_data = {}
        for key, value in RESOURCE_RETURN_MAPPING['ext_globalip'].iteritems():
            if isinstance(value, dict):
                resource_data[key] = []
                for resource_row in fixture.RESOURCE_DATA_GLOBALIP[key]:
                    resource_data[key].append(Resource(resource_row, value))

        node_data = []
        for data in fixture.NODE_DATA_LIST:
            node_data.append(Node(data,
                                  NODE_RETURN_MAPPING['all_node']['Virtual']))

        nal_api.get_resources(IsA(http.HttpRequest),
                              IsA('str'),
                              func_type='ext_globalip')\
            .AndReturn(resource_data)

        nal_api.get_nodes(IsA(http.HttpRequest),
                          IsA('str'),
                          func_type='all_node')\
            .AndReturn(node_data)

        nal_api.update_resource(IsA(http.HttpRequest),
                                IsA({})).AndRaise(OSError)

        self.mox.ReplayAll()

        obj_id = '|'.join(['ext_globalip',
                           'global_ip',
                           '133'])
        formData = {'func_type': 'ext_globalip',
                    'resource': '133',
                    'status': '0',
                    'update_type': 'change_status'}
        self.assertRaises(OSError,
                          self.client.post,
                          reverse(RESOURCE_UPDATE_URL,
                                  args=(obj_id, 'change_status')),
                          formData)

    @test.create_stubs({nal_api: ('get_resources',
                                  'update_resource')})
    def test_delete(self):

        resource_data = {}
        disp_id = '|'.join(['ext_globalip',
                            'global_ip',
                            'ext_globalip_table'])
        for key, value in RESOURCE_RETURN_MAPPING['ext_globalip'].iteritems():
            if isinstance(value, dict):
                resource_data[key] = []
                for resource_row in fixture.RESOURCE_DATA_GLOBALIP[key]:
                    resource_data[key].append(Resource(resource_row, value))

        nal_api.get_resources(IsA(http.HttpRequest),
                              IsA('str'),
                              func_type=disp_id.split('|')[0])\
            .AndReturn(resource_data)

        nal_api.get_resources(IsA(http.HttpRequest),
                              IsA('str'),
                              func_type=disp_id.split('|')[0])\
            .AndReturn(resource_data)

        nal_api.update_resource(IsA(http.HttpRequest),
                                IsA({})).AndReturn(True)

        self.mox.ReplayAll()

        obj_id = '|'.join(['ext_globalip',
                           'global_ip',
                           '135'])
        formData = {'action': 'resource_globalip__delete__%s' % obj_id}

        res = self.client.post(reverse(RESOURCE_DETAIL_URL,
                                       kwargs={"resource_id": disp_id}),
                               formData)

        self.assertRedirectsNoFollow(res,
                                     reverse(RESOURCE_DETAIL_URL,
                                             kwargs={"resource_id": disp_id}))

    @test.create_stubs({nal_api: ('get_resources',
                                  'update_resource')})
    def test_delete_api_error(self):

        resource_data = {}
        disp_id = '|'.join(['ext_globalip',
                            'global_ip',
                            'ext_globalip_table'])
        for key, value in RESOURCE_RETURN_MAPPING['ext_globalip'].iteritems():
            if isinstance(value, dict):
                resource_data[key] = []
                for resource_row in fixture.RESOURCE_DATA_GLOBALIP[key]:
                    resource_data[key].append(Resource(resource_row, value))

        nal_api.get_resources(IsA(http.HttpRequest),
                              IsA('str'),
                              func_type=disp_id.split('|')[0])\
            .AndReturn(resource_data)

        nal_api.get_resources(IsA(http.HttpRequest),
                              IsA('str'),
                              func_type=disp_id.split('|')[0])\
            .AndReturn(resource_data)

        nal_api.update_resource(IsA(http.HttpRequest),
                                IsA({})).AndRaise(OSError)

        self.mox.ReplayAll()

        obj_id = '|'.join(['ext_globalip',
                           'global_ip',
                           '135'])
        formData = {'action': 'resource_globalip__delete__%s' % obj_id}

        res = self.client.post(reverse(RESOURCE_DETAIL_URL,
                                       kwargs={"resource_id": disp_id}),
                               formData)
        self.assertRedirectsNoFollow(res,
                                     reverse(RESOURCE_DETAIL_URL,
                                             kwargs={"resource_id": disp_id}))


class Node(object):
    """Node class"""
    def __init__(self, return_obj, mapping):

        for key, value in mapping.iteritems():
            set_value = return_obj.get(value, '')
            self.__dict__[key] = set_value


class Resource(object):
    """Resource class"""
    def __init__(self, return_obj, mapping):

        for key, value in mapping.iteritems():
            set_value = return_obj.get(value, '')
            self.__dict__[key] = set_value
