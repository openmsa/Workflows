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
from django.template.defaultfilters import title  # noqa
from django.utils.translation import ugettext_lazy as _

from horizon import tables

from nec_portal.dashboards.project.resource.conf import setting
from nec_portal.dashboards.project.resource import constants
from nec_portal.local import nal_portal_settings

LOG = logging.getLogger(__name__)

RESOURCE_ALL_BUTTONS = getattr(nal_portal_settings,
                               'RESOURCE_ALL_BUTTONS', None)
RESOURCE_BUTTON_DISPLAY_FOR_TYPE = \
    getattr(nal_portal_settings, 'RESOURCE_BUTTON_DISPLAY_FOR_TYPE', None)
STATUS_MAPPING = getattr(nal_portal_settings, 'STATUS_MAPPING', None)
RESOURCE_STATUS_MAPPING = getattr(nal_portal_settings,
                                  'RESOURCE_STATUS_MAPPING', None)
RESOURCE_SCREEN_TRANSITION = getattr(nal_portal_settings,
                                     'RESOURCE_SCREEN_TRANSITION', None)


class CreateResourceAction(tables.LinkAction):
    name = "create"
    verbose_name = _("Create Resource")
    url = constants.RESOURCE_CREATE_URL
    classes = ("ajax-modal",)
    icon = "plus"
    policy_rules = (("nal", "nal:create_resource"),)

    def allowed(self, request, resource):
        func_type = self.table.kwargs['func_type']
        if self.__class__.__name__ \
                in RESOURCE_BUTTON_DISPLAY_FOR_TYPE[func_type]:
            return True
        return False

    def get_link_url(self, datum=None):
        try:
            func_type = self.table.kwargs['func_type']
            resource_key = self.table.kwargs['resource_key']
            resource_id = '|'.join([func_type, resource_key])
            return reverse(self.url, args=(resource_id,))
        except urlresolvers.NoReverseMatch as ex:
            LOG.info('No reverse found for "%s": %s' % (self.url, ex))
            return self.url


class ResourceFilterAction(tables.FilterAction):
    def filter(self, table, resources, filter_string):
        """Naive case-insensitive search."""
        q = filter_string.lower()

        def comp(resource):
            if q in resource.name.lower():
                return True
            return False

        return filter(comp, resources)


class ResourceKindFilterAction(tables.FilterAction):
    def filter(self, table, resources, filter_string):
        """Naive case-insensitive search."""
        q = filter_string.lower()

        def comp(resource):
            if q in resource.name.lower():
                return True
            return False

        return filter(comp, resources)


STATUS_DISPLAY_CHOICES = []
for status_num, status_name in STATUS_MAPPING.iteritems():
    STATUS_DISPLAY_CHOICES.append((status_num, status_name))

GLOBALIP_STATUS_DISPLAY_CHOICES = []
for status_num, status_name in RESOURCE_STATUS_MAPPING.iteritems():
    GLOBALIP_STATUS_DISPLAY_CHOICES.append((status_num, status_name))


def get_resource_name(resource):
    return resource.name if resource.name else None


def get_resource(resource):
    return resource.resource if resource.resource else None


class ResourceTable(tables.DataTable):
    resource_name = tables.Column('resource_name',
                                  verbose_name=_('Resource'),
                                  link=constants.RESOURCE_DETAIL_URL)
    contract_cnt = tables.Column('contract_cnt',
                                 verbose_name=_('Contract Count'))
    use_cnt = tables.Column('use_cnt', verbose_name=_('Used Count'))

    def get_object_id(self, resource):
        func_type = resource.func_type
        resource_key = resource.resource_key
        detail_table = RESOURCE_SCREEN_TRANSITION[func_type]
        return '|'.join([func_type, resource_key, detail_table])

    class Meta(object):
        name = "resource"
        verbose_name = _("Resource")
        multi_select = False
        table_actions = (ResourceFilterAction,)


class ResourceKindTable(tables.DataTable):
    used = tables.Column('status', verbose_name=_('Utilization'),
                         display_choices=GLOBALIP_STATUS_DISPLAY_CHOICES)
    name = tables.Column(get_resource_name, verbose_name=_('Name'))
    status = tables.Column('status_name', verbose_name=_('Status'))

    def get_object_id(self, resource):
        func_type = self.kwargs['func_type']
        resource_key = self.kwargs['resource_key']
        return '|'.join([func_type, resource_key, str(resource.id)])

    class Meta(object):
        name = "resource_kind"
        verbose_name = _("Resource Kind")
        multi_select = False
        row_actions = []
        for resource_button in RESOURCE_ALL_BUTTONS['row']:
            button_class = getattr(setting, resource_button)
            row_actions.append(button_class)
        table_actions = (ResourceKindFilterAction, CreateResourceAction)


class ResourceGlobalipTable(tables.DataTable):
    used = tables.Column('status', verbose_name=_('Utilization'),
                         display_choices=GLOBALIP_STATUS_DISPLAY_CHOICES)
    resource = tables.Column(get_resource, verbose_name=_('Resource'))
    name = tables.Column(get_resource_name, verbose_name=_('Name'))

    def get_object_id(self, resource):
        func_type = self.kwargs['func_type']
        resource_key = self.kwargs['resource_key']
        return '|'.join([func_type, resource_key, str(resource.id)])

    class Meta(object):
        name = "resource_globalip"
        verbose_name = _("Resource Kind")
        multi_select = False
        row_actions = []
        for resource_button in RESOURCE_ALL_BUTTONS['row']:
            button_class = getattr(setting, resource_button)
            row_actions.append(button_class)
        table_actions = (ResourceKindFilterAction, CreateResourceAction)
