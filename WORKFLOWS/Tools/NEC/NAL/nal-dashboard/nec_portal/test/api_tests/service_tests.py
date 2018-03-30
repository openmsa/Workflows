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

from nec_portal import api
from nec_portal.api import nal_api  # noqa
from nec_portal.dashboards.project.service import fixture
from nec_portal.local import nal_portal_settings
from openstack_dashboard.test import helpers as test

SERVICE_RETURN_MAPPING = getattr(nal_portal_settings,
                                 'SERVICE_RETURN_MAPPING', None)


class ServiceApiTests(test.APITestCase):

    def setUp(self):
        super(ServiceApiTests, self).setUp()

        # Store the original clients
        self._original_nalclient = api.nal_api.client

        # Replace the clients with our stubs.
        api.nal_api.client = lambda request: self.stub_nalclient()

    def tearDown(self):
        super(ServiceApiTests, self).tearDown()

        api.nal_api.client = self._original_nalclient

    def stub_nalclient(self):
        if not hasattr(self, "nalclient"):
            self.mox.StubOutWithMock(nalclient, 'Client')
            self.nalclient = self.mox.CreateMock(nalclient.Client)
        return self.nalclient

    def test_service_list_no_param(self):
        """Verify that service list
        """
        cli_services = fixture.SERVICE_DATA_LIST

        client = self.stub_nalclient()
        client.service = self.mox.CreateMockAnything()
        client.service.get({'operation_id': self.request.user.id,
                            'function_type': 'all_dcconnect'}) \
            .AndReturn(cli_services)
        self.mox.ReplayAll()

        api_services = api.nal_api.get_services(self.request)

        for (api_service, cli_service) in zip(api_services, cli_services):
            for key, value \
                    in SERVICE_RETURN_MAPPING['all_dcconnect'].iteritems():
                self.assertEqual(getattr(api_service, key),
                                 cli_service.get(value, ''))

    def test_service_list_all_param(self):
        """Verify that service list
        """
        cli_services = fixture.SERVICE_DATA_LIST

        input_param = {'operation_id': self.request.user.id,
                       'IaaS_tenant_id': 'tenant_id_00001',
                       'group_id': 'group_id_00001',
                       'function_type': 'all_dcconnect'}

        client = self.stub_nalclient()
        client.service = self.mox.CreateMockAnything()
        client.service.get(input_param).AndReturn(cli_services)
        self.mox.ReplayAll()

        api_services = api.nal_api.get_services(
            self.request,
            IaaS_tenant_id='tenant_id_00001',
            group_id='group_id_00001',
            func_type='all_dcconnect')

        for (api_service, cli_service) in zip(api_services, cli_services):
            for key, value \
                    in SERVICE_RETURN_MAPPING['all_dcconnect'].iteritems():
                self.assertEqual(getattr(api_service, key),
                                 cli_service.get(value, ''))

    def test_service_list_error(self):
        """Verify that service list
        """
        input_param = {'operation_id': self.request.user.id,
                       'IaaS_tenant_id': 'tenant_id_00001',
                       'function_type': 'all_dcconnect'}

        client = self.stub_nalclient()
        client.service = self.mox.CreateMockAnything()
        client.service.get(input_param).AndRaise(OSError)
        self.mox.ReplayAll()

        self.assertRaises(OSError,
                          api.nal_api.get_services,
                          self.request,
                          IaaS_tenant_id='tenant_id_00001',
                          func_type='all_dcconnect')

    def test_service_detail(self):
        """Verify that service list
        """
        cli_services = fixture.SERVICE_DATA_DEFAULT

        input_param = {'operation_id': '1',
                       'IaaS_tenant_id': 'tenant_id_00001',
                       'group_id': 'group_id_00001',
                       'function_type': 'dcconnect'}

        client = self.stub_nalclient()
        client.service = self.mox.CreateMockAnything()
        client.service.get(input_param).AndReturn(cli_services)
        self.mox.ReplayAll()

        api_services = api.nal_api.get_services(
            self.request,
            IaaS_tenant_id='tenant_id_00001',
            group_id='group_id_00001',
            func_type='dcconnect')

        mapping = SERVICE_RETURN_MAPPING['dcconnect']
        for (api_service, cli_service) in zip(api_services['dc_group_info'],
                                              cli_services['dc_group_info']):
            for key, value in mapping['dc_group_info'].iteritems():
                self.assertEqual(getattr(api_service, key),
                                 cli_service.get(value, ''))
        for (api_service, cli_service) in zip(api_services['dc_info'],
                                              cli_services['dc_info']):
            for key, value in mapping['dc_info'].iteritems():
                self.assertEqual(getattr(api_service, key),
                                 cli_service.get(value, ''))
        for (api_service, cli_service) in zip(api_services['dc_member_info'],
                                              cli_services['dc_member_info']):
            for key, value in mapping['dc_member_info'].iteritems():
                self.assertEqual(getattr(api_service, key),
                                 cli_service.get(value, ''))

    def test_service_detail_no_member(self):
        """Verify that service list
        """
        cli_services = fixture.SERVICE_DATA_NO_MEMBER_LIST

        input_param = {'operation_id': self.request.user.id,
                       'IaaS_tenant_id': 'tenant_id_00001',
                       'group_id': 'group_id_00001',
                       'function_type': 'dcconnect'}

        client = self.stub_nalclient()
        client.service = self.mox.CreateMockAnything()
        client.service.get(input_param).AndReturn(cli_services)
        self.mox.ReplayAll()

        api_services = api.nal_api.get_services(
            self.request,
            IaaS_tenant_id='tenant_id_00001',
            group_id='group_id_00001',
            func_type='dcconnect')

        mapping = SERVICE_RETURN_MAPPING['dcconnect']
        for (api_service, cli_service) in zip(api_services['dc_group_info'],
                                              cli_services['dc_group_info']):
            for key, value in mapping['dc_group_info'].iteritems():
                self.assertEqual(getattr(api_service, key),
                                 cli_service.get(value, ''))
        for (api_service, cli_service) in zip(api_services['dc_member_info'],
                                              cli_services['dc_member_info']):
            for key, value in mapping['dc_member_info'].iteritems():
                self.assertEqual(getattr(api_service, key),
                                 cli_service.get(value, ''))
        self.assertEqual(api_services['dc_info'], [])

    def test_service_detail_no_network(self):
        """Verify that service list
        """
        cli_services = fixture.SERVICE_DATA_NO_NETWORK_LIST

        input_param = {'operation_id': self.request.user.id,
                       'IaaS_tenant_id': 'tenant_id_00001',
                       'group_id': 'group_id_00001',
                       'function_type': 'dcconnect'}

        client = self.stub_nalclient()
        client.service = self.mox.CreateMockAnything()
        client.service.get(input_param).AndReturn(cli_services)
        self.mox.ReplayAll()

        api_services = api.nal_api.get_services(
            self.request,
            IaaS_tenant_id='tenant_id_00001',
            group_id='group_id_00001',
            func_type='dcconnect')

        mapping = SERVICE_RETURN_MAPPING['dcconnect']
        for (api_service, cli_service) in zip(api_services['dc_group_info'],
                                              cli_services['dc_group_info']):
            for key, value in mapping['dc_group_info'].iteritems():
                self.assertEqual(getattr(api_service, key),
                                 cli_service.get(value, ''))
        for (api_service, cli_service) in zip(api_services['dc_info'],
                                              cli_services['dc_info']):
            for key, value in mapping['dc_info'].iteritems():
                self.assertEqual(getattr(api_service, key),
                                 cli_service.get(value, ''))
        self.assertEqual(api_services['dc_member_info'], [])

    def test_service_create(self):
        """Verify that service create
        """
        cli_services = {"status": "success",
                        "error-code": " NAL100000",
                        "message": ""}

        input_param = {'service_name': 'host_nameA',
                       'service_type': '10.58.70.1',
                       'function_type': 'dcconnect'}

        cli_param = {'operation_id': self.request.user.id,
                     'IaaS_tenant_id': self.request.user.project_id,
                     'IaaS_tenant_name': self.request.user.project_name,
                     'IaaS_region_id': self.request.user.services_region}
        cli_param.update(input_param)

        client = self.stub_nalclient()
        client.service = self.mox.CreateMockAnything()
        client.service.create(cli_param).AndReturn(cli_services)
        self.mox.ReplayAll()

        api_services = api.nal_api.create_service(self.request, input_param)

        self.assertEqual(api_services['status'], 'success')

    def test_service_create_validate_error(self):
        """Verify that service create
        """
        input_param = {'service_name': 'host_nameA',
                       'service_type': '10.58.70.1',
                       'function_type': 'dcconnect'}

        cli_param = {'operation_id': self.request.user.id,
                     'IaaS_tenant_id': self.request.user.project_id,
                     'IaaS_tenant_name': self.request.user.project_name,
                     'IaaS_region_id': self.request.user.services_region}
        cli_param.update(input_param)

        client = self.stub_nalclient()
        client.service = self.mox.CreateMockAnything()
        client.service.create(cli_param) \
            .AndRaise(client_exc.NalBadRequest('error_message'))

        self.mox.ReplayAll()

        self.request.META['HTTP_X_REQUESTED_WITH'] = 'XMLHttpRequest'
        self.assertRaises(exceptions.NotAvailable,
                          api.nal_api.create_service,
                          self.request,
                          input_param)

    def test_service_create_error(self):
        """Verify that service create
        """
        input_param = {'service_name': 'host_nameA',
                       'service_type': '10.58.70.1',
                       'function_type': 'dcconnect'}

        cli_param = {'operation_id': self.request.user.id,
                     'IaaS_tenant_id': self.request.user.project_id,
                     'IaaS_tenant_name': self.request.user.project_name,
                     'IaaS_region_id': self.request.user.services_region}
        cli_param.update(input_param)

        client = self.stub_nalclient()
        client.service = self.mox.CreateMockAnything()
        client.service.create(cli_param).AndRaise(client_exc.InvalidEndpoint)

        self.mox.ReplayAll()

        self.assertRaises(client_exc.InvalidEndpoint,
                          api.nal_api.create_service,
                          self.request,
                          input_param)

    def test_service_update(self):
        """Verify that service update
        """
        cli_services = {"status": "success",
                        "error-code": " NAL100000",
                        "message": ""}

        input_param = {'group_id': 'group_id_00001',
                       'IaaS_network_type': 'vxlan',
                       'IaaS_network_id': 'net_id_00001',
                       'function_type': 'dcconnect'}

        cli_param = {'operation_id': self.request.user.id,
                     'IaaS_tenant_id': self.request.user.project_id,
                     'IaaS_tenant_name': self.request.user.project_name,
                     'IaaS_region_id': self.request.user.services_region}
        cli_param.update(input_param)

        client = self.stub_nalclient()
        client.service = self.mox.CreateMockAnything()
        client.service.update(cli_param).AndReturn(cli_services)
        self.mox.ReplayAll()

        api_services = api.nal_api.update_service(self.request, input_param)

        self.assertEqual(api_services['status'], 'success')

    def test_service_update_validate_error(self):
        """Verify that service update
        """
        input_param = {'group_id': 'group_id_00001',
                       'IaaS_network_type': 'vxlan',
                       'IaaS_network_id': 'net_id_00001',
                       'function_type': 'dcconnect'}

        cli_param = {'operation_id': self.request.user.id,
                     'IaaS_tenant_id': self.request.user.project_id,
                     'IaaS_tenant_name': self.request.user.project_name,
                     'IaaS_region_id': self.request.user.services_region}
        cli_param.update(input_param)

        client = self.stub_nalclient()
        client.service = self.mox.CreateMockAnything()
        client.service.update(cli_param) \
            .AndRaise(client_exc.NalBadRequest('error_message'))

        self.mox.ReplayAll()

        self.request.META['HTTP_X_REQUESTED_WITH'] = 'XMLHttpRequest'
        self.assertRaises(exceptions.NotAvailable,
                          api.nal_api.update_service,
                          self.request,
                          input_param)

    def test_service_update_error(self):
        """Verify that service update
        """
        input_param = {'group_id': 'group_id_00001',
                       'IaaS_network_type': 'vxlan',
                       'IaaS_network_id': 'net_id_00001',
                       'function_type': 'dcconnect'}

        cli_param = {'operation_id': self.request.user.id,
                     'IaaS_tenant_id': self.request.user.project_id,
                     'IaaS_tenant_name': self.request.user.project_name,
                     'IaaS_region_id': self.request.user.services_region}
        cli_param.update(input_param)

        client = self.stub_nalclient()
        client.service = self.mox.CreateMockAnything()
        client.service.update(cli_param).AndRaise(client_exc.InvalidEndpoint)

        self.mox.ReplayAll()

        self.assertRaises(client_exc.InvalidEndpoint,
                          api.nal_api.update_service,
                          self.request,
                          input_param)

    def test_service_delete(self):
        """Verify that service delete
        """
        cli_services = {"status": "success",
                        "error-code": " NAL100000",
                        "message": ""}

        service_id = 'service_id_00001'
        func_type = 'dcconnect'

        cli_param = {'operation_id': self.request.user.id,
                     'IaaS_tenant_id': self.request.user.project_id,
                     'IaaS_region_id': self.request.user.services_region}
        form_param = {'service_id': service_id,
                      'function_type': func_type,
                      'service_type': '1',
                      'apl_type': '1',
                      'type': '3',
                      'device_type': '1',
                      'job_cleaning_mode': '0'}
        cli_param.update(form_param)

        client = self.stub_nalclient()
        client.service = self.mox.CreateMockAnything()
        client.service.delete(cli_param).AndReturn(cli_services)
        self.mox.ReplayAll()

        api_services = api.nal_api.delete_service(self.request, form_param)

        self.assertEqual(api_services['status'], 'success')

    def test_service_delete_error(self):
        """Verify that service delete
        """
        service_id = 'service_id_00001'
        func_type = 'dcconnect'

        cli_param = {'operation_id': self.request.user.id,
                     'IaaS_tenant_id': self.request.user.project_id,
                     'IaaS_region_id': self.request.user.services_region}
        form_param = {'service_id': service_id,
                      'function_type': func_type,
                      'service_type': '1',
                      'apl_type': '1',
                      'type': '3',
                      'device_type': '1',
                      'job_cleaning_mode': '0'}
        cli_param.update(form_param)

        client = self.stub_nalclient()
        client.service = self.mox.CreateMockAnything()
        client.service.delete(cli_param).AndRaise(client_exc.InvalidEndpoint)
        self.mox.ReplayAll()

        self.assertRaises(client_exc.InvalidEndpoint,
                          api.nal_api.delete_service,
                          self.request,
                          form_param)
