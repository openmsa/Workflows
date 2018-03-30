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


import logging

from django.core.urlresolvers import reverse
from django.core.urlresolvers import reverse_lazy
from django.utils.translation import ugettext_lazy as _

from horizon import exceptions
from horizon import tables
from horizon.utils import memoized

from openstack_dashboard import api

from nec_portal.api import nal_api
from nec_portal.dashboards.admin.resource import constants
from nec_portal.dashboards.admin.resource \
    import tables as resource_tables
from nec_portal.local import nal_portal_settings

LOG = logging.getLogger(__name__)
RESOURCE_DETAIL_DISPLAY_COLUMNS = \
    getattr(nal_portal_settings, 'RESOURCE_DETAIL_DISPLAY_COLUMNS', None)
RESOURCE_UPDATE_DEF = getattr(nal_portal_settings,
                              'RESOURCE_UPDATE_DEF', None)
RESOURCE_FUNCTION_TYPE_MAPPING = \
    getattr(nal_portal_settings, 'RESOURCE_FUNCTION_TYPE_MAPPING', None)
RESOURCE_NAME_MAPPING = \
    getattr(nal_portal_settings, 'RESOURCE_NAME_MAPPING', None)
RESOURCE_DISPLAY_NAME_MAPPING = \
    getattr(nal_portal_settings, 'RESOURCE_DISPLAY_NAME_MAPPING', None)
RESOURCE_TASK_STATUS_MAPPING = getattr(nal_portal_settings,
                                       'RESOURCE_TASK_STATUS_MAPPING', None)
RESOURCE_SCREEN_TRANSITION = getattr(nal_portal_settings,
                                     'RESOURCE_SCREEN_TRANSITION', None)


class IndexView(tables.DataTableView):
    table_class = resource_tables.ResourceTable
    template_name = constants.RESOURCE_INDEX_VIEW_TEMPLATE
    page_title = _("Resources")

    def get_data(self):
        resources = []
        try:
            resource_api = nal_api.get_resources(self.request,
                                                 func_type='all_resource')
            resources = resource_api.get('contract_info', [])
        except Exception:
            exceptions.handle(self.request,
                              _('Unable to retrieve resource list.'))

        resource_list = []
        for resource in resources:
            functions = RESOURCE_FUNCTION_TYPE_MAPPING['admin']
            func_type = functions[str(resource.nw_resource_kind)]
            resource_name_map = RESOURCE_NAME_MAPPING[func_type]

            if isinstance(resource_name_map, dict) \
                    and resource.type:
                resource_name_map = resource_name_map[str(resource.type)]

            if isinstance(resource_name_map, dict) \
                    and resource.device_type:
                resource_name_map = \
                    resource_name_map[str(resource.device_type)]

            if isinstance(resource_name_map, dict) \
                    and resource.type_detail:
                resource_name_map = \
                    resource_name_map[str(resource.type_detail)]

            if isinstance(resource_name_map, dict) \
                    and resource.redundant:
                resource_name_map = resource_name_map[str(resource.redundant)]

            resource_name = RESOURCE_DISPLAY_NAME_MAPPING[resource_name_map]
            setattr(resource, 'func_type', func_type)
            setattr(resource, 'resource_key', resource_name_map)
            setattr(resource, 'resource_name', resource_name)
            resource_list.append(resource)
        return resource_list


class LicenseDetailView(tables.DataTableView):
    table_class = resource_tables.LicenseDetailTable
    template_name = constants.RESOURCE_DETAIL_VIEW_TEMPLATE
    page_title = _("Resource Detail")

    @memoized.memoized_method
    def _get_data(self):
        try:
            func_type = self.kwargs['func_type']
            resource_key = self.kwargs['resource_key']

            resource_info = self.get_resource_info(func_type, resource_key)
            resource_api = nal_api.get_resources(self.request,
                                                 func_type=func_type,
                                                 add_params=resource_info)
        except Exception:
            msg = _('Unable to retrieve resource for each kind.')
            exceptions.handle(self.request, msg,
                              redirect=self.get_redirect_url())

        return resource_api

    def get_data(self):
        resource_api = self._get_data()
        resources = resource_api.get('contract_info', [])

        tenants = []
        try:
            tenants, _more = api.keystone.tenant_list(
                self.request,
                paginate=True)
        except Exception:
            msg = _('Unable to retrieve all tenant information.')
            exceptions.handle(self.request, msg,
                              redirect=self.get_redirect_url())

        tenant_names = {}
        for tenant in tenants:
            tenant_names[tenant.id] = tenant.name

        resource_list = []
        for resource in resources:
            resource.tenant_name = tenant_names.get(resource.tenant_id, None)
            resource_list.append(resource)

        return resource_list

    def get_context_data(self, **kwargs):
        context = super(LicenseDetailView, self).get_context_data(**kwargs)

        resource_api = self._get_data()
        detail_data = resource_api['total_info']

        detail_info = RESOURCE_DETAIL_DISPLAY_COLUMNS['license']
        context['resource'] = []
        for disp_info in detail_info['detail']:
            disp_data = getattr(detail_data, disp_info[1], '')
            if disp_data == '' and len(disp_info) == 3:
                disp_data = disp_info[2]
            contract_info = [disp_info[0], disp_data]
            context["resource"].append(contract_info)

        context["url"] = self.get_redirect_url()
        title_name = RESOURCE_DISPLAY_NAME_MAPPING[self.kwargs['resource_key']]
        context["page_title"] = self.page_title + ": %s" % title_name

        return context

    @staticmethod
    def get_redirect_url():
        return reverse_lazy(constants.RESOURCE_INDEX_URL)

    def get_resource_info(self, func_type, resource_key):
        resource_map = RESOURCE_NAME_MAPPING[func_type]
        for type, type_info in resource_map.iteritems():
            for device_type, device_info in type_info.iteritems():
                if isinstance(device_info, str):
                    if device_info == resource_key:
                        return {'type': type,
                                'device_type': device_type}
                else:
                    for type_detail, type_detail_info in \
                            device_info.iteritems():
                        if type_detail_info == resource_key:
                            return {'type': type,
                                    'device_type': device_type,
                                    'type_detail': type_detail}


class PnfDetailView(tables.DataTableView):
    table_class = resource_tables.PnfDetailTable
    template_name = constants.RESOURCE_DETAIL_VIEW_TEMPLATE
    page_title = _("Resource Detail")

    @memoized.memoized_method
    def _get_data(self):
        try:
            func_type = self.kwargs['func_type']
            resource_key = self.kwargs['resource_key']

            resource_info = self.get_resource_info(func_type, resource_key)
            resource_api = nal_api.get_resources(self.request,
                                                 func_type=func_type,
                                                 add_params=resource_info)
        except Exception:
            msg = _('Unable to retrieve resource for each kind.')
            exceptions.handle(self.request, msg,
                              redirect=self.get_redirect_url())

        return resource_api

    def get_data(self):
        resource_api = self._get_data()
        resources = resource_api.get('contract_info', [])

        tenants = []
        try:
            tenants, _more = api.keystone.tenant_list(
                self.request,
                paginate=True)
        except Exception:
            msg = _('Unable to retrieve all tenant information.')
            exceptions.handle(self.request, msg,
                              redirect=self.get_redirect_url())

        tenant_names = {}
        for tenant in tenants:
            tenant_names[tenant.id] = tenant.name

        func_type = self.kwargs['func_type']
        task_status_name = RESOURCE_TASK_STATUS_MAPPING[func_type]
        resource_list = []
        for resource in resources:
            resource.tenant_name = tenant_names.get(resource.tenant_id, None)
            resource.status_name = task_status_name[str(resource.task_status)]
            resource_list.append(resource)

        return resource_list

    def get_context_data(self, **kwargs):
        context = super(PnfDetailView, self).get_context_data(**kwargs)

        resource_api = self._get_data()
        detail_data = resource_api['total_info']

        detail_info = RESOURCE_DETAIL_DISPLAY_COLUMNS['license']
        context['resource'] = []
        for disp_info in detail_info['detail']:
            disp_data = getattr(detail_data, disp_info[1], '')
            if disp_data == '' and len(disp_info) == 3:
                disp_data = disp_info[2]
            contract_info = [disp_info[0], disp_data]
            context["resource"].append(contract_info)

        context["url"] = self.get_redirect_url()
        title_name = RESOURCE_DISPLAY_NAME_MAPPING[self.kwargs['resource_key']]
        context["page_title"] = self.page_title + ": %s" % title_name

        return context

    @staticmethod
    def get_redirect_url():
        return reverse_lazy(constants.RESOURCE_INDEX_URL)

    def get_resource_info(self, func_type, resource_key):
        resource_map = RESOURCE_NAME_MAPPING[func_type]
        if isinstance(resource_map, str):
            return {}

        for type, type_info in resource_map.iteritems():
            for device_type, device_info in type_info.iteritems():
                if isinstance(device_info, str):
                    if device_info == resource_key:
                        return {'type': type,
                                'device_type': device_type}
                else:
                    for redundant, redundant_info in device_info.iteritems():
                        if redundant_info == resource_key:
                            return {'type': type,
                                    'device_type': device_type,
                                    'redundant_configuration_flg': redundant}


class VlanDetailView(tables.DataTableView):
    table_class = resource_tables.VlanDetailTable
    template_name = constants.RESOURCE_DETAIL_VIEW_TEMPLATE
    page_title = _("Resource Detail")

    @memoized.memoized_method
    def _get_data(self):
        try:
            func_type = self.kwargs['func_type']
            resource_api = nal_api.get_resources(self.request,
                                                 func_type=func_type)
        except Exception:
            msg = _('Unable to retrieve resource for each kind.')
            exceptions.handle(self.request, msg,
                              redirect=self.get_redirect_url())

        return resource_api

    def get_data(self):
        resource_api = self._get_data()
        resources = resource_api.get('contract_info', [])

        tenants = []
        try:
            tenants, _more = api.keystone.tenant_list(
                self.request,
                paginate=True)
        except Exception:
            msg = _('Unable to retrieve all tenant information.')
            exceptions.handle(self.request, msg,
                              redirect=self.get_redirect_url())

        tenant_names = {}
        for tenant in tenants:
            tenant_names[tenant.id] = tenant.name

        func_type = self.kwargs['func_type']
        task_status_name = RESOURCE_TASK_STATUS_MAPPING[func_type]
        resource_list = []
        for resource in resources:
            resource.tenant_name = tenant_names.get(resource.tenant_id, None)
            resource.status_name = task_status_name[str(resource.task_status)]
            resource_list.append(resource)

        return resource_list

    def get_context_data(self, **kwargs):
        context = super(VlanDetailView, self).get_context_data(**kwargs)

        resource_api = self._get_data()
        detail_data = resource_api['total_info']

        detail_info = RESOURCE_DETAIL_DISPLAY_COLUMNS['vlan_id']
        context['resource'] = []
        for disp_info in detail_info['detail']:
            disp_data = getattr(detail_data, disp_info[1], '')
            if disp_data == '' and len(disp_info) == 3:
                disp_data = disp_info[2]
            contract_info = [disp_info[0], disp_data]
            context["resource"].append(contract_info)

        context["url"] = self.get_redirect_url()
        title_name = RESOURCE_DISPLAY_NAME_MAPPING[self.kwargs['resource_key']]
        context["page_title"] = self.page_title + ": %s" % title_name

        return context

    @staticmethod
    def get_redirect_url():
        return reverse_lazy(constants.RESOURCE_INDEX_URL)


class PodListDetailView(tables.DataTableView):
    table_class = resource_tables.PodListDetailTable
    template_name = constants.RESOURCE_DETAIL_VIEW_TEMPLATE
    page_title = _("Resource Detail")

    @memoized.memoized_method
    def _get_data(self):
        try:
            func_type = self.kwargs['func_type']
            resource_key = self.kwargs['resource_key']

            resource_info = self.get_resource_info(func_type, resource_key)
            resource_api = nal_api.get_resources(self.request,
                                                 func_type=func_type,
                                                 add_params=resource_info)
        except Exception:
            msg = _('Unable to retrieve resource for each kind.')
            exceptions.handle(self.request, msg,
                              redirect=self.get_redirect_url())

        return resource_api

    def get_data(self):
        resource_api = self._get_data()
        resources = resource_api.get('contract_info', [])

        func_type = self.kwargs['func_type']
        resource_key = self.kwargs['resource_key']
        resource_list = []
        for resource in resources:
            resource.func_type = func_type
            resource.resource_key = resource_key
            resource_list.append(resource)

        return resource_list

    def get_context_data(self, **kwargs):
        context = super(PodListDetailView, self).get_context_data(**kwargs)

        resource_api = self._get_data()
        detail_data = resource_api['total_info']

        detail_info = RESOURCE_DETAIL_DISPLAY_COLUMNS['pod_list']
        context['resource'] = []
        for disp_info in detail_info['detail']:
            disp_data = getattr(detail_data, disp_info[1], '')
            if disp_data == '' and len(disp_info) == 3:
                disp_data = disp_info[2]
            contract_info = [disp_info[0], disp_data]
            context["resource"].append(contract_info)

        context["url"] = self.get_redirect_url()
        title_name = RESOURCE_DISPLAY_NAME_MAPPING[self.kwargs['resource_key']]
        context["page_title"] = self.page_title + ": %s" % title_name

        return context

    @staticmethod
    def get_redirect_url():
        return reverse_lazy(constants.RESOURCE_INDEX_URL)

    def get_resource_info(self, func_type, resource_key):
        resource_map = RESOURCE_NAME_MAPPING[func_type]
        for type_detail, type_detail_info in resource_map.iteritems():
            if isinstance(type_detail_info, str):
                if type_detail_info == resource_key:
                    return {'type_detail': type_detail}


class PodDetailView(tables.DataTableView):
    table_class = resource_tables.PodDetailTable
    template_name = constants.RESOURCE_DETAIL_VIEW_TEMPLATE
    page_title = _("Resource Detail")

    @memoized.memoized_method
    def _get_data(self):
        try:
            func_type = self.kwargs['func_type']
            resource_key = self.kwargs['resource_key']
            pod_id = self.kwargs['pod_id']

            resource_info = self.get_resource_info(func_type, resource_key)
            resource_info['pod_id'] = pod_id
            resources = nal_api.get_resources(self.request,
                                              func_type=func_type,
                                              add_params=resource_info)
        except Exception:
            msg = _('Unable to retrieve resource for each kind.')
            exceptions.handle(self.request, msg,
                              redirect=self.get_redirect_url())

        return resources

    def get_data(self):
        resource_api = self._get_data()
        resources = resource_api.get('contract_info', [])

        tenants = []
        try:
            tenants, _more = api.keystone.tenant_list(
                self.request,
                paginate=True)
        except Exception:
            msg = _('Unable to retrieve all tenant information.')
            exceptions.handle(self.request, msg,
                              redirect=self.get_redirect_url())

        tenant_names = {}
        for tenant in tenants:
            tenant_names[tenant.id] = tenant.name

        func_type = self.kwargs['func_type']
        resource_list = []
        for resource in resources:
            resource.func_type = func_type
            resource.tenant_name = tenant_names.get(resource.tenant_id, None)
            resource_list.append(resource)

        return resource_list

    def get_context_data(self, **kwargs):
        context = super(PodDetailView, self).get_context_data(**kwargs)

        resource_api = self._get_data()
        detail_data = resource_api['total_info']

        detail_info = RESOURCE_DETAIL_DISPLAY_COLUMNS['pod_detail']
        context['resource'] = []
        for disp_info in detail_info['detail']:
            disp_data = getattr(detail_data, disp_info[1], '')
            if disp_data == '' and len(disp_info) == 3:
                disp_data = disp_info[2]
            contract_info = [disp_info[0], disp_data]
            context["resource"].append(contract_info)

        context["url"] = self.get_redirect_url()
        title_name = self.kwargs['pod_id']
        resource = RESOURCE_DISPLAY_NAME_MAPPING[self.kwargs['resource_key']]
        context["page_title"] = \
            self.page_title + ": %s" % resource + ": " + title_name

        return context

    def get_redirect_url(self):
        func_type = self.kwargs['func_type']
        resource_key = self.kwargs['resource_key']
        for front_func, next_func in \
                RESOURCE_FUNCTION_TYPE_MAPPING['admin_detail'].items():
            if next_func == func_type:
                set_func = front_func
                break
        detail_table = RESOURCE_SCREEN_TRANSITION[set_func]

        args = '|'.join([set_func, resource_key, detail_table])
        return reverse(constants.RESOURCE_DETAIL_URL,
                       args=(args,))

    def get_resource_info(self, func_type, resource_key):
        resource_map = RESOURCE_NAME_MAPPING[func_type]
        for type_detail, type_detail_info in resource_map.iteritems():
            if isinstance(type_detail_info, str):
                if type_detail_info == resource_key:
                    return {'type_detail': type_detail}
