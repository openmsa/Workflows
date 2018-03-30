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

from django.core import urlresolvers
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ungettext_lazy
from horizon import exceptions
from horizon import tables

from openstack_dashboard import api

from nec_portal.api import nal_api
from nec_portal.dashboards.project.node import constants
from nec_portal.local import nal_portal_settings

LOG = logging.getLogger(__name__)
NODE_DETAIL_DISPLAY_COLUMNS = \
    getattr(nal_portal_settings, 'PROJECT_NODE_DETAIL_DISPLAY_COLUMNS', None)
NODE_DISPLAY_BUTTONS_FOR_DEVICE = \
    getattr(nal_portal_settings, 'NODE_DISPLAY_BUTTONS_FOR_DEVICE', None)
NODE_DISPLAY_BUTTONS_FOR_STATUS = \
    getattr(nal_portal_settings, 'NODE_DISPLAY_BUTTONS_FOR_STATUS', None)


class DeleteNodeAction(tables.DeleteAction):
    @staticmethod
    def action_present(count):
        return ungettext_lazy(
            u"Delete Node",
            u"Delete Nodes",
            count
        )

    @staticmethod
    def action_past(count):
        return ungettext_lazy(
            u"Scheduled deletion of Node",
            u"Scheduled deletion of Nodes",
            count
        )

    name = "delete"
    help_text = _("This action cannot be undone. ")
    policy_rules = (("nal", "nal:delete_node"),)

    def allowed(self, request, node):
        device_name = node.device_name
        allow_list = NODE_DISPLAY_BUTTONS_FOR_DEVICE[device_name]
        if self.__class__.__name__ in allow_list \
            and self.__class__.__name__ in \
                NODE_DISPLAY_BUTTONS_FOR_STATUS[str(node.task_status)]:
            return True
        return False

    def delete(self, request, obj_id):
        func_type = obj_id.split('|')[0]
        node_id = obj_id.split('|')[1]

        node = nal_api.get_nodes(request, rec_id=node_id,
                                 func_type=func_type)
        detail_data = \
            node[NODE_DETAIL_DISPLAY_COLUMNS[func_type]['detail_name']][0]

        job_cleaning_mode = '0'
        if str(detail_data.task_status) == '9':
            job_cleaning_mode = '1'

        try:
            LOG.info('Deleting node "%s".' % node_id)
            nal_api.delete_node(request, func_type, node_id,
                                detail_data.device_type, job_cleaning_mode)
        except Exception:
            redirect = reverse(constants.NODE_INDEX_URL)
            exceptions.handle(request, redirect=redirect)


class DeleteNetworkAction(tables.DeleteAction):
    @staticmethod
    def action_present(count):
        return ungettext_lazy(
            u"Delete Network",
            u"Delete Networks",
            count
        )

    @staticmethod
    def action_past(count):
        return ungettext_lazy(
            u"Scheduled deletion of Network",
            u"Scheduled deletion of Networks",
            count
        )

    name = "delete"
    help_text = _("This action cannot be undone. ")
    policy_rules = (("nal", "nal:delete_node_network"),)

    def allowed(self, request, network):
        device_name = network.device_name
        allow_list = NODE_DISPLAY_BUTTONS_FOR_DEVICE[device_name]
        status_ck = NODE_DISPLAY_BUTTONS_FOR_STATUS[str(network.task_status)]
        if self.__class__.__name__ in allow_list:
            if getattr(network, 'del_flg', '') == '1':
                if self.__class__.__name__ in status_ck:
                    return True
        return False

    def delete(self, request, obj_id):
        func_type = obj_id.split('|')[0]
        node_id = obj_id.split('|')[1]
        port_id = obj_id.split('|')[2]

        node = nal_api.get_nodes(request, rec_id=node_id,
                                 func_type=func_type)
        detail_data = \
            node[NODE_DETAIL_DISPLAY_COLUMNS[func_type]['detail_name']][0]
        port_list = \
            node[NODE_DETAIL_DISPLAY_COLUMNS[func_type]['network_name']]
        for port_data in port_list:
            if port_data.port_id == port_id:
                IaaS_network_id = port_data.IaaS_network_id
                IaaS_port_id = port_data.IaaS_port_id
                IaaS_port_info = api.neutron.port_get(request, IaaS_port_id)
                IaaS_subnet_id = IaaS_port_info.fixed_ips[0]['subnet_id']
        try:
            LOG.info('Deleting port "%s".' % IaaS_network_id)
            params = {'function_type': func_type + '_port_d',
                      'node_id': detail_data.node_id,
                      'IaaS_network_id': IaaS_network_id,
                      'IaaS_subnet_id': IaaS_subnet_id,
                      'IaaS_port_id': IaaS_port_id,
                      'port_id': port_id,
                      'device_type': detail_data.device_type}
            nal_api.update_node(request, params)
        except Exception:
            msg = _('Failed to delete network')
            redirect_id = '|'.join([func_type, node_id])
            redirect = reverse(constants.NODE_DETAIL_URL,
                               kwargs={"node_id": redirect_id})
            exceptions.handle(request, msg, redirect=redirect)


class NodeBaseLink(tables.LinkAction):
    url = constants.NODE_UPDATE_URL
    name = 'interface'
    classes = ("ajax-modal",)
    icon = "plus"

    def disp_check(self, class_name, node):
        device_name = node.device_name
        allow_list = NODE_DISPLAY_BUTTONS_FOR_DEVICE[device_name]
        if class_name in allow_list \
            and class_name in \
                NODE_DISPLAY_BUTTONS_FOR_STATUS[str(node.task_status)]:
            return True
        return False

    def get_link_url(self, datum=None):
        try:
            if datum:
                obj_id = self.table.get_object_id(datum)
                return urlresolvers.reverse(self.url, args=(obj_id, self.name))
            else:
                return urlresolvers.reverse(self.url)
        except urlresolvers.NoReverseMatch as ex:
            LOG.info('No reverse found for "%s": %s' % (self.url, ex))
            return self.url


class UpdateAddPortLink(NodeBaseLink):
    name = "interface"
    verbose_name = _("Connect Interface")
    policy_rules = (("nal", "nal:update_node_interface"),)

    def allowed(self, request, node):
        return NodeBaseLink.disp_check(self, self.__class__.__name__, node)


class UpdateNetworkV6Link(NodeBaseLink):
    name = "IPv6Add"
    verbose_name = _("Add IPv6 Address")
    policy_rules = (("nal", "nal:update_node_network_ipv6"),)

    def allowed(self, request, network):
        if network.network_type_detail == "1":
            if network.ip_address_v6 == "":
                return NodeBaseLink.disp_check(self, self.__class__.__name__,
                                               network)
        return False
