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
from django.utils.translation import ugettext_lazy as _

from horizon import tables

from nec_portal.dashboards.admin.resource import constants
from nec_portal.local import nal_portal_settings

LOG = logging.getLogger(__name__)
RESOURCE_OPERATION_MAPPING = getattr(nal_portal_settings,
                                     'RESOURCE_OPERATION_MAPPING', None)
RESOURCE_SCREEN_TRANSITION = getattr(nal_portal_settings,
                                     'RESOURCE_SCREEN_TRANSITION', None)
RESOURCE_FUNCTION_TYPE_MAPPING = \
    getattr(nal_portal_settings, 'RESOURCE_FUNCTION_TYPE_MAPPING', None)
RESOURCE_STATUS_MAPPING = getattr(nal_portal_settings,
                                  'RESOURCE_STATUS_MAPPING', None)
RESOURCE_TASK_STATUS_MAPPING = getattr(nal_portal_settings,
                                       'RESOURCE_TASK_STATUS_MAPPING', None)


class ResourceFilterAction(tables.FilterAction):
    def filter(self, table, resources, filter_string):
        """Naive case-insensitive search."""
        q = filter_string.lower()

        def comp(resource):
            if q in resource.name.lower():
                return True
            return False

        return filter(comp, resources)


STATUS_DISPLAY_CHOICES = []
for status_num, status_name in RESOURCE_STATUS_MAPPING.iteritems():
    STATUS_DISPLAY_CHOICES.append((status_num, status_name))

TASK_STATUS_DISPLAY_CHOICES = []
for status_num, status_name in RESOURCE_TASK_STATUS_MAPPING.iteritems():
    TASK_STATUS_DISPLAY_CHOICES.append((status_num, status_name))


def get_unavailable_cnt(resource):
    if resource.unavailable_cnt == '':
        return None
    return resource.unavailable_cnt


def get_tenant_name(resource):
    if resource.tenant_name == '':
        return None
    return resource.tenant_name


def get_node_name(resource):
    if resource.node_name == '':
        return None
    return resource.node_name


def get_threshold(resource):
    if resource.threshold == '':
        return None
    return str(resource.threshold) + "%"


def get_warning(resource):
    if resource.warning_flg == '':
        return None
    return _('Warning')


class ResourceTable(tables.DataTable):
    resource_name = tables.Column('resource_name',
                                  verbose_name=_('Resource'),
                                  link=constants.RESOURCE_DETAIL_URL)
    quota = tables.Column('quota', verbose_name=_('Max'))
    contract_cnt = tables.Column('contract_cnt',
                                 verbose_name=_('Contract Count'))
    unavailable_cnt = tables.Column(get_unavailable_cnt,
                                    verbose_name=_('Unavailable Count'))
    threshold = tables.Column(get_threshold, verbose_name=_('Threshold'))
    status = tables.Column(get_warning, verbose_name=_('Status'))
    use_cnt = tables.Column('use_cnt', verbose_name=_('Used Count'))

    def get_object_id(self, resource):
        func_type = resource.func_type
        resource_key = resource.resource_key
        detail_table = RESOURCE_SCREEN_TRANSITION[func_type]
        return '|'.join([func_type, resource_key, detail_table])

    class Meta(object):
        name = "resource"
        verbose_name = _("Node")
        multi_select = False
        table_actions = (ResourceFilterAction,)


class LicenseDetailTable(tables.DataTable):
    tenant_name = tables.Column(get_tenant_name,
                                verbose_name=_('Tenant Name'))
    contract_cnt = tables.Column('contract_cnt',
                                 verbose_name=_('Contract Count'))
    use_cnt = tables.Column('use_cnt', verbose_name=_('Used Count'))

    class Meta(object):
        name = "license_detail"
        verbose_name = _("License Detail")
        multi_select = False
        table_actions = (ResourceFilterAction,)


class PnfDetailTable(tables.DataTable):
    tenant_name = tables.Column(get_tenant_name,
                                verbose_name=_('Tenant Name'))
    resource = tables.Column('resource', verbose_name=_('Resource'))
    status = tables.Column('status', verbose_name=_('Utilization'),
                           display_choices=STATUS_DISPLAY_CHOICES)
    node_name = tables.Column(get_node_name, verbose_name=_('Name'))
    task_status = tables.Column('status_name', verbose_name=_('Status'))

    class Meta(object):
        name = "pnf_detail"
        verbose_name = _("Pnf Detail")
        multi_select = False
        table_actions = (ResourceFilterAction,)


class VlanDetailTable(tables.DataTable):
    tenant_name = tables.Column(get_tenant_name,
                                verbose_name=_('Tenant Name'))
    resource = tables.Column('resource', verbose_name=_('Resource'))
    status = tables.Column('status', verbose_name=_('Utilization'),
                           display_choices=STATUS_DISPLAY_CHOICES)
    task_status = tables.Column('status_name', verbose_name=_('Status'))

    class Meta(object):
        name = "vlan_detail"
        verbose_name = _("Vlan Detail")
        multi_select = False
        table_actions = (ResourceFilterAction,)


class PodListDetailTable(tables.DataTable):
    pod_name = tables.Column('pod_name', verbose_name=_('Pod Name'),
                             link=constants.RESOURCE_DETAIL_URL)
    quota = tables.Column('quota', verbose_name=_('Max'))
    use_cnt = tables.Column('use_cnt', verbose_name=_('Used Count'))

    def get_object_id(self, resource):
        func_type = resource.func_type
        resource_key = resource.resource_key
        next_func_type = \
            RESOURCE_FUNCTION_TYPE_MAPPING['admin_detail'][func_type]
        pod_id = resource.pod_name

        detail_table = RESOURCE_SCREEN_TRANSITION[next_func_type]
        return '|'.join([next_func_type, resource_key, pod_id, detail_table])

    class Meta(object):
        name = "pod_list"
        verbose_name = _("Pod List")
        multi_select = False
        table_actions = (ResourceFilterAction,)


class PodDetailTable(tables.DataTable):
    tenant_name = tables.Column(get_tenant_name,
                                verbose_name=_('Tenant Name'))
    contract_cnt = tables.Column('contract_cnt',
                                 verbose_name=_('Contract Count'))
    use_cnt = tables.Column('use_cnt', verbose_name=_('Used Count'))

    def get_object_id(self, resource):
        return resource.tenant_id

    class Meta(object):
        name = "pod_detail"
        verbose_name = _("Pod Detail")
        multi_select = False
        table_actions = (ResourceFilterAction,)
