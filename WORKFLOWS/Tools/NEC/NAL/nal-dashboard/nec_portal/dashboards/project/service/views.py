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
from horizon.utils import memoized

from nec_portal.api import nal_api
from nec_portal.dashboards.project.service import constants
from nec_portal.dashboards.project.service \
    import forms as service_forms
from nec_portal.dashboards.project.service \
    import tables as service_tables
from nec_portal.local import nal_portal_settings

LOG = logging.getLogger(__name__)
SERVICE_DETAIL_DISPLAY_COLUMNS = \
    getattr(nal_portal_settings, 'SERVICE_DETAIL_DISPLAY_COLUMNS', None)
SERVICE_UPDATE_COLUMNS = getattr(nal_portal_settings,
                                 'SERVICE_UPDATE_COLUMNS', None)
SERVICE_TYPE_MAPPING = getattr(nal_portal_settings,
                               'SERVICE_TYPE_MAPPING', None)
STATUS_MAPPING = getattr(nal_portal_settings, 'STATUS_MAPPING', None)


class IndexView(tables.DataTableView):
    table_class = service_tables.ServiceTable
    template_name = constants.SERVICE_INDEX_VIEW_TEMPLATE
    page_title = _("Services")

    def get_data(self):
        services = []
        try:
            tenant_id = self.request.user.project_id
            services = nal_api.get_services(self.request, tenant_id,
                                            func_type='all_dcconnect')
        except Exception:
            exceptions.handle(self.request,
                              _('Unable to retrieve service list.'))

        return services


class DetailView(tables.MultiTableView):
    table_classes = (service_tables.MemberTable, service_tables.NetworkTable)
    template_name = constants.SERVICE_DETAIL_VIEW_TEMPLATE
    page_title = _("Service Details: {{ service.name }}")

    @memoized.memoized_method
    def _get_data(self):
        try:
            func_type = self.kwargs['group_id'].split('|')[0]
            group_id = self.kwargs['group_id'].split('|')[1]
            service = nal_api.get_services(self.request, group_id=group_id,
                                           func_type=func_type)
        except Exception:
            msg = _('Unable to retrieve details for service "%s".') \
                % (group_id)
            exceptions.handle(self.request, msg,
                              redirect=self.get_redirect_url())
        return service

    def get_member_data(self):
        func_type = self.kwargs['group_id'].split('|')[0]
        detail_service = self._get_data()
        member_data = []

        network_name = \
            SERVICE_DETAIL_DISPLAY_COLUMNS[func_type]['network_name']
        detail_name = SERVICE_DETAIL_DISPLAY_COLUMNS[func_type]['detail_name']

        check_dc = []
        for network in detail_service[network_name]:
            if getattr(network, 'dc_id') not in check_dc:
                check_dc.append(getattr(network, 'dc_id'))
                setattr(network, 'func_type', func_type)
                setattr(network, 'my_dc_id',
                        getattr(detail_service[detail_name][0],
                                'my_dc_id'))
                setattr(network, 'task_status',
                        getattr(detail_service[detail_name][0],
                                'task_status'))
                setattr(network, 'service_type',
                        getattr(detail_service[detail_name][0],
                                'service_type'))
                member_data.append(network)

        return member_data

    def get_network_data(self):
        func_type = self.kwargs['group_id'].split('|')[0]
        detail_service = self._get_data()
        network_data = []

        network_name = \
            SERVICE_DETAIL_DISPLAY_COLUMNS[func_type]['network_name']
        detail_name = SERVICE_DETAIL_DISPLAY_COLUMNS[func_type]['detail_name']
        for network in detail_service[network_name]:
            cider = getattr(network, 'ip_address', '')
            ip_address = cider.split('/')[0]
            setattr(network, 'ip_address', ip_address)
            cider_v6 = getattr(network, 'ip_address_v6', '')
            ip_address_v6 = cider_v6.split('/')[0]
            setattr(network, 'ip_address_v6', ip_address_v6)
            setattr(network, 'func_type', func_type)
            setattr(network, 'group_id',
                    getattr(detail_service[detail_name][0], 'id'))
            setattr(network, 'my_dc_id',
                    getattr(detail_service[detail_name][0],
                            'my_dc_id'))
            setattr(network, 'task_status',
                    getattr(detail_service[detail_name][0],
                            'task_status'))
            setattr(network, 'service_type',
                    getattr(detail_service[detail_name][0],
                            'service_type'))
            network_data.append(network)
        return network_data

    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)

        func_type = kwargs['group_id'].split('|')[0]
        detail_service = self._get_data()

        detail_name = SERVICE_DETAIL_DISPLAY_COLUMNS[func_type]['detail_name']
        add_detail_name = \
            SERVICE_DETAIL_DISPLAY_COLUMNS[func_type]['add_detail_name']
        dc_info_name = SERVICE_DETAIL_DISPLAY_COLUMNS[func_type]['member_name']
        detail_data = detail_service[detail_name][0]
        if len(detail_service[add_detail_name]) == 0:
            add_detail_data = {}
        else:
            add_detail_data = detail_service[add_detail_name][0]

        context['service'] = []
        for disp_info in SERVICE_DETAIL_DISPLAY_COLUMNS[func_type]['detail']:
            if disp_info[1] == 'service_type':
                type = getattr(detail_data, disp_info[1])
                disp_data = SERVICE_TYPE_MAPPING[str(type)]
            elif disp_info[1] == 'dc_name':
                my_dc_id = getattr(detail_data, 'my_dc_id')
                disp_data = ''
                for dc_info in detail_service[dc_info_name]:
                    if dc_info.id == my_dc_id:
                        disp_data = dc_info.name
                        break
            elif disp_info[1] == 'task_status':
                task_status = getattr(detail_data, disp_info[1])
                disp_data = STATUS_MAPPING[str(task_status)]
            else:
                if hasattr(detail_data, disp_info[1]):
                    disp_data = getattr(detail_data, disp_info[1])
                else:
                    disp_data = getattr(add_detail_data, disp_info[1], '')

                if disp_data == '' and len(disp_info) == 3:
                    disp_data = disp_info[2]

            service_info = [disp_info[0], disp_data]
            context["service"].append(service_info)

        context["url"] = self.get_redirect_url()
        context["page_title"] = \
            _(SERVICE_DETAIL_DISPLAY_COLUMNS[func_type]['title']) + \
            " %s" % detail_data.service_name  # noqa

        return context

    @staticmethod
    def get_redirect_url():
        return reverse_lazy(constants.SERVICE_INDEX_URL)


class CreateView(forms.ModalFormView):
    form_class = service_forms.CreateServiceForm
    form_id = "create_service_form"
    modal_header = _("Create Service")
    template_name = constants.SERVICE_CREATE_VIEW_TEMPLATE
    success_url = reverse_lazy(constants.SERVICE_INDEX_URL)
    page_title = _("Create Service")
    submit_label = _("Create Service")
    submit_url = reverse_lazy(constants.SERVICE_CREATE_URL)


class UpdateView(forms.ModalFormView):
    form_class = service_forms.UpdateServiceForm
    form_id = "update_form"
    modal_header = _("Update Service")
    template_name = constants.SERVICE_UPDATE_VIEW_TEMPLATE
    success_url = constants.SERVICE_DETAIL_URL
    page_title = _("Update Service")
    submit_label = _("Update Service")
    submit_url = constants.SERVICE_UPDATE_URL

    def get_success_url(self):
        return reverse(self.success_url,
                       args=(self.kwargs['group_id'],))

    def get_context_data(self, **kwargs):
        context = super(UpdateView, self).get_context_data(**kwargs)
        group_id = self.kwargs['group_id']
        update_type = self.kwargs['update_type']
        args = (group_id, update_type)
        context['submit_url'] = reverse(self.submit_url, args=args)

        if 'description' in SERVICE_UPDATE_COLUMNS[update_type]:
            context['description'] = \
                SERVICE_UPDATE_COLUMNS[update_type]['description']

        return context

    def get_initial(self):
        return {'obj_id': self.kwargs['group_id'],
                'update_type': self.kwargs['update_type']}
