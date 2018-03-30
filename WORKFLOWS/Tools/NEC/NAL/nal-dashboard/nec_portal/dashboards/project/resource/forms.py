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
from nec_portal.dashboards.project.resource import constants
from nec_portal.local import nal_portal_settings

LOG = logging.getLogger(__name__)
RESOURCE_OPERATION_MAPPING = getattr(nal_portal_settings,
                                     'RESOURCE_OPERATION_MAPPING', None)
RESOURCE_CREATE_COLUMNS_DEF = getattr(nal_portal_settings,
                                      'RESOURCE_CREATE_COLUMNS_DEF', None)
RESOURCE_UPDATE_COLUMNS_DEF = getattr(nal_portal_settings,
                                      'RESOURCE_UPDATE_COLUMNS_DEF', None)
RESOURCE_SCREEN_TRANSITION = getattr(nal_portal_settings,
                                     'RESOURCE_SCREEN_TRANSITION', None)


class CreateResourceForm(forms.SelfHandlingForm):
    resource_id = forms.CharField(widget=forms.HiddenInput())

    def __init__(self, request, *args, **kwargs):

        super(CreateResourceForm, self).__init__(request, *args, **kwargs)

        self.fields['resource_id'].initial = kwargs['initial']['resource_id']
        func_type = kwargs['initial']['resource_id'].split('|')[0]

        for column_class in ['common', 'separate']:
            for column in RESOURCE_CREATE_COLUMNS_DEF[func_type][column_class]:
                if column[1]['field'] == 'ChoiceField':
                    self.fields[column[0]] = getattr(forms,
                                                     column[1]['field'])(
                        label=column[1]['label'],
                        choices=column[1]['choices'],
                        required=column[1]['required'])
                elif column[1]['field'] == 'IntegerField':
                    self.fields[column[0]] = getattr(forms,
                                                     column[1]['field'])(
                        label=column[1]['label'],
                        required=column[1]['required'],
                        min_value=column[1]['min_value'],
                        initial=column[1]['initial'])
                else:
                    self.fields[column[0]] = getattr(forms,
                                                     column[1]['field'])(
                        label=column[1]['label'],
                        required=column[1]['required'])

                if 'resource_kind' == column[0]:
                    input_attrs = {}
                    for attr_key, attr_val in column[1]['widget'].items():
                        input_attrs[attr_key] = attr_val
                    self.fields['resource_kind'].initial = func_type
                    self.fields['resource_kind'].widget = \
                        forms.TextInput(attrs=input_attrs)

    def handle(self, request, data):
        try:
            resource_id = data['resource_id']
            func_type = resource_id.split('|')[0]
            create_def = RESOURCE_CREATE_COLUMNS_DEF[func_type]

            params = {'function_type': func_type}
            for column_class in ['common', 'separate']:
                for column in create_def[column_class]:
                    params[column[0]] = data[column[0]]

            if 'create_type' in create_def:
                params['function_type'] = create_def['create_type']

            if create_def['method'] == 'update':
                nal_api.update_resource(request, params)
                msg = _('Job of resource creation is running.')
                LOG.debug(msg)
                messages.success(request, msg)
                return True
            else:
                nal_api.create_resource(request, params)
                msg = _('Job of resource creation is running.')
                LOG.debug(msg)
                messages.success(request, msg)
                return True

        except exceptions.NotAvailable:
            return False
        except Exception:
            detail_table = RESOURCE_SCREEN_TRANSITION[func_type]
            set_args = '|'.join([resource_id, detail_table])
            redirect = reverse(constants.RESOURCE_DETAIL_URL,
                               args=(set_args,))
            exceptions.handle(request, redirect=redirect)

    def clean(self):
        data = super(CreateResourceForm, self).clean()

        return data


class UpdateResourceForm(forms.SelfHandlingForm):
    resource = forms.CharField(widget=forms.HiddenInput())
    func_type = forms.CharField(widget=forms.HiddenInput())
    update_type = forms.CharField(widget=forms.HiddenInput())

    def __init__(self, request, *args, **kwargs):
        super(UpdateResourceForm, self).__init__(request, *args, **kwargs)

        func_type = kwargs['initial']['resource_id'].split('|')[0]
        resource_id = kwargs['initial']['resource_id'].split('|')[2]
        update_type = kwargs['initial']['update_type']

        tenant_id = self.request.user.project_id
        resource = nal_api.get_resources(self.request, tenant_id,
                                         func_type=func_type)
        self.fields['resource'].initial = resource_id
        self.fields['func_type'].initial = func_type
        self.fields['update_type'].initial = update_type

        update_detail_info = RESOURCE_UPDATE_COLUMNS_DEF[update_type]
        if update_detail_info['display_type'] == 'input_column':
            for contract_data in resource['contract_info']:
                if str(contract_data.id) == resource_id:
                    detail_data = contract_data
                    self.fields['resource'].initial = contract_data.resource
                    break
            else:
                raise exceptions.NotFound

            for column in update_detail_info['common']:
                input_attrs = {}
                for attr_key, attr_val in column[1]['widget'].items():
                    input_attrs[attr_key] = attr_val

                if column[1]['field'] == 'ChoiceField':
                    self.fields[column[0]] = getattr(forms,
                                                     column[1]['field'])(
                        label=column[1]['label'],
                        choices=column[1]['choices'],
                        required=column[1]['required'],
                        widget=forms.Select(attrs=input_attrs))
                else:
                    self.fields[column[0]] = getattr(forms,
                                                     column[1]['field'])(
                        label=column[1]['label'],
                        required=column[1]['required'],
                        widget=forms.TextInput(attrs=input_attrs))

                if hasattr(detail_data, column[0]):
                    self.fields[column[0]].initial = getattr(detail_data,
                                                             column[0])

            for column in update_detail_info['separate']:
                input_attrs = {}
                for input in column[1]['input_type']:
                    input_attrs['data-' + input] = column[1]['label']

                input_attrs['class'] = 'switched'
                input_attrs['id'] = column[0]

                if column[1]['field'] == 'ChoiceField':
                    self.fields[column[0]] = \
                        getattr(forms, column[1]['field'])(
                            label=column[1]['label'],
                            choices=column[1]['choices'],
                            required=column[1]['required'],
                            widget=forms.Select(attrs=input_attrs))
                else:
                    self.fields[column[0]] = \
                        getattr(forms, column[1]['field'])(
                            label=column[1]['label'],
                            required=column[1]['required'],
                            widget=forms.TextInput(attrs=input_attrs))

                if hasattr(detail_data, column[0]):
                    self.fields[column[0]].initial = getattr(detail_data,
                                                             column[0])

            if 'node_id' in self.fields:
                nodes = nal_api.get_nodes(self.request, tenant_id,
                                          func_type='all_node')

                node_choices = []
                for node in nodes:
                    if node.type == '2':
                        node_choices.append((node.node_id,
                                             node.name or node.node_id))

                if node_choices:
                    self.fields['node_id'].choices = node_choices

                if getattr(detail_data, 'status') != '0':
                    self.fields['status'].initial = '2'
                    self.fields['node_id'].initial = getattr(detail_data,
                                                             'node_id')
        else:
            pass

    def handle(self, request, data):
        try:
            params = {'function_type': data['func_type'],
                      'global_ip': data['resource']}

            up_type = data['update_type']
            display_type = RESOURCE_UPDATE_COLUMNS_DEF[up_type]['display_type']
            if display_type == 'input_column':

                for column in RESOURCE_UPDATE_COLUMNS_DEF[up_type]['common']:
                    params[column[0]] = data[column[0]]

                for column in RESOURCE_UPDATE_COLUMNS_DEF[up_type]['separate']:
                    if data['status'] in column[1]['input_type']:
                        params[column[0]] = data[column[0]]

            nal_api.update_resource(request, params)
            msg = _('Job of resource update process is running.')
            LOG.debug(msg)
            messages.success(request, msg)
            return True

        except exceptions.NotAvailable:
            return False
        except Exception:
            redirect = reverse(constants.RESOURCE_DETAIL_URL,
                               args=(data['func_type'],))
            exceptions.handle(request, redirect=redirect)

    def clean(self):
        data = super(UpdateResourceForm, self).clean()
        status = data['status']
        update_type = data['update_type']
        for column in RESOURCE_UPDATE_COLUMNS_DEF[update_type]['separate']:
            if column[1]['required'] and column[0] in self._errors:
                if status not in column[1]['input_type']:
                    del self._errors[column[0]]
        return data
