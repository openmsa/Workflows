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

from django.template.defaultfilters import title  # noqa
from django.utils.translation import pgettext_lazy
from django.utils.translation import ugettext_lazy as _

from horizon import exceptions
from horizon import tables

from nec_portal.api import nal_api
from nec_portal.dashboards.project.node.conf import setting
from nec_portal.dashboards.project.node import constants
from nec_portal.local import nal_portal_settings


LOG = logging.getLogger(__name__)
LOGOUT_URL = 'logout'
NODE_ALL_BUTTONS = getattr(nal_portal_settings, 'NODE_ALL_BUTTONS', None)
NODE_DISPLAY_BUTTONS_FOR_USER = \
    getattr(nal_portal_settings, 'NODE_DISPLAY_BUTTONS_FOR_USER', None)
NODE_DISPLAY_BUTTONS_FOR_CLASS = \
    getattr(nal_portal_settings, 'NODE_DISPLAY_BUTTONS_FOR_CLASS', None)
NODE_FUNCTION_TYPE_MAPPING = \
    getattr(nal_portal_settings, 'NODE_FUNCTION_TYPE_MAPPING', None)
NODE_DETAIL_DISPLAY_COLUMNS = \
    getattr(nal_portal_settings, 'PROJECT_NODE_DETAIL_DISPLAY_COLUMNS', None)
APL_TYPE_MAPPING = getattr(nal_portal_settings, 'APL_TYPE_MAPPING', None)
TYPE_MAPPING = getattr(nal_portal_settings, 'TYPE_MAPPING', None)
DEVICE_TYPE_MAPPING = getattr(nal_portal_settings, 'DEVICE_TYPE_MAPPING', None)
NETWORK_TYPE_MAPPING = \
    getattr(nal_portal_settings, 'NETWORK_TYPE_MAPPING', None)
STATUS_MAPPING = getattr(nal_portal_settings, 'STATUS_MAPPING', None)
TASK_MAPPING = getattr(nal_portal_settings, 'TASK_MAPPING', None)


class CreateNodeLink(tables.LinkAction):
    name = "create"
    verbose_name = _("Create Node")
    url = constants.NODE_CREATE_URL
    classes = ("ajax-modal",)
    icon = "plus"
    policy_rules = (("nal", "nal:create_node"),)


class UpdateNodeRow(tables.Row):
    ajax = True

    def get_data(self, request, obj_id):
        func_type = obj_id.split('|')[0]
        node_id = obj_id.split('|')[1]
        node = nal_api.get_nodes(request, rec_id=node_id, func_type=func_type)

        if node[NODE_DETAIL_DISPLAY_COLUMNS[func_type]['detail_name']] == []:
            raise exceptions.NotFound

        detail_data = \
            node[NODE_DETAIL_DISPLAY_COLUMNS[func_type]['detail_name']][0]
        detail_data.device_name = \
            DEVICE_TYPE_MAPPING[func_type][str(detail_data.device_type)]
        return detail_data


APL_TYPE_DISPLAY_CHOICES = []
for apl_key, apl_value in APL_TYPE_MAPPING.iteritems():
    APL_TYPE_DISPLAY_CHOICES.append((apl_key, apl_value))

TYPE_DISPLAY_CHOICES = []
for type_key, type_value in TYPE_MAPPING.iteritems():
    TYPE_DISPLAY_CHOICES.append((type_key, type_value))

NETWORK_TYPE_DISPLAY_CHOICES = []
for net_type_key, net_type_value in NETWORK_TYPE_MAPPING.iteritems():
    NETWORK_TYPE_DISPLAY_CHOICES.append((net_type_key, net_type_value))

TASK_STATUS_CHOICES = (
    ("0", None),
    ("1", True),
    ("2", True),
    ("9", True),
    (None, None),
)

STATUS_DISPLAY_CHOICES = []
for status_num, status_name in STATUS_MAPPING.iteritems():
    STATUS_DISPLAY_CHOICES.append((status_num, status_name))

TASK_DISPLAY_NONE = pgettext_lazy("Task status of an Instance", u"None")

TASK_DISPLAY_CHOICES = []
for status_num, status_name in TASK_MAPPING.iteritems():
    TASK_DISPLAY_CHOICES.append((status_num, status_name))


class NodeFilterAction(tables.FilterAction):
    def filter(self, table, nodes, filter_string):
        """Naive case-insensitive search."""
        q = filter_string.lower()

        def comp(node):
            if q in node.name.lower():
                return True
            return False

        return filter(comp, nodes)


def get_ip_address_v6(node):
    return node.ip_address_v6 if node.ip_address_v6 else None


class NodeTable(tables.DataTable):
    name = tables.Column('name',
                         verbose_name=_('Name'),
                         link=constants.NODE_DETAIL_URL)
    apl_type = tables.Column('apl_type', verbose_name=_('Apl Type'),
                             display_choices=APL_TYPE_DISPLAY_CHOICES)
    type = tables.Column('type', verbose_name=_('Type'),
                         display_choices=TYPE_DISPLAY_CHOICES)
    device = tables.Column('device_name', verbose_name=_('Device Type'))
    status = tables.Column('task_status',
                           verbose_name=_("Status"),
                           display_choices=STATUS_DISPLAY_CHOICES)
    task = tables.Column('task_status',
                         verbose_name=_("Task"),
                         status=True,
                         empty_value=TASK_DISPLAY_NONE,
                         status_choices=TASK_STATUS_CHOICES,
                         display_choices=TASK_DISPLAY_CHOICES)

    def get_object_id(self, node):
        func_type = \
            NODE_FUNCTION_TYPE_MAPPING[str(node.apl_type)][str(node.type)]
        return '|'.join([func_type, str(node.id)])

    class Meta(object):
        name = "node"
        verbose_name = _("Node")
        status_columns = ["task", ]
        multi_select = False
        row_class = UpdateNodeRow
        row_actions = []
        for node_button in NODE_ALL_BUTTONS:
            if node_button in NODE_DISPLAY_BUTTONS_FOR_USER['project'] and \
                    node_button in NODE_DISPLAY_BUTTONS_FOR_CLASS['node']:
                button_class = getattr(setting, node_button)
                row_actions.append(button_class)
        table_actions = (NodeFilterAction, CreateNodeLink)


class NetworkTable(tables.DataTable):
    nic = tables.Column('nic',
                        verbose_name=_('NIC'))
    ip_address = tables.Column('ip_address',
                               verbose_name=_('IPv4 Address'))
    ip_address_v6 = tables.Column(get_ip_address_v6,
                                  verbose_name=_('IPv6 Address'))
    network_name = tables.Column('network_name',
                                 verbose_name=_('Network Name'))
    network_type = tables.Column('network_type_detail',
                                 verbose_name=_('Network Type'),
                                 display_choices=NETWORK_TYPE_DISPLAY_CHOICES)

    def get_object_id(self, network):
        return '|'.join([network.func_type,
                         str(network.id),
                         str(network.port_id)])

    class Meta(object):
        name = "networks"
        verbose_name = _("Networks")
        hidden_title = False
        row_actions = []
        for node_button in NODE_ALL_BUTTONS:
            if node_button in NODE_DISPLAY_BUTTONS_FOR_USER['project'] and \
                    node_button in NODE_DISPLAY_BUTTONS_FOR_CLASS['network']:
                button_class = getattr(setting, node_button)
                row_actions.append(button_class)
