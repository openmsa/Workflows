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
from django.utils.translation import ugettext_lazy as _

from horizon import exceptions
from horizon import forms
from horizon import messages

from nec_portal.api import nal_api
from nec_portal.dashboards.admin.node import constants
from nec_portal.local import nal_portal_settings

LOG = logging.getLogger(__name__)
NODE_DETAIL_DISPLAY_COLUMNS = \
    getattr(nal_portal_settings, 'ADMIN_NODE_DETAIL_DISPLAY_COLUMNS', None)
NODE_UPDATE_COLUMNS = getattr(nal_portal_settings, 'NODE_UPDATE_COLUMNS', None)


class UpdateNodeForm(forms.SelfHandlingForm):
    node_id = forms.CharField(widget=forms.HiddenInput())
    function_type = forms.CharField(widget=forms.HiddenInput())
    update_type = forms.CharField(widget=forms.HiddenInput())
    type = forms.CharField(widget=forms.HiddenInput())
    device_type = forms.CharField(widget=forms.HiddenInput())

    def __init__(self, request, *args, **kwargs):
        super(UpdateNodeForm, self).__init__(request, *args, **kwargs)

        func_type = kwargs['initial']['obj_id'].split('|')[0]
        node_id = kwargs['initial']['obj_id'].split('|')[1]
        update_type = kwargs['initial']['update_type']

        node = nal_api.get_nodes(self.request, rec_id=node_id,
                                 func_type=func_type)
        detail_data = \
            node[NODE_DETAIL_DISPLAY_COLUMNS[func_type]['detail_name']][0]

        self.fields['node_id'].initial = detail_data.node_id
        self.fields['function_type'].initial = func_type
        self.fields['update_type'].initial = update_type
        self.fields['type'].initial = detail_data.type
        self.fields['device_type'].initial = detail_data.device_type

    def handle(self, request, data):
        try:
            params = {'node_id': data['node_id'],
                      'device_type': data['device_type']}
            update_type = data['update_type']

            if NODE_UPDATE_COLUMNS[update_type]['display_type'] == 'check':
                params['type'] = data['type']
                params['function_type'] = data['update_type']
            else:
                pass

            nal_api.update_node(request, params)
            msg = _('Job of license input is running.')
            LOG.debug(msg)
            messages.success(request, msg)
            return True

        except exceptions.NotAvailable:
            return False
        except Exception:
            redirect = reverse(constants.NODE_INDEX_URL)
            exceptions.handle(request, redirect=redirect)

    def clean(self):
        data = super(UpdateNodeForm, self).clean()
        return data
