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


import nalclient
from nalclient import exc as client_exc

from horizon import exceptions

from nec_portal.api import nal_api
from nec_portal.dashboards.admin.resource import fixture as admin_fixture
from nec_portal.dashboards.project.resource import fixture as project_fixture
from nec_portal.local import nal_portal_settings
from openstack_dashboard.test import helpers as test

RESOURCE_RETURN_MAPPING = getattr(nal_portal_settings,
                                  'RESOURCE_RETURN_MAPPING', None)


class ResourceApiTests(test.APITestCase):

    def setUp(self):
        super(ResourceApiTests, self).setUp()

        # Store the original clients
        self._original_nalclient = nal_api.client

        # Replace the clients with our stubs.
        nal_api.client = lambda request: self.stub_nalclient()

    def tearDown(self):
        super(ResourceApiTests, self).tearDown()

        nal_api.client = self._original_nalclient

    def stub_nalclient(self):
        if not hasattr(self, "nalclient"):
            self.mox.StubOutWithMock(nalclient, 'Client')
            self.nalclient = self.mox.CreateMock(nalclient.Client)
        return self.nalclient

    def test_resource_get_project_list(self):
        """Verify that project resource list
        """
        cli_resources = project_fixture.RESOURCE_DATA_LIST

        client = self.stub_nalclient()
        client.resource = self.mox.CreateMockAnything()
        client.resource.get({'operation_id': '1',
                             'IaaS_tenant_id': 'tenant_id_00001',
                             'function_type': 'all_resource'})\
            .AndReturn(cli_resources)
        self.mox.ReplayAll()

        api_resources = nal_api.get_resources(self.request,
                                              'tenant_id_00001',
                                              'all_resource')

        for info_key, mapping_dict \
                in RESOURCE_RETURN_MAPPING['all_resource'].iteritems():
            for (api_resource, cli_resource) in zip(api_resources[info_key],
                                                    cli_resources[info_key]):
                for key, value in mapping_dict.iteritems():
                    self.assertEqual(getattr(api_resource, key),
                                     cli_resource.get(value, ''))

    def test_resource_list_error(self):
        """Verify that resource list
        """
        client = self.stub_nalclient()
        client.resource = self.mox.CreateMockAnything()
        client.resource.get({'operation_id': '1',
                             'IaaS_tenant_id': 'tenant_id_00001',
                             'function_type': 'all_resource'})\
            .AndRaise(OSError)
        self.mox.ReplayAll()

        self.assertRaises(OSError,
                          nal_api.get_resources,
                          self.request,
                          'tenant_id_00001',
                          'all_resource')

    def test_resource_get_appliances(self):
        """Verify that get appliance
        """
        cli_resources = project_fixture.RESOURCE_DATA_VNF

        client = self.stub_nalclient()
        client.resource = self.mox.CreateMockAnything()
        client.resource.get({'operation_id': '1',
                             'IaaS_tenant_id': 'tenant_id_00001',
                             'function_type': 'appliances'})\
            .AndReturn(cli_resources)
        self.mox.ReplayAll()

        api_resources = nal_api.get_resources(self.request,
                                              'tenant_id_00001',
                                              'appliances')

        for info_key, mapping_dict \
                in RESOURCE_RETURN_MAPPING['appliances'].iteritems():
            for (api_resource, cli_resource) in zip(api_resources[info_key],
                                                    cli_resources[info_key]):
                for key, value in mapping_dict.iteritems():
                    self.assertEqual(getattr(api_resource, key),
                                     cli_resource.get(value, ''))

    def test_resource_get_service(self):
        """Verify that get service
        """
        cli_resources = project_fixture.RESOURCE_DATA_ROUTER

        client = self.stub_nalclient()
        client.resource = self.mox.CreateMockAnything()
        client.resource.get({'operation_id': '1',
                             'IaaS_tenant_id': 'tenant_id_00001',
                             'function_type': 'service'})\
            .AndReturn(cli_resources)
        self.mox.ReplayAll()

        api_resources = nal_api.get_resources(self.request,
                                              'tenant_id_00001',
                                              'service')

        for info_key, mapping_dict \
                in RESOURCE_RETURN_MAPPING['service'].iteritems():
            for (api_resource, cli_resource) in zip(api_resources[info_key],
                                                    cli_resources[info_key]):
                for key, value in mapping_dict.iteritems():
                    self.assertEqual(getattr(api_resource, key),
                                     cli_resource.get(value, ''))

    def test_resource_get_ext_globalip(self):
        """Verify that get globalip
        """
        cli_resources = project_fixture.RESOURCE_DATA_GLOBALIP

        client = self.stub_nalclient()
        client.resource = self.mox.CreateMockAnything()
        client.resource.get({'operation_id': '1',
                             'IaaS_tenant_id': 'tenant_id_00001',
                             'function_type': 'ext_globalip'})\
            .AndReturn(cli_resources)
        self.mox.ReplayAll()

        api_resources = nal_api.get_resources(self.request,
                                              'tenant_id_00001',
                                              'ext_globalip')

        for info_key, mapping_dict \
                in RESOURCE_RETURN_MAPPING['ext_globalip'].iteritems():
            for (api_resource, cli_resource) in zip(api_resources[info_key],
                                                    cli_resources[info_key]):
                for key, value in mapping_dict.iteritems():
                    self.assertEqual(getattr(api_resource, key),
                                     cli_resource.get(value, ''))

    def test_resource_get_admin_list(self):
        """Verify that get admin list
        """
        cli_resources = admin_fixture.RESOURCE_DATA_LIST

        client = self.stub_nalclient()
        client.resource = self.mox.CreateMockAnything()
        client.resource.get({'operation_id': '1',
                             'function_type': 'all_resource'})\
            .AndReturn(cli_resources)
        self.mox.ReplayAll()

        api_resources = nal_api.get_resources(self.request)

        for info_key, mapping_dict \
                in RESOURCE_RETURN_MAPPING['all_resource'].iteritems():
            for (api_resource, cli_resource) in zip(api_resources[info_key],
                                                    cli_resources[info_key]):
                for key, value in mapping_dict.iteritems():
                    self.assertEqual(getattr(api_resource, key),
                                     cli_resource.get(value, ''))

    def test_resource_get_license(self):
        """Verify that get license
        """
        cli_resources = admin_fixture.RESOURCE_DATA_LICENSE

        client = self.stub_nalclient()
        client.resource = self.mox.CreateMockAnything()
        client.resource.get({'operation_id': '1',
                             'function_type': 'license',
                             'type': '1'})\
            .AndReturn(cli_resources)
        self.mox.ReplayAll()

        api_resources = nal_api.get_resources(self.request,
                                              func_type='license',
                                              add_params={'type': '1'})

        return_map = RESOURCE_RETURN_MAPPING['license']
        for key, value in return_map['total_info'].iteritems():
            self.assertEqual(getattr(api_resources['total_info'], key),
                             cli_resources['total_info'].get(value, ''))
        for key, value in return_map['contract_info'].iteritems():
            for (api_resource, cli_resource) in \
                    zip(api_resources['contract_info'],
                        cli_resources['contract_info']):
                self.assertEqual(getattr(api_resource, key),
                                 cli_resource.get(value, ''))

    def test_resource_get_pnf(self):
        """Verify that get pnf
        """
        cli_resources = admin_fixture.RESOURCE_DATA_PNF

        client = self.stub_nalclient()
        client.resource = self.mox.CreateMockAnything()
        client.resource.get({'operation_id': '1',
                             'function_type': 'pnf',
                             'type': '1'})\
            .AndReturn(cli_resources)
        self.mox.ReplayAll()

        api_resources = nal_api.get_resources(self.request,
                                              func_type='pnf',
                                              add_params={'type': '1'})

        return_map = RESOURCE_RETURN_MAPPING['pnf']
        for key, value in return_map['total_info'].iteritems():
            self.assertEqual(getattr(api_resources['total_info'], key),
                             cli_resources['total_info'].get(value, ''))
        for key, value in return_map['contract_info'].iteritems():
            for (api_resource, cli_resource) in \
                    zip(api_resources['contract_info'],
                        cli_resources['contract_info']):
                self.assertEqual(getattr(api_resource, key),
                                 cli_resource.get(value, ''))

    def test_resource_get_globalip(self):
        """Verify that get globalip
        """
        cli_resources = admin_fixture.RESOURCE_DATA_GLOBALIP

        client = self.stub_nalclient()
        client.resource = self.mox.CreateMockAnything()
        client.resource.get({'operation_id': '1',
                             'function_type': 'globalip'})\
            .AndReturn(cli_resources)
        self.mox.ReplayAll()

        api_resources = nal_api.get_resources(self.request,
                                              func_type='globalip',
                                              add_params={})

        return_map = RESOURCE_RETURN_MAPPING['globalip']
        for key, value in return_map['total_info'].iteritems():
            self.assertEqual(getattr(api_resources['total_info'], key),
                             cli_resources['total_info'].get(value, ''))
        for key, value in return_map['contract_info'].iteritems():
            for (api_resource, cli_resource) in \
                    zip(api_resources['contract_info'],
                        cli_resources['contract_info']):
                self.assertEqual(getattr(api_resource, key),
                                 cli_resource.get(value, ''))

    def test_resource_get_msa_vlan(self):
        """Verify that get msa_vlan
        """
        cli_resources = admin_fixture.RESOURCE_DATA_MSA_VLAN

        client = self.stub_nalclient()
        client.resource = self.mox.CreateMockAnything()
        client.resource.get({'operation_id': '1',
                             'function_type': 'msa_vlan'})\
            .AndReturn(cli_resources)
        self.mox.ReplayAll()

        api_resources = nal_api.get_resources(self.request,
                                              func_type='msa_vlan',
                                              add_params={})

        return_map = RESOURCE_RETURN_MAPPING['msa_vlan']
        for key, value in return_map['total_info'].iteritems():
            self.assertEqual(getattr(api_resources['total_info'], key),
                             cli_resources['total_info'].get(value, '-'))
        for key, value in return_map['contract_info'].iteritems():
            for (api_resource, cli_resource) in \
                    zip(api_resources['contract_info'],
                        cli_resources['contract_info']):
                self.assertEqual(getattr(api_resource, key),
                                 cli_resource.get(value, ''))

    def test_resource_get_wan_vlan(self):
        """Verify that get wan_vlan
        """
        cli_resources = admin_fixture.RESOURCE_DATA_WAN_VLAN

        client = self.stub_nalclient()
        client.resource = self.mox.CreateMockAnything()
        client.resource.get({'operation_id': '1',
                             'function_type': 'wan_vlan'})\
            .AndReturn(cli_resources)
        self.mox.ReplayAll()

        api_resources = nal_api.get_resources(self.request,
                                              func_type='wan_vlan',
                                              add_params={})

        return_map = RESOURCE_RETURN_MAPPING['wan_vlan']
        for key, value in return_map['total_info'].iteritems():
            self.assertEqual(getattr(api_resources['total_info'], key),
                             cli_resources['total_info'].get(value, ''))
        for key, value in return_map['contract_info'].iteritems():
            for (api_resource, cli_resource) in \
                    zip(api_resources['contract_info'],
                        cli_resources['contract_info']):
                self.assertEqual(getattr(api_resource, key),
                                 cli_resource.get(value, ''))

    def test_resource_get_cpu_list(self):
        """Verify that get cpu_list
        """
        cli_resources = admin_fixture.RESOURCE_DATA_POD_LIST

        client = self.stub_nalclient()
        client.resource = self.mox.CreateMockAnything()
        client.resource.get({'operation_id': '1',
                             'function_type': 'cpu_list'})\
            .AndReturn(cli_resources)
        self.mox.ReplayAll()

        api_resources = nal_api.get_resources(self.request,
                                              func_type='cpu_list',
                                              add_params={})

        return_map = RESOURCE_RETURN_MAPPING['cpu_list']
        for key, value in return_map['total_info'].iteritems():
            self.assertEqual(getattr(api_resources['total_info'], key),
                             cli_resources['total_info'].get(value, ''))
        for key, value in return_map['contract_info'].iteritems():
            for (api_resource, cli_resource) in \
                    zip(api_resources['contract_info'],
                        cli_resources['contract_info']):
                self.assertEqual(getattr(api_resource, key),
                                 cli_resource.get(value, ''))

    def test_resource_get_memory_list(self):
        """Verify that get memory_list
        """
        cli_resources = admin_fixture.RESOURCE_DATA_POD_LIST

        client = self.stub_nalclient()
        client.resource = self.mox.CreateMockAnything()
        client.resource.get({'operation_id': '1',
                             'function_type': 'memory_list'})\
            .AndReturn(cli_resources)
        self.mox.ReplayAll()

        api_resources = nal_api.get_resources(self.request,
                                              func_type='memory_list',
                                              add_params={})

        return_map = RESOURCE_RETURN_MAPPING['memory_list']
        for key, value in return_map['total_info'].iteritems():
            self.assertEqual(getattr(api_resources['total_info'], key),
                             cli_resources['total_info'].get(value, ''))
        for key, value in return_map['contract_info'].iteritems():
            for (api_resource, cli_resource) in \
                    zip(api_resources['contract_info'],
                        cli_resources['contract_info']):
                self.assertEqual(getattr(api_resource, key),
                                 cli_resource.get(value, ''))

    def test_resource_get_storage_list(self):
        """Verify that get storage_list
        """
        cli_resources = admin_fixture.RESOURCE_DATA_POD_LIST

        client = self.stub_nalclient()
        client.resource = self.mox.CreateMockAnything()
        client.resource.get({'operation_id': '1',
                             'function_type': 'storage_list'})\
            .AndReturn(cli_resources)
        self.mox.ReplayAll()

        api_resources = nal_api.get_resources(self.request,
                                              func_type='storage_list',
                                              add_params={})

        return_map = RESOURCE_RETURN_MAPPING['storage_list']
        for key, value in return_map['total_info'].iteritems():
            self.assertEqual(getattr(api_resources['total_info'], key),
                             cli_resources['total_info'].get(value, ''))
        for key, value in return_map['contract_info'].iteritems():
            for (api_resource, cli_resource) in \
                    zip(api_resources['contract_info'],
                        cli_resources['contract_info']):
                self.assertEqual(getattr(api_resource, key),
                                 cli_resource.get(value, ''))

    def test_resource_get_cpu_detail(self):
        """Verify that get cpu_detail
        """
        cli_resources = admin_fixture.RESOURCE_DATA_POD_DETAIL

        client = self.stub_nalclient()
        client.resource = self.mox.CreateMockAnything()
        client.resource.get({'operation_id': '1',
                             'function_type': 'cpu_detail'})\
            .AndReturn(cli_resources)
        self.mox.ReplayAll()

        api_resources = nal_api.get_resources(self.request,
                                              func_type='cpu_detail',
                                              add_params={})

        return_map = RESOURCE_RETURN_MAPPING['cpu_detail']
        for key, value in return_map['total_info'].iteritems():
            self.assertEqual(getattr(api_resources['total_info'], key),
                             cli_resources['total_info'].get(value, ''))
        for key, value in return_map['contract_info'].iteritems():
            for (api_resource, cli_resource) in \
                    zip(api_resources['contract_info'],
                        cli_resources['contract_info']):
                self.assertEqual(getattr(api_resource, key),
                                 cli_resource.get(value, ''))

    def test_resource_get_memory_detail(self):
        """Verify that get memory_detail
        """
        cli_resources = admin_fixture.RESOURCE_DATA_POD_DETAIL

        client = self.stub_nalclient()
        client.resource = self.mox.CreateMockAnything()
        client.resource.get({'operation_id': '1',
                             'function_type': 'memory_detail'})\
            .AndReturn(cli_resources)
        self.mox.ReplayAll()

        api_resources = nal_api.get_resources(self.request,
                                              func_type='memory_detail',
                                              add_params={})

        return_map = RESOURCE_RETURN_MAPPING['memory_detail']
        for key, value in return_map['total_info'].iteritems():
            self.assertEqual(getattr(api_resources['total_info'], key),
                             cli_resources['total_info'].get(value, ''))
        for key, value in return_map['contract_info'].iteritems():
            for (api_resource, cli_resource) in \
                    zip(api_resources['contract_info'],
                        cli_resources['contract_info']):
                self.assertEqual(getattr(api_resource, key),
                                 cli_resource.get(value, ''))

    def test_resource_get_storage_detail(self):
        """Verify that get storage_detail
        """
        cli_resources = admin_fixture.RESOURCE_DATA_POD_DETAIL

        client = self.stub_nalclient()
        client.resource = self.mox.CreateMockAnything()
        client.resource.get({'operation_id': '1',
                             'function_type': 'storage_detail'})\
            .AndReturn(cli_resources)
        self.mox.ReplayAll()

        api_resources = nal_api.get_resources(self.request,
                                              func_type='storage_detail',
                                              add_params={})

        return_map = RESOURCE_RETURN_MAPPING['storage_detail']
        for key, value in return_map['total_info'].iteritems():
            self.assertEqual(getattr(api_resources['total_info'], key),
                             cli_resources['total_info'].get(value, ''))
        for key, value in return_map['contract_info'].iteritems():
            for (api_resource, cli_resource) in \
                    zip(api_resources['contract_info'],
                        cli_resources['contract_info']):
                self.assertEqual(getattr(api_resource, key),
                                 cli_resource.get(value, ''))

    def test_resource_create(self):
        """Verify that resource create
        """
        cli_resources = {"status": "success",
                         "error-code": " NAL100000",
                         "message": ""}

        input_param = {'num': '2',
                       'function_type': 'ext_globalip'}

        cli_param = {'operation_id': self.request.user.id,
                     'IaaS_tenant_id': self.request.user.project_id,
                     'IaaS_tenant_name': self.request.user.project_name,
                     'IaaS_region_id': self.request.user.services_region}
        cli_param.update(input_param)

        client = self.stub_nalclient()
        client.resource = self.mox.CreateMockAnything()
        client.resource.create(cli_param).AndReturn(cli_resources)
        self.mox.ReplayAll()

        api_resources = nal_api.create_resource(self.request, input_param)

        self.assertEqual(api_resources['status'], 'success')

    def test_resource_create_validate_error(self):
        """Verify that resource create
        """
        input_param = {'num': '2a',
                       'function_type': 'ext_globalip'}

        cli_param = {'operation_id': self.request.user.id,
                     'IaaS_tenant_id': self.request.user.project_id,
                     'IaaS_tenant_name': self.request.user.project_name,
                     'IaaS_region_id': self.request.user.services_region}
        cli_param.update(input_param)

        client = self.stub_nalclient()
        client.resource = self.mox.CreateMockAnything()
        client.resource.create(cli_param) \
            .AndRaise(client_exc.NalBadRequest('error_message'))

        self.mox.ReplayAll()

        self.request.META['HTTP_X_REQUESTED_WITH'] = 'XMLHttpRequest'
        self.assertRaises(exceptions.NotAvailable,
                          nal_api.create_resource,
                          self.request,
                          input_param)

    def test_resource_create_error(self):
        """Verify that resource create
        """
        input_param = {'num': '2',
                       'function_type': 'ext_globalip'}

        cli_param = {'operation_id': self.request.user.id,
                     'IaaS_tenant_id': self.request.user.project_id,
                     'IaaS_tenant_name': self.request.user.project_name,
                     'IaaS_region_id': self.request.user.services_region}
        cli_param.update(input_param)

        client = self.stub_nalclient()
        client.resource = self.mox.CreateMockAnything()
        client.resource.create(cli_param).AndRaise(client_exc.InvalidEndpoint)
        self.mox.ReplayAll()

        self.assertRaises(client_exc.InvalidEndpoint,
                          nal_api.create_resource,
                          self.request,
                          input_param)

    def test_resource_update(self):
        """Verify that resource update
        """
        cli_resources = {"status": "success",
                         "error-code": " NAL100000",
                         "message": ""}

        input_param = {'status': '2',
                       'node_id': 'node_id_00001',
                       'function_type': 'ext_globalip'}

        cli_param = {'operation_id': self.request.user.id,
                     'IaaS_tenant_id': self.request.user.project_id,
                     'IaaS_tenant_name': self.request.user.project_name,
                     'IaaS_region_id': self.request.user.services_region}
        cli_param.update(input_param)

        client = self.stub_nalclient()
        client.resource = self.mox.CreateMockAnything()
        client.resource.update(cli_param).AndReturn(cli_resources)
        self.mox.ReplayAll()

        api_resources = nal_api.update_resource(self.request, input_param)

        self.assertEqual(api_resources['status'], 'success')

    def test_resource_update_validate_error(self):
        """Verify that resource update
        """
        input_param = {'status': '4',
                       'node_id': 'node_id_00001',
                       'function_type': 'ext_globalip'}

        cli_param = {'operation_id': self.request.user.id,
                     'IaaS_tenant_id': self.request.user.project_id,
                     'IaaS_tenant_name': self.request.user.project_name,
                     'IaaS_region_id': self.request.user.services_region}
        cli_param.update(input_param)

        client = self.stub_nalclient()
        client.resource = self.mox.CreateMockAnything()
        client.resource.update(cli_param)\
            .AndRaise(client_exc.NalBadRequest('error_message'))

        self.mox.ReplayAll()

        self.request.META['HTTP_X_REQUESTED_WITH'] = 'XMLHttpRequest'
        self.assertRaises(exceptions.NotAvailable,
                          nal_api.update_resource,
                          self.request,
                          input_param)

    def test_resource_update_error(self):
        """Verify that resource update
        """
        input_param = {'status': '4',
                       'node_id': 'node_id_00001',
                       'function_type': 'ext_globalip'}

        cli_param = {'operation_id': self.request.user.id,
                     'IaaS_tenant_id': self.request.user.project_id,
                     'IaaS_tenant_name': self.request.user.project_name,
                     'IaaS_region_id': self.request.user.services_region}
        cli_param.update(input_param)

        client = self.stub_nalclient()
        client.resource = self.mox.CreateMockAnything()
        client.resource.update(cli_param).AndRaise(client_exc.InvalidEndpoint)
        self.mox.ReplayAll()

        self.assertRaises(client_exc.InvalidEndpoint,
                          nal_api.update_resource,
                          self.request,
                          input_param)

    def test_resource_delete(self):
        """Verify that resource delete
        """
        cli_resources = {"status": "success",
                         "error-code": " NAL100000",
                         "message": ""}

        resource_id = 'globalip_id_00001'
        func_type = 'ext_globalip'

        cli_param = {'operation_id': self.request.user.id,
                     'IaaS_tenant_id': self.request.user.project_id,
                     'IaaS_region_id': self.request.user.services_region}
        cli_param.update({'ID': resource_id,
                          'function_type': func_type})

        client = self.stub_nalclient()
        client.resource = self.mox.CreateMockAnything()
        client.resource.delete(cli_param).AndReturn(cli_resources)
        self.mox.ReplayAll()

        api_resources = nal_api.delete_resource(self.request, func_type,
                                                resource_id)

        self.assertEqual(api_resources['status'], 'success')

    def test_resource_delete_error(self):
        """Verify that resource delete
        """
        resource_id = 'globalip_id_00001'
        func_type = 'ext_globalip'

        cli_param = {'operation_id': self.request.user.id,
                     'IaaS_tenant_id': self.request.user.project_id,
                     'IaaS_region_id': self.request.user.services_region}
        cli_param.update({'ID': resource_id,
                          'function_type': func_type})

        client = self.stub_nalclient()
        client.resource = self.mox.CreateMockAnything()
        client.resource.delete(cli_param).AndRaise(client_exc.InvalidEndpoint)
        self.mox.ReplayAll()

        self.assertRaises(client_exc.InvalidEndpoint,
                          nal_api.delete_resource,
                          self.request,
                          func_type,
                          resource_id)
