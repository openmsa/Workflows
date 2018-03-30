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
from django.utils.translation import ugettext_lazy as _
from horizon import tables

from nec_portal.dashboards.admin.node import constants
from nec_portal.local import nal_portal_settings

LOG = logging.getLogger(__name__)
NODE_DETAIL_DISPLAY_COLUMNS = \
    getattr(nal_portal_settings, 'ADMIN_NODE_DETAIL_DISPLAY_COLUMNS', None)
NODE_DISPLAY_BUTTONS_FOR_DEVICE = \
    getattr(nal_portal_settings, 'NODE_DISPLAY_BUTTONS_FOR_DEVICE', None)
NODE_DISPLAY_BUTTONS_FOR_STATUS = \
    getattr(nal_portal_settings, 'NODE_DISPLAY_BUTTONS_FOR_STATUS', None)


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


class UpdateLicenseLink(NodeBaseLink):
    name = "license"
    verbose_name = _("Create License")
    policy_rules = (("nal", "nal:update_node_license"),)

    def allowed(self, request, node):
        return NodeBaseLink.disp_check(self, self.__class__.__name__, node)
