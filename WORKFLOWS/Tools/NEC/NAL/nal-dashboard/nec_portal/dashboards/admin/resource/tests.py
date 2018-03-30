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

from nec_portal.api import nal_api
from nec_portal.dashboards.admin.resource import fixture
from nec_portal.dashboards.admin.resource import panel  # noqa
from nec_portal.local import nal_portal_settings

from openstack_dashboard import api
from openstack_dashboard.test import helpers as test


RESOURCE_INDEX_URL = reverse('horizon:admin:resource:index')
RESOURCE_DETAIL_URL = 'horizon:admin:resource:detail'

RESOURCE_RETURN_MAPPING = getattr(nal_portal_settings,
                                  'RESOURCE_RETURN_MAPPING', None)
NODE_RETURN_MAPPING = getattr(nal_portal_settings, 'NODE_RETURN_MAPPING', None)
RESOURCE_DETAIL_DEF = getattr(nal_portal_settings, 'RESOURCE_DETAIL_DEF', None)
RESOURCE_DETAIL_DISPLAY_COLUMNS = \
    getattr(nal_portal_settings, 'RESOURCE_DETAIL_DISPLAY_COLUMNS', None)


class ResourceViewTests(test.BaseAdminViewTests):

    @test.create_stubs({nal_api: ('get_resources',)})
    def test_index_multi_data(self):

        resource_data = {}
        for key, value in RESOURCE_RETURN_MAPPING['all_resource'].iteritems():
            if isinstance(value, dict):
                resource_data[key] = []
                for resource_row in fixture.RESOURCE_DATA_LIST[key]:
                    resource_data[key].append(Resource(resource_row, value))

        nal_api.get_resources(IsA(http.HttpRequest),
                              func_type='all_resource')\
            .AndReturn(resource_data)

        self.mox.ReplayAll()
        res = self.client.get(RESOURCE_INDEX_URL)
        self.assertNoFormErrors(res)
        self.assertTemplateUsed(res, 'admin/resource/index.html')
        self.assertItemsEqual(res.context['table'].data,
                              resource_data['contract_info'])

    @test.create_stubs({nal_api: ('get_resources',)})
    def test_index_no_data(self):

        resource_data = {}
        for key, value in RESOURCE_RETURN_MAPPING['all_resource'].iteritems():
            if isinstance(value, dict):
                resource_data[key] = []

        nal_api.get_resources(IsA(http.HttpRequest),
                              func_type='all_resource')\
            .AndReturn(resource_data)

        self.mox.ReplayAll()
        res = self.client.get(RESOURCE_INDEX_URL)
        self.assertNoFormErrors(res)
        self.assertTemplateUsed(res, 'admin/resource/index.html')
        self.assertItemsEqual(res.context['table'].data, [])

    @test.create_stubs({nal_api: ('get_resources',)})
    def test_index_api_error(self):

        nal_api.get_resources(IsA(http.HttpRequest),
                              func_type='all_resource').AndRaise(OSError)

        self.mox.ReplayAll()
        res = self.client.get(RESOURCE_INDEX_URL)
        self.assertTemplateUsed(res, 'admin/resource/index.html')
        self.assertMessageCount(res, error=1)

    @test.create_stubs({nal_api: ('get_resources',)})
    @test.create_stubs({api.keystone: ('tenant_list',)})
    def test_detail_license_data(self):
        resource_data = {}
        obj_id = '|'.join(['license',
                           'intersec_sg_ext',
                           'license_table'])
        for key, value in RESOURCE_RETURN_MAPPING['license'].iteritems():
            api_return_data = fixture.RESOURCE_DATA_LICENSE[key]
            if isinstance(api_return_data, dict):
                resource_data[key] = Resource(api_return_data, value)
            else:
                resource_data[key] = []
                for resource_row in api_return_data:
                    resource_data[key].append(Resource(resource_row, value))

        tenant_list = [{'id': 'aaa8f50f82da4370813e6ea797b1fb87',
                        'name': 'network_nameA'},
                       {'id': 'bbb8f50f82da4370813e6ea797b1fb87',
                        'name': 'network_nameB'},
                       {'id': 'ccc8f50f82da4370813e6ea797b1fb87',
                        'name': 'network_nameC'}]
        tenant_data = []
        for data in tenant_list:
            tenant_data.append(Tenant(data))

        nal_api.get_resources(IsA(http.HttpRequest),
                              func_type='license',
                              add_params=IsA({})).AndReturn(resource_data)

        api.keystone.tenant_list(IsA(http.HttpRequest),
                                 paginate=True).AndReturn([tenant_data, True])

        self.mox.ReplayAll()
        res = self.client.get(reverse(RESOURCE_DETAIL_URL,
                                      kwargs={"resource_id": obj_id}))
        self.assertNoFormErrors(res)
        self.assertTemplateUsed(res, 'admin/resource/detail.html')
        disp_column = RESOURCE_DETAIL_DISPLAY_COLUMNS['license']['detail']
        for i, detail in enumerate(disp_column):
            self.assertItemsEqual(res.context['resource'][i][0], detail[0])

    @test.create_stubs({nal_api: ('get_resources',)})
    @test.create_stubs({api.keystone: ('tenant_list',)})
    def test_detail_license_paloalto_data(self):
        resource_data = {}
        obj_id = '|'.join(['license',
                           'paloalto_vm_base',
                           'license_table'])
        for key, value in RESOURCE_RETURN_MAPPING['license'].iteritems():
            api_return_data = fixture.RESOURCE_DATA_LICENSE[key]
            if isinstance(api_return_data, dict):
                resource_data[key] = Resource(api_return_data, value)
            else:
                resource_data[key] = []
                for resource_row in api_return_data:
                    resource_data[key].append(Resource(resource_row, value))

        tenant_list = [{'id': 'aaa8f50f82da4370813e6ea797b1fb87',
                        'name': 'network_nameA'},
                       {'id': 'bbb8f50f82da4370813e6ea797b1fb87',
                        'name': 'network_nameB'},
                       {'id': 'ccc8f50f82da4370813e6ea797b1fb87',
                        'name': 'network_nameC'}]
        tenant_data = []
        for data in tenant_list:
            tenant_data.append(Tenant(data))

        nal_api.get_resources(IsA(http.HttpRequest),
                              func_type='license',
                              add_params=IsA({})).AndReturn(resource_data)

        api.keystone.tenant_list(IsA(http.HttpRequest),
                                 paginate=True).AndReturn([tenant_data, True])

        self.mox.ReplayAll()
        res = self.client.get(reverse(RESOURCE_DETAIL_URL,
                                      kwargs={"resource_id": obj_id}))
        self.assertNoFormErrors(res)
        self.assertTemplateUsed(res, 'admin/resource/detail.html')
        disp_column = RESOURCE_DETAIL_DISPLAY_COLUMNS['license']['detail']
        for i, detail in enumerate(disp_column):
            self.assertItemsEqual(res.context['resource'][i][0], detail[0])

    @test.create_stubs({nal_api: ('get_resources',)})
    @test.create_stubs({api.keystone: ('tenant_list',)})
    def test_detail_license_no_contract_info(self):
        resource_data = {}
        obj_id = '|'.join(['license',
                           'intersec_sg_ext',
                           'license_table'])
        for key, value in RESOURCE_RETURN_MAPPING['license'].iteritems():
            api_return_data = fixture.RESOURCE_DATA_LICENSE[key]
            if isinstance(api_return_data, dict):
                resource_data[key] = Resource(api_return_data, value)
            else:
                resource_data[key] = []

        tenant_list = [{'id': 'aaa8f50f82da4370813e6ea797b1fb87',
                        'name': 'network_nameA'},
                       {'id': 'bbb8f50f82da4370813e6ea797b1fb87',
                        'name': 'network_nameB'},
                       {'id': 'ccc8f50f82da4370813e6ea797b1fb87',
                        'name': 'network_nameC'}]
        tenant_data = []
        for data in tenant_list:
            tenant_data.append(Tenant(data))

        nal_api.get_resources(IsA(http.HttpRequest),
                              func_type='license',
                              add_params=IsA({})).AndReturn(resource_data)

        api.keystone.tenant_list(IsA(http.HttpRequest),
                                 paginate=True).AndReturn([tenant_data, True])

        self.mox.ReplayAll()
        res = self.client.get(reverse(RESOURCE_DETAIL_URL,
                                      kwargs={"resource_id": obj_id}))
        self.assertNoFormErrors(res)
        self.assertTemplateUsed(res, 'admin/resource/detail.html')
        disp_column = RESOURCE_DETAIL_DISPLAY_COLUMNS['license']['detail']
        for i, detail in enumerate(disp_column):
            self.assertItemsEqual(res.context['resource'][i][0], detail[0])

    @test.create_stubs({nal_api: ('get_resources',)})
    def test_detail_license_api_error(self):
        resource_data = {}
        obj_id = '|'.join(['license',
                           'intersec_sg_ext',
                           'license_table'])
        for key, value in RESOURCE_RETURN_MAPPING['license'].iteritems():
            api_return_data = fixture.RESOURCE_DATA_LICENSE[key]
            if isinstance(api_return_data, dict):
                resource_data[key] = Resource(api_return_data, value)
            else:
                resource_data[key] = []
                for resource_row in api_return_data:
                    resource_data[key].append(Resource(resource_row, value))

        nal_api.get_resources(IsA(http.HttpRequest),
                              func_type='license',
                              add_params=IsA({})).AndRaise(OSError)

        resource_data = {}
        for key, value in RESOURCE_RETURN_MAPPING['all_resource'].iteritems():
            if isinstance(value, dict):
                resource_data[key] = []
                for resource_row in fixture.RESOURCE_DATA_LIST[key]:
                    resource_data[key].append(Resource(resource_row, value))

        nal_api.get_resources(IsA(http.HttpRequest),
                              func_type='all_resource')\
            .AndReturn(resource_data)

        self.mox.ReplayAll()
        res = self.client.get(reverse(RESOURCE_DETAIL_URL,
                                      kwargs={"resource_id": obj_id}))
        self.assertRedirects(res, RESOURCE_INDEX_URL)

    @test.create_stubs({nal_api: ('get_resources',)})
    @test.create_stubs({api.keystone: ('tenant_list',)})
    def test_detail_license_tenant_error(self):
        resource_data = {}
        obj_id = '|'.join(['license',
                           'intersec_sg_ext',
                           'license_table'])
        for key, value in RESOURCE_RETURN_MAPPING['license'].iteritems():
            api_return_data = fixture.RESOURCE_DATA_LICENSE[key]
            if isinstance(api_return_data, dict):
                resource_data[key] = Resource(api_return_data, value)
            else:
                resource_data[key] = []
                for resource_row in api_return_data:
                    resource_data[key].append(Resource(resource_row, value))

        tenant_list = [{'id': 'aaa8f50f82da4370813e6ea797b1fb87',
                        'name': 'network_nameA'},
                       {'id': 'bbb8f50f82da4370813e6ea797b1fb87',
                        'name': 'network_nameB'},
                       {'id': 'ccc8f50f82da4370813e6ea797b1fb87',
                        'name': 'network_nameC'}]
        tenant_data = []
        for data in tenant_list:
            tenant_data.append(Tenant(data))

        nal_api.get_resources(IsA(http.HttpRequest),
                              func_type='license',
                              add_params=IsA({})).AndReturn(resource_data)

        api.keystone.tenant_list(IsA(http.HttpRequest),
                                 paginate=True).AndRaise(OSError)

        resource_data = {}
        for key, value in RESOURCE_RETURN_MAPPING['all_resource'].iteritems():
            if isinstance(value, dict):
                resource_data[key] = []
                for resource_row in fixture.RESOURCE_DATA_LIST[key]:
                    resource_data[key].append(Resource(resource_row, value))

        nal_api.get_resources(IsA(http.HttpRequest),
                              func_type='all_resource')\
            .AndReturn(resource_data)

        self.mox.ReplayAll()
        res = self.client.get(reverse(RESOURCE_DETAIL_URL,
                                      kwargs={"resource_id": obj_id}))
        self.assertRedirects(res, RESOURCE_INDEX_URL)

    @test.create_stubs({nal_api: ('get_resources',)})
    @test.create_stubs({api.keystone: ('tenant_list',)})
    def test_detail_pnf_data(self):
        resource_data = {}
        obj_id = '|'.join(['pnf',
                           'fortigate_redundancy',
                           'pnf_table'])
        for key, value in RESOURCE_RETURN_MAPPING['pnf'].iteritems():
            api_return_data = fixture.RESOURCE_DATA_PNF[key]
            if isinstance(api_return_data, dict):
                resource_data[key] = Resource(api_return_data, value)
            else:
                resource_data[key] = []
                for resource_row in api_return_data:
                    resource_data[key].append(Resource(resource_row, value))

        tenant_list = [{'id': 'aaa8f50f82da4370813e6ea797b1fb87',
                        'name': 'network_nameA'},
                       {'id': 'bbb8f50f82da4370813e6ea797b1fb87',
                        'name': 'network_nameB'},
                       {'id': 'ccc8f50f82da4370813e6ea797b1fb87',
                        'name': 'network_nameC'}]
        tenant_data = []
        for data in tenant_list:
            tenant_data.append(Tenant(data))

        nal_api.get_resources(IsA(http.HttpRequest),
                              func_type='pnf',
                              add_params=IsA({})).AndReturn(resource_data)

        api.keystone.tenant_list(IsA(http.HttpRequest),
                                 paginate=True).AndReturn([tenant_data, True])

        self.mox.ReplayAll()
        res = self.client.get(reverse(RESOURCE_DETAIL_URL,
                                      kwargs={"resource_id": obj_id}))
        self.assertNoFormErrors(res)
        self.assertTemplateUsed(res, 'admin/resource/detail.html')
        disp_column = RESOURCE_DETAIL_DISPLAY_COLUMNS['pnf_gip']['detail']
        for i, detail in enumerate(disp_column):
            self.assertItemsEqual(res.context['resource'][i][0], detail[0])

    @test.create_stubs({nal_api: ('get_resources',)})
    @test.create_stubs({api.keystone: ('tenant_list',)})
    def test_detail_pnf_share_data(self):
        resource_data = {}
        obj_id = '|'.join(['pnf',
                           'fortigate_share',
                           'pnf_table'])
        for key, value in RESOURCE_RETURN_MAPPING['pnf'].iteritems():
            api_return_data = fixture.RESOURCE_DATA_PNF[key]
            if isinstance(api_return_data, dict):
                resource_data[key] = Resource(api_return_data, value)
            else:
                resource_data[key] = []
                for resource_row in api_return_data:
                    resource_data[key].append(Resource(resource_row, value))

        tenant_list = [{'id': 'aaa8f50f82da4370813e6ea797b1fb87',
                        'name': 'network_nameA'},
                       {'id': 'bbb8f50f82da4370813e6ea797b1fb87',
                        'name': 'network_nameB'},
                       {'id': 'ccc8f50f82da4370813e6ea797b1fb87',
                        'name': 'network_nameC'}]
        tenant_data = []
        for data in tenant_list:
            tenant_data.append(Tenant(data))

        nal_api.get_resources(IsA(http.HttpRequest),
                              func_type='pnf',
                              add_params=IsA({})).AndReturn(resource_data)

        api.keystone.tenant_list(IsA(http.HttpRequest),
                                 paginate=True).AndReturn([tenant_data, True])

        self.mox.ReplayAll()
        res = self.client.get(reverse(RESOURCE_DETAIL_URL,
                                      kwargs={"resource_id": obj_id}))
        self.assertNoFormErrors(res)
        self.assertTemplateUsed(res, 'admin/resource/detail.html')
        disp_column = RESOURCE_DETAIL_DISPLAY_COLUMNS['pnf_gip']['detail']
        for i, detail in enumerate(disp_column):
            self.assertItemsEqual(res.context['resource'][i][0], detail[0])

    @test.create_stubs({nal_api: ('get_resources',)})
    @test.create_stubs({api.keystone: ('tenant_list',)})
    def test_detail_globalip_data(self):
        resource_data = {}
        obj_id = '|'.join(['globalip',
                           'global_ip',
                           'pnf_table'])
        for key, value in RESOURCE_RETURN_MAPPING['globalip'].iteritems():
            api_return_data = fixture.RESOURCE_DATA_GLOBALIP[key]
            if isinstance(api_return_data, dict):
                resource_data[key] = Resource(api_return_data, value)
            else:
                resource_data[key] = []
                for resource_row in api_return_data:
                    resource_data[key].append(Resource(resource_row, value))

        tenant_list = [{'id': 'aaa8f50f82da4370813e6ea797b1fb87',
                        'name': 'network_nameA'},
                       {'id': 'bbb8f50f82da4370813e6ea797b1fb87',
                        'name': 'network_nameB'},
                       {'id': 'ccc8f50f82da4370813e6ea797b1fb87',
                        'name': 'network_nameC'}]
        tenant_data = []
        for data in tenant_list:
            tenant_data.append(Tenant(data))

        nal_api.get_resources(IsA(http.HttpRequest),
                              func_type='globalip',
                              add_params=IsA({})).AndReturn(resource_data)

        api.keystone.tenant_list(IsA(http.HttpRequest),
                                 paginate=True).AndReturn([tenant_data, True])

        self.mox.ReplayAll()
        res = self.client.get(reverse(RESOURCE_DETAIL_URL,
                                      kwargs={"resource_id": obj_id}))
        self.assertNoFormErrors(res)
        self.assertTemplateUsed(res, 'admin/resource/detail.html')
        disp_column = RESOURCE_DETAIL_DISPLAY_COLUMNS['pnf_gip']['detail']
        for i, detail in enumerate(disp_column):
            self.assertItemsEqual(res.context['resource'][i][0], detail[0])

    @test.create_stubs({nal_api: ('get_resources',)})
    @test.create_stubs({api.keystone: ('tenant_list',)})
    def test_detail_pnf_no_contract_info(self):
        resource_data = {}
        obj_id = '|'.join(['pnf',
                           'fortigate_single',
                           'pnf_table'])
        for key, value in RESOURCE_RETURN_MAPPING['pnf'].iteritems():
            api_return_data = fixture.RESOURCE_DATA_PNF[key]
            if isinstance(api_return_data, dict):
                resource_data[key] = Resource(api_return_data, value)
            else:
                resource_data[key] = []

        tenant_list = [{'id': 'aaa8f50f82da4370813e6ea797b1fb87',
                        'name': 'network_nameA'},
                       {'id': 'bbb8f50f82da4370813e6ea797b1fb87',
                        'name': 'network_nameB'},
                       {'id': 'ccc8f50f82da4370813e6ea797b1fb87',
                        'name': 'network_nameC'}]
        tenant_data = []
        for data in tenant_list:
            tenant_data.append(Tenant(data))

        nal_api.get_resources(IsA(http.HttpRequest),
                              func_type='pnf',
                              add_params=IsA({})).AndReturn(resource_data)

        api.keystone.tenant_list(IsA(http.HttpRequest),
                                 paginate=True).AndReturn([tenant_data, True])

        self.mox.ReplayAll()
        res = self.client.get(reverse(RESOURCE_DETAIL_URL,
                                      kwargs={"resource_id": obj_id}))
        self.assertNoFormErrors(res)
        self.assertTemplateUsed(res, 'admin/resource/detail.html')
        disp_column = RESOURCE_DETAIL_DISPLAY_COLUMNS['pnf_gip']['detail']
        for i, detail in enumerate(disp_column):
            self.assertItemsEqual(res.context['resource'][i][0], detail[0])

    @test.create_stubs({nal_api: ('get_resources',)})
    def test_detail_pnf_api_error(self):
        resource_data = {}
        obj_id = '|'.join(['pnf',
                           'fortigate_single',
                           'pnf_table'])
        for key, value in RESOURCE_RETURN_MAPPING['pnf'].iteritems():
            api_return_data = fixture.RESOURCE_DATA_PNF[key]
            if isinstance(api_return_data, dict):
                resource_data[key] = Resource(api_return_data, value)
            else:
                resource_data[key] = []
                for resource_row in api_return_data:
                    resource_data[key].append(Resource(resource_row, value))

        nal_api.get_resources(IsA(http.HttpRequest),
                              func_type='pnf',
                              add_params=IsA({})).AndRaise(OSError)

        resource_data = {}
        for key, value in RESOURCE_RETURN_MAPPING['all_resource'].iteritems():
            if isinstance(value, dict):
                resource_data[key] = []
                for resource_row in fixture.RESOURCE_DATA_LIST[key]:
                    resource_data[key].append(Resource(resource_row, value))

        nal_api.get_resources(IsA(http.HttpRequest),
                              func_type='all_resource')\
            .AndReturn(resource_data)

        self.mox.ReplayAll()
        res = self.client.get(reverse(RESOURCE_DETAIL_URL,
                                      kwargs={"resource_id": obj_id}))
        self.assertRedirects(res, RESOURCE_INDEX_URL)

    @test.create_stubs({nal_api: ('get_resources',)})
    @test.create_stubs({api.keystone: ('tenant_list',)})
    def test_detail_pnf_tenant_error(self):
        resource_data = {}
        obj_id = '|'.join(['pnf',
                           'fortigate_single',
                           'pnf_table'])
        for key, value in RESOURCE_RETURN_MAPPING['pnf'].iteritems():
            api_return_data = fixture.RESOURCE_DATA_PNF[key]
            if isinstance(api_return_data, dict):
                resource_data[key] = Resource(api_return_data, value)
            else:
                resource_data[key] = []
                for resource_row in api_return_data:
                    resource_data[key].append(Resource(resource_row, value))

        tenant_list = [{'id': 'aaa8f50f82da4370813e6ea797b1fb87',
                        'name': 'network_nameA'},
                       {'id': 'bbb8f50f82da4370813e6ea797b1fb87',
                        'name': 'network_nameB'},
                       {'id': 'ccc8f50f82da4370813e6ea797b1fb87',
                        'name': 'network_nameC'}]
        tenant_data = []
        for data in tenant_list:
            tenant_data.append(Tenant(data))

        nal_api.get_resources(IsA(http.HttpRequest),
                              func_type='pnf',
                              add_params=IsA({})).AndReturn(resource_data)

        api.keystone.tenant_list(IsA(http.HttpRequest),
                                 paginate=True).AndRaise(OSError)

        resource_data = {}
        for key, value in RESOURCE_RETURN_MAPPING['all_resource'].iteritems():
            if isinstance(value, dict):
                resource_data[key] = []
                for resource_row in fixture.RESOURCE_DATA_LIST[key]:
                    resource_data[key].append(Resource(resource_row, value))

        nal_api.get_resources(IsA(http.HttpRequest),
                              func_type='all_resource')\
            .AndReturn(resource_data)

        self.mox.ReplayAll()
        res = self.client.get(reverse(RESOURCE_DETAIL_URL,
                                      kwargs={"resource_id": obj_id}))
        self.assertRedirects(res, RESOURCE_INDEX_URL)

    @test.create_stubs({nal_api: ('get_resources',)})
    @test.create_stubs({api.keystone: ('tenant_list',)})
    def test_detail_msa_vlan_data(self):
        resource_data = {}
        obj_id = '|'.join(['msa_vlan',
                           'msa_vlan',
                           'vlan_table'])
        for key, value in RESOURCE_RETURN_MAPPING['msa_vlan'].iteritems():
            api_return_data = fixture.RESOURCE_DATA_MSA_VLAN[key]
            if isinstance(api_return_data, dict):
                resource_data[key] = Resource(api_return_data, value)
            else:
                resource_data[key] = []
                for resource_row in api_return_data:
                    resource_data[key].append(Resource(resource_row, value))

        tenant_list = [{'id': 'aaa8f50f82da4370813e6ea797b1fb87',
                        'name': 'network_nameA'},
                       {'id': 'bbb8f50f82da4370813e6ea797b1fb87',
                        'name': 'network_nameB'},
                       {'id': 'ccc8f50f82da4370813e6ea797b1fb87',
                        'name': 'network_nameC'}]
        tenant_data = []
        for data in tenant_list:
            tenant_data.append(Tenant(data))

        nal_api.get_resources(IsA(http.HttpRequest),
                              func_type='msa_vlan').AndReturn(resource_data)

        api.keystone.tenant_list(IsA(http.HttpRequest),
                                 paginate=True).AndReturn([tenant_data, True])

        self.mox.ReplayAll()
        res = self.client.get(reverse(RESOURCE_DETAIL_URL,
                                      kwargs={"resource_id": obj_id}))
        self.assertNoFormErrors(res)
        self.assertTemplateUsed(res, 'admin/resource/detail.html')
        disp_column = RESOURCE_DETAIL_DISPLAY_COLUMNS['vlan_id']['detail']
        for i, detail in enumerate(disp_column):
            self.assertItemsEqual(res.context['resource'][i][0], detail[0])

    @test.create_stubs({nal_api: ('get_resources',)})
    @test.create_stubs({api.keystone: ('tenant_list',)})
    def test_detail_msa_vlan_no_contract_info(self):
        resource_data = {}
        obj_id = '|'.join(['msa_vlan',
                           'msa_vlan',
                           'vlan_table'])
        for key, value in RESOURCE_RETURN_MAPPING['msa_vlan'].iteritems():
            api_return_data = fixture.RESOURCE_DATA_MSA_VLAN[key]
            if isinstance(api_return_data, dict):
                resource_data[key] = Resource(api_return_data, value)
            else:
                resource_data[key] = []

        tenant_list = [{'id': 'aaa8f50f82da4370813e6ea797b1fb87',
                        'name': 'network_nameA'},
                       {'id': 'bbb8f50f82da4370813e6ea797b1fb87',
                        'name': 'network_nameB'},
                       {'id': 'ccc8f50f82da4370813e6ea797b1fb87',
                        'name': 'network_nameC'}]
        tenant_data = []
        for data in tenant_list:
            tenant_data.append(Tenant(data))

        nal_api.get_resources(IsA(http.HttpRequest),
                              func_type='msa_vlan').AndReturn(resource_data)

        api.keystone.tenant_list(IsA(http.HttpRequest),
                                 paginate=True).AndReturn([tenant_data, True])

        self.mox.ReplayAll()
        res = self.client.get(reverse(RESOURCE_DETAIL_URL,
                                      kwargs={"resource_id": obj_id}))
        self.assertNoFormErrors(res)
        self.assertTemplateUsed(res, 'admin/resource/detail.html')
        disp_column = RESOURCE_DETAIL_DISPLAY_COLUMNS['vlan_id']['detail']
        for i, detail in enumerate(disp_column):
            self.assertItemsEqual(res.context['resource'][i][0], detail[0])

    @test.create_stubs({nal_api: ('get_resources',)})
    def test_detail_vlan_api_error(self):
        resource_data = {}
        obj_id = '|'.join(['msa_vlan',
                           'msa_vlan',
                           'vlan_table'])
        for key, value in RESOURCE_RETURN_MAPPING['msa_vlan'].iteritems():
            api_return_data = fixture.RESOURCE_DATA_MSA_VLAN[key]
            if isinstance(api_return_data, dict):
                resource_data[key] = Resource(api_return_data, value)
            else:
                resource_data[key] = []
                for resource_row in api_return_data:
                    resource_data[key].append(Resource(resource_row, value))

        nal_api.get_resources(IsA(http.HttpRequest),
                              func_type='msa_vlan').AndRaise(OSError)

        resource_data = {}
        for key, value in RESOURCE_RETURN_MAPPING['all_resource'].iteritems():
            if isinstance(value, dict):
                resource_data[key] = []
                for resource_row in fixture.RESOURCE_DATA_LIST[key]:
                    resource_data[key].append(Resource(resource_row, value))

        nal_api.get_resources(IsA(http.HttpRequest),
                              func_type='all_resource')\
            .AndReturn(resource_data)

        self.mox.ReplayAll()
        res = self.client.get(reverse(RESOURCE_DETAIL_URL,
                                      kwargs={"resource_id": obj_id}))
        self.assertRedirects(res, RESOURCE_INDEX_URL)

    @test.create_stubs({nal_api: ('get_resources',)})
    @test.create_stubs({api.keystone: ('tenant_list',)})
    def test_detail_vlan_tenant_error(self):
        resource_data = {}
        obj_id = '|'.join(['msa_vlan',
                           'msa_vlan',
                           'vlan_table'])
        for key, value in RESOURCE_RETURN_MAPPING['msa_vlan'].iteritems():
            api_return_data = fixture.RESOURCE_DATA_MSA_VLAN[key]
            if isinstance(api_return_data, dict):
                resource_data[key] = Resource(api_return_data, value)
            else:
                resource_data[key] = []
                for resource_row in api_return_data:
                    resource_data[key].append(Resource(resource_row, value))

        tenant_list = [{'id': 'aaa8f50f82da4370813e6ea797b1fb87',
                        'name': 'network_nameA'},
                       {'id': 'bbb8f50f82da4370813e6ea797b1fb87',
                        'name': 'network_nameB'},
                       {'id': 'ccc8f50f82da4370813e6ea797b1fb87',
                        'name': 'network_nameC'}]
        tenant_data = []
        for data in tenant_list:
            tenant_data.append(Tenant(data))

        nal_api.get_resources(IsA(http.HttpRequest),
                              func_type='msa_vlan').AndReturn(resource_data)

        api.keystone.tenant_list(IsA(http.HttpRequest),
                                 paginate=True).AndRaise(OSError)

        resource_data = {}
        for key, value in RESOURCE_RETURN_MAPPING['all_resource'].iteritems():
            if isinstance(value, dict):
                resource_data[key] = []
                for resource_row in fixture.RESOURCE_DATA_LIST[key]:
                    resource_data[key].append(Resource(resource_row, value))

        nal_api.get_resources(IsA(http.HttpRequest),
                              func_type='all_resource')\
            .AndReturn(resource_data)

        self.mox.ReplayAll()
        res = self.client.get(reverse(RESOURCE_DETAIL_URL,
                                      kwargs={"resource_id": obj_id}))
        self.assertRedirects(res, RESOURCE_INDEX_URL)

    @test.create_stubs({nal_api: ('get_resources',)})
    @test.create_stubs({api.keystone: ('tenant_list',)})
    def test_detail_pod_list_data(self):
        resource_data = {}
        obj_id = '|'.join(['cpu_list',
                           'cpu(vim)',
                           'pod_list_table'])
        for key, value in RESOURCE_RETURN_MAPPING['cpu_list'].iteritems():
            api_return_data = fixture.RESOURCE_DATA_POD_LIST[key]
            if isinstance(api_return_data, dict):
                resource_data[key] = Resource(api_return_data, value)
            else:
                resource_data[key] = []
                for resource_row in api_return_data:
                    resource_data[key].append(Resource(resource_row, value))

        nal_api.get_resources(IsA(http.HttpRequest),
                              func_type='cpu_list',
                              add_params=IsA({})).AndReturn(resource_data)

        self.mox.ReplayAll()
        res = self.client.get(reverse(RESOURCE_DETAIL_URL,
                                      kwargs={"resource_id": obj_id}))
        self.assertNoFormErrors(res)
        self.assertTemplateUsed(res, 'admin/resource/detail.html')
        disp_column = RESOURCE_DETAIL_DISPLAY_COLUMNS['pod_list']['detail']
        for i, detail in enumerate(disp_column):
            self.assertItemsEqual(res.context['resource'][i][0], detail[0])

    @test.create_stubs({nal_api: ('get_resources',)})
    @test.create_stubs({api.keystone: ('tenant_list',)})
    def test_detail_pod_list_no_contract_info(self):
        resource_data = {}
        obj_id = '|'.join(['cpu_list',
                           'cpu(vim)',
                           'pod_list_table'])
        for key, value in RESOURCE_RETURN_MAPPING['cpu_list'].iteritems():
            api_return_data = fixture.RESOURCE_DATA_POD_LIST[key]
            if isinstance(api_return_data, dict):
                resource_data[key] = Resource(api_return_data, value)
            else:
                resource_data[key] = []

        nal_api.get_resources(IsA(http.HttpRequest),
                              func_type='cpu_list',
                              add_params=IsA({})).AndReturn(resource_data)

        self.mox.ReplayAll()
        res = self.client.get(reverse(RESOURCE_DETAIL_URL,
                                      kwargs={"resource_id": obj_id}))
        self.assertNoFormErrors(res)
        self.assertTemplateUsed(res, 'admin/resource/detail.html')
        disp_column = RESOURCE_DETAIL_DISPLAY_COLUMNS['pod_list']['detail']
        for i, detail in enumerate(disp_column):
            self.assertItemsEqual(res.context['resource'][i][0], detail[0])

    @test.create_stubs({nal_api: ('get_resources',)})
    def test_detail_pod_list_api_error(self):
        resource_data = {}
        obj_id = '|'.join(['cpu_list',
                           'cpu(vim)',
                           'pod_list_table'])
        for key, value in RESOURCE_RETURN_MAPPING['cpu_list'].iteritems():
            api_return_data = fixture.RESOURCE_DATA_POD_LIST[key]
            if isinstance(api_return_data, dict):
                resource_data[key] = Resource(api_return_data, value)
            else:
                resource_data[key] = []
                for resource_row in api_return_data:
                    resource_data[key].append(Resource(resource_row, value))

        nal_api.get_resources(IsA(http.HttpRequest),
                              func_type='cpu_list',
                              add_params=IsA({})).AndRaise(OSError)

        resource_data = {}
        for key, value in RESOURCE_RETURN_MAPPING['all_resource'].iteritems():
            if isinstance(value, dict):
                resource_data[key] = []
                for resource_row in fixture.RESOURCE_DATA_LIST[key]:
                    resource_data[key].append(Resource(resource_row, value))

        nal_api.get_resources(IsA(http.HttpRequest),
                              func_type='all_resource')\
            .AndReturn(resource_data)

        self.mox.ReplayAll()
        res = self.client.get(reverse(RESOURCE_DETAIL_URL,
                                      kwargs={"resource_id": obj_id}))
        self.assertRedirects(res, RESOURCE_INDEX_URL)

    @test.create_stubs({nal_api: ('get_resources',)})
    @test.create_stubs({api.keystone: ('tenant_list',)})
    def test_detail_pod_detail_data(self):
        resource_data = {}
        obj_id = '|'.join(['cpu_detail',
                           'cpu(wim)',
                           'pod0001',
                           'pod_detail_table'])
        for key, value in RESOURCE_RETURN_MAPPING['cpu_detail'].iteritems():
            api_return_data = fixture.RESOURCE_DATA_POD_DETAIL[key]
            if isinstance(api_return_data, dict):
                resource_data[key] = Resource(api_return_data, value)
            else:
                resource_data[key] = []
                for resource_row in api_return_data:
                    resource_data[key].append(Resource(resource_row, value))

        tenant_list = [{'id': 'aaa8f50f82da4370813e6ea797b1fb87',
                        'name': 'network_nameA'},
                       {'id': 'bbb8f50f82da4370813e6ea797b1fb87',
                        'name': 'network_nameB'},
                       {'id': 'ccc8f50f82da4370813e6ea797b1fb87',
                        'name': 'network_nameC'}]
        tenant_data = []
        for data in tenant_list:
            tenant_data.append(Tenant(data))

        nal_api.get_resources(IsA(http.HttpRequest),
                              func_type='cpu_detail',
                              add_params=IsA({})).AndReturn(resource_data)

        api.keystone.tenant_list(IsA(http.HttpRequest),
                                 paginate=True).AndReturn([tenant_data, True])

        self.mox.ReplayAll()
        res = self.client.get(reverse(RESOURCE_DETAIL_URL,
                                      kwargs={"resource_id": obj_id}))
        self.assertNoFormErrors(res)
        self.assertTemplateUsed(res, 'admin/resource/detail.html')
        disp_column = RESOURCE_DETAIL_DISPLAY_COLUMNS['pod_detail']['detail']
        for i, detail in enumerate(disp_column):
            self.assertItemsEqual(res.context['resource'][i][0], detail[0])

    @test.create_stubs({nal_api: ('get_resources',)})
    @test.create_stubs({api.keystone: ('tenant_list',)})
    def test_detail_pod_detail_no_contract_info(self):
        resource_data = {}
        obj_id = '|'.join(['cpu_detail',
                           'cpu(vim)',
                           'pod0001',
                           'pod_detail_table'])
        for key, value in RESOURCE_RETURN_MAPPING['cpu_detail'].iteritems():
            api_return_data = fixture.RESOURCE_DATA_POD_DETAIL[key]
            if isinstance(api_return_data, dict):
                resource_data[key] = Resource(api_return_data, value)
            else:
                resource_data[key] = []

        tenant_list = [{'id': 'aaa8f50f82da4370813e6ea797b1fb87',
                        'name': 'network_nameA'},
                       {'id': 'bbb8f50f82da4370813e6ea797b1fb87',
                        'name': 'network_nameB'},
                       {'id': 'ccc8f50f82da4370813e6ea797b1fb87',
                        'name': 'network_nameC'}]
        tenant_data = []
        for data in tenant_list:
            tenant_data.append(Tenant(data))

        nal_api.get_resources(IsA(http.HttpRequest),
                              func_type='cpu_detail',
                              add_params=IsA({})).AndReturn(resource_data)

        api.keystone.tenant_list(IsA(http.HttpRequest),
                                 paginate=True).AndReturn([tenant_data, True])

        self.mox.ReplayAll()
        res = self.client.get(reverse(RESOURCE_DETAIL_URL,
                                      kwargs={"resource_id": obj_id}))
        self.assertNoFormErrors(res)
        self.assertTemplateUsed(res, 'admin/resource/detail.html')
        disp_column = RESOURCE_DETAIL_DISPLAY_COLUMNS['pod_detail']['detail']
        for i, detail in enumerate(disp_column):
            self.assertItemsEqual(res.context['resource'][i][0], detail[0])

    @test.create_stubs({nal_api: ('get_resources',)})
    def test_detail_pod_detail_api_error(self):
        obj_id = '|'.join(['cpu_detail',
                           'cpu(vim)',
                           'pod0001',
                           'pod_detail_table'])

        nal_api.get_resources(IsA(http.HttpRequest),
                              func_type='cpu_detail',
                              add_params=IsA({})).AndRaise(OSError)

        resource_data = {}
        for key, value in RESOURCE_RETURN_MAPPING['cpu_list'].iteritems():
            api_return_data = fixture.RESOURCE_DATA_POD_LIST[key]
            if isinstance(api_return_data, dict):
                resource_data[key] = Resource(api_return_data, value)
            else:
                resource_data[key] = []
                for resource_row in api_return_data:
                    resource_data[key].append(Resource(resource_row, value))

        nal_api.get_resources(IsA(http.HttpRequest),
                              func_type='cpu_list',
                              add_params=IsA({})).AndReturn(resource_data)

        self.mox.ReplayAll()
        res = self.client.get(reverse(RESOURCE_DETAIL_URL,
                                      kwargs={"resource_id": obj_id}))

        obj_id = '|'.join(['cpu_list',
                           'cpu(vim)',
                           'pod_list_table'])
        self.assertRedirects(res, reverse(RESOURCE_DETAIL_URL,
                                          kwargs={"resource_id": obj_id}))

    @test.create_stubs({nal_api: ('get_resources',)})
    @test.create_stubs({api.keystone: ('tenant_list',)})
    def test_detail_pod_detail_tenant_error(self):
        resource_data = {}
        obj_id = '|'.join(['cpu_detail',
                           'cpu(vim)',
                           'pod0001',
                           'pod_detail_table'])
        for key, value in RESOURCE_RETURN_MAPPING['cpu_detail'].iteritems():
            api_return_data = fixture.RESOURCE_DATA_POD_DETAIL[key]
            if isinstance(api_return_data, dict):
                resource_data[key] = Resource(api_return_data, value)
            else:
                resource_data[key] = []
                for resource_row in api_return_data:
                    resource_data[key].append(Resource(resource_row, value))

        tenant_list = [{'id': 'aaa8f50f82da4370813e6ea797b1fb87',
                        'name': 'network_nameA'},
                       {'id': 'bbb8f50f82da4370813e6ea797b1fb87',
                        'name': 'network_nameB'},
                       {'id': 'ccc8f50f82da4370813e6ea797b1fb87',
                        'name': 'network_nameC'}]
        tenant_data = []
        for data in tenant_list:
            tenant_data.append(Tenant(data))

        nal_api.get_resources(IsA(http.HttpRequest),
                              func_type='cpu_detail',
                              add_params=IsA({})).AndReturn(resource_data)

        api.keystone.tenant_list(IsA(http.HttpRequest),
                                 paginate=True).AndRaise(OSError)

        resource_data = {}
        for key, value in RESOURCE_RETURN_MAPPING['cpu_list'].iteritems():
            api_return_data = fixture.RESOURCE_DATA_POD_LIST[key]
            if isinstance(api_return_data, dict):
                resource_data[key] = Resource(api_return_data, value)
            else:
                resource_data[key] = []
                for resource_row in api_return_data:
                    resource_data[key].append(Resource(resource_row, value))

        nal_api.get_resources(IsA(http.HttpRequest),
                              func_type='cpu_list',
                              add_params=IsA({})).AndReturn(resource_data)

        self.mox.ReplayAll()
        res = self.client.get(reverse(RESOURCE_DETAIL_URL,
                                      kwargs={"resource_id": obj_id}))

        obj_id = '|'.join(['cpu_list',
                           'cpu(vim)',
                           'pod_list_table'])
        self.assertRedirects(res, reverse(RESOURCE_DETAIL_URL,
                                          kwargs={"resource_id": obj_id}))


class Tenant(object):
    """Tenant class"""
    def __init__(self, network_data):

        for key, value in network_data.iteritems():
                self.__dict__[key] = value


class Resource(object):
    """Resource class"""
    def __init__(self, return_obj, mapping):

        for key, value in mapping.iteritems():
            set_value = return_obj.get(value, '')
            self.__dict__[key] = set_value
