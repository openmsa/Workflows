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

from nec_portal.api import nal_api
from nec_portal.dashboards.project.service import constants
from nec_portal.local import nal_portal_settings

LOG = logging.getLogger(__name__)
SERVICE_DISPLAY_BUTTONS_LIST = \
    getattr(nal_portal_settings, 'SERVICE_DISPLAY_BUTTONS_LIST', None)
SERVICE_DETAIL_DISPLAY_COLUMNS = \
    getattr(nal_portal_settings, 'SERVICE_DETAIL_DISPLAY_COLUMNS', None)
SERVICE_DISPLAY_BUTTONS_FOR_STATUS = \
    getattr(nal_portal_settings, 'SERVICE_DISPLAY_BUTTONS_FOR_STATUS', None)
SERVICE_DISPLAY_BUTTONS_FOR_DEVICE = \
    getattr(nal_portal_settings, 'SERVICE_DISPLAY_BUTTONS_FOR_DEVICE', None)
SERVICE_TYPE_MAPPING = \
    getattr(nal_portal_settings, 'SERVICE_TYPE_MAPPING', None)
SERVICE_TYPE_DETAIL_MAPPING = \
    getattr(nal_portal_settings, 'SERVICE_TYPE_DETAIL_MAPPING', None)


class DeleteServiceAction(tables.DeleteAction):
    @staticmethod
    def action_present(count):
        return ungettext_lazy(
            u"Delete Service",
            u"Delete Services",
            count
        )

    @staticmethod
    def action_past(count):
        return ungettext_lazy(
            u"Scheduled deletion of Service",
            u"Scheduled deletion of Services",
            count
        )

    name = "delete"
    help_text = _("This action cannot be undone. ")
    policy_rules = (("nal", "nal:delete_service"),)

    def allowed(self, request, service):
        if service.my_group_flg == '1':
            allow_member = SERVICE_DISPLAY_BUTTONS_LIST['is_member']
        else:
            allow_member = SERVICE_DISPLAY_BUTTONS_LIST['is_not_member']
        allow_status = \
            SERVICE_DISPLAY_BUTTONS_FOR_STATUS[str(service.task_status)]
        service_name = SERVICE_TYPE_MAPPING[str(service.service_type)]
        allow_device = SERVICE_DISPLAY_BUTTONS_FOR_DEVICE[service_name]

        allow_set = set(allow_member) & set(allow_status) & set(allow_device)
        if self.__class__.__name__ in list(allow_set):
            return True
        return False

    def delete(self, request, obj_id):
        func_type = obj_id.split('|')[0]
        service_id = obj_id.split('|')[1]

        service = nal_api.get_services(request, group_id=service_id,
                                       func_type=func_type)
        detail_list = \
            service[SERVICE_DETAIL_DISPLAY_COLUMNS[func_type]['detail_name']]
        detail_data = detail_list[0]

        params = {'function_type': func_type,
                  'group_id': service_id,
                  'service_type': detail_data.service_type}

        service_name = SERVICE_TYPE_MAPPING.get(detail_data.service_type, '')
        service_detail = SERVICE_TYPE_DETAIL_MAPPING.get(service_name, {})
        for key, value in service_detail.iteritems():
            params[key] = value

        if str(detail_data.task_status) == '9':
            params['job_cleaning_mode'] = 1

        try:
            LOG.info('Deleting service "%s".' % service_id)
            nal_api.delete_service(request, params)
        except Exception:
            redirect = reverse(constants.SERVICE_INDEX_URL)
            msg = 'Unable to delete service.'
            exceptions.handle(request, msg, redirect=redirect)


class DeleteMemberAction(tables.DeleteAction):
    @staticmethod
    def action_present(count):
        return ungettext_lazy(
            u"Delete Service",
            u"Delete Services",
            count
        )

    @staticmethod
    def action_past(count):
        return ungettext_lazy(
            u"Scheduled deletion of Service",
            u"Scheduled deletion of Services",
            count
        )

    name = "delete"
    help_text = _("This action cannot be undone. ")
    policy_rules = (("nal", "nal:delete_service"),)

    def allowed(self, request, member):
        if member.dc_id == member.my_dc_id:
            allow_member = SERVICE_DISPLAY_BUTTONS_LIST['is_member']
        else:
            allow_member = SERVICE_DISPLAY_BUTTONS_LIST['is_not_member']
        allow_status = \
            SERVICE_DISPLAY_BUTTONS_FOR_STATUS[str(member.task_status)]
        service_name = SERVICE_TYPE_MAPPING[str(member.service_type)]
        allow_device = SERVICE_DISPLAY_BUTTONS_FOR_DEVICE[service_name]

        allow_set = set(allow_member) & set(allow_status) & set(allow_device)
        if self.__class__.__name__ in list(allow_set):
            return True
        return False

    def delete(self, request, obj_id):
        func_type = self.table.kwargs['group_id'].split('|')[0]
        service_id = self.table.kwargs['group_id'].split('|')[1]

        service = nal_api.get_services(request, group_id=service_id,
                                       func_type=func_type)
        detail_list = \
            service[SERVICE_DETAIL_DISPLAY_COLUMNS[func_type]['detail_name']]
        detail_data = detail_list[0]

        params = {'function_type': func_type,
                  'group_id': service_id,
                  'service_type': detail_data.service_type}

        service_name = SERVICE_TYPE_MAPPING.get(detail_data.service_type, '')
        service_detail = SERVICE_TYPE_DETAIL_MAPPING.get(service_name, {})
        for key, value in service_detail.iteritems():
            params[key] = value

        if str(detail_data.task_status) == '9':
            params['job_cleaning_mode'] = 1

        try:
            LOG.info('Deleting service "%s".' % service_id)
            nal_api.delete_service(request, params)
        except Exception:
            redirect = reverse(constants.SERVICE_INDEX_URL)
            msg = 'Unable to delete service.'
            exceptions.handle(request, msg, redirect=redirect)


class ServiceBaseLink(tables.LinkAction):
    url = constants.SERVICE_UPDATE_URL
    name = 'interface'
    classes = ("ajax-modal",)
    icon = "plus"

    def allowed(self, request, service):
        if service.my_group_flg == '1':
            allow_member = SERVICE_DISPLAY_BUTTONS_LIST['is_member']
        else:
            allow_member = SERVICE_DISPLAY_BUTTONS_LIST['is_not_member']
        allow_status = \
            SERVICE_DISPLAY_BUTTONS_FOR_STATUS[str(service.task_status)]
        service_name = SERVICE_TYPE_MAPPING[str(service.service_type)]
        allow_device = SERVICE_DISPLAY_BUTTONS_FOR_DEVICE[service_name]

        allow_set = set(allow_member) & set(allow_status) & set(allow_device)
        if self.__class__.__name__ in list(allow_set):
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


class MemberBaseLink(tables.LinkAction):
    url = constants.SERVICE_UPDATE_URL
    name = 'bandwidth'
    classes = ("ajax-modal",)
    icon = "plus"

    def allowed(self, request, member):
        if member.dc_id == member.my_dc_id:
            allow_member = SERVICE_DISPLAY_BUTTONS_LIST['is_member']
        else:
            allow_member = SERVICE_DISPLAY_BUTTONS_LIST['is_not_member']
        allow_status = \
            SERVICE_DISPLAY_BUTTONS_FOR_STATUS[str(member.task_status)]
        service_name = SERVICE_TYPE_MAPPING[str(member.service_type)]
        allow_device = SERVICE_DISPLAY_BUTTONS_FOR_DEVICE[service_name]

        allow_set = set(allow_member) & set(allow_status) & set(allow_device)
        if self.__class__.__name__ in list(allow_set):
            return True
        return False

    def get_link_url(self, datum=None):
        try:
            obj_id = self.table.kwargs['group_id']
            return urlresolvers.reverse(self.url, args=(obj_id, self.name))
        except urlresolvers.NoReverseMatch as ex:
            LOG.info('No reverse found for "%s": %s' % (self.url, ex))
            return self.url


class NetworkBaseLink(tables.LinkAction):
    url = constants.SERVICE_UPDATE_URL
    name = 'bandwidth'
    classes = ("ajax-modal",)
    icon = "plus"

    def allowed(self, request, network):
        if network.dc_id == network.my_dc_id:
            allow_member = SERVICE_DISPLAY_BUTTONS_LIST['is_member']
        else:
            allow_member = SERVICE_DISPLAY_BUTTONS_LIST['is_not_member']
        allow_status = \
            SERVICE_DISPLAY_BUTTONS_FOR_STATUS[str(network.task_status)]
        service_name = SERVICE_TYPE_MAPPING[str(network.service_type)]
        allow_device = SERVICE_DISPLAY_BUTTONS_FOR_DEVICE[service_name]

        allow_set = set(allow_member) & set(allow_status) & set(allow_device)
        if self.__class__.__name__ in list(allow_set):
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


class ServiceBaseAction(tables.LinkAction):
    url = constants.SERVICE_UPDATE_URL
    name = 'interface'
    classes = ("ajax-modal",)
    icon = "plus"

    def allowed(self, request, service):
        func_type = self.table.kwargs['group_id'].split('|')[0]
        group_id = self.table.kwargs['group_id'].split('|')[1]

        service = nal_api.get_services(self.table.request, group_id=group_id,
                                       func_type=func_type)
        detail_list = \
            service[SERVICE_DETAIL_DISPLAY_COLUMNS[func_type]['detail_name']]
        detail_data = detail_list[0]
        network_data = \
            service[SERVICE_DETAIL_DISPLAY_COLUMNS[func_type]['network_name']]

        if getattr(detail_data, 'my_dc_id') in [getattr(network, 'dc_id')
                                                for network in network_data]:
            allow_member = SERVICE_DISPLAY_BUTTONS_LIST['is_member']
        else:
            allow_member = SERVICE_DISPLAY_BUTTONS_LIST['is_not_member']
        allow_status = \
            SERVICE_DISPLAY_BUTTONS_FOR_STATUS[str(detail_data.task_status)]
        service_name = SERVICE_TYPE_MAPPING[str(detail_data.service_type)]
        allow_device = SERVICE_DISPLAY_BUTTONS_FOR_DEVICE[service_name]

        allow_set = set(allow_member) & set(allow_status) & set(allow_device)
        if self.__class__.__name__ in list(allow_set):
            return True
        return False

    def get_link_url(self, datum=None):
        try:
            obj_id = self.table.kwargs['group_id']
            return urlresolvers.reverse(self.url, args=(obj_id, self.name))
        except urlresolvers.NoReverseMatch as ex:
            LOG.info('No reverse found for "%s": %s' % (self.url, ex))
            return self.url


class UpdateNetworkLink(ServiceBaseLink):
    name = "interface"
    verbose_name = _("Connect Interface")
    policy_rules = (("nal", "nal:update_service_interface"),)


class UpdateMemberLink(ServiceBaseLink):
    name = "member_create"
    verbose_name = _("Add Member")
    policy_rules = (("nal", "nal:update_service_member"),)


class UpdateBandwidthLink(ServiceBaseLink):
    name = "bandwidth"
    verbose_name = _("Update Bandwidth")
    policy_rules = (("nal", "nal:update_service_bandwidth"),)


class UpdateSettingLink(ServiceBaseLink):
    name = "serviceSetting"
    verbose_name = _("Update Setting")
    policy_rules = (("nal", "nal:update_service_setting"),)


class UpdateNetworkTableAction(ServiceBaseAction):
    name = "interface"
    verbose_name = _("Connect Interface")
    policy_rules = (("nal", "nal:update_service_interface"),)


class UpdateMemberTableAction(ServiceBaseAction):
    name = "member_create"
    verbose_name = _("Add Member")
    policy_rules = (("nal", "nal:update_service_member"),)


class UpdateBandwidthMemberLink(MemberBaseLink):
    name = "bandwidth"
    verbose_name = _("Update Bandwidth")
    policy_rules = (("nal", "nal:update_service_bandwidth"),)


class UpdateSettingMemberLink(MemberBaseLink):
    name = "serviceSetting"
    verbose_name = _("Update Setting")
    policy_rules = (("nal", "nal:update_service_setting"),)


class UpdateNetworkV6Link(NetworkBaseLink):
    name = "serviceIPv6Add"
    verbose_name = _("Add IPv6 Address")
    policy_rules = (("nal", "nal:update_service_network_ipv6"),)

    def allowed(self, request, network):
        if network.ip_address_v6 == "":
            return NetworkBaseLink.allowed(self, self.__class__.__name__,
                                           network)
        return False
