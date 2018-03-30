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
from horizon import forms
from horizon import tables

from nec_portal.api import nal_api
from nec_portal.dashboards.project.resource import constants
from nec_portal.dashboards.project.resource \
    import forms as resource_forms
from nec_portal.dashboards.project.resource \
    import tables as resource_tables
from nec_portal.local import nal_portal_settings

LOG = logging.getLogger(__name__)
RESOURCE_DETAIL_DEF = getattr(nal_portal_settings,
                              'RESOURCE_DETAIL_DEF', None)
RESOURCE_UPDATE_DEF = getattr(nal_portal_settings,
                              'RESOURCE_UPDATE_DEF', None)
RESOURCE_FUNCTION_TYPE_MAPPING = \
    getattr(nal_portal_settings, 'RESOURCE_FUNCTION_TYPE_MAPPING', None)
RESOURCE_NAME_MAPPING = getattr(nal_portal_settings,
                                'RESOURCE_NAME_MAPPING', None)
RESOURCE_DISPLAY_NAME_MAPPING = \
    getattr(nal_portal_settings, 'RESOURCE_DISPLAY_NAME_MAPPING', None)
RESOURCE_SCREEN_TRANSITION = getattr(nal_portal_settings,
                                     'RESOURCE_SCREEN_TRANSITION', None)
RESOURCE_TASK_STATUS_MAPPING = getattr(nal_portal_settings,
                                       'RESOURCE_TASK_STATUS_MAPPING', None)


class IndexView(tables.DataTableView):
    table_class = resource_tables.ResourceTable
    template_name = constants.RESOURCE_INDEX_VIEW_TEMPLATE
    page_title = _("Resources")

    def get_data(self):
        resources = []
        try:
            tenant_id = self.request.user.project_id
            resource_api = nal_api.get_resources(self.request, tenant_id,
                                                 func_type='all_resource')
            resources = resource_api.get('contract_info', [])
        except Exception:
            exceptions.handle(self.request,
                              _('Unable to retrieve resource list.'))

        resource_list = []
        for resource in resources:
            functions = RESOURCE_FUNCTION_TYPE_MAPPING['project']
            func_type = functions[str(resource.contract_kind)]
            resource_name_map = RESOURCE_NAME_MAPPING[func_type]

            if isinstance(resource_name_map, dict)\
                    and resource.apl_type:
                resource_name_map = resource_name_map[str(resource.apl_type)]

            if isinstance(resource_name_map, dict)\
                    and resource.type:
                resource_name_map = resource_name_map[str(resource.type)]

            if isinstance(resource_name_map, dict)\
                    and resource.device_type:
                resource_name_map = \
                    resource_name_map[str(resource.device_type)]

            if isinstance(resource_name_map, dict)\
                    and resource.redundant:
                resource_name_map = resource_name_map[str(resource.redundant)]

            resource_name = RESOURCE_DISPLAY_NAME_MAPPING[resource_name_map]
            setattr(resource, 'func_type', func_type)
            setattr(resource, 'resource_key', resource_name_map)
            setattr(resource, 'resource_name', resource_name)
            resource_list.append(resource)
        return resource_list


class DetailView(tables.DataTableView):
    table_class = resource_tables.ResourceKindTable
    template_name = constants.RESOURCE_INDEX_VIEW_TEMPLATE
    page_title = _("Resource Detail")

    def get_data(self):
        resources = []
        try:
            func_type = self.kwargs['func_type']
            resource_key = self.kwargs['resource_key']

            resource_info = self.get_resource_info(func_type, resource_key)
            tenant_id = self.request.user.project_id
            resource_api = nal_api.get_resources(self.request, tenant_id,
                                                 func_type=func_type,
                                                 add_params=resource_info)
            resources = resource_api.get('contract_info', [])
        except Exception:
            msg = _('Unable to retrieve resource for each kind.')
            exceptions.handle(self.request, msg,
                              redirect=self.get_redirect_url())

        func_type = self.kwargs['func_type']
        task_status_name = RESOURCE_TASK_STATUS_MAPPING[func_type]
        resource_data = []
        for resource in resources:
            setattr(resource, 'func_type', func_type)
            resource.status_name = task_status_name[str(resource.task_status)]
            resource_data.append(resource)
        return resource_data

    def get_resource_info(self, func_type, resource_key):
        resource_map = RESOURCE_NAME_MAPPING[func_type]
        for apl_type, apl_info in resource_map.iteritems():
            for type, type_info in apl_info.iteritems():
                for device_type, device_info in type_info.iteritems():
                    if isinstance(device_info, str):
                        if device_info == resource_key:
                            return {'apl_type': apl_type,
                                    'type': type,
                                    'device_type': device_type}
                    else:
                        for red_flg, resource_info in device_info.iteritems():
                            if resource_info == resource_key:
                                return {'apl_type': apl_type,
                                        'type': type,
                                        'device_type': device_type,
                                        'redundant_configuration_flg': red_flg}

    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)

        title_name = RESOURCE_DISPLAY_NAME_MAPPING[self.kwargs['resource_key']]
        context["page_title"] = self.page_title + ": %s" % title_name

        return context

    @staticmethod
    def get_redirect_url():
        return reverse_lazy(constants.RESOURCE_INDEX_URL)


class DetailGlobalipView(tables.DataTableView):
    table_class = resource_tables.ResourceGlobalipTable
    template_name = constants.RESOURCE_INDEX_VIEW_TEMPLATE
    page_title = _("Resource Detail")

    def get_data(self):
        resources = []
        try:
            func_type = self.kwargs['func_type']
            tenant_id = self.request.user.project_id
            resource_api = nal_api.get_resources(self.request, tenant_id,
                                                 func_type=func_type)
            resources = resource_api.get('contract_info', [])
        except Exception:
            msg = _('Unable to retrieve resource for each kind.')
            exceptions.handle(self.request, msg,
                              redirect=self.get_redirect_url())

        resource_data = []
        for resource in resources:
            setattr(resource, 'func_type', func_type)
            resource_data.append(resource)
        return resource_data

    def get_context_data(self, **kwargs):
        context = super(DetailGlobalipView, self).get_context_data(**kwargs)

        title_name = RESOURCE_DISPLAY_NAME_MAPPING[self.kwargs['resource_key']]
        context["page_title"] = self.page_title + ": %s" % title_name

        return context

    @staticmethod
    def get_redirect_url():
        return reverse_lazy(constants.RESOURCE_INDEX_URL)


class CreateView(forms.ModalFormView):
    form_class = resource_forms.CreateResourceForm
    form_id = "create_resource_form"
    modal_header = _("Create Resource")
    template_name = constants.RESOURCE_CREATE_VIEW_TEMPLATE
    success_url = constants.RESOURCE_DETAIL_URL
    page_title = _("Create Resource")
    submit_label = _("Create Resource")
    submit_url = constants.RESOURCE_CREATE_URL

    def get_success_url(self):
        func_type = self.kwargs['resource_id'].split('|')[0]
        detail_table = RESOURCE_SCREEN_TRANSITION[func_type]
        set_args = '|'.join([self.kwargs['resource_id'], detail_table])
        return reverse(self.success_url, args=(set_args,))

    def get_context_data(self, **kwargs):
        context = super(CreateView, self).get_context_data(**kwargs)
        context['submit_url'] = reverse(self.submit_url,
                                        args=(self.kwargs['resource_id'],))
        return context

    def get_initial(self):
        return {'resource_id': self.kwargs['resource_id']}


class UpdateView(forms.ModalFormView):
    form_class = resource_forms.UpdateResourceForm
    form_id = "update_form"
    modal_header = _("Update Resource")
    template_name = constants.RESOURCE_UPDATE_VIEW_TEMPLATE
    success_url = constants.RESOURCE_DETAIL_URL
    page_title = _("Update Resource")
    submit_label = _("Update Resource")
    submit_url = constants.RESOURCE_UPDATE_URL

    def get_success_url(self):
        func_type = self.kwargs['resource_id'].split('|')[0]
        resource_key = self.kwargs['resource_id'].split('|')[1]
        detail_table = RESOURCE_SCREEN_TRANSITION[func_type]
        set_args = '|'.join([func_type, resource_key, detail_table])
        return reverse(self.success_url, args=(set_args,))

    def get_context_data(self, **kwargs):
        context = super(UpdateView, self).get_context_data(**kwargs)
        resource_id = self.kwargs['resource_id']
        update_type = self.kwargs['update_type']
        args = (resource_id, update_type)
        context['submit_url'] = reverse(self.submit_url, args=args)

        return context

    def get_initial(self):
        return {'resource_id': self.kwargs['resource_id'],
                'update_type': self.kwargs['update_type']}
