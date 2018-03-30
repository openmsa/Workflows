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
from nec_portal.dashboards.project.resource import constants
from nec_portal.local import nal_portal_settings

LOG = logging.getLogger(__name__)

RESOURCE_BUTTON_DISPLAY_FOR_TYPE = \
    getattr(nal_portal_settings, 'RESOURCE_BUTTON_DISPLAY_FOR_TYPE', None)
RESOURCE_BUTTON_DISPLAY_FOR_STATUS = \
    getattr(nal_portal_settings, 'RESOURCE_BUTTON_DISPLAY_FOR_STATUS', None)
RESOURCE_SCREEN_TRANSITION = \
    getattr(nal_portal_settings, 'RESOURCE_SCREEN_TRANSITION', None)


class DeleteResourceAction(tables.DeleteAction):
    @staticmethod
    def action_present(count):
        return ungettext_lazy(
            u"Delete Resource",
            u"Delete Resources",
            count
        )

    @staticmethod
    def action_past(count):
        return ungettext_lazy(
            u"Scheduled deletion of Resource",
            u"Scheduled deletion of Resources",
            count
        )

    name = "delete"
    help_text = _("This action cannot be undone. ")
    policy_rules = (("nal", "nal:delete_resource"),)

    def allowed(self, request, resource):
        func_type = resource.func_type
        status = resource.status
        if self.__class__.__name__ in \
                RESOURCE_BUTTON_DISPLAY_FOR_TYPE[func_type] \
                and self.__class__.__name__ in \
                RESOURCE_BUTTON_DISPLAY_FOR_STATUS[str(status)]:
            return True
        return False

    def delete(self, request, obj_id):
        func_type = obj_id.split('|')[0]
        resource_key = obj_id.split('|')[1]
        resource_id = obj_id.split('|')[2]
        try:
            tenant_id = request.user.project_id
            resource = nal_api.get_resources(request, tenant_id,
                                             func_type=func_type)
            for contract_data in resource['contract_info']:
                if str(contract_data.id) == resource_id:
                    global_ip = contract_data.resource
                    break
            LOG.info('Deleting resource "%s".' % global_ip)
            params = {'function_type': 'globalip_return',
                      'global_ip': global_ip}
            nal_api.update_resource(request, params)
        except Exception:
            detail_table = RESOURCE_SCREEN_TRANSITION[func_type]
            set_args = '|'.join([func_type, resource_key, detail_table])
            redirect = reverse(constants.RESOURCE_DETAIL_URL,
                               args=(set_args,))
            exceptions.handle(request, redirect=redirect)


class ResourceBaseLink(tables.LinkAction):
    url = constants.RESOURCE_UPDATE_URL
    name = 'interface'
    classes = ("ajax-modal",)
    icon = "plus"

    def disp_check(self, class_name, resource):
        func_type = resource.func_type
        status = resource.status
        if class_name in RESOURCE_BUTTON_DISPLAY_FOR_TYPE[func_type] \
                and class_name \
                in RESOURCE_BUTTON_DISPLAY_FOR_STATUS[str(status)]:
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


class UpdateResourceLink(ResourceBaseLink):
    name = "change_status"
    verbose_name = _("Update Resource")
    policy_rules = (("nal", "nal:update_resource"),)

    def allowed(self, request, resource):
        return ResourceBaseLink.disp_check(self, self.__class__.__name__,
                                           resource)
