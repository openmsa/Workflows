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

from openstack_dashboard import api

from nec_portal.api import nal_api
from nec_portal.dashboards.admin.service import constants
from nec_portal.local import nal_portal_settings


LOG = logging.getLogger(__name__)
SERVICE_FUNCTION_TYPE_MAPPING = \
    getattr(nal_portal_settings, 'SERVICE_FUNCTION_TYPE_MAPPING', None)
SERVICE_DETAIL_DISPLAY_COLUMNS = \
    getattr(nal_portal_settings, 'SERVICE_DETAIL_DISPLAY_COLUMNS', None)
SERVICE_TYPE_MAPPING = getattr(nal_portal_settings,
                               'SERVICE_TYPE_MAPPING', None)
SERVICE_BANDWIDTH_MAPPING = getattr(nal_portal_settings,
                                    'SERVICE_BANDWIDTH_MAPPING', None)
STATUS_MAPPING = getattr(nal_portal_settings, 'STATUS_MAPPING', None)
TASK_MAPPING = getattr(nal_portal_settings, 'TASK_MAPPING', None)


class UpdateServiceRow(tables.Row):
    ajax = True

    def get_data(self, request, obj_id):
        func_type = obj_id.split('|')[0]
        group_id = obj_id.split('|')[1]
        detail_service = nal_api.get_services(request,
                                              group_id=group_id,
                                              func_type=func_type)

        service_columns = SERVICE_DETAIL_DISPLAY_COLUMNS[func_type]
        detail_data = detail_service[service_columns['detail_name']][0]
        network_list = detail_service[service_columns['network_name']]

        tenant_name = detail_data.tenant_id
        try:
            if tenant_name != '-':
                tenant_data = api.keystone.tenant_get(request,
                                                      detail_data.tenant_id)
                tenant_name = getattr(tenant_data, 'name', '-')
        except Exception:
            exceptions.handle(request,
                              _("Unable to retrieve tenant information."))
        detail_data.tenant_name = tenant_name

        for network in network_list:
            if getattr(network, 'dc_id') == detail_data.my_dc_id:
                setattr(detail_data, 'my_group_flg', '1')
                break
        return detail_data


SERVICE_TYPE_DISPLAY_CHOICES = []
for type_key, type_value in SERVICE_TYPE_MAPPING.iteritems():
    SERVICE_TYPE_DISPLAY_CHOICES.append((type_key, type_value))

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

BANDWIDTH_DISPLAY_CHOICES = []
for bandwidth_num, bandwidth_name in SERVICE_BANDWIDTH_MAPPING.iteritems():
    BANDWIDTH_DISPLAY_CHOICES.append((bandwidth_num, bandwidth_name))


class ServiceFilterAction(tables.FilterAction):
    def filter(self, table, services, filter_string):
        """Naive case-insensitive search."""
        q = filter_string.lower()

        def comp(service):
            if q in service.name.lower():
                return True
            return False

        return filter(comp, services)


def get_bandwidth(service):
    return service.bandwidth if service.bandwidth else None


def get_default_gateway(service):
    return service.default_gateway if service.default_gateway else None


def get_ip_address_v6(service):
    return service.ip_address_v6 if service.ip_address_v6 else None


class ServiceTable(tables.DataTable):
    tenant_name = tables.Column('tenant_name', verbose_name=_('Tenant Name'))
    name = tables.Column('service_name',
                         verbose_name=_('Name'),
                         link=constants.SERVICE_DETAIL_URL)
    type = tables.Column('service_type', verbose_name=_('Type'),
                         display_choices=SERVICE_TYPE_DISPLAY_CHOICES)
    status = tables.Column('task_status',
                           verbose_name=_("Status"),
                           display_choices=STATUS_DISPLAY_CHOICES)
    task = tables.Column('task_status',
                         verbose_name=_("Task"),
                         status=True,
                         empty_value=TASK_DISPLAY_NONE,
                         status_choices=TASK_STATUS_CHOICES,
                         display_choices=TASK_DISPLAY_CHOICES)

    def get_object_id(self, service):
        func_type = SERVICE_FUNCTION_TYPE_MAPPING[str(service.service_type)]
        return '|'.join([func_type, str(service.id)])

    class Meta(object):
        name = "service"
        verbose_name = _("Service")
        multi_select = False
        status_columns = ["task", ]
        row_class = UpdateServiceRow
        table_actions = (ServiceFilterAction, )


class MemberTable(tables.DataTable):
    name = tables.Column('dc_name', verbose_name=_('DC Name'))
    bandwidth = tables.Column(get_bandwidth, verbose_name=_('Bandwidth'),
                              display_choices=BANDWIDTH_DISPLAY_CHOICES)
    default_gateway = tables.Column(get_default_gateway,
                                    verbose_name=_('Default Gateway'))

    def get_object_id(self, member):
        return member.dc_id

    class Meta(object):
        name = "member"
        verbose_name = _("Member")
        multi_select = False


class NetworkTable(tables.DataTable):
    dc_name = tables.Column('dc_name', verbose_name=_('DC Name'))
    network_name = tables.Column('network_name',
                                 verbose_name=_('Network Name'))
    ip_address = tables.Column('ip_address', verbose_name=_('IP Address'))
    ip_address_v6 = tables.Column(get_ip_address_v6,
                                  verbose_name=_('IPv6 Address'))
    dc_id = tables.Column('dc_id', verbose_name=_('DC ID'), hidden=True)

    def get_object_id(self, service):
        return '|'.join([str(service.dc_id), str(service.network_id)])

    class Meta(object):
        name = "network"
        verbose_name = _("Network")
        multi_select = False
