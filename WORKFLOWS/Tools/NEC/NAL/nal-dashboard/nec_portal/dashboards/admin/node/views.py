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

from openstack_dashboard import api

from nec_portal.api import nal_api
from nec_portal.dashboards.admin.node import constants
from nec_portal.dashboards.admin.node \
    import forms as node_forms
from nec_portal.dashboards.admin.node \
    import tables as node_tables
from nec_portal.local import nal_portal_settings

LOG = logging.getLogger(__name__)

NODE_FUNCTION_TYPE_MAPPING = \
    getattr(nal_portal_settings, 'NODE_FUNCTION_TYPE_MAPPING', None)
DEVICE_TYPE_MAPPING = getattr(nal_portal_settings, 'DEVICE_TYPE_MAPPING', None)
NODE_DETAIL_DISPLAY_COLUMNS = \
    getattr(nal_portal_settings, 'ADMIN_NODE_DETAIL_DISPLAY_COLUMNS', None)
NODE_CREATE_SEPARATE_DEF = getattr(nal_portal_settings,
                                   'NODE_CREATE_SEPARATE_DEF', None)
NODE_UPDATE_COLUMNS = getattr(nal_portal_settings, 'NODE_UPDATE_COLUMNS', None)
APL_TYPE_MAPPING = getattr(nal_portal_settings, 'APL_TYPE_MAPPING', None)
TYPE_MAPPING = getattr(nal_portal_settings, 'TYPE_MAPPING', None)
STATUS_MAPPING = getattr(nal_portal_settings, 'STATUS_MAPPING', None)
NETWORK_NAME_MAPPING = getattr(nal_portal_settings,
                               'NETWORK_NAME_MAPPING', None)
REDUNDANT_CONFIG_MAPPING = getattr(nal_portal_settings,
                                   'REDUNDANT_CONFIG_MAPPING', None)


class IndexView(tables.DataTableView):
    table_class = node_tables.NodeTable
    template_name = constants.NODE_INDEX_VIEW_TEMPLATE
    page_title = _("Nodes")

    def get_data(self):
        nodes = []
        try:
            nodes = nal_api.get_nodes(self.request, func_type='all_node')
        except Exception:
            exceptions.handle(self.request,
                              _('Unable to retrieve node list.'))

        tenants = []
        try:
            tenants, _more = api.keystone.tenant_list(
                self.request,
                paginate=True)
        except Exception:
            exceptions.handle(self.request,
                              _("Unable to retrieve all node information."))

        tenant_names = {}
        for tenant in tenants:
            tenant_names[tenant.id] = tenant.name

        node_list = []
        for node in nodes:
            node.tenant_name = tenant_names.get(node.tenant_id, None)
            node.func_type = \
                NODE_FUNCTION_TYPE_MAPPING[str(node.apl_type)][str(node.type)]
            node.device_name = \
                DEVICE_TYPE_MAPPING[node.func_type][str(node.device_type)]
            node_list.append(node)

        return node_list


class DetailView(tables.DataTableView):
    table_class = node_tables.NetworkTable
    template_name = constants.NODE_DETAIL_VIEW_TEMPLATE
    page_title = _("Node Details: {{ node.name }}")

    @memoized.memoized_method
    def _get_data(self):
        try:
            func_type = self.kwargs['node_id'].split('|')[0]
            node_id = self.kwargs['node_id'].split('|')[1]
            node = nal_api.get_nodes(self.request, rec_id=node_id,
                                     func_type=func_type)
        except Exception:
            msg = _('Unable to retrieve details for node "%s".') \
                % (node_id)
            exceptions.handle(self.request, msg,
                              redirect=self.get_redirect_url())
        return node

    def _get_network_list(self):
        try:
            tenant_id = self.request.user.tenant_id
            networks = api.neutron.network_list_for_tenant(self.request,
                                                           tenant_id)
        except Exception:
            msg = _('Failed to get network list.')
            exceptions.handle(self.request, msg)
            networks = []

        network_list = {}
        for network in networks:
            network_list[network.id] = network.name
        return network_list

    def get_data(self):
        func_type = self.kwargs['node_id'].split('|')[0]
        detail_node = self._get_data()
        network_name_list = self._get_network_list()

        detail_info = NODE_DETAIL_DISPLAY_COLUMNS[func_type]
        detail_data = detail_node[detail_info['detail_name']][0]
        network_data = []
        for network in detail_node[detail_info['network_name']]:
            if network.network_type_detail in ('1', '2', '3', '4'):
                if network.network_type_detail == '1':
                    network_name = \
                        network_name_list.get(network.IaaS_network_id, '')
                else:
                    network_name = \
                        NETWORK_NAME_MAPPING[str(network.network_type_detail)]
                setattr(network, 'network_name', network_name)
                setattr(network, 'func_type', func_type)
                setattr(network, 'id', detail_data.id)
                device_map = DEVICE_TYPE_MAPPING[func_type]
                setattr(network, 'device_name',
                        device_map[str(detail_data.device_type)])
                setattr(network, 'task_status', detail_data.task_status)
                network_data.append(network)
        return network_data

    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)

        func_type = kwargs['node_id'].split('|')[0]
        detail_node = self._get_data()

        detail_info = NODE_DETAIL_DISPLAY_COLUMNS[func_type]
        detail_data = detail_node[detail_info['detail_name']][0]
        setattr(detail_data, 'device_name',
                DEVICE_TYPE_MAPPING[func_type][str(detail_data.device_type)])

        context['node'] = []
        tenant_name = detail_data.tenant_id
        try:
            if tenant_name != '':
                tenant_data = api.keystone.tenant_get(self.request,
                                                      detail_data.tenant_id)
                tenant_name = getattr(tenant_data, 'name', '')
        except Exception:
            msg =  _("Unable to retrieve tenant information.")
            exceptions.handle(self.request, msg,
                              redirect=self.get_redirect_url())

        for disp_info in detail_info['detail']:
            if disp_info[1] == 'tenant_id':
                disp_data = tenant_name
            elif disp_info[1] == 'apl_type':
                apl_type = getattr(detail_data, disp_info[1])
                disp_data = APL_TYPE_MAPPING[str(apl_type)]
            elif disp_info[1] == 'type':
                type = getattr(detail_data, disp_info[1])
                disp_data = TYPE_MAPPING[str(type)]
            elif disp_info[1] == 'device_type':
                device_type = getattr(detail_data, disp_info[1])
                disp_data = DEVICE_TYPE_MAPPING[func_type][str(device_type)]
            elif disp_info[1] == 'task_status':
                task_status = getattr(detail_data, disp_info[1])
                disp_data = STATUS_MAPPING[str(task_status)]
            elif disp_info[1] == 'redundant_configuration_flg':
                redundant_config = getattr(detail_data, disp_info[1])
                disp_data = REDUNDANT_CONFIG_MAPPING.get(str(redundant_config),
                                                         '-')
            else:
                disp_data = getattr(detail_data, disp_info[1], '')
                if disp_data == '' and len(disp_info) == 3:
                    disp_data = disp_info[2]
            node_info = [disp_info[0], disp_data]
            context["node"].append(node_info)

        context["url"] = self.get_redirect_url()
        context["page_title"] = \
            _(detail_info['title']) + " %s" % detail_data.name  # noqa

        table = node_tables.NodeTable(self.request)
        context["actions"] = table.render_row_actions(detail_data)

        return context

    @staticmethod
    def get_redirect_url():
        return reverse_lazy(constants.NODE_INDEX_URL)


class UpdateView(forms.ModalFormView):
    form_class = node_forms.UpdateNodeForm
    form_id = "update_form"
    modal_header = _("Update Node")
    template_name = constants.NODE_UPDATE_VIEW_TEMPLATE
    success_url = constants.NODE_DETAIL_URL
    page_title = _("Update Node")
    submit_label = _("Update Node")
    submit_url = constants.NODE_UPDATE_URL

    def get_success_url(self):
        return reverse(self.success_url,
                       args=(self.kwargs['node_id'],))

    @memoized.memoized_method
    def _get_data(self):
        try:
            func_type = self.kwargs['node_id'].split('|')[0]
            node_id = self.kwargs['node_id'].split('|')[1]
            node = nal_api.get_nodes(self.request, rec_id=node_id,
                                     func_type=func_type)
        except Exception:
            msg = _('Unable to retrieve details for node "%s".') \
                % (node_id)
            exceptions.handle(self.request, msg,
                              redirect=self.get_redirect_url())
        return node

    def get_context_data(self, **kwargs):

        context = super(UpdateView, self).get_context_data(**kwargs)
        node_id = self.kwargs['node_id']
        update_type = self.kwargs['update_type']
        args = (node_id, update_type)
        context['submit_url'] = reverse(self.submit_url, args=args)

        if NODE_UPDATE_COLUMNS[update_type]['display_type'] == 'check':
            func_type = node_id.split('|')[0]
            detail_node = self._get_data()
            text = NODE_UPDATE_COLUMNS[update_type]['text']

            detail_info = NODE_DETAIL_DISPLAY_COLUMNS[func_type]
            detail_data = detail_node[detail_info['detail_name']][0]

            if NODE_UPDATE_COLUMNS[update_type]['target']:
                input_text = \
                    getattr(detail_data,
                            NODE_UPDATE_COLUMNS[update_type]['target'])
                text = text % (input_text)
            context['text'] = text

        return context

    def get_initial(self):
        return {'obj_id': self.kwargs['node_id'],
                'update_type': self.kwargs['update_type']}

    @staticmethod
    def get_redirect_url():
        return reverse_lazy(constants.NODE_INDEX_URL)
