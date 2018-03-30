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
from nec_portal.dashboards.project.node import fixture
from nec_portal.local import nal_portal_settings
from openstack_dashboard.test import helpers as test

NODE_RETURN_MAPPING = getattr(nal_portal_settings, 'NODE_RETURN_MAPPING', None)


class NodeApiTests(test.APITestCase):

    def setUp(self):
        super(NodeApiTests, self).setUp()

        # Store the original clients
        self._original_nalclient = api.nal_api.client

        # Replace the clients with our stubs.
        api.nal_api.client = lambda request: self.stub_nalclient()

    def tearDown(self):
        super(NodeApiTests, self).tearDown()

        api.nal_api.client = self._original_nalclient

    def stub_nalclient(self):
        if not hasattr(self, "nalclient"):
            self.mox.StubOutWithMock(nalclient, 'Client')
            self.nalclient = self.mox.CreateMock(nalclient.Client)
        return self.nalclient

    def test_node_list_no_param(self):
        """Verify that node list
        """
        cli_nodes = fixture.NODE_DATA_LIST

        client = self.stub_nalclient()
        client.node = self.mox.CreateMockAnything()
        client.node.get({'operation_id': '1',
                         'function_type': 'all_node'}).AndReturn(cli_nodes)
        self.mox.ReplayAll()

        api_nodes = api.nal_api.get_nodes(self.request)

        for (api_node, cli_node) in zip(api_nodes, cli_nodes):
            if getattr(api_node, 'apl_type') == '1':
                apl_type_name = 'Virtual'
            else:
                apl_type_name = 'Physical'
            for key, value in NODE_RETURN_MAPPING['all_node'][apl_type_name]\
                    .iteritems():
                self.assertEqual(getattr(api_node, key),
                                 cli_node.get(value, ''))

    def test_node_list_all_param(self):
        """Verify that node list
        """

        input_param = {'IaaS_tenant_id': 'tenant_id_00001',
                       'apl_type': '1',
                       'type': '1',
                       'device_type': '1',
                       'ID': 'node_id_00001',
                       'function_type': 'all_node',
                       'operation_id': '1'}

        client = self.stub_nalclient()
        client.node = self.mox.CreateMockAnything()
        client.node.get(input_param).AndReturn([])
        self.mox.ReplayAll()

        api_nodes = api.nal_api.get_nodes(self.request,
                                          IaaS_tenant_id='tenant_id_00001',
                                          apl_type='1', type='1',
                                          device_type='1',
                                          rec_id='node_id_00001',
                                          func_type='all_node')

        self.assertEqual(api_nodes, [])

    def test_node_list_error(self):
        """Verify that node list
        """

        input_param = {'IaaS_tenant_id': 'tenant_id_00001',
                       'function_type': 'all_node',
                       'operation_id': '1'}

        client = self.stub_nalclient()
        client.node = self.mox.CreateMockAnything()
        client.node.get(input_param).AndRaise(OSError)
        self.mox.ReplayAll()

        self.assertRaises(OSError,
                          api.nal_api.get_nodes,
                          self.request,
                          IaaS_tenant_id='tenant_id_00001',
                          func_type='all_node')

    def test_node_detail(self):
        """Verify that node list
        """
        cli_nodes = fixture.NODE_DATA_VFW

        input_param = {'IaaS_tenant_id': 'tenant_id_00001',
                       'ID': 'node_id_00001',
                       'function_type': 'vfw',
                       'operation_id': '1'}

        client = self.stub_nalclient()
        client.node = self.mox.CreateMockAnything()
        client.node.get(input_param).AndReturn(cli_nodes)
        self.mox.ReplayAll()

        api_nodes = api.nal_api.get_nodes(self.request,
                                          IaaS_tenant_id='tenant_id_00001',
                                          rec_id='node_id_00001',
                                          func_type='vfw')

        for (api_node, cli_node) in zip(api_nodes['vnf_info'],
                                        cli_nodes['vnf_info']):
            for key, value in \
                    NODE_RETURN_MAPPING['vfw']['vnf_info'].iteritems():
                self.assertEqual(getattr(api_node, key),
                                 cli_node.get(value, ''))
        for (api_node, cli_node) in zip(api_nodes['port_info'],
                                        cli_nodes['port_info']):
            for key, value in \
                    NODE_RETURN_MAPPING['vfw']['port_info'].iteritems():
                self.assertEqual(getattr(api_node, key),
                                 cli_node.get(value, ''))

    def test_node_detail_no_network(self):
        """Verify that node detail
        """
        cli_nodes = fixture.NODE_DATA_NO_NET

        input_param = {'IaaS_tenant_id': 'tenant_id_00001',
                       'ID': 'node_id_00001',
                       'function_type': 'vlb',
                       'operation_id': '1'}

        client = self.stub_nalclient()
        client.node = self.mox.CreateMockAnything()
        client.node.get(input_param).AndReturn(cli_nodes)
        self.mox.ReplayAll()

        api_nodes = api.nal_api.get_nodes(self.request,
                                          IaaS_tenant_id='tenant_id_00001',
                                          rec_id='node_id_00001',
                                          func_type='vlb')

        for (api_node, cli_node) in zip(api_nodes['vnf_info'],
                                        cli_nodes['vnf_info']):
            for key, value in \
                    NODE_RETURN_MAPPING['vlb']['vnf_info'].iteritems():
                self.assertEqual(getattr(api_node, key),
                                 cli_node.get(value, ''))
        self.assertEqual(api_nodes['port_info'], [])

    def test_node_create(self):
        """Verify that node create
        """
        cli_nodes = {"status": "success",
                     "error-code": " NAL100000",
                     "message": ""}

        input_param = {'host_name': 'host_nameA',
                       'webclient_ip': '10.58.70.1',
                       'ntp_ip': '10.58.70.1',
                       'zabbix_vip_ip': '10.58.70.1',
                       'zabbix_01_ip': '10.58.70.1',
                       'zabbix_02_ip': '10.58.70.1',
                       'static_route_ip': '10.58.70.1',
                       'remarks': 'xxxxxxxxxxxxxxxxxxx',
                       'function_type': 'vfw'}

        cli_param = {'operation_id': self.request.user.id,
                     'IaaS_tenant_id': self.request.user.project_id,
                     'IaaS_tenant_name': self.request.user.project_name,
                     'IaaS_region_id': self.request.user.services_region}
        cli_param.update(input_param)

        client = self.stub_nalclient()
        client.node = self.mox.CreateMockAnything()
        client.node.create(cli_param).AndReturn(cli_nodes)
        self.mox.ReplayAll()

        api_nodes = api.nal_api.create_node(self.request, input_param)

        self.assertEqual(api_nodes['status'], 'success')

    def test_node_create_validate_error(self):
        """Verify that node create
        """
        input_param = {'host_name': 'host_nameA',
                       'webclient_ip': '10.58.70.1',
                       'ntp_ip': '10.58.70.1',
                       'zabbix_vip_ip': '10.58.70.1',
                       'zabbix_01_ip': '10.58.70.1',
                       'zabbix_02_ip': '10.58.70.1',
                       'static_route_ip': '10.58.70.1',
                       'remarks': 'xxxxxxxxxxxxxxxxxxx',
                       'function_type': 'vfw'}

        cli_param = {'operation_id': self.request.user.id,
                     'IaaS_tenant_id': self.request.user.project_id,
                     'IaaS_tenant_name': self.request.user.project_name,
                     'IaaS_region_id': self.request.user.services_region}
        cli_param.update(input_param)

        client = self.stub_nalclient()
        client.node = self.mox.CreateMockAnything()
        client.node.create(cli_param) \
            .AndRaise(client_exc.NalBadRequest('error_message'))

        self.mox.ReplayAll()

        self.request.META['HTTP_X_REQUESTED_WITH'] = 'XMLHttpRequest'
        self.assertRaises(exceptions.NotAvailable,
                          api.nal_api.create_node,
                          self.request,
                          input_param)

    def test_node_create_error(self):
        """Verify that node create
        """
        input_param = {'host_name': 'host_nameA',
                       'webclient_ip': '10.58.70.1',
                       'ntp_ip': '10.58.70.1',
                       'zabbix_vip_ip': '10.58.70.1',
                       'zabbix_01_ip': '10.58.70.1',
                       'zabbix_02_ip': '10.58.70.1',
                       'static_route_ip': '10.58.70.1',
                       'remarks': 'xxxxxxxxxxxxxxxxxxx',
                       'function_type': 'vfw'}

        cli_param = {'operation_id': self.request.user.id,
                     'IaaS_tenant_id': self.request.user.project_id,
                     'IaaS_tenant_name': self.request.user.project_name,
                     'IaaS_region_id': self.request.user.services_region}
        cli_param.update(input_param)

        client = self.stub_nalclient()
        client.node = self.mox.CreateMockAnything()
        client.node.create(cli_param).AndRaise(client_exc.InvalidEndpoint)
        self.mox.ReplayAll()

        self.assertRaises(client_exc.InvalidEndpoint,
                          api.nal_api.create_node,
                          self.request,
                          input_param)

    def test_node_update(self):
        """Verify that node update
        """
        cli_nodes = {"status": "success",
                     "error-code": " NAL100000",
                     "message": ""}

        input_param = {'IaaS_network_type': 'vxlan',
                       'IaaS_network_id': 'net_id_00001',
                       'function_type': 'vfw_port_p'}

        cli_param = {'operation_id': self.request.user.id,
                     'IaaS_tenant_id': self.request.user.project_id,
                     'IaaS_tenant_name': self.request.user.project_name,
                     'IaaS_region_id': self.request.user.services_region}
        cli_param.update(input_param)

        client = self.stub_nalclient()
        client.node = self.mox.CreateMockAnything()
        client.node.update(cli_param).AndReturn(cli_nodes)
        self.mox.ReplayAll()

        api_nodes = api.nal_api.update_node(self.request, input_param)

        self.assertEqual(api_nodes['status'], 'success')

    def test_node_update_validate_error(self):
        """Verify that node update
        """
        input_param = {'IaaS_network_type': 'vxlan',
                       'IaaS_network_id': 'net_id_00001',
                       'function_type': 'vfw_port_p'}

        cli_param = {'operation_id': self.request.user.id,
                     'IaaS_tenant_id': self.request.user.project_id,
                     'IaaS_tenant_name': self.request.user.project_name,
                     'IaaS_region_id': self.request.user.services_region}
        cli_param.update(input_param)

        client = self.stub_nalclient()
        client.node = self.mox.CreateMockAnything()
        client.node.update(cli_param) \
            .AndRaise(client_exc.NalBadRequest('error_message'))

        self.mox.ReplayAll()

        self.request.META['HTTP_X_REQUESTED_WITH'] = 'XMLHttpRequest'
        self.assertRaises(exceptions.NotAvailable,
                          api.nal_api.update_node,
                          self.request,
                          input_param)

    def test_node_update_error(self):
        """Verify that node update
        """
        input_param = {'IaaS_network_type': 'vxlan',
                       'IaaS_network_id': 'net_id_00001',
                       'function_type': 'vfw_port_p'}

        cli_param = {'operation_id': self.request.user.id,
                     'IaaS_tenant_id': self.request.user.project_id,
                     'IaaS_tenant_name': self.request.user.project_name,
                     'IaaS_region_id': self.request.user.services_region}
        cli_param.update(input_param)

        client = self.stub_nalclient()
        client.node = self.mox.CreateMockAnything()
        client.node.update(cli_param).AndRaise(client_exc.InvalidEndpoint)
        self.mox.ReplayAll()

        self.assertRaises(client_exc.InvalidEndpoint,
                          api.nal_api.update_node,
                          self.request,
                          input_param)

    def test_node_delete(self):
        """Verify that node delete
        """
        cli_nodes = {"status": "success",
                     "error-code": " NAL100000",
                     "message": ""}

        apl_table_rec_id = '188'
        func_type = 'vfw'
        device_type = '1'

        cli_param = {'operation_id': self.request.user.id,
                     'IaaS_tenant_id': self.request.user.project_id,
                     'IaaS_region_id': self.request.user.services_region}
        cli_param.update({'apl_table_rec_id': apl_table_rec_id,
                          'function_type': func_type,
                          'device_type': '1',
                          'job_cleaning_mode': '0'})

        client = self.stub_nalclient()
        client.node = self.mox.CreateMockAnything()
        client.node.delete(cli_param).AndReturn(cli_nodes)
        self.mox.ReplayAll()

        api_nodes = api.nal_api.delete_node(self.request, func_type,
                                            apl_table_rec_id, device_type)

        self.assertEqual(api_nodes['status'], 'success')

    def test_node_delete_error(self):
        """Verify that node delete
        """
        apl_table_rec_id = '189'
        func_type = 'vfw'
        device_type = '1'

        cli_param = {'operation_id': self.request.user.id,
                     'IaaS_tenant_id': self.request.user.project_id,
                     'IaaS_region_id': self.request.user.services_region}
        cli_param.update({'apl_table_rec_id': apl_table_rec_id,
                          'function_type': func_type,
                          'device_type': '1',
                          'job_cleaning_mode': '0'})

        client = self.stub_nalclient()
        client.node = self.mox.CreateMockAnything()
        client.node.delete(cli_param).AndRaise(client_exc.InvalidEndpoint)
        self.mox.ReplayAll()

        self.assertRaises(client_exc.InvalidEndpoint,
                          api.nal_api.delete_node,
                          self.request,
                          func_type,
                          apl_table_rec_id,
                          device_type,
                          '0')
